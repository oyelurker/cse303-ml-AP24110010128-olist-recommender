# Olist Product Recommendation and Customer Retention

A machine learning capstone project using the Olist Brazilian E-Commerce dataset to explore customer behavior, recommend products, and predict repeat purchases. A conversational application will build on the verified notebook pipeline.

## Project objective

Help a direct-to-consumer business understand its customers and explore retention opportunities. The proposed application will let a marketing employee inspect customer history, view product recommendations, and ask questions about customer insights and model outputs.

The project corresponds to catalog topic 9.2, Tier A E-commerce Recommendation.

See [the syllabus comparison and viva walkthrough](SYLLABUS_ALIGNMENT.md) for the working model scope, exact course mappings, supporting extensions, and study priorities.

## Current status

The agreed core notebook is complete: **92 executed code cells and 24 figures**, with passed checks, final held-out evaluation, worked learning examples, an isolated leakage experiment, decision/problem/AI-use logs and reproducibility records. The application and chatbot are the next stage.

Read [the implementation handoff](NOTEBOOK_HANDOFF.md) for frozen choices, function contracts, results and limitations. [Pipeline notes](PIPELINE_NOTES.md) explain each completed topic and its viva questions.

### Final honest results

The classification test has 14,213 customers and 120 repeat events.

| Model | Test average precision | Test ROC-AUC |
|---|---|---|
| Training prior | 0.008443 | 0.500000 |
| Original Logistic Regression | 0.012347 | 0.459006 |
| Frozen reduced Logistic Regression, C=0.1 | 0.015311 | 0.474569 |

At the declared 0.02 review threshold, the selected model detects six repeats with 170 false positives and misses 114 repeats. It predicts no repeats at 0.5. Overall discrimination is weak, so repeat scores remain experimental rather than reliable business predictions. No model choices changed after test scoring.

| Recommendation method | K | Precision | Recall | NDCG |
|---|---|---|---|---|
| Content | 5 | 0.012371 | 0.056701 | 0.034836 |
| Content | 10 | 0.007216 | 0.067010 | 0.038273 |
| Popularity | 5 | 0 | 0 | 0 |
| Popularity | 10 | 0 | 0 | 0 |

Recommendation results cover 97 eligible warm-discovery customers, only 1.5847 percent of 6,121 future shoppers. Six customers receive a relevant content top-five suggestion. New customers receive explicit popularity fallback. Prices are historical medians and stock availability is unknown.

Historical RFM K=2 separates single-order and multiple-order histories, without a future-loyalty claim. The notebook also includes KNN, CART, categorical ID3, Bayes, SVM, forests, a small ANN and neural-learning demonstrations as course comparisons. Both supplied notebooks remain references, with attribution and an adaptation map inside our notebook. Optional boosting, hybrid, SVD and advanced NLP remain outside the completed core scope.

The full notebook rerun passed. The exact environment is recorded in [the notebook lock file](requirements-notebook-lock.txt), and [the input manifest](notebook-data-manifest.json) identifies the local CSVs by SHA-256. Publisher version and download date were not recorded. Earlier development-stage metrics and decisions remain documented in the notes.

## Workflow

### Notebook environment

