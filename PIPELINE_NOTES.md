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
7. Once the complete topic is finished and verified, review and commit the notebook, notes, and relevant README updates together.

A topic may span several sections and coding sessions. Keep notes current throughout the work, then create one meaningful contribution for the completed topic, such as data cleaning or EDA. Record genuine problems and fixes when they occur.

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

**Contribution** — Included in the data cleaning and preparation topic.

**Commit status** — Pending.

## Step 4 Investigate reviews and prepare order-level summaries

**Notebook location** — `olist_pipeline.ipynb`, sections 3.4 through 3.6.

**Purpose** — Distinguish repeated identifiers from multiple reviews per order, then create a reproducible one-row-per-order review summary.

**Inputs** — Timestamp-prepared review and order tables.

### Code and method explanations

| Code or method | Explanation and reason |
|---|---|
| `review_events = prepared_tables["order_reviews"].copy()` | Creates an independent review working table and retains all original review rows. |
| `.groupby("review_id").agg(...)` | Counts records and distinct orders sharing each review identifier. |
| `.groupby("order_id").agg(...)` | Counts review rows, distinct review identifiers, and distinct scores per order. |
| `"size"` | Counts rows in a group. |
| `"nunique"` | Counts distinct observed values in a group. |
| `multiple_reviews` | Selects orders with more than one review row. |
| `changing_scores` | Selects those orders whose observed review scores differ. |
| `.duplicated(["review_id", "order_id"])` | Checks the combined review-order key instead of assuming review ID alone is unique. |
| `.head(3).index` | Chooses three example order identifiers with changing scores. |
| `.loc[...isin(example_order_ids), ...]` | Displays the relevant records and fields for those example orders. |
| `review_available_at` | Uses the recorded answer timestamp as an availability proxy. |
| `raise ValueError(...)` | Stops selection if timestamps or combined keys need further investigation. |
| `.sort_values(..., kind="stable")` | Orders events chronologically with explicit tie breakers. |
| `.drop_duplicates(subset="order_id", keep="first")` | Selects the earliest answered review for each order after sorting. |
| `.rename(columns=...)` | Makes the first-review meaning explicit in the resulting column names. |
| `.reset_index(drop=True)` | Gives the selected summary a consecutive row index. |
| `.set_index("order_id")` | Builds a purchase-time lookup keyed by unique order identifier. |
| `.map(purchase_times)` | Looks up the associated purchase timestamp for each review row. |
| `eligible_review_events` | Selects reviews with an observed purchase date and an answer at or after that purchase. |
| `.merge(..., how="left", validate="one_to_one")` | Tests review enrichment while preserving orders and checking key uniqueness. |
| `validate="many_to_one"` | Allows several review events to link to one order while checking the order-side key. |
| `first_review_available_at <= prediction_time` | The eligibility rule to apply when constructing future historical review features. |
| `.groupby(...).min()` | Independently finds the earliest eligible availability time per order. |
| `.equals(...)` | Verifies selected timestamps match those earliest times for every order. |

### Observed review audit

| check | count |
| --- | --- |
| Exact duplicate review rows | 0 |
| Repeated review ID groups | 789 |
| Review IDs attached to multiple orders | 789 |
| Repeated review and order key rows | 0 |
| Orders with multiple review rows | 547 |
| Multi-review orders with different scores | 202 |
| Repeated order and answer timestamp rows | 0 |

### Selection counts

| measure | count |
| --- | --- |
| Review event rows retained | 99224 |
| Review rows eligible after timing check | 99161 |
| Answers before purchase excluded from selection | 63 |
| First review rows selected | 98613 |
| All event rows outside the selected summary | 611 |

### Join and timing checks

| check | count |
| --- | --- |
| Orders before review join | 99441 |
| Orders after review join | 99441 |
| Orders without selected review | 828 |
| Answers recorded before purchase | 63 |
| Answers recorded before review creation | 0 |

### Decisions and interpretation

- Found 63 answers timestamped before their associated purchases. Retained and flagged these in the event table, then excluded them from summary selection.
- Mapped each order's purchase date using a unique order index. Selected eligible reviews only when a purchase date exists and the answer is at or after it.
- The timing eligibility check complements the later prediction-date availability check.

- The audit found repeated review identifiers attached to different orders. Removing records by review ID alone would lose order-review relationships.
- Multiple review rows on one order can have different scores. Earliest response among records passing the purchase-timing check is the documented initial selection rule.
- Keep the full `review_events` table for future analysis and alternative time-aware policies.
- Keep the first review's timestamp with its score. Future feature construction must check that timestamp against the historical prediction date.
- Review availability uses the recorded answer time as a proxy. The dataset cannot establish earlier visibility of content that may have been edited.
- Orders lacking a review retain a missing review signal in the test left join.
- Retain later reviews in the event table and keep descriptive review selection separate from a future repeat-purchase target.

### Verification and commit checkpoint

- Executed all thirteen code cells in notebook order against the actual CSVs.
- Verified unique order identifiers and one selected row for each order with an eligible review.
- Independently checked every selected timestamp against the minimum eligible answer timestamp for its order.
- Verified that the test review merge preserves the source order count.
- Saved executed outputs, changing-score examples, and measured audit tables in the notebook.

**Contribution** — Included in the data cleaning and preparation topic.

**Commit status** — Pending.

## Complete topic Data cleaning and preparation

The timestamp and review sections above are parts of this single topic. Notebook execution and learning notes are reviewed and committed together at topic completion.

### Geolocation lookup

**Notebook section** — 3.7.

Drop exact duplicate observations before calculating median coordinates per prefix. Exclude missing or physically invalid coordinates from this lookup input. Left-join the unique lookup to customers and sellers using a many-to-one validation and keep match flags.

| measure | count |
| --- | --- |
| Original observations | 1000163 |
| Exact duplicate rows removed from lookup inputs | 261831 |
| Distinct observations excluded by coordinate checks | 0 |
| Unique postal prefixes in lookup | 19015 |
| Customer records without coordinates | 278 |
| Seller records without coordinates | 7 |

### Product metadata

**Notebook section** — 3.8.

Join category translations with many-to-one validation. Use an explicit unknown label for missing categories and preserve untranslated original names in fallback labels. Keep separate missing and untranslated flags. The 13 untranslated products use the original categories portateis_cozinha_e_preparadores_de_alimentos and pc_gamer.

Nonpositive physical weight or dimensions become missing measurements with flags. Other observed missing physical or descriptive values remain available for later training-fitted imputation.

| column | original_missing | nonpositive_to_missing |
| --- | --- | --- |
| product_weight_g | 2 | 4 |
| product_length_cm | 2 | 0 |
| product_height_cm | 2 | 0 |
| product_width_cm | 2 | 0 |

### Items and payments

**Notebook section** — 3.9.

Validate composite keys, then aggregate items and payments separately to order-level summaries. Count source item rows as item count and preserve distinct product and seller counts. Sum prices and freight from item rows, and payment values from payment rows. Keep observed zero payments and freight. Flag the two zero-installment records.

### Analytical tables and validation

**Notebook sections** — 3.10 and 3.11.

Use left joins to create order_facts at one row per order, with stable customer identity and optional detail signals. Create purchase_events at one row per order item. Both retain the source row counts for their respective row units.

| table | rows | row_unit |
| --- | --- | --- |
| order_facts | 99441 | one source order |
| purchase_events | 112650 | one source order item |
| products_prepared | 32951 | one source product |
| first_review_per_order | 98613 | one order with an eligible review |
| geolocation_lookup | 19015 | one postal-code prefix |

| amount | source_total | prepared_total | absolute_difference |
| --- | --- | --- | --- |
| items_value | 13591643.7 | 13591643.7 | 0.0 |
| freight_total | 2251909.54 | 2251909.54 | 0.0 |
| payment_total | 16008872.12 | 16008872.12 | 0.0 |

### Code reference

| Code or method | Explanation and reason |
|---|---|
| `.drop_duplicates()` | Removes identical geolocation observations from lookup inputs. |
| `.between(lower, upper)` | Checks physical latitude and longitude bounds. |
| `.groupby(..., as_index=False).agg(...)` | Creates one record per grouping key with explicit summary calculations. |
| `"median"` | Calculates a representative coordinate robust to extreme observations. |
| `"size"` | Counts source records within each group. |
| `"nunique"` | Counts distinct product, seller, or payment-method values. |
| `"sum"` | Adds values once at the chosen input grain. |
| `.merge(..., validate="many_to_one")` | Checks that the enrichment table is unique on the join key. |
| `.merge(..., validate="one_to_one")` | Checks uniqueness on both sides of an order-level merge. |
| `how="left"` | Preserves the left table's records while representing missing matches. |
| `.fillna(...)` | Applies explicit category labels using translations, original category names, and then unknown. |
| `.le(0)` | Flags nonpositive physical measurements. |
| `.loc[invalid, column] = float("nan")` | Replaces invalid working measurements with missing values, retaining the product and its flag. |
| `.eq(0)` | Identifies zero-installment records for an explicit flag. |
| `.notna()` | Creates match and record-availability flags. |
| `.is_unique` | Checks identifier uniqueness after preparation. |
| `assert` | Stops notebook execution if a required validation fails. |
| `abs(source_total - prepared_total)` | Measures any monetary change introduced by aggregation and joins. |

