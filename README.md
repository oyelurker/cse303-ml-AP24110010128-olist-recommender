# Olist Product Recommendation and Customer Retention

A machine learning capstone project using the Olist Brazilian E-Commerce dataset to explore customer behavior, recommend products, and predict repeat purchases. A conversational application will build on the verified notebook pipeline.

## Project objective

Help a direct-to-consumer business understand its customers and explore retention opportunities. The proposed application will let a marketing employee inspect customer history, view product recommendations, and ask questions about customer insights and model outputs.

The project corresponds to catalog topic 9.2, Tier A E-commerce Recommendation.

## Current status

All nine source tables have been loaded and inspected for column types, missing values, exact duplicates, identifier uniqueness, and relationship coverage. The notebook includes executed outputs and explanations of the findings. Cleaning, EDA, model training, and application development are pending. The application framework and chatbot technology will be selected as the pipeline develops.

Open [the project notebook](olist_pipeline.ipynb) in VS Code, select a Python Jupyter kernel with pandas installed, and run the cells from top to bottom with the repository root as the working directory. The initial section includes saved outputs from execution against the local CSVs.

## Planned workflow

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

The dataset publisher describes approximately 100,000 Brazilian e-commerce orders from 2016 to 2018. The linked CSV tables cover customers, orders, order items, products, payments, reviews, sellers, geolocation, and category translations. Exact counts and usable date coverage will be recorded during initial inspection. [Olist dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), [publisher introduction](https://www.kaggle.com/general/67613).

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

The count should be `9`, and the filenames should match the expected layout. This checks file presence. Schema, completeness, and data quality checks will follow in the notebook.

Raw CSV files are excluded through `.gitignore`. Each collaborator can download their own copy using these instructions. Record the dataset version and download date during acquisition, and follow the licence stated on the Kaggle dataset page.

## Planned analysis and models

| Component | Initial approach |
|---|---|
| Customer analysis | RFM features and customer segmentation |
| Repeat-purchase prediction | Dummy and logistic baselines followed by comparative course models and ensembles |
| Product recommendations | Popularity, content-based similarity, item-based collaborative filtering, and sparse SVD comparisons |
| Evaluation | Chronological partitions, classification and ranking metrics, coverage, and repeated evaluation |
| Conversational application | Customer summaries, model explanations, product suggestions, and outreach message drafting |

The prediction horizon and model selection will depend on measured data feasibility. All reported results will come from executed experiments.

## References and attribution

- Olist provides the underlying dataset. [Dataset source](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
- Mohab Allam's notebook is a reference for EDA, cleaning, satisfaction analysis, customer segmentation, and deployment. Adapted methods and code will receive attribution in the relevant notebook sections. [Reference notebook](https://www.kaggle.com/code/mohabovic/eda-satisfaction-prediction-nlp-rfm-deployment/notebook).
- The CSE303 project catalog, kickoff guide, and Week 10 recommender starter inform the academic deliverables and understanding checks.
