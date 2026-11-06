# Olist Pipeline Reference Notes

This is the running learning record for our project. It explains the notebook work in plain language so that each step can be revised, reproduced, and explained during a demonstration or viva.

Update this document after each completed notebook section or meaningful code block. Record actual operations and observed results. Keep future work in the planned sequence until it has been executed and checked.

## Working sequence

| Step | Work | What the notes will explain |
|---|---|---|
| 1 | Project introduction and data loading | What each file contains, how it is loaded, and which variables hold it |
| 2 | Data inspection | Shapes, column types, keys, missing values, duplicates, and relationships |
| 3 | Cleaning and table preparation | Each cleaning rule, method, reason, and before-and-after effect |
| 4 | Exploratory data analysis | Each question, calculation or plot, finding, and modeling implication |
| 5 | Features, targets, and splits | Feature formulas, prediction timing, future labels, and leakage prevention |
| 6 | Model development and evaluation | Baselines, algorithms, parameters, metrics, results, and selection decisions |
| 7 | Reusable pipeline and application | Saved components, inputs, outputs, application integration, and chatbot behavior |

Recommendation and repeat-purchase prediction will have separate explanations wherever their data, models, or evaluation differ.

## Workflow for each completed section

1. State the question or purpose in a notebook Markdown cell.
2. Write a small, readable code block.
3. Run it and inspect the output.
4. Explain each meaningful line or related group of lines in the notes, including the role of important variables and methods.
5. Record the observed result and any checks, issues, or decisions.
6. Save the notebook and update these notes together.
7. Review the changes and create a focused Git commit for the completed section.

A section may contain several related cells. Commit when the section produces a verified, understandable result. Record genuine problems and fixes when they occur.

## Format for future entries

Use the following fields for each completed step or substep.

| Field | What to record |
|---|---|
| Purpose | The question or task being addressed |
| Notebook location | Notebook filename and the relevant section or cell heading |
| Inputs | Files, tables, columns, or outputs used from earlier steps |
| Code explanation | Important lines, variables, functions, parameters, and what they do |
| Method and reason | The technique used and why it fits this task |
| Observed output | Actual counts, values, plots, or model outputs from execution |
| Verification | How the output was checked |
| Decision or limitation | What we concluded and what remains uncertain |
| Commit | The descriptive commit message, with the hash once committed |

## Completed preparation

### Dataset files acquired

**Purpose** — Make the source CSVs available for the first notebook section.

**Location** — `data/raw/` at the repository root.

**Observed output** — All nine expected CSV files are present and have nonzero file sizes.

| File | Intended use |
|---|---|
| `olist_customers_dataset.csv` | Customer identity and location |
| `olist_orders_dataset.csv` | Orders and event timestamps |
| `olist_order_items_dataset.csv` | Product purchases, prices, and freight |
| `olist_order_payments_dataset.csv` | Payment records |
| `olist_order_reviews_dataset.csv` | Review scores and comments |
| `olist_products_dataset.csv` | Product categories and attributes |
| `olist_sellers_dataset.csv` | Seller identity and location |
| `olist_geolocation_dataset.csv` | Geographic coordinates by postal-code prefix |
| `product_category_name_translation.csv` | English category translations |

**Verification** — Inspected local filenames and file sizes. CSV contents, schemas, row counts, and quality checks are pending the loading and inspection sections.

### Reference notebook acquired

**Location** — `SOURCE FILES/eda-satisfaction-prediction-nlp-rfm-deployment.ipynb`.

**Purpose** — Reference for understanding data preparation, EDA, satisfaction analysis, segmentation, and deployment. Adaptations will be explained and attributed in our own notebook.

**Verification** — Confirmed that the downloaded notebook file is present and has a nonzero file size. Local execution and compatibility checks are pending.

### Reference notes established

**Purpose** — Keep a step-by-step learning record alongside the project notebook.

**Files** — `PIPELINE_NOTES.md`, with the broader scope in `PROJECT_PLAN.md` and dataset download instructions in `README.md`.

**Suggested commit message** — `docs: add pipeline learning notes and working sequence`.

**Commit status** — Pending.

## Step 1 Load the source tables

**Purpose** — Create our notebook, load the source tables, and record their dimensions.

**Notebook location** — `olist_pipeline.ipynb`, section 1 Load the source tables.

**Inputs** — The nine CSV files directly inside `data/raw/`.

### Code explanations