### Interpretation and deferred modeling decisions

- Coordinate lookup and optional enrichment preserve customer and seller row counts.
- Source order status and all source orders remain available for EDA. Eligible purchase or retention cohorts will be defined with the target and prediction time.
- Timing flags are retained as evidence for later feature or eligibility decisions.
- Selected review features require a prediction-date availability check even after the review timing audit.
- No statistical outlier trimming or full-dataset imputation has been applied. EDA will inform later preprocessing choices.
- Prepared tables are in-memory outputs of notebook execution. The application will later use extracted, verified pipeline components.
- Full-snapshot analytical tables describe the downloaded data. Historical model features must be computed from information available at the prediction date.

### Topic verification

Executed all eighteen code cells in order and saved their outputs. Validated source row counts at the order, item, product, customer, and seller grains. Checked category completeness, stable customer mapping, lookup uniqueness, and independent monetary reconciliation.

**Topic commit message** — `feat: complete Olist data cleaning and validated table preparation`.

**Files in the same contribution** — `olist_pipeline.ipynb`, `PIPELINE_NOTES.md`, and the relevant `README.md` update.

**Commit status** — Pending user review and commit.

## Complete topic Exploratory data analysis

**Notebook location** — Section 4, subsections 4.1 through 4.9.

**Purpose** — Understand the prepared data and collect evidence for feature engineering, prediction targets, recommendation methods, and evaluation.

### Cohort definitions and row units

The status and monthly coverage views use all 99,441 source orders. Behavioral analyses use 96,478 delivered orders with item records, containing 110,197 item rows and 93,358 distinct customers. This is a retrospective descriptive cohort. Eventual delivery status requires a separate availability check in future historical prediction tasks.

Merchandise value sums item prices once per order and excludes freight. Review comparisons use the earliest eligible answered review from cleaning and record the smaller cohort with usable delivery dates. Repeated purchases are counted using stable customer identity and distinct orders.

### Plot-by-plot findings


#### Order status and scope

The delivered cohort contains 96,478 of 99,441 source orders. Smaller status groups remain relevant when choosing a later prediction-time cohort.

#### Monthly activity and observation boundaries

The snapshot contains 6,512 source orders in August 2018, then 16 in September and 4 in October. The latter two months contain no delivered orders in this cohort. Treat the sparse tail as a coverage concern when choosing the modeling interval, rather than interpreting it as an established collapse in demand.

#### Spending and freight

Median merchandise value is BRL 86.57, while the 99th percentile is BRL 990.00. The broad range supports evaluating a log transform or robust preprocessing later. The scatter uses at most 5,000 orders with random seed 42 for readability, while statistics use the full cohort.

#### Customer activity and repeat intervals

There are 93,358 customers and 2,801 observed repeat buyers, or 3.00 percent. Among observed repeat buyers, the median first-to-second interval is 28.98 days. Different history lengths make the follow-up analysis necessary before using a repeat label.

#### Product demand and sparse interactions

The cohort has 99,785 distinct customer-product pairs and 32,216 products. Interaction sparsity is 99.99668 percent, and 59.52 percent of products have just one observed buyer. Compare collaborative methods with popularity and content-based fallbacks, and report the eligible recommendation cohort.

#### Geographic concentration

SP accounts for 41.98 percent of delivered orders in the cohort. Compare later error rates together with subgroup sample sizes so a dominant region does not hide weak performance elsewhere.

#### Reviews and delivery experience

The comparison includes 95,821 reviewed orders with usable delivery timing. Scores 1 to 3 occur in 73.20 percent of late cases and 17.32 percent of on-time cases. This is a strong descriptive association. Confounding, review selection, and review timing prevent a causal conclusion. Review scores describe the order experience and require care before use as product-preference labels.

#### Numeric correlations

Delivery duration and the first review score have a negative Pearson correlation of approximately -0.33 in this cohort. Merchandise value and freight correlate at approximately 0.41. Evaluate skew, temporal availability, and missingness before turning an association into a feature choice.

#### Candidate repeat-purchase windows

The provisional 90-day cohort contains 75,320 customers with 1,714 observed repeaters, or 2.28 percent. A constant non-repeat classification would have arithmetic accuracy of 97.72 percent in this cohort, showing why accuracy alone is insufficient. The final target still needs a verified coverage boundary and a prediction-date definition.

### Follow-up cohort measurements

| Window in days | Eligible customers | Repeat customers | Repeat percent |
|---|---:|---:|---:|
| 30 | 86,772 | 1,373 | 1.58 |
| 60 | 81,203 | 1,584 | 1.95 |
| 90 | 75,320 | 1,714 | 2.28 |


Eligibility denominators differ between windows. Each includes customers whose first purchase plus the stated horizon falls on or before the provisional delivered-purchase coverage end. Percentages reflect horizon and cohort composition. Same-day distinct orders count as repeats. This is target-feasibility analysis. The final model cohort and prediction-date convention remain to be established.

### Code and method reference

| Code or method | What it does and why it is used |
|---|---|
| `import numpy as np` | Imports numeric array operations used for plot bins, labels, and conditions. |
| `import matplotlib.pyplot as plt` | Imports plotting functions. |
| `%matplotlib inline` | Enables embedded figures in a notebook environment. |
| `plt.rcParams.update(...)` | Sets shared fonts, resolution, and visual formatting for consistent figures. |
| `.loc[condition].copy()` | Creates an independent analysis cohort using explicit eligibility rules. |
| `.value_counts()` | Counts statuses, scores, or category occurrences. |
| `.groupby(...).size()` | Counts records at the specified group grain. |
| `.dt.to_period("M")` | Groups purchase timestamps by calendar month. |
| `pd.period_range(...)` | Creates a complete monthly index across the observed range. |
| `.reindex(..., fill_value=0)` | Includes months or score levels with no observations. |
| `.describe(percentiles=...)` | Reports counts, location, spread, and tail percentiles. |
| `np.geomspace(...)` | Creates logarithmically spaced histogram bins over the full positive range. |
| `.sample(..., random_state=42)` | Selects a deterministic plotting sample without changing the full-cohort calculations. |
| `.agg(...)` | Defines distinct order counts, spending sums, and purchase dates per customer. |
| `.ge(2)` | Flags customers with at least two observed delivered orders. |
| `.cumcount()` | Numbers each customer's sorted orders from zero, allowing selection of the second one. |
| `.set_index(...)` | Aligns second-purchase timestamps with the customer-level summary. |
| `.dt.total_seconds().div(86400)` | Expresses timestamp differences in fractional days. |
| `.drop_duplicates()` | Counts each observed customer-product pair once for binary interactions. |
| `1 - pairs / (users * products)` | Calculates interaction sparsity from counts without creating a dense matrix. |
| `.cumsum()` | Calculates cumulative demand share after ranking products by observed buyers. |
| `.head(10)` | Selects leading categories or states for readable displays. |
| `.dt.normalize()` | Compares delivery and promised dates at the calendar-day level. |
| `np.where(...)` | Creates readable delivery-timing groups from a boolean condition. |
| `.le(3)` | Flags review scores from 1 to 3 for the stated descriptive comparison. |
| `.corr(method="pearson")` | Measures linear pairwise associations among numeric order fields. |
| `pd.Timedelta(days=...)` | Constructs candidate future follow-up windows. |
| `first_purchase + horizon <= coverage_end` | Excludes customers without a full candidate observation window. |
| `second_purchase <= first_purchase + horizon` | Identifies a repeat event within the candidate window. |
| `plt.subplots(...)` | Creates a figure and its axes, using constrained layout to preserve labels. |
| `.bar(), .barh(), .hist(), .plot(), .scatter()` | Visualizes counts, distributions, time trends, and paired measurements. |
| `.set_xscale("log") / .set_yscale("log")` | Displays a broad positive range without hiding small groups. |
| `"symlog"` | Supports a logarithmic-like axis while retaining zero freight values. |
| `.bar_label(...)` | Adds measured counts, percentages, or cohort sizes to bars. |
| `.imshow(..., vmin=-1, vmax=1)` | Draws correlations on their fixed mathematical range. |
| `plt.show()` | Embeds the current figure as a notebook output. |

### Decisions supported by the evidence

- Compare recommendation methods against popularity and use content metadata or popularity fallbacks for limited histories.
- Report ranking evaluation eligibility and catalog coverage because extreme sparsity restricts who and what can be tested.
- Plan imbalance-sensitive retention metrics and compare with simple baselines. A high raw accuracy can result from the majority class alone.
- Verify the modeling coverage end before constructing historical labels and chronological partitions.
- Evaluate skew-aware numeric preprocessing after the split. Preserve outliers until a task-specific rule has evidence.
- Include review and delivery features only when their underlying events would be available at the prediction date.
- Treat delivery-score differences and correlations as associations. This EDA does not identify a causal effect of delivery or marketing outreach.

### Reproducibility and verification

