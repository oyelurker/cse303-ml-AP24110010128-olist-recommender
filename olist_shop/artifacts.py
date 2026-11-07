"""Build once from CSVs; serving loads fitted artifacts without notebook execution."""
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data import BASE_DATE, FEATURES, REDUCED_NUMERIC, load_data, retention_dataset, rfm_snapshot
from .recommendations import RecommendationEngine

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "shop.joblib"


def build_artifacts(destination=ARTIFACT):
    data = load_data(ROOT / "data" / "raw")
    frame = retention_dataset(data)
    training = frame.loc[frame.outcome_end.lt("2017-11-01")]
    if len(training) != 14362 or training.repeat_90d.sum() != 140:
        raise ValueError("Training cohort differs from the notebook; verify source files.")
    preprocessing = ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
            ("scaler", StandardScaler()),
        ]), REDUCED_NUMERIC),
        ("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="constant", fill_value="unknown")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
        ]), ["customer_state"]),
    ], remainder="drop", sparse_threshold=1.0)
    model = Pipeline([("preprocessing", preprocessing),
                      ("classifier", LogisticRegression(C=.1, max_iter=2000, random_state=42))])
    model.fit(training[FEATURES], training.repeat_90d)
    engine = RecommendationEngine.fit(data.items, data.products, BASE_DATE)
    orders = data.orders.loc[data.orders.order_purchase_timestamp.lt(BASE_DATE)].copy()
    items = data.items.loc[data.items.order_purchase_timestamp.lt(BASE_DATE),
                          ["order_id", "product_id", "customer_unique_id", "order_purchase_timestamp", "price"]].copy()
    risk = frame.loc[frame.snapshot_at.le(BASE_DATE)].copy()
    risk["score"] = model.predict_proba(risk[FEATURES])[:, 1]
    risk = risk[["customer_unique_id", "snapshot_at", "score"]].set_index("customer_unique_id")
    rfm = rfm_snapshot(data.orders, "2017-11-01")
    rfm_scaler = StandardScaler().fit(np.log1p(rfm))
    rfm_model = KMeans(n_clusters=2, n_init=10, max_iter=300, random_state=42, algorithm="lloyd").fit(rfm_scaler.transform(np.log1p(rfm)))
    completed = orders.loc[orders.order_delivered_customer_date.le(BASE_DATE) &
                           orders.order_delivered_customer_date.ge(orders.order_purchase_timestamp)]
    recent = completed.loc[completed.order_purchase_timestamp.ge(BASE_DATE-pd.Timedelta(days=90))]
    frequency = recent.groupby("customer_unique_id").agg(count=("order_id", "nunique"), dates=("order_purchase_timestamp", lambda s: s.dt.date.nunique()))
    last = completed.groupby("customer_unique_id").order_purchase_timestamp.max()
    personas = []
    frequent = frequency.loc[(frequency["count"] >= 3) & (frequency.dates >= 2)].index
    if len(frequent):
        personas.append({"label": "Frequent shopper", "id": str(frequent[0])})
    inactive = last.loc[last.lt(BASE_DATE-pd.Timedelta(days=60))].index
    if len(inactive):
        personas.append({"label": "Returning after a break", "id": str(inactive[0])})
    personas.append({"label": "One-purchase history", "id": str(engine.users[np.flatnonzero(np.diff(engine.history.indptr) == 1)[0]])})
    # Choose an evidence-backed product, and a customer who owns its source but not its neighbor.
    shared = engine.shared_buyers.tocoo()
    columns = engine.history.tocsc()
    featured = None
    for source, target, count in zip(shared.row, shared.col, shared.data):
        if count < 2 or engine.popularity[source] <= count:
            continue
        candidates = sorted(set(columns.getcol(source).nonzero()[0]) - set(columns.getcol(target).nonzero()[0]))
        if candidates:
            featured = str(engine.catalog.index[source])
            personas.append({"label": "Explore shared-buyer suggestions", "id": str(engine.users[candidates[0]])})
            break
    manifest = json.loads((ROOT / "notebook-data-manifest.json").read_text(encoding="utf-8"))
    for row in manifest["files"]:
        path = ROOT / "data" / "raw" / row["file"]
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024*1024), b""):
                digest.update(block)
        if digest.hexdigest() != row["sha256"]:
            raise ValueError(f"Input differs from notebook manifest: {row['file']}")
    bundle = {"version": 1, "engine": engine, "orders": orders, "items": items,
              "model": model, "risk": risk, "rfm_scaler": rfm_scaler, "rfm_model": rfm_model,
              "personas": personas, "featured_product": featured, "cutoff": BASE_DATE}
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".tmp")
    joblib.dump(bundle, temporary, compress=3)
    temporary.replace(destination)
    metadata = {"artifact_version": 1, "cutoff": str(BASE_DATE), "training_customers": len(training),
                "training_repeats": int(training.repeat_90d.sum()), "catalog_items": len(engine.catalog),
                "history_customers": len(engine.users), "personas": personas, "featured_product": featured,
                "source_manifest": manifest}
    destination.with_suffix(".json").write_text(json.dumps(metadata, indent=2)+"\n", encoding="utf-8")
    return bundle


def load_artifacts(path=ARTIFACT):
    # Only locally built, trusted artifacts are accepted. No uploaded pickle loading.
    bundle = joblib.load(path)
    if bundle.get("version") != 1:
        raise ValueError("Unsupported artifact version; rebuild the local artifacts.")
    return bundle