| Code or method | Explanation and reason |
|---|---|
| `from pathlib import Path` | Imports Python's filesystem path class. |
| `import pandas as pd` | Imports pandas under a short name for data analysis. |
| `pd.__version__` | Records the pandas version used during execution. |
| `Path.cwd()` | Finds the current working directory, which should be the repository root. |
| `project_root / "data" / "raw"` | Builds the source-folder path without a computer-specific absolute path. |
| `data_dir.is_dir()` | Checks that the source directory exists. |
| `data_files` | Maps meaningful table names to original CSV filenames. |
| `data_files.values()` | Supplies filenames for the presence check. |
| `missing_files` | Collects expected files that are absent. |
| `.is_file()` | Checks that a path points to a file. |
| `raise FileNotFoundError(...)` | Stops with an actionable message when the source folder or files are missing. |
| `postal_code_types` | Requests string storage for postal-code identifiers, preserving any leading zeros in the CSV source. |
| `tables = {}` | Creates the dictionary for the loaded DataFrames. |
| `data_files.items()` | Supplies each table name together with its filename. |
| `pd.read_csv(..., dtype=postal_code_types)` | Reads each CSV with the requested identifier types. Other types are inferred initially. |
| `tables[table_name]` | Stores and retrieves a DataFrame by its table name. |
| `summary_rows = []` | Creates a list for the summary records. |
| `tables.items()` | Supplies the loaded table names and DataFrames. |
| `dataframe.shape[0]` | Returns the row count. |
| `dataframe.shape[1]` | Returns the column count. |
| `summary_rows.append(...)` | Adds the current table's name and dimensions to the list. |
| `pd.DataFrame(summary_rows)` | Converts the summary records into a DataFrame. |
| `.to_string(index=False)` | Prints a readable table without an extra row-number column. |
| `len(tables)` | Returns the number of loaded tables. |

### Observed output

Executed using Python 3.12.14 and pandas 3.0.1.

| Table | Rows | Columns |
|---|---:|---:|
| customers | 99,441 | 5 |
| orders | 99,441 | 8 |
| order_items | 112,650 | 7 |
| order_payments | 103,886 | 5 |
| order_reviews | 99,224 | 7 |
| products | 32,951 | 9 |
| sellers | 3,095 | 4 |
| geolocation | 1,000,163 | 5 |
| category_translation | 71 | 2 |

### Verification and decisions

- Executed all three code cells in order against the actual CSV files and saved their observed outputs in the notebook.
- Confirmed nine loaded DataFrames and nonzero row and column counts.
- Confirmed string dtypes for customer, seller, and geolocation postal-code prefix columns.
- Kept the source tables separate for the upcoming key and relationship inspection.
- Timestamps remain as initially loaded. Parsing and data quality decisions will be documented later.
- Verified execution using the available Python runtime. Rerunning in VS Code requires a Python Jupyter kernel with pandas installed.

**Suggested commit message** — `feat: start Olist notebook and load source tables`.

**Commit status** — Pending.

## Step 2 Inspect the source data

**Purpose** — Understand the source tables and measure quality issues before choosing cleaning or join rules.

**Notebook location** — `olist_pipeline.ipynb`, section 2 Inspect the source data.

**Inputs** — The nine loaded DataFrames in `tables`.

### Step 2.1 Sample rows

**Method and reason** — Print the first two rows of every table to understand the available fields and the meaning of a record. Sample rows illustrate structure and are not representative statistical summaries.

| Code | Plain-language explanation |
|---|---|
| `for table_name, dataframe in tables.items()` | Visits each named DataFrame loaded in step 1. |
| `dataframe.head(2)` | Selects the first two rows for display. |
| `.to_string(index=False, max_colwidth=40)` | Formats the sample as readable text and truncates long displayed values. The stored values are preserved. |
| `print()` | Adds spacing between the displayed tables. |

**Observed output** — Printed samples from all nine tables. Order items contain products within an order. Payment records include a sequence field. Review records include scores, text, and dates.

### Step 2.2 Column types and missing values

**Method and reason** — Profile all 52 columns to understand their loaded representation, completeness, and number of distinct observed values.

| Code | Plain-language explanation |
|---|---|
| `profile_rows = []` | Creates a list for the column-level inspection records. |
| `for column_name in dataframe.columns` | Visits every column in the current table. |
| `column = dataframe[column_name]` | Selects one column as a pandas Series. |
| `column.isna()` | Marks missing values with True and observed values with False. |
| `column.isna().sum()` | Counts the missing values in that column. |
| `int(...)` | Converts a count to a Python integer for the summary. |
| `str(column.dtype)` | Records the column's loaded data type as text. |
| `100 * missing_count / len(dataframe)` | Calculates the percentage of rows missing this field. |
| `round(..., 2)` | Rounds the displayed percentage to two decimal places. |
| `column.nunique(dropna=True)` | Counts distinct non-missing values. |
| `profile_rows.append({...})` | Records the current column's measurements. |
| `pd.DataFrame(profile_rows)` | Builds the full column-profile table. |
| `.loc[column_profile["missing_count"] > 0]` | Selects only columns containing missing values. |
| `.sort_values("missing_percent", ascending=False)` | Lists the most incomplete columns first. |