Created a local .venv environment and requirements.txt for pandas, NumPy, plotting, notebook kernels, and notebook schema validation. Ignore rules cover the local environment and future untracked raw downloads. All nine current raw CSVs are already tracked in Git, so the rule does not untrack them. Repository data tracking can be handled separately from this EDA contribution.

Executed all 29 code cells in order using in-process IPython and validated the saved notebook with nbformat. The separate Jupyter-kernel launch stalled, so verification used the in-process execution route. All nine figure outputs are embedded in the notebook and were visually inspected for readable labels, complete plots, units, cohort labels, and scales.

The source data and earlier preparation validations ran again before EDA. No model training or fitted preprocessing is part of this topic.

**Topic commit message** — `feat: complete Olist exploratory analysis and document findings`.

**Files in the same contribution** — `olist_pipeline.ipynb`, `PIPELINE_NOTES.md`, `README.md`, `requirements.txt`, and `.gitignore`.

**Commit status** — Pending user review and commit.

## Complete topic Historical features targets and chronological partitions

**Notebook location** — Section 5, configuration and subsections 5.1 through 5.6.

**Purpose** — Define a reproducible business prediction time, build historical-only inputs, create future labels, and establish fair partitions for both retention and recommendation.

### Decisions and operating scope

- Working observation boundary is 1 September 2018, exclusive, because the later source months are sparse. This is a documented completeness assumption to revisit in sensitivity analysis.
- Use item-bearing placed orders. Final delivery status is excluded from event eligibility, avoiding a future outcome as a historical filter.
- Another placed order is the target event, including a later-canceled order with line items. This measures future placed-order activity.
- Assign one snapshot 30 days after each customer's first observed placed purchase. Predict an order strictly after that snapshot and within the next 90 days.
- Require the full outcome window to end before the observation boundary. Incomplete follow-up is excluded from the labeled cohort.
- The fixed-age retention task supports scoring at that customer age. Applying it at arbitrary ages would require a broader snapshot design and new evaluation.
- Checkout amounts and product identifiers are treated as order-time observations. Review answers use their recorded timestamps as availability proxies. Later edits cannot be reconstructed from the static CSV snapshot.

### Snapshot and label measurements

| measure | count |
| --- | --- |
| Customers with an observed item-bearing order | 95420 |
| Snapshots meeting start and complete-follow-up rules | 71105 |
| Eligible snapshots with a future repeat order | 665 |

The EDA repeat percentages use different event eligibility and follow-up origins. They should not be compared as if they were the same target.

### Historical feature definitions

| Feature | Formula or definition | Availability rule |
|---|---|---|
| recency_days | Days from snapshot to latest historical placed purchase | Purchase is at or before snapshot |
| historical_order_count | Distinct historical order identifiers | Purchase is at or before snapshot |
| distinct_products | Distinct product IDs across historical item rows | Item's order is in historical orders |
| distinct_sellers | Distinct seller IDs across historical item rows | Item's order is in historical orders |
| log1p_merchandise_spend | Natural logarithm of one plus historical item-price total | Amounts from historical orders only |
| log1p_average_order_value | Natural logarithm of one plus mean historical merchandise order value | One observation per historical order |
| freight_ratio | Historical freight total divided by historical merchandise value | Both totals from historical orders |
| known_review_count | Number of first eligible order reviews known by snapshot | Answer time is at or before snapshot |
| mean_known_review_score | Mean score across those known reviews | Unavailable mean remains missing |
| known_delivery_count | Count of customer deliveries recorded by snapshot | Delivery is by snapshot and at or after purchase |
| mean_known_delivery_days | Mean purchase-to-delivery duration across known deliveries | Unavailable mean remains missing |
| customer_state | State on earliest observed historical order | Uses only the customer's historical order records |

Identifiers, raw final status, future_order_count, repeat_90d, outcome_end, and audit timestamps stay outside the explicit model predictor lists. Customer age is constant at 30 days by design, so it is omitted from the features.

The log1p transform is a fixed arithmetic operation. It fits no distribution parameters. Imputation, encoding, scaling, class weights, and models will be learned from training data in the baseline topic.

### Retention partitions and maturation gaps

Training outcome windows must end before 1 November 2017, the validation prediction start. Validation snapshots start on that date and must have outcomes ending before 1 April 2018, the test prediction start. Test snapshots start in April and must retain complete 90-day follow-up before the working boundary.

| partition | customers | repeat_customers | repeat_percent | first_snapshot | last_snapshot | latest_outcome_end |
| --- | --- | --- | --- | --- | --- | --- |
| train | 14362 | 140 | 0.975 | 2017-01-22 23:16:47 | 2017-08-02 23:50:35 | 2017-10-31 23:50:35 |
| validation | 11768 | 97 | 0.824 | 2017-11-01 00:28:03 | 2017-12-31 23:54:03 | 2018-03-31 23:54:03 |
| test | 14213 | 120 | 0.844 | 2018-04-01 00:07:09 | 2018-06-02 23:59:21 | 2018-08-31 23:59:21 |

Snapshots excluded from the primary comparison in the maturation gaps — 30,762.


Customers have one assigned snapshot, so customer IDs are disjoint across these primary partitions. The gaps deliberately prevent outcomes from a later evaluation period from entering earlier training labels.

Positive counts are 140, 97, and 120 in train, validation, and test. The rare class and small counts constrain tuning and require uncertainty reporting. High majority-class accuracy alone would be insufficient evidence.

### Recommendation event and candidate protocol

Use user, item, order_id, and time from item-bearing placed-order events. Maintain source events and deduplicated customer-product pairs separately.

Validation history ends before 1 April 2018, with a future window ending before 1 May. Final test history ends before 1 June, with a future window ending before 1 July. Final fitting may use prior validation-period interactions once settings are selected, while test-future interactions remain held out.

Candidates are products observed in history. Eligible relevance consists of future customer-product pairs where the customer has historical purchases, the product is in the historical candidate catalog, and the same pair was not already observed.

| partition | history_pairs | candidate_products | future_customers | future_unique_pairs | cold_customer_pairs | unseen_catalog_pairs | already_purchased_pairs | eligible_relevance_pairs | eligible_ranking_customers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| validation | 68203 | 22964 | 6878 | 7210 | 7023 | 2497 | 26 | 97 | 90 |
| test | 82461 | 26895 | 6121 | 6394 | 6187 | 2243 | 29 | 102 | 97 |

Cold-user pairs, unseen-catalog pairs, and already-purchased pairs are reported as separate diagnostics. Categories can overlap. Most future activity is from cold users. Only 90 validation and 97 test customers have positive eligible warm-discovery relevance. Report this limited benchmark population alongside application fallbacks and coverage.

Unobserved pairs are unknown, and no dislike labels or artificial explicit ratings are created. No minimum of five interactions is imposed on historical customers.

### Code and method reference

| Code or method | Explanation and reason |
|---|---|
| pd.Timestamp | Stores explicit chronological boundaries. |
| pd.Timedelta | Adds the fixed customer age or future outcome horizon. |
| .lt, .le, .gt, .ge | Makes inclusive and exclusive time rules explicit. |
| .groupby(...).min() | Finds each customer's first observed placed purchase. |
| .rename(...).to_frame() | Gives the first-purchase series a named table representation. |
| .merge(..., validate='many_to_one') | Links many events to one customer snapshot or order record while checking parent uniqueness. |
| .merge(..., validate='one_to_one') | Checks uniqueness when combining customer-level feature blocks. |
| .nunique() | Counts distinct orders, products, or sellers at the intended grain. |
| .map(future_counts).fillna(0) | Assigns a zero future-order count only to snapshots with complete follow-up and no observed qualifying order. |
| .gt(0).astype(int) | Creates the binary repeat target from future order counts. |
| .sort_values(...) | Gives earliest-state selection a reproducible historical ordering. |
| .agg(...) | Creates explicit order, breadth, and known-event summaries. |
| .where(availability_mask) | Keeps review or delivery values only when available by the snapshot, representing other values as missing. |
| .count() | Counts observed known-event values, excluding missing values. |
| .mean() | Averages only observed eligible historical values. |
| np.log1p | Applies the fixed log transform to nonnegative historical monetary values. |
| RETENTION_FEATURES | Declares the exact predictor allowlist used to create X matrices. |
| X_train and y_train | Hold training predictors and labels with aligned row indices. |
| X_validation and X_test | Preserve chronological holdouts for later tuning and final evaluation. |
| build_recommendation_window | Reuses one candidate and relevance protocol for validation and test. |
| .drop_duplicates() | Creates one row per customer-product pair without assigning ratings. |
| history_pairs.assign(...) | Marks previously observed pairs for a validated future-pair lookup. |
| .isin(...) | Checks whether future users and products exist in history. |
| .eq(True) | Converts matched history markers into the already-purchased flag. |
| .isdisjoint(...) | Verifies that no customer occurs in multiple primary retention partitions. |
| np.isinf(...) | Checks numeric matrices for invalid infinite results while allowing missing means for later imputation. |
| .sample(..., random_state=42) | Selects reproducible positive and negative records for independent source-event label checks. |

### Model-ready in-memory objects