Use Python 3.12 (verified with 3.12.14). Create an isolated environment and install the pinned notebook dependencies from the repository root.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-notebook-lock.txt
```

In VS Code, open `olist_pipeline.ipynb`, choose **Select Kernel**, and select the Python interpreter inside `.venv`. Run the notebook from top to bottom. Plot outputs are embedded in the saved notebook. Dependencies and the local environment are separate from the downloaded data.

### Development sequence

1. Inspect the dataset files, schema, identifiers, and time coverage.
2. Clean the data and validate joins at the appropriate customer, order, and item levels.
3. Perform exploratory data analysis of customer behavior, product popularity, and repeat activity.
4. Engineer historical customer features, including Recency, Frequency, and Monetary values.
5. Define the repeat-purchase target and chronological evaluation partitions.
6. Build and compare recommendation and repeat-purchase models.
7. Evaluate the models, document limitations, and save reusable pipeline components.
8. Develop an application with a conversational interface connected to those components.

See [the project plan](PROJECT_PLAN.md) for the proposed methods, evaluation approach, and deliverables.

See [the pipeline reference notes](PIPELINE_NOTES.md) for step-by-step code explanations, observed results, decisions, and commit checkpoints as the notebook develops.

## Dataset

The dataset publisher describes approximately 100,000 Brazilian e-commerce orders from 2016 to 2018. The linked CSV tables cover customers, orders, order items, products, payments, reviews, sellers, geolocation, and category translations. Exact counts and usable date coverage are recorded in the executed notebook. [Olist dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), [publisher introduction](https://www.kaggle.com/general/67613).

### Download instructions

1. Open the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
2. Sign in to Kaggle if prompted.
3. Click **Download** and choose the ZIP download if a menu appears. Download the complete dataset.
4. Locate the downloaded ZIP in your Downloads folder. Its filename may vary.
5. In Windows File Explorer, right-click the ZIP and select **Extract All**.
6. Create a `data` folder at the repository root and a `raw` folder inside it.
7. Copy all nine extracted CSV files directly into `data/raw/`, keeping their original filenames.
8. Check that the files match the list below. If extraction created an extra nested directory, move the CSVs into `data/raw/`.

Download the data from the dataset page linked above. The Kaggle notebook linked in the references is an implementation reference.

### Expected data layout

```text
data/
  raw/
    olist_customers_dataset.csv
    olist_geolocation_dataset.csv
    olist_order_items_dataset.csv
    olist_order_payments_dataset.csv
    olist_order_reviews_dataset.csv
    olist_orders_dataset.csv
    olist_products_dataset.csv
    olist_sellers_dataset.csv
    product_category_name_translation.csv
```

### Dataset files

| File | Main information |
|---|---|
| `olist_customers_dataset.csv` | Customer identifiers and location |
| `olist_orders_dataset.csv` | Order identifiers, status, and timestamps |
| `olist_order_items_dataset.csv` | Products and sellers within orders, prices, and freight |
| `olist_order_payments_dataset.csv` | Payment methods, installments, and values |
| `olist_order_reviews_dataset.csv` | Review scores, comments, and timestamps |
| `olist_products_dataset.csv` | Product categories and physical attributes |
| `olist_sellers_dataset.csv` | Seller identifiers and locations |
| `olist_geolocation_dataset.csv` | Postal-code prefixes and geographic coordinates |
| `product_category_name_translation.csv` | Portuguese-to-English product category translations |

### Check the local download

Run these commands in the VS Code PowerShell terminal from the repository root.

```powershell
Get-ChildItem -LiteralPath .\data\raw -Filter *.csv | Select-Object Name
(Get-ChildItem -LiteralPath .\data\raw -Filter *.csv -File).Count
```

The count should be `9`, and the filenames should match the expected layout. This checks file presence. Schema, completeness and data quality checks are included in the completed notebook.

The `data/raw/` ignore rule excludes newly untracked downloads. The nine current CSV files are already tracked in this repository, so adding the rule does not remove them from Git. Each collaborator can download their own copy using these instructions. Record the dataset version and download date during acquisition, and follow the licence stated on the Kaggle dataset page.

## Analysis and models

| Component | Approach |
|---|---|
| Customer analysis | RFM features and customer segmentation |
| Repeat-purchase prediction | Dummy and logistic baselines followed by comparative course models and ensembles |
| Product recommendations | Popularity, content-based similarity, and item-based collaborative filtering. Simple hybrid optional, SVD deferred |
| Evaluation | Chronological partitions, classification and ranking metrics, coverage, and repeated evaluation |
| Conversational application | Customer summaries, model explanations, product suggestions, and outreach message drafting |

The notebook fixes the 30-day customer-age decision and next-90-day repeat horizon, selected pipelines and historical recommendation windows. Reported results come from executed experiments; the frozen choices and limitations are documented in NOTEBOOK_HANDOFF.md.

## References and attribution

- Olist provides the underlying dataset. [Dataset source](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
- Mohab Allam's notebook is a reference for EDA, cleaning, satisfaction analysis, customer segmentation, and deployment. Adapted methods and code will receive attribution in the relevant notebook sections. [Reference notebook](https://www.kaggle.com/code/mohabovic/eda-satisfaction-prediction-nlp-rfm-deployment/notebook).
- The CSE303 project catalog, kickoff guide, and Week 10 recommender starter inform the academic deliverables and understanding checks.