**Observed output** — The review title column is missing 87,656 values, or 88.34 percent. Review messages are missing 58,247 values, or 58.70 percent. Product categories are missing for 610 products. Four product physical-attribute columns each have two missing values. Approval, carrier, and customer-delivery timestamps also have missing values.

**Decision** — Keep missingness visible for the cleaning discussion. Review text availability will need a separate eligibility policy if we add an NLP task. Timestamp conversion remains a later operation.

### Step 2.3 Exact duplicates and identifiers

**Method and reason** — Separate identical rows from repeated identifiers. Identifiers have different intended roles, so interpreting repetition requires knowing the table's row unit.

| Code | Plain-language explanation |
|---|---|
| `dataframe.duplicated().sum()` | Counts identical full rows after the first occurrence. |
| `key_definitions` | Lists the identifier columns to inspect and how repetition should be interpreted. |
| `dataframe[key_columns]` | Selects the single or composite identifier under inspection. |
| `.isna().any(axis=1).sum()` | Counts rows where at least one component of that identifier is missing. |
| `.duplicated(subset=key_columns).sum()` | Counts additional rows sharing the same key after the first occurrence. |
| `" + ".join(key_columns)` | Formats a composite key clearly in the summary. |
| `pd.DataFrame(key_rows)` | Collects the key checks into one table. |

**Observed output**

| Check | Measured result |
|---|---:|
| Unique stable customer identifiers | 96,096 |
| Customer records beyond the first stable-ID occurrence | 3,345 |
| Exact duplicate geolocation rows after the first occurrence | 261,831 |
| Exact duplicate rows in the other eight tables | 0 |
| Additional repeated review-ID occurrences | 814 |
| Additional repeated order-ID occurrences in reviews | 551 |
| Missing or duplicated expected-unique keys | 0 |

**Interpretation** — Additional repeated-key rows are not the number of distinct groups affected. Several order-level customer records may correspond to one person. Several line items or payment records may belong to one order. Repeated review identifiers need deeper inspection. Repeated postal prefixes can represent multiple geographic observations.

**Decision** — Preserve the source rows during this checkpoint. In the cleaning section, inspect review multiplicity and prepare a justified geolocation lookup. Frequency and spending calculations will use a deliberate aggregation grain.

### Step 2.4 Relationship coverage

**Method and reason** — Check parent references without merging tables, then measure which orders lack item, payment, or review records. This reveals possible row loss from future inner joins.

| Code | Plain-language explanation |
|---|---|
| `relationships` | Lists child and parent table-column pairs to check. |
| `child_values` and `parent_values` | Select the identifiers on either side of a relationship. |
| `parent_values.dropna()` | Excludes missing parent values from the matching lookup. |
| `child_values.isin(parent_values)` | Checks whether each child value appears in the parent values. |
| `~...` | Reverses a boolean mask, selecting the non-matches. |
| `child_values.notna() & ~child_values.isin(parent_values)` | Selects observed child identifiers with no parent match, separating them from missing child identifiers. |
| `unmatched.sum()` | Counts unmatched child rows. |
| `order_ids.isin(tables[related_table]["order_id"])` | Checks whether each order has at least one related record. |
| `(~...).sum()` | Counts orders without such a record. |

**Observed output**

| Relationship or coverage check | Result |
|---|---:|
| Unmatched order customer identifiers | 0 |
| Unmatched item order, product, or seller identifiers | 0 |
| Unmatched payment or review order identifiers | 0 |
| Products with an observed category absent from translations | 13 |
| Customer records with postal prefixes absent from geolocation | 278 |
| Seller records with postal prefixes absent from geolocation | 7 |
| Orders without item records | 775 |
| Orders without payment records | 1 |
| Orders without review records | 768 |

**Decision** — Inspect missing relationships before choosing join types or order eligibility. Aggregate repeated detail records before joining when necessary. An optional geographic or text field should have a deliberate missing-data policy.

### Verification and commit checkpoint

- Reran the notebook's seven code cells in order against the actual CSV files and saved their outputs.
- Checked that the column profile contains one entry for each of the 52 source columns.
- Confirmed all expected-unique keys have zero missing or duplicated key rows.
- Verified all nine defined relationship checks ran.
- Added interpretation of measured findings in notebook section 2.5.
- Created diagnostic summaries while retaining the loaded source tables for subsequent work.

**Suggested commit message** — `feat: inspect Olist schemas missing data and keys`.

**Commit status** — Pending.

## Step 3 Prepare timestamps and inspect order timing

**Notebook location** — `olist_pipeline.ipynb`, sections 3.1 through 3.3.

**Purpose** — Convert timestamp strings for date comparisons while retaining evidence about missing or inconsistent events.