- retention_dataset contains features, labels, and audit fields.
- retention_partitions holds the three chronological customer cohorts.
- X_train, X_validation, and X_test contain only the declared predictors.
- y_train, y_validation, and y_test contain the repeat_90d label.
- recommendation_partitions contains history events, historical pairs, candidates, future windows, coverage annotations, and positive discovery relevance.
- The notebook regenerates these objects. Model artifact saving and application integration belong to later topics.

### Verification

Executed all 36 notebook code cells in order using in-process IPython, with the prior cleaning checks and EDA still producing their saved outputs.

Verified customer uniqueness, historical feature availability, complete target follow-up, future event intervals, disjoint customer IDs, label maturation, predictor allowlists, finite numeric inputs, and both target classes in each retention partition. Independently recomputed labels and future order counts for 50 positive and 50 negative sampled snapshots from the source event times.

For each recommendation window, verified historical and future event boundaries, candidate uniqueness, known-user and known-product relevance, absence of previously purchased relevance pairs, and a nonempty eligible cohort.

**Topic commit message** — `feat: define historical features repeat targets and temporal splits`.

**Files in the same contribution** — `olist_pipeline.ipynb`, `PIPELINE_NOTES.md`, and `README.md`.

**Commit status** — Pending user review and commit.

## Complete topic Training-fitted preprocessing and baseline models

**Notebook location** — Section 6 and baseline validation checks, with supplementary uncertainty in Appendix A.

**Purpose** — Establish initial validation reference performance for future repeat-order classification and product discovery, using permitted training data only.

### How the two provided notebooks inform this work

| Source | Actual adaptation in our notebook | Remaining source-inspired work |
|---|---|---|
| eda-satisfaction-prediction-nlp-rfm-deployment.ipynb | Data-preparation and EDA workflow, customer RFM concepts, Pipeline and ColumnTransformer structure, median imputation, scaling, categorical encoding, and classification workflow | Comparative classifiers, justified customer segmentation, and deployment. Review-text NLP is optional |
| Week10_Project_Starter_Template (1).ipynb | Recommender progression, historical popularity, seen-item exclusion, Precision at K, Recall at K, NDCG at K, basic cold-user and short-history checks | Content-based and collaborative methods, SVD, hybrid comparison, extended cold-start experiments, collaborative by-hand calculation, deliberate leakage experiment, and full understanding logs |

The Kaggle reference classifies satisfaction and also analyzes review text. Our supervised target is future repeat-order activity under the explicit customer-age and follow-up rules. Its reported scores therefore measure a different task.

The source Kaggle RFM example counts product rows and sums payments in a merged table. Our feature pipeline counts distinct orders and aggregates item and payment tables separately before order-level joins. Our historical features use snapshot cutoffs.

The starter helpers illustrate explicit-rating workflows, including dense matrices and a rating relevance threshold. Our implementation uses binary purchase relevance and chronological candidate catalogs, with count-based popularity and on-demand recommendation lists.

Both notebooks are references and attributions for the implemented adaptations. They remain preserved under SOURCE FILES. The reference-use map near the notebook introduction identifies the actual current use and pending methods.

### Retention preprocessing and fitting

Numeric features use training medians with missingness indicators, followed by StandardScaler. State uses an explicit missing category and OneHotEncoder with unknown-category handling. ColumnTransformer applies only the predictor allowlist and drops other fields. The full preprocessing and Logistic Regression sequence is one fitted Pipeline.

Fit Logistic Regression using the 14,362 training snapshots with 140 positives. Its fixed initial regularization is C=1, with up to 2,000 iterations and random_state=42. The fit converged in 27 iterations. No sampling or class weighting was introduced in this baseline. The encoded validation representation has 40 columns.

The prior DummyClassifier learns only the training label prevalence. A constant one-column input makes that lack of feature dependence explicit.

### Retention validation measurements

| model | average_precision | roc_auc | brier_score | precision_at_0_5 | recall_at_0_5 | f1_at_0_5 | predicted_positives |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Training prior | 0.008243 | 0.5 | 0.008177 | 0.0 | 0.0 | 0.0 | 0 |
| Logistic Regression | 0.016882 | 0.515552 | 0.00819 | 0.0 | 0.0 | 0.0 | 0 |

Evaluate all 11,768 validation customers with 97 positives. At threshold 0.5, both models classify every validation customer as non-repeat, giving 11,671 true negatives and 97 false negatives.

Logistic average precision is 0.016882 compared with prior average precision 0.008243. ROC-AUC is 0.515552, showing weak overall discrimination. Its Brier score of 0.008190 is slightly worse than the prior's 0.008177. These are initial validation benchmarks. Class imbalance, fixed-age features, and small positive counts limit conclusions.

The precision-recall and ROC curves are saved in the notebook. Threshold selection is deferred until model comparison and an explicit decision policy. Final test predictions have not been generated in this topic.

### Historical popularity recommendation

Use distinct historical buyer counts from the 68,203 pre-validation customer-product pairs. The candidate catalog contains 22,964 products. Sort by buyer count descending, then product identifier ascending for deterministic ties.

recommend_popular excludes previously purchased products and returns product ID, category label, and historical buyer count. New users receive the same historical popularity fallback. Metadata-only new products have no evidence for this baseline.

Top-K metric formulas adapt the Week 10 helper cell. Precision uses K as its denominator, recall uses the relevant future discovery set, and NDCG normalizes discounted hits by the ideal arrangement. Duplicate recommendation IDs are rejected by the metric helper.

### Ranking validation measurements

| k | users | precision | recall | ndcg | hit_rate |
| --- | --- | --- | --- | --- | --- |
| 5 | 90 | 0.002222 | 0.011111 | 0.005556 | 0.011111 |
| 10 | 90 | 0.002222 | 0.022222 | 0.009061 | 0.022222 |

Catalog coverage at ten recommendations across evaluated users — 0.0479 percent.


Only 90 validation users have eligible warm-discovery relevance. The top-five baseline hits one user's future relevant item, and the top-ten baseline hits two users. Cold customers and unseen catalog products are outside this warm-ranking metric. Their counts remain visible in the partition coverage audit.

### Conditional bootstrap uncertainty as supplementary material

| metric | lower_95 | upper_95 | resamples |
| --- | --- | --- | --- |
| Logistic validation average precision | 0.008922 | 0.044339 | 300 |
| Popularity validation NDCG at 5 | 0.0 | 0.016667 | 1000 |

Resample retention validation customers 300 times for an average-precision percentile interval. Resample the 90 per-user NDCG at five values 1,000 times for a ranking interval. Use random generator seed 42. These intervals condition on the current fitted model and observed cohort. They do not measure training variability, future temporal changes, or cold-population performance.

The final repeated-run and literature benchmark comparison remains pending with comparative modeling and tuning.

### Code and method reference

| Code or method | Explanation and reason |
|---|---|
| SimpleImputer(strategy='median', add_indicator=True) | Learns numeric medians from training and exposes the missingness pattern. |
| keep_empty_features=True | Preserves the numeric schema if a training feature is entirely missing. |
| StandardScaler | Learns numeric location and scale from the training representation. |
| OneHotEncoder(handle_unknown='ignore') | Learns state categories from training and handles a new state at prediction time. |
| ColumnTransformer(remainder='drop') | Uses only the declared numeric and categorical features. |
| Pipeline | Fits and reuses preprocessing and classifier as one object. |
| LogisticRegression(C=1.0, max_iter=2000) | Defines the fixed initial regularized classifier. |
| .fit(X_train, y_train) | Learns transformations and classifier parameters from training only. |
| DummyClassifier(strategy='prior') | Learns the training class proportions without feature-based discrimination. |
| .predict_proba(...)[:, 1] | Gets the repeat-class probability for validation. |
| average_precision_score | Summarizes positive-case ranking using precision and recall. |
| roc_auc_score | Measures ordering across positive and negative cases. |
| brier_score_loss | Measures squared probability error. |
| probability >= 0.5 | Defines the initial thresholded classification policy. |
| zero_division=0 | Reports zero precision or F1 when the model predicts no positive cases. |
| confusion_matrix(labels=[0,1]) | Makes negative and positive class ordering explicit. |
| precision_recall_curve and roc_curve | Generate the plotted validation trade-offs. |
| .groupby('item').size() on distinct pairs | Counts each historical buyer once per product. |
| .sort_values(..., ascending=[False,True]) | Gives reproducible popularity ranking and tie breaking. |
| .agg(set).to_dict() | Builds customer histories and future relevance sets. |
| recommend_popular(user,n) | Produces an on-demand top-N list excluding already purchased products. |
| top_k_metrics | Computes binary purchase Precision, Recall, NDCG, and hit rate. |
| 1 / log2(rank + 1) | Discounts lower-ranked hits in NDCG, with rank starting at one. |
| np.random.default_rng(42) | Makes bootstrap resampling reproducible. |
| rng.integers and rng.choice | Resample customers or per-user metric values with replacement. |
| np.quantile(..., [0.025,0.975]) | Obtains the percentile interval endpoints. |
| np.testing.assert_allclose | Verifies fitted medians and prior probabilities against training-derived values. |
| n_samples_seen_ | Checks that scaling was fitted with the training row count. |

