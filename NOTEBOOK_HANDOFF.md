# Notebook completion and implementation handoff

The core notebook is complete: 92 executed code cells, 24 embedded figures, final honest held-out results, understanding logs and reproducibility records. The first local application is now implemented in Streamlit with SQLite and a bounded assistant. This document retains the frozen notebook contracts; APP_REFERENCE.md describes their extracted implementation and tests.

## Frozen choices

| Component | Selected design |
|---|---|
| Retention | Logistic Regression C=0.1, excluding log average order value, with training-only preprocessing |
| Classification decision | Report 0.5 benchmark and illustrative 0.02 review threshold; no optimal business-cost claim |
| Recommendations | Content cosine, category weight 2 and price-band weight 1; popularity ties/fallback; seen products excluded |
| Segmentation | Historical log-RFM scaling and K-means K=2; neutral group IDs |
| Comparison-only methods | KNN, CART, categorical ID3, GaussianNB, SVM, Random Forest, small ANN, sampled Ward |
| Deferred extras | Boosting, recommendation hybrid, SVD, advanced NLP, external LLM integration |

Model and threshold choices were fixed before the final test outputs. Test results do not trigger another tuning round.

## Final measured results

Classification test has 14,213 customers and 120 repeat events.

| Model | AP | ROC-AUC |
|---|---|---|
| Prior | 0.008443 | 0.500000 |
| Original logistic | 0.012347 | 0.459006 |
| Selected reduced logistic | 0.015311 | 0.474569 |

At the 0.02 review threshold, there are 176 flags, six true positives, 170 false positives and 114 missed repeats. Precision is 0.034091 and recall 0.05. At 0.5 there are no positive decisions. This classifier is experimental and weak, with below-chance overall ROC-AUC. Its scores must not be presented as reliable or calibrated retention predictions.

Recommendation test metrics apply to 97 eligible warm-discovery customers out of 6,121 future shoppers. Candidates are 26,895 products observed before the June 2018 cutoff.

| Method | K | Precision | Recall | NDCG | Hit rate |
|---|---|---|---|---|---|
| Content | 5 | 0.012371 | 0.056701 | 0.034836 | 0.061856 |
| Content | 10 | 0.007216 | 0.067010 | 0.038273 | 0.072165 |
| Popularity | 5 | 0 | 0 | 0 | 0 |
| Popularity | 10 | 0 | 0 | 0 | 0 |

Only six customers receive a relevant content top-five suggestion. The small eligible cohort is 1.5847 percent of future shoppers; these metrics are not overall shopping success or sales lift. Fallback behavior and historical stock limitations remain explicit.

RFM K=2 exactly separates 30,014 single-order customers and 856 multiple-order customers in the November 2017 learning snapshot. It describes observed purchasing rather than future loyalty.

## Functions and objects to extract during implementation

| Notebook component | Input and output contract | Implementation constraint |
|---|---|---|
| Prepared `order_facts` | One row per order, timestamps, stable customer, item/payment/review aggregates | Preserve row grain and reconciliation checks |
| Prepared `purchase_events` | One row per original item event with customer, product, timestamp and metadata | Preserve item grain and historical timestamps |
| Retention feature construction, Sections 5–6 | Historical customer snapshot to the `RETENTION_FEATURES` DataFrame schema | Review/delivery evidence must be known by snapshot time; do not use future labels or final status as historical evidence |
| `final_retention_model` | Fitted pipeline; `predict_proba(frame)[:,1]` returns repeat-class score | Keep preprocessing with model; full schema is accepted and reduced preprocessor ignores log average order value |
| `fit_frozen_content_engine(history_pairs, cutoff)` | Historical user/product pairs and cutoff to fitted content/popularity engine | Notebook currently reads prepared item/product globals; make those dependencies explicit when extracting, and retain strict earlier-price filtering |
| `recommend_frozen(engine, user, method, n)` | Known or unknown customer to unique product IDs, categories, scores and fallback flags | Supports content/popularity and 1–100 requested items; excludes historical purchases and rejects invalid methods/counts |
| `build_rfm_snapshot(cutoff)` and fitted `rfm_scaler`/`rfm_kmeans` | Historical orders to RFM row and descriptive segment | Shared calendar reference differs from the fixed-age classifier; no assignment without purchase history |
| Evaluation functions | Known future relevance to metrics | Keep evaluation labels and the intentionally leaky engine out of runtime inference |

The reusable modules are now extracted into olist_shop/ and app.py. scripts/build_artifacts.py creates the fitted local bundle. The notebook provides the verified reference behavior and result contracts, with independent parity checks in scripts/verify_notebook_parity.py.

## Time and catalog rules

- Retention scores at 30 days after the first observed item-bearing placed order, predicting another placed order in the following 90 days. This includes later-cancelled item-bearing orders; it does not mean completed-sales revenue or arbitrary-date churn.
- Reviews and deliveries are features only when their timestamps are known by that customer snapshot.
- Recommendation validation is 1 April–1 May 2018; final recommendation evaluation is 1 June–1 July 2018. Catalogs and profiles for honest ranking use only earlier events.
- The exclusive coverage boundary is the working assumption 1 September 2018. Observation history is incomplete before dataset collection.
- Product categories are treated as static metadata. Displayed prices are historical medians, not current offers. Olist IDs are anonymized; real names, images and stock are not supplied.
- The simulated metadata-only product demonstrates scoring principles. A real new-item catalog-registration path remains implementation work.
- The invalid future-profile diagnostic is clearly labeled and never selected. Its NDCG@5 of 0.052285 is excluded from honest results; honest content NDCG@5 is 0.034836.

## Reproduce the notebook

Verified environment is Windows with Python 3.12.14. Package pins are in `requirements-notebook-lock.txt`; broad dependency ranges remain in `requirements.txt`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-notebook-lock.txt
```

Open `olist_pipeline.ipynb` in VS Code, select the `.venv` kernel, use the repository root as working directory and run all cells in order. All nine original CSVs must be in `data/raw/`. `notebook-data-manifest.json` records their byte sizes and SHA-256 hashes. Publisher version and exact download date were not recorded, so do not invent them.

The final fresh run passed every code cell. Figures were visually checked. Normal reruns reproduce the fixed experiment; changing decisions after reading the test would require a new independent evaluation design.

## Implementation status

The first implementation extracts preparation, historical feature building, frozen inference and honest recommendation helpers. Independent parity checks passed against notebook features, model probabilities and recommendation lists. The Streamlit interface adds persistent activity/cart/checkout, rule-based rewards, descriptive insights and a bounded assistant. APP_REFERENCE.md records setup, limitations and eleven passing tests. Weak repeat scores remain explicitly experimental.
