"""Independent reference check. Notebook cells run only here, never in the app."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import nbformat
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.base import clone
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.preprocessing import normalize

from olist_shop.artifacts import ROOT, load_artifacts
from olist_shop.data import FEATURES, REDUCED_NUMERIC, load_data, retention_dataset


def verify():
    notebook = nbformat.read(ROOT/"olist_pipeline.ipynb", 4)
    reference = {"np": np, "sparse": sparse, "normalize": normalize}
    selected = {"feature-design-configuration", "construct-retention-labels", "construct-purchase-features",
                "construct-known-event-features", "split-retention-cohorts", "baseline-define-pipeline"}
    with redirect_stdout(StringIO()):
        for cell in notebook.cells:
            if cell.cell_type == "code" and (cell.execution_count <= 18 or cell.id in selected):
                exec(compile(cell.source, f"notebook:{cell.id}", "exec"), reference)
    data = load_data(ROOT/"data/raw")
    actual = retention_dataset(data).set_index("customer_unique_id").sort_index()
    expected = reference["retention_dataset"].set_index("customer_unique_id").sort_index()
    pd.testing.assert_frame_equal(actual[FEATURES+['repeat_90d']], expected[FEATURES+['repeat_90d']], check_dtype=False, rtol=1e-12, atol=1e-12)
    bundle = load_artifacts()
    model = bundle["model"]
    reference_preprocessing = clone(reference["retention_preprocessing"])
    reference_preprocessing.transformers = [
        ("numeric", clone(reference["numeric_preprocessing"]), REDUCED_NUMERIC),
        ("categorical", clone(reference["categorical_preprocessing"]), ["customer_state"]),
    ]
    reference_model = reference["Pipeline"]([
        ("preprocessing", reference_preprocessing),
        ("classifier", reference["LogisticRegression"](C=.1, max_iter=2000, random_state=42)),
    ])
    reference_model.fit(reference["X_train"], reference["y_train"])
    for partition in ["validation", "test"]:
        inputs = reference[f"X_{partition}"]
        np.testing.assert_allclose(model.predict_proba(inputs), reference_model.predict_proba(inputs), rtol=1e-7, atol=1e-9)
    test = reference["X_test"]
    score = model.predict_proba(test)[:, 1]
    assert np.isclose(average_precision_score(reference["y_test"], score), .015311358505194642)
    assert np.isclose(roc_auc_score(reference["y_test"], score), .47456893493223584)
    # Independently execute only the notebook's honest reference helper definitions.
    import ast
    source = next(c.source for c in notebook.cells if c.id == "fit-frozen-content-engines")
    definitions = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)]
    reference["purchase_events"] = reference["purchase_events"]
    reference["products_prepared"] = reference["products_prepared"]
    exec(compile(ast.Module(body=definitions, type_ignores=[]), "notebook:honest-helpers", "exec"), reference)
    pairs = data.items.loc[data.items.order_purchase_timestamp.lt("2018-06-01"), ["customer_unique_id", "product_id"]].drop_duplicates().rename(columns={"customer_unique_id": "user", "product_id": "item"})
    engine_ref = reference["fit_frozen_content_engine"](pairs, pd.Timestamp("2018-06-01"))
    engine = bundle["engine"]
    rng = np.random.default_rng(42)
    users = list(engine.users[rng.choice(len(engine.users), 100, replace=False)]) + ["__new_customer__"]
    for user in users:
        for method in ["content", "popularity"]:
            expected_ids = reference["recommend_frozen"](engine_ref, user, method, 10).product_id.tolist()
            actual_ids = engine.recommend(user, 10, mode="popular" if method == "popularity" else "personalized").product_id.tolist()
            assert actual_ids == expected_ids, (user, method)
    print("PASS: all 71,105 feature rows match notebook; validation/test probability vectors match.")
    print("PASS: frozen AP/AUC reproduced; 202 top-ten lists match the honest notebook helpers.")


if __name__ == "__main__":
    verify()