### Verification and notebook status

Executed all 43 code cells in order with in-process IPython. Validated the notebook schema, previous preparation checks, and nine existing EDA figures, plus the new validation curve figure.

Verified imputer values equal training medians, scaler fit counts match training size, and encoded states equal the training state set. Checked model convergence, finite transformed validation data, valid probabilities, and the prior average-precision identity.

Validated ranking formulas on a small by-hand example. For every evaluated user, checked unique recommendations, historical candidate membership, and seen-product exclusion. Exercised new-user and single-history fallback behavior.

The toy metric check is an integrity test. The full collaborative by-hand example requires the future collaborative model. Extended new-item handling requires content-based features.

**Topic commit message** — `feat: add training-only preprocessing and validated baseline models`.

**Files in the same contribution** — `olist_pipeline.ipynb`, `PIPELINE_NOTES.md`, `README.md`, and `requirements.txt`.

**Commit status** — Pending user review and commit.

## Complete topic Neighbors decision trees and ID3

**Syllabus mapping** — Unit II, distance-measures Lab 4, KNN Lab 5, and ID3 Lab 6.

**Notebook location** — Section 7, including the KNN worked example and the ID3 root calculation.

**Purpose** — Compare a small set of syllabus configurations, understand locality and tree complexity, and distinguish a library CART model from categorical ID3.

### Configurations and shared evaluation

Use the existing 14,362 training customers and 11,768 validation customers. Preserve the rare-class distribution. KNN configurations use K=5 and K=15, uniform voting, Euclidean distance, and training-fitted numeric scaling.

The tree configurations use entropy, maximum depths 3 and 6, and at least 50 training samples per leaf. Numeric scaling is passed through for trees, while training-fitted imputation and state encoding remain. This keeps thresholds in prepared feature units, including previously defined log monetary values.

Clone the preprocessing definitions for each estimator. Clone resets learned state. Every candidate fits only on X_train and y_train. Reuse repeat_classification_metrics so baseline and new classifier comparisons use the same metrics and 0.5 threshold.

### Training and validation results

| model | average_precision | roc_auc | precision_at_0_5 | recall_at_0_5 | f1_at_0_5 | predicted_positives | training_average_precision | validation_customers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KNN k=5 | 0.008216 | 0.49825 | 0.0 | 0.0 | 0.0 | 0 | 0.215187 | 11768 |
| KNN k=15 | 0.008963 | 0.52969 | 0.0 | 0.0 | 0.0 | 0 | 0.074084 | 11768 |
| Tree depth=3 | 0.007915 | 0.471039 | 0.0 | 0.0 | 0.0 | 0 | 0.019506 | 11768 |
| Tree depth=6 | 0.007718 | 0.467589 | 0.0 | 0.0 | 0.0 | 0 | 0.03275 | 11768 |

KNN K=5 has optimistic in-sample average precision of 0.215187 and validation average precision of 0.008216. Training queries can include themselves. K=15 reduces the apparent gap, with validation ROC-AUC 0.529690 and average precision 0.008963.

The depth-six tree has higher training average precision than depth three, with slightly lower validation performance. In this fixed comparison, additional tree complexity does not improve validation quality.

The existing Logistic Regression baseline retains the highest validation average precision among these library candidates, at approximately 0.016882. Its overall ROC-AUC remains weak. The model comparison is still in progress.

### Validation error counts

| model | true_negative | false_positive | false_negative | true_positive | maximum_repeat_probability |
| --- | --- | --- | --- | --- | --- |
| KNN k=5 | 11671 | 0 | 97 | 0 | 0.4 |
| KNN k=15 | 11671 | 0 | 97 | 0 | 0.2 |
| Tree depth=3 | 11671 | 0 | 97 | 0 | 0.072993 |
| Tree depth=6 | 11671 | 0 | 97 | 0 | 0.113924 |

All four configurations predict no repeat cases at 0.5, yielding 97 false negatives and zero true positives in validation. Their scores vary, but their maximum scores are below that decision threshold. Threshold selection belongs to the later model-selection and decision-policy topic.

Changing a fixed threshold changes precision, recall, F1 and confusion counts. It does not improve the underlying probability ranking measured by average precision or ROC-AUC.

### KNN worked example

The example is deliberately selected as the highest-scored validation customer under the K=5 model. It illustrates mechanics rather than a typical customer.

| neighbor_rank | euclidean_distance | independent_distance | training_repeat_label |
| --- | --- | --- | --- |
| 1 | 1.05851 | 1.05851 | 1 |
| 2 | 1.085889 | 1.085889 | 0 |
| 3 | 1.16392 | 1.16392 | 0 |
| 4 | 1.253343 | 1.253343 | 0 |
| 5 | 1.378057 | 1.378057 | 1 |

Two neighbor labels are positive and three are negative. Uniform repeat score is 2 / 5 = 0.4. The library returns 0.4 for the same query, and the query's observed validation label is zero.

Euclidean distance is the square root of the sum of squared coordinate differences. Independently calculated distances over the transformed numeric and one-hot features match the library's five distances.

### Read the CART tree

The saved tree plot shows the upper two levels of the depth-three tree. Read each threshold, entropy, sample count and ordered class count. The displayed model uses entropy-based binary threshold splits. A log1p monetary threshold t corresponds to original monetary value exp(t) - 1.

Scikit-learn's tree implementation is CART. Choosing its entropy criterion does not turn it into ID3.

### Categorical ID3 example

Use three declared historical attributes on the same customer cohorts.

- order_history is one_order or multiple_orders.
- known_review is unknown, score_1_to_3, or score_4_to_5.
- known_delivery is unknown, up_to_10_days, or over_10_days.

The fixed bins are teaching choices. The example has a different feature representation from the 12-input library models, so its results cannot isolate an algorithm-only effect.

The recursive implementation stores sample count, training repeat proportion, selected attribute and branches. Stop when labels are pure, attributes are exhausted, or no positive information gain remains. Otherwise select the highest-gain attribute, create branches for its categorical values, and recurse after removing it from the remaining attributes.

Prediction follows those branches. An unseen categorical value returns the current node's training class proportion. These leaf proportions are empirical scores.

### ID3 root information gains

| attribute | information_gain |
| --- | --- |
| order_history | 0.000593 |
| known_review | 6.9e-05 |
| known_delivery | 3e-06 |

### Worked root calculation

| branch | non_repeat | repeat | samples | entropy_bits | weight | weighted_entropy |
| --- | --- | --- | --- | --- | --- | --- |
| multiple_orders | 274 | 10 | 284 | 0.219888 | 0.019774 | 0.004348 |
| one_order | 13948 | 130 | 14078 | 0.075673 | 0.980226 | 0.074177 |

The selected root is order_history. Parent entropy is 0.07911751 bits. Weighted child entropy is 0.07852473 bits. Their difference is information gain of 0.00059278 bits.

The parent has 14,222 non-repeat labels and 140 repeat labels. Its low entropy reflects class imbalance. The multiple-orders branch contains 274 non-repeat and 10 repeat labels. The one-order branch contains 13,948 non-repeat and 130 repeat labels.

For binary labels, entropy H equals -p0 log2(p0) - p1 log2(p1), with zero-probability contributions treated as zero. Gain equals parent entropy minus the sum of each child's entropy weighted by its fraction of training samples.

### ID3 validation result

| model | average_precision | roc_auc | precision_at_0_5 | recall_at_0_5 | f1_at_0_5 | predicted_positives |
| --- | --- | --- | --- | --- | --- | --- |
| Teaching ID3 with 3 categorical attributes | 0.012043 | 0.527934 | 0.0 | 0.0 | 0.0 | 0 |

The ID3 representation has validation ROC-AUC about 0.527934 and average precision 0.012043. Its current role is a course learning example with weak predictive discrimination. Application model selection follows the full comparison.

### Code and method reference

| Code or method | Explanation and reason |
|---|---|
| clone(preprocessing) | Creates an unfitted estimator with the same configuration. |
| set_params(numeric__scaler='passthrough') | Leaves numeric tree inputs in their prepared units. |
| KNeighborsClassifier | Stores training examples for distance-based neighbor voting. |
| n_neighbors | Chooses how many nearest labels contribute to the vote. |
| weights='uniform' | Gives each chosen neighbor one equal vote. |
| metric='euclidean' | Uses the square root of summed squared coordinate differences. |
| algorithm='brute' | Evaluates distances directly for the sparse encoded representation. |
| config_context(working_memory=128) | Bounds computation work buffers without changing the mathematical distance definition. |
| DecisionTreeClassifier(criterion='entropy') | Fits an entropy-based CART classifier. |
| max_depth | Limits the number of split levels. |
| min_samples_leaf | Requires a minimum number of training rows in each leaf. |
| predict_proba | Returns class scores or learned class proportions. |
| repeat_classification_metrics | Shares the same validation measurements across baseline and new classifiers. |
| confusion_matrix(...).ravel() | Reads true negatives, false positives, false negatives and true positives in the stated class order. |
| kneighbors | Returns the nearest training positions and distances for the worked query. |
| .toarray() | Converts only the small worked-example vectors for independent distance calculation. |
| get_feature_names_out | Gets the fitted numeric and one-hot names for the tree diagram. |
| plot_tree(max_depth=2) | Displays a readable upper portion of the fitted tree. |
| np.select | Applies the declared categorical teaching bins, including unknown cases. |
| value_counts(normalize=True) | Calculates class proportions used by entropy. |
| np.log2 | Measures entropy contributions in bits. |
| categorical_information_gain | Subtracts weighted child entropy from parent entropy. |
| fit_id3 | Recursively selects categorical attributes by information gain. |
| remaining attributes | Prevents repeatedly selecting an already used attribute on the same path. |
| id3_probability | Traverses learned branches and handles unseen values using node training prevalence. |