| Code or method | Explanation and reason |
|---|---|
| `date_columns` | Lists the eight timestamp columns in orders, items, and reviews. |
| `prepared_tables = tables.copy()` | Copies the dictionary mapping. Its DataFrames are initially shared. |
| `tables[table_name].copy()` | Creates an independent working DataFrame for each table being changed. |
| `pd.to_datetime(..., format=..., errors="coerce")` | Parses the stated timestamp format and represents unparseable values as NaT. |
| `original.notna() & converted.isna()` | Identifies newly missing values caused by failed parsing, separating them from pre-existing missingness. |
| `conversion_rows.append(...)` | Records counts before and after each conversion and the resulting dtype. |
| `prepared_tables[table_name][column_name] = converted` | Assigns converted dates to the copied working table. |
| `.isna()` | Creates missing-value indicators for lifecycle dates. |
| `.insert(0, ...)` | Adds the status or group-size column at the beginning of a summary. |
| `.groupby("order_status").sum()` | Counts missing dates within each recorded status. |
| `.groupby("order_status").size()` | Counts orders in each status group. |
| `.agg(["min", "max"])` | Finds the earliest and latest observed purchase timestamps. |
| `event_pairs` | Defines actual event sequences to inspect. |
| `earlier.notna() & later.notna()` | Restricts each sequence check to orders with both timestamps available. |
| `later < earlier` | Detects a reversed event sequence. |
| `order_timing_flags` | Holds order identifiers and separate boolean flags for later inspection. |
| `.any(axis=1).sum()` | Counts distinct rows with at least one flag, avoiding double counting across checks. |

### Observed conversion results

| table | column | missing_before | parse_failures | missing_after | new_dtype |
| --- | --- | --- | --- | --- | --- |
| orders | order_purchase_timestamp | 0 | 0 | 0 | datetime64[us] |
| orders | order_approved_at | 160 | 0 | 160 | datetime64[us] |
| orders | order_delivered_carrier_date | 1783 | 0 | 1783 | datetime64[us] |
| orders | order_delivered_customer_date | 2965 | 0 | 2965 | datetime64[us] |
| orders | order_estimated_delivery_date | 0 | 0 | 0 | datetime64[us] |
| order_items | shipping_limit_date | 0 | 0 | 0 | datetime64[us] |
| order_reviews | review_creation_date | 0 | 0 | 0 | datetime64[us] |
| order_reviews | review_answer_timestamp | 0 | 0 | 0 | datetime64[us] |

### Missing lifecycle dates by recorded status

| order_status | orders | order_purchase_timestamp | order_approved_at | order_delivered_carrier_date | order_delivered_customer_date | order_estimated_delivery_date |
| --- | --- | --- | --- | --- | --- | --- |
| approved | 2 | 0 | 0 | 2 | 2 | 0 |
| canceled | 625 | 0 | 141 | 550 | 619 | 0 |
| created | 5 | 0 | 5 | 5 | 5 | 0 |
| delivered | 96478 | 0 | 14 | 2 | 8 | 0 |
| invoiced | 314 | 0 | 0 | 314 | 314 | 0 |
| processing | 301 | 0 | 0 | 301 | 301 | 0 |
| shipped | 1107 | 0 | 0 | 0 | 1107 | 0 |
| unavailable | 609 | 0 | 0 | 609 | 609 | 0 |

### Event sequence results

| check | orders_with_both_events | inconsistent_orders |
| --- | --- | --- |
| approval_before_purchase | 99281 | 0 |
| carrier_before_approval | 97644 | 1359 |
| delivery_before_carrier | 96475 | 23 |
| delivery_before_purchase | 96476 | 0 |

Distinct orders with at least one timing flag — 1382.

Observed purchase timestamp coverage — 2016-09-04 21:15:19 through 2018-10-17 17:30:18.


### Verification and decisions

- Executed all ten notebook code cells in order and saved their actual outputs.
- Verified eight conversion audit entries and the identity between original missingness, parse failures, and final missingness.
- Verified the three changed working tables retain their row counts.
- Verified original date columns remain in their loaded representation and working date columns have datetime dtypes.
- Kept missing lifecycle values as NaT while inspecting status. Future missing-data handling will depend on task and event availability.
- Stored chronological flags for investigation before choosing exclusions.
- Recorded statuses are descriptive here. Predictive features will need historical availability checks.
- The prepared mapping shares unchanged source DataFrames. Future transformations must copy a table before modifying it.

**Suggested commit message** — `feat: parse Olist timestamps and audit order timing`.

**Commit status** — Pending.

## Next notebook section

Investigate repeated review identifiers and multiple reviews per order. Choose a reproducible selection or aggregation rule with explicit review timing, before preparing order-level review features.