### Viva questions and short answers

1. Why scale for KNN? Euclidean distance depends on coordinate magnitude, so unscaled monetary values could dominate other inputs.
2. What changes when K increases? Voting averages a broader neighborhood, reducing sensitivity to individual examples while potentially smoothing away a rare class.
3. Why can KNN training scores look good? In-sample queries can include their own stored examples and are not independent evaluation.
4. What is entropy? A measure of uncertainty in the label distribution. Pure labels have zero entropy.
5. What is information gain? The reduction in entropy after a split, weighted by branch sizes.
6. How do we limit a tree? Set a maximum depth and a minimum leaf sample count, then check validation performance.
7. Is our library tree ID3? It is CART with entropy. The separate recursive example implements categorical ID3.
8. Why are the ID3 results a separate teaching comparison? It uses three coarsened attributes rather than the library models' full prepared representation.
9. What happens for an unseen categorical value? The implementation returns the current node's training class proportion.
10. Why do all these models return negative decisions at 0.5? Their estimated repeat scores remain below 0.5 in this rare-event cohort.
11. Can lowering the threshold fix ranking quality? It changes decisions and error trade-offs. Ranking quality still needs separate evaluation.
12. Why is the next step another topic? Course recommender methods address product discovery using a different representation and evaluation protocol.

### Verification and topic completion

Executed all 51 code cells in order using in-process IPython. Twelve figures are embedded, including the two new comparison and tree figures. Visually inspected both new figures.

Verified every fitted imputer uses training medians and every state encoder uses the training state set. Checked KNN scaler fit counts, tree depth and leaf constraints, finite probability ranges, model result counts and cohort alignment.

The worked KNN vote and independent distances matched the library. ID3 checks covered pure-label entropy, balanced-label entropy, a perfect categorical split, a no-gain constant attribute, the root gain calculation and unseen-value fallback. Final test scoring remains reserved.

Moved existing bootstrap output and Brier reporting to supplementary Appendix A in the notebook. Baseline result variables are preserved for compatibility, while primary displayed comparisons focus on course-relevant metrics.

The syllabus scope is now the working implementation guide. SVD, advanced boosting libraries, SHAP, advanced NLP and LLM-training extensions remain outside the core implementation path.

**Topic commit message** — `feat: compare KNN and trees with ID3 viva examples`.

**Files in the same contribution** — `olist_pipeline.ipynb`, `PIPELINE_NOTES.md`, `README.md`, `PROJECT_PLAN.md`, and the scope guide `SYLLABUS_ALIGNMENT.md`.

**Commit status** — Pending user review and commit.

## Topic 8 — Content-based and item-based collaborative recommendations

### Purpose and data used

Implement the two Unit II recommender approaches using the same validation protocol as popularity. Historical purchases before 1 April 2018 form the learning data. The following 30 days supply future discovery relevance. Candidates are products observed in history, and purchased products are excluded from each customer's suggestions. The 90 eligible warm customers have at least one future, previously unseen product in that historical catalog. This is a restricted cohort, not every future shopper.

The historical matrix contains 63,881 customers, 22,964 candidate products and 68,203 distinct customer-product pairs. No minimum-history filter removes short-history users. Repeat purchases of the same product contribute one binary interaction. Purchase records are implicit positive evidence. Unobserved pairs are unknown, rather than explicit dislikes.

### Notebook blocks and what each line of work does

| Block | Processing steps and reason |
|---|---|
| `fit-content-item-vectors` | Select historical candidate IDs. Filter item events before the cutoff. Calculate median historical price per product. Join prepared category metadata. Learn price quartiles from historical candidates. Encode category and price band, apply fixed weights, and normalize vectors. |
| `fit-item-collaborative-similarities` | Map customer and product IDs to integer positions. Build a binary CSR matrix from distinct historical pairs. Normalize product columns. Multiply transposed columns by columns to obtain cosine similarities. Remove self-links and retain at most 20 outgoing neighbors per product. |
| `define-syllabus-recommenders` | Build a content profile or sum collaborative neighbor scores. Exclude seen products. Order by score, historical buyer count and product ID. Fill zero-score positions with popularity and label those rows. Return readable reasons. |
| `evaluate-syllabus-recommenders` | Apply all three methods to the same 90 customers at K=5 and K=10. Reuse the checked top-K metrics. Report catalog coverage and fallback fractions, then plot Recall and NDCG at five. |
| `check-recommender-cold-start` | Exercise a new customer and a one-product customer. Score a simulated metadata-only product separately from the benchmark. Show recommendations with readable categories and explicit fallback reasons. |
| `worked-content-cosine` | Compare two actual products by hand and by encoded sparse-vector multiplication. |
| `worked-collaborative-score` | Select a retained collaborative link, count shared and total buyers, calculate cosine by hand, and sum retained contributions for a real customer's candidate. |
| `validate-syllabus-recommenders` | Check historical cutoffs, matrix structure, vector norms, neighbor limits, baseline parity, unique unseen candidates, cold-start behavior and manual score agreement. |

### Content representation and manual calculation

`OneHotEncoder` learns category and price-band coordinates on historical candidates. Product median prices are divided at BRL 39.90, 78.99 and 152.00 into four bands. Missing metadata has explicit unknown labels. The resulting item matrix has 77 columns.

Category coordinates have weight 2 and price-band coordinates weight 1. These are declared teaching choices. Each training product therefore has squared vector length 2² + 1² = 5. `normalize` divides a vector by its Euclidean length. Cosine is the dot product of normalized vectors.

The worked products are both in category `auto`, priced at BRL 129.90 and BRL 52.00, in different bands. Their cosine is `(2×2 + 0)/5 = 0.8`, matching the encoded-vector result. Same category and band gives 1, same band alone gives 0.2, and neither match gives 0.

For a known customer, multiply their binary interaction row by the item vectors, then normalize that summed profile. Score each candidate by its cosine with the profile. Repeated units do not strengthen a binary history entry. Coarse metadata creates ties, resolved with historical popularity and then product ID. Similarity scores are not purchase probabilities.

### Collaborative representation and manual calculation

Each item is represented by its vector of historical buyers. For two products A and B, cosine is `shared_buyers / sqrt(buyers_A × buyers_B)`. Normalizing matrix columns and multiplying `X_normalized.T @ X_normalized` computes these similarities. Diagonal removal prevents a product recommending itself.

Retaining at most 20 neighbors per source product bounds the stored neighborhood. Pruning can make the retained relation directional, even though the original cosine is symmetric. A customer's candidate score is the sum of retained similarities from their purchased products. Links discarded by pruning contribute zero.

The worked historical product has 12 buyers and its candidate has 18. They share one buyer, giving `1 / sqrt(12×18) = 0.068041`. The example customer's summed retained contribution and implemented score both equal 0.068041. One shared buyer is weak evidence, even when cosine is positive.

There are 9,928 retained directed links. The customer-product matrix's stored CSR data, index and pointer arrays use about 1.02 MiB, compared with a theoretical 10.93 GiB float64 dense grid. This is the interaction matrix storage comparison, not total process memory or similarity-computation peak memory.

### Shared serving rules and cold starts

Already purchased products receive excluded scores. Recommendations sort first by model score, then buyer count, then product ID for deterministic ties. A positive content or collaborative score retains its method reason. When positive scores run out, remaining positions are filled from popularity and marked `popularity_fallback=True`.

| Example case | Popularity fills in content top five | Popularity fills in collaborative top five |
|---|---|---|
| New customer | 5 | 5 |
| Selected one-product customer | 0 | 5 |

The popularity method is itself the baseline, so its own rows are not counted as fallback. These two fixtures demonstrate behavior. The full validation cohort supplies aggregate fallback measurements.

A simulated new product with a known category and example price receives content score 1.0 for the selected customer's matching profile. It has no collaborative interaction column. This checks metadata encoding and scoring only. It is outside benchmark candidates and does not establish real new-product ranking quality. The application will need an explicit catalog-registration path and supplied metadata before recommending new products. Unknown encoder categories are ignored, so wholly unfamiliar metadata may supply little or no content evidence.

### Executed validation results

Metrics are macro averages over the same 90 eligible customers. Precision uses K as the denominator. Recall divides each customer's hits by their relevant product count. NDCG rewards earlier hits using logarithmic discounts and normalizes by the ideal ranking. Hit rate is the fraction with at least one hit.

| Method | K | Precision | Recall | NDCG | Hit rate | Catalog coverage |
|---|---|---|---|---|---|---|
| Popularity | 5 | 0.002222 | 0.011111 | 0.005556 | 0.011111 | 0.000261 |
| Content | 5 | 0.004444 | 0.022222 | 0.015409 | 0.022222 | 0.011235 |
| Collaborative | 5 | 0.002222 | 0.005556 | 0.006813 | 0.011111 | 0.004311 |
| Popularity | 10 | 0.002222 | 0.022222 | 0.009061 | 0.022222 | 0.000479 |
| Content | 10 | 0.003333 | 0.033333 | 0.018621 | 0.033333 | 0.022383 |
| Collaborative | 10 | 0.002222 | 0.016667 | 0.010318 | 0.022222 | 0.005443 |

Content leads this validation comparison, but only two customers receive a relevant top-five item. Each other method hits one customer. One customer can have multiple relevant future products, explaining why collaborative Recall at 5 is below its hit rate. Low absolute quality and the small cohort limit any superiority claim.

Collaborative filtering fills 77.11 percent of top-five slots and 84.89 percent of top-ten slots from popularity. Entire lists use fallback for 61.11 percent of evaluated customers. Content has zero fallback slots in this cohort, although popularity still breaks tied positive scores. Report these as recommendation systems with the documented fallback behavior. The standalone collaborative evidence is sparse.

Catalog coverage is the distinct recommended product count divided by 22,964 historical candidates. Higher coverage means broader catalog exposure, without establishing relevance or sales benefit. Static category descriptions are assumed available for observed products. Historical prices are computed before the cutoff, but the dataset does not establish historical stock availability or later category edits.

The weights 2 and 1, four price bands and 20 retained neighbors are fixed configurations. No optimal tuning claim is made. Final recommendation test scores remain reserved for the locked model comparison.

### Code and method reference

| Method or expression | Meaning |
|---|---|
| `groupby(...).median()` | Calculates a robust historical product price from earlier item records. |
| `quantile` and `pd.cut` | Learn historical price boundaries and assign discrete bands using those fixed edges. |
| `OneHotEncoder(handle_unknown='ignore')` | Converts categorical attributes to coordinates and tolerates unseen categories at scoring. |
| `sparse.csr_matrix` | Stores observed interactions and index pointers without allocating the full customer-product grid. |
| `get_indexer` | Maps stable external IDs to matrix row or column positions. |
| `normalize(..., axis=0)` | Gives each item buyer column unit length for collaborative cosine. |
| `normalize(..., axis=1)` | Gives item content rows and customer profiles unit length. |
| `@` | Matrix multiplication, used to build profiles and sum similarity evidence. |
| `setdiag(0)` and `eliminate_zeros()` | Remove self-similarity and explicit stored zeros. |
| `np.lexsort` | Applies deterministic score, popularity and ID tie breaking. |
| `tocsc()` | Supports convenient product-column access for the independent buyer-count calculation. |
| `nonzero()[0]` | Gets customer positions with observed purchases in a product column. |
| `top_k_metrics` | Reuses the earlier tested Precision, Recall, NDCG and hit-rate formulas. |

### Viva questions and short answers

1. What does content-based recommendation use? Product attributes and the customer's previously purchased product profile.
2. What does collaborative filtering use? Purchase patterns shared across customers and products.
3. Why can both use cosine? They compare vectors, but their coordinates represent different evidence.
4. Why use category and price bands? They are available, understandable product descriptors. Bands avoid raw price magnitude dominating similarity.
5. Why weight category more? It is a declared modeling assumption that category match matters more than price-band match. Validation can later test alternatives.
6. What does an unobserved interaction mean? No observed purchase evidence. It is not an explicit negative rating.
7. What happens for a new customer? With no history profile, return documented historical popularity suggestions.
8. What happens for a new product? Content can use supplied metadata. Collaborative similarity needs interaction evidence. The notebook fixture illustrates this separately.
9. Why exclude seen products? The evaluation target is future product discovery. Replenishment would require a different task definition.
10. Why sparse matrices? Almost every customer-product cell is unobserved, so storing the full dense grid wastes memory.
11. What does neighborhood pruning change? It retains only up to 20 strongest outgoing similarities per item and can make links directional.
12. Why does collaborative filtering often fall back? Many historical products have too few shared buyers to provide usable unseen neighbors.
13. Why use NDCG as well as Recall? Recall counts retrieved relevant products, while NDCG also rewards ranking them early.
14. Is a similarity of 0.8 an 80 percent purchase probability? No. It is a geometric match score from the chosen features.
15. Has content solved the problem? Its validation result leads these fixed configurations, but only two of 90 customers receive a top-five hit.
16. How did we avoid future leakage? Fit candidate data, product prices, encoders, profiles and interaction similarities from pre-cutoff history. Future purchases supply evaluation labels only.

### Verification and topic completion

The saved notebook contains 59 consecutively executed code cells, no error outputs and 13 embedded figures. Visually inspected the new comparison figure. Checks verify historical price cutoffs, unique binary pairs, normalized content vectors, finite bounded similarities, zero diagonal and the 20-neighbor limit.

For every eligible validation customer, checked unique valid candidates and seen-item exclusion across all three methods. Popularity outputs and aggregate metrics match the earlier baseline exactly. Both independent cosine calculations match implementation, and new-user and one-history cases return full five-item lists. The synthetic new-product check remains separate from benchmark scores. Final test performance is reserved.

Both supplied notebooks continue to guide the project. The Kaggle reference informs preparation, EDA and preprocessing. The Week 10 starter informs this topic's recommendation progression, metrics, cold-start checks and by-hand understanding exercise. Our chronological protocol, metadata design and sparse implementation are documented adaptations. SVD and advanced NLP remain deferred. The rest of the full understanding pack is pending.

**Topic commit message** — `feat: add syllabus recommenders and cold-start evaluation`.

**Files in the same contribution** — `olist_pipeline.ipynb`, `PIPELINE_NOTES.md`, `README.md`, `SYLLABUS_ALIGNMENT.md`, and `requirements.txt`. SciPy is now declared explicitly because this topic directly uses its sparse matrices.

**Commit status** — Pending user review and commit. No commit created automatically.

## Topic 9 — Naive Bayes and linear SVM

### Goal and inputs

Extend the Unit III retention comparison using the existing 14,362 training customers and 11,768 validation customers. Validation has 97 repeat events. Keep the fixed 30-day decision age and next-90-day target. This topic does not modify labels, partitions, or final test scoring.

Gaussian Naive Bayes uses the eleven numeric historical features. A training-fitted median imputer handles missing values. State and missingness indicators are excluded to avoid interpreting binary one-hot coordinates as Gaussian measurements. Numeric counts and ratios still depart from a Gaussian distribution, and correlated features violate conditional independence. This is an explicitly approximate teaching baseline. Its input representation differs from the SVM and logistic pipelines, so results compare complete pipelines rather than isolating the classifier alone.

Both linear SVM configurations reuse training-only numeric median imputation, missing indicators, StandardScaler and state one-hot encoding. LinearSVC uses C=1, the default squared-hinge loss and L2 regularization. One fit uses ordinary weights and one uses balanced class weights. These are fixed, understandable configurations. No nonlinear kernel, large search or probability-calibration layer is added.

### Notebook blocks and processing sequence

| Block | Steps and reason |
|---|---|
| `fit-naive-bayes-and-svm` | Define a numeric-only GaussianNB pipeline and two full-feature LinearSVC pipelines. Fit on training rows. Promote convergence warnings to errors so an unconverged fit cannot silently supply results. |
| `evaluate-naive-bayes-and-svm` | Obtain Bayes probabilities and signed SVM scores. Calculate AP and ROC-AUC from scores, then precision, recall, F1 and confusion counts from each model's native predictions. Compare training AP with validation AP and plot ranking quality. |
| `worked-gaussian-bayes` | Choose the highest-scored validation example, impute its numeric values and calculate both class log likelihoods feature by feature. Add training log priors, normalize with log-sum-exp and compare with library probabilities. |
| `worked-linear-svm` | Choose the balanced SVM's highest-scored validation example. Multiply each transformed coordinate by its coefficient, add the intercept and compare with the library decision score. Calculate signed hyperplane distance and training class weights. |
| `validate-naive-bayes-and-svm` | Verify training medians, state categories, scaler sample counts, fitted Bayes class counts and positive variances. Check finite outputs, confusion totals, zero-boundary decisions and both independent worked calculations. |

### Gaussian Bayes reasoning

Bayes' rule combines a prior and observed evidence. GaussianNB estimates each feature's mean and variance separately within each training class. For a class c and input x, the unnormalized log score is:

`log_prior_c - 0.5 * sum_j [log(2*pi*variance_cj) + (x_j - mean_cj)^2 / variance_cj]`

The conditional independence assumption lets us add individual feature log densities. Subtracting `logsumexp` of the two class scores and exponentiating gives probabilities that sum to one. This is numerically safer than multiplying many small densities. The implementation uses fitted variances, including GaussianNB's small smoothing term. Its probabilities may still be poorly calibrated if its distribution assumptions are wrong.

The contribution table reports each feature's repeat-class log density minus its nonrepeat-class log density. Positive contributions favor repeat, while negative ones favor nonrepeat. Adding all contributions to the prior log odds gives posterior log odds. These are model calculations, not causal effects.

### SVM reasoning

The linear decision score is `w dot transformed_x + b`. Positive values predict repeat, while nonpositive values predict nonrepeat. The score is not a probability. StandardScaler learns training means and standard deviations to prevent raw monetary units from dominating geometry. Encoded states and missingness indicators are part of this transformed feature space.

A maximum-margin classifier balances regularization against errors. LinearSVC's squared-hinge penalty applies to margins below one. C controls the penalty strength relative to regularization. Larger C penalizes errors more strongly. C=1 is a declared initial configuration rather than an optimized value.

Balanced class weights use `training_rows / (2 * training_class_count)`. This gives each class the same total training weight. The minority class receives a larger per-row weight. These weights change fitting, and can increase false positives. They do not change the observed repeat prevalence or calibrate the decision score.

The signed distance `score / ||w||` describes distance to the fitted hyperplane in transformed feature space. Individual coefficient contributions explain the arithmetic for a row. They are sensitive to feature representation and correlations and are not causal feature effects.

### Why the evaluation treats scores differently

AP and ROC-AUC require an ordering score, so both probabilities and signed margins are valid inputs. Native class decisions use a Bayes probability boundary of 0.5 and an SVM score boundary of zero. The result table explicitly records those boundaries. We do not pass signed SVM scores into the earlier helper that assumes probabilities and a 0.5 threshold.

Training AP is in-sample fit and is not independent performance. Validation guides later model selection. The final chronological test remains reserved. Threshold tuning and business costs require a separate declared evaluation decision.

### Code reference

| Method | Meaning |
|---|---|
| `GaussianNB` | Estimates a prior, mean and variance for each class using a conditionally independent Gaussian feature model. |
| `var_smoothing=1e-9` | Adds a small variance stabilizer based on training feature variation. |
| `LinearSVC` | Fits a linear support vector classifier without an automatic probability layer. |
| `class_weight="balanced"` | Weights training classes inversely to their counts. |
| `dual="auto"` | Lets the estimator choose its optimization formulation from the training shape and supported settings. |
| `warnings.simplefilter("error", ConvergenceWarning)` | Stops this topic if the optimizer reports failure to converge. |
| `decision_function` | Returns the signed linear decision score. |
| `predict` | Applies each classifier's native decision rule. |
| `logsumexp` | Computes a stable log of summed exponentials for Bayes normalization. |
| `theta_`, `var_`, `class_prior_` | Fitted Gaussian class means, stabilized variances and training priors. |
| `coef_`, `intercept_` | Fitted linear SVM weights and bias. |
| `get_feature_names_out` | Maps transformed SVM coordinates back to readable names. |
| `confusion_matrix(..., labels=[0,1])` | Keeps nonrepeat and repeat class order explicit in error counts. |

### Viva questions and short answers

1. Why is the classifier called naive? It assumes features are conditionally independent given the class.
2. What is a prior? A class probability before considering the input features, estimated here from training labels.
3. What is a likelihood? The model's density of observed feature values conditional on a class.
4. Why use GaussianNB? We have numeric features and need an understandable Unit III baseline. Count and ratio distributions make its Gaussian assumption approximate.
5. Why exclude state from GaussianNB? A one-hot state indicator is a binary variable rather than a Gaussian measurement. A mixed-likelihood Bayes model would require additional design.
6. Does scaling fix the Gaussian assumption? Scaling changes units but does not turn a skewed or discrete distribution into a Gaussian one.
7. Why calculate log likelihoods? Adding logs is more numerically stable than multiplying many small densities.
8. Why can Naive Bayes be overconfident? Correlated evidence and wrong likelihood assumptions can exaggerate class evidence.
9. What does SVM learn? A separating hyperplane that balances margin-related regularization against training errors.
10. What is C? The relative penalty strength for training errors. Larger C penalizes errors more strongly.
11. Why scale SVM numeric inputs? Margin geometry depends on feature units, so numeric features are standardized using training statistics.
12. What is the difference between linear and kernel SVM? Linear SVM uses a hyperplane in the supplied feature space. Kernels can represent nonlinear separation through implicit feature mappings.
13. Why choose a linear SVM here? It is manageable on this dataset, easy to inspect and directly supports the course's margin discussion.
14. Is an SVM score of 0.8 an 80 percent probability? No. It is a signed decision score, with zero as the decision boundary.
15. Why try class balancing? Rare repeat customers otherwise contribute much less total training weight. Balancing can trade precision for recall and needs validation.
16. Why report AP and ROC-AUC? They assess ranking without confusing the Bayes 0.5 boundary with the SVM zero boundary. AP also reflects the rare positive-class setting.
17. Is training performance proof of generalization? No. Training examples were used during fitting. The chronological validation and reserved test assess unseen periods.
18. Do the worked examples prove the models predict well? They verify score arithmetic. The full validation metrics assess predictive performance.

### Executed results and interpretation

| Model | Training AP | Validation AP | ROC-AUC | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| Gaussian NB numeric | 0.014551 | 0.013115 | 0.528977 | 0.023936 | 0.092784 | 0.038055 |
| Linear SVM | 0.023872 | 0.010308 | 0.512059 | 0 | 0 | 0 |
| Linear SVM balanced | 0.019595 | 0.010450 | 0.523457 | 0.008566 | 0.443299 | 0.016807 |

| Model | True negatives | False positives | False negatives | True positives | Positive decisions |
|---|---|---|---|---|---|
| Gaussian NB numeric | 11304 | 367 | 88 | 9 | 376 |
| Linear SVM | 11671 | 0 | 97 | 0 | 0 |
| Linear SVM balanced | 6694 | 4977 | 54 | 43 | 5020 |

The prior validation AP is 0.008243, and earlier Logistic Regression AP is 0.016882. All three new configurations are above the prior AP reference but below Logistic Regression on this metric. GaussianNB's ROC-AUC is 0.528977, while Logistic Regression's earlier value is 0.515552. Those metrics assess different aspects of the score ordering. Neither establishes useful real-world prediction quality in this rare-event task.

Ordinary SVM still makes zero repeat decisions at its native boundary. Balanced SVM catches 43 of 97 repeats but raises 4,977 false positives. Its precision is about 0.857 percent. This makes the class-weight trade-off explicit. Class balancing does not automatically improve minority precision or ranking enough for deployment.

GaussianNB catches nine repeats among 376 positive predictions, precision about 2.394 percent. Its worked highest-scored example receives a repeat probability effectively 1.0 but has actual label 0. Both manual and library outputs agree, with nonrepeat probability about 6.975e-16. The feature log-likelihood ratio is particularly large for distinct sellers (17.736906) and historical order count (12.067656). Correlated historical counts and approximate Gaussian likelihoods can amplify confidence. This single example demonstrates a failure case rather than establishing a dataset-wide calibration result.

Training class priors are approximately 0.990252 nonrepeat and 0.009748 repeat. Balanced SVM uses class weights 0.504922 and 51.292857 for the 14,222 nonrepeat and 140 repeat training rows respectively. Each class therefore contributes total weight 7,181.

The worked balanced SVM has intercept -0.382292. Its manual feature sum plus intercept and library decision score both equal 1.196948. Signed distance is 0.214712 in the transformed feature space. The selected customer's actual label is 0. The highest-score selection is for reproducible arithmetic, so these two worked examples are not representative samples.

### Verification and topic completion

Executed all 64 code cells sequentially from data loading through supplementary evaluation. There are 14 embedded figures and no error outputs. Visually inspected the new AP/ROC-AUC plot. All three new models fit without convergence warnings.

Independently checked training-only imputation statistics, SVM scaling sample counts and state encoder categories. Verified Gaussian class counts and positive variances, finite score lengths, confusion matrix totals and repeat counts. Native SVM predictions match positive decision scores. Manual Bayes normalization, manual SVM weighted sum and balanced weight totals match their fitted implementations. Static checks confirm the new code does not use X_test or y_test. Final test performance remains reserved.

The notebook uses existing dependencies. This topic adds no application framework, nonlinear kernel search or probability calibration layer. Both supplied notebooks remain references as mapped near the notebook start. The Gaussian and SVM teaching exercises are our course-aligned additions.

**Suggested topic commit message for later** — `feat: compare Naive Bayes and linear SVM with viva examples`.

**Files for this topic** — `olist_pipeline.ipynb`, `PIPELINE_NOTES.md`, `README.md`, and `SYLLABUS_ALIGNMENT.md`.

**Commit status** — Left uncommitted at the user's request. The preceding recommendation topic is also still uncommitted. No Git commit or staging action was performed.

## Next notebook topic

Add a small, controlled Random Forest comparison for repeat-purchase prediction. Explain bootstrap sampling, random feature subsets, tree diversity and overfitting. Compare the same validation metrics and error trade-offs, with training-only preprocessing and matching reference notes. Keep final test scoring reserved until the model comparison is locked.
