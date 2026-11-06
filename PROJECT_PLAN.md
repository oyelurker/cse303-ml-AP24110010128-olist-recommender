# Olist Recommendation and Customer Retention Project Plan

Follow [the syllabus comparison and viva walkthrough](SYLLABUS_ALIGNMENT.md) when selecting methods. It defines the course-aligned scope, manageable supporting extensions, supplementary material, and learning sequence for the next stages.

## Project overview

Build an application using the Olist Brazilian E-Commerce dataset for catalog topic 9.2, Tier A E-commerce Recommendation. The application will combine product recommendations, repeat-purchase prediction, and a conversational assistant for exploring customer insights.

Development will begin with a readable, reproducible notebook covering data preparation, analysis, model development, and evaluation. Once the notebook pipeline is verified, its reusable components will support the application.

This plan follows the technical deliverables in the course catalog and kickoff guide. Work proceeds in the sequence below, without the guide's historical deadlines or milestone schedule.

## Business objective

Help a direct-to-consumer business understand its customers, identify possible retention opportunities, and suggest relevant cross-sell products. The proposed initial application user is a marketing employee examining customer history and deciding whom to contact and what to recommend.

We will state the assumptions behind any outreach budget or discount analysis. Historical predictions can support decisions, while the effect of a campaign on sales requires separate evidence.

## Reference materials

- The course project catalog defines topic 9.2 as recommendation combined with churn or repeat-purchase prediction.
- The kickoff guide supplies expectations for data analysis, comparative modeling, evaluation, reproducibility, and a working application.
- The Week 10 starter notebook supplies recommender concepts and understanding checks.
- The Gemini conversation supplies the proposed D2C retention use case, RFM features, item-based recommendations, and application direction.
- The public Kaggle notebook provides examples of data exploration, cleaning, satisfaction modeling, review NLP, customer segmentation, and deployment. It will be credited wherever its methods or code inform our work.

[Reference Kaggle notebook](https://www.kaggle.com/code/mohabovic/eda-satisfaction-prediction-nlp-rfm-deployment/notebook)

[Olist dataset source](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## Phase 1 Understand and validate the dataset

Confirm the chosen dataset version and record its source, licence, files, date coverage, and measured counts. Inspect the relationships among customers, orders, order items, products, payments, reviews, and sellers.

Use the stable `customer_unique_id` for customer history. Check the frequency of repeat purchases and the number of interactions per product and customer before finalizing model scope or evaluation windows.

**Output** — A dataset description, schema explanation, and data quality summary in the notebook.

## Phase 2 Clean and prepare the data

Handle missing values, duplicate keys, timestamp formats, and invalid records with documented reasons. Establish the unit of each table before joining it to others.

Aggregate order payments and other repeated records at the appropriate level to prevent inflated spending or purchase counts. Keep order frequency distinct from the number of product line items.

Create separate derived tables for customer analysis and customer-product interactions. Keep product identifiers, customer identity, and event timestamps available for later recommendation and evaluation work.

**Output** — Reproducible preparation steps and validated analytical tables.

## Phase 3 Explore customer and product behavior

Analyze purchase activity over time, customer order counts, product popularity, category distribution, spending, reviews, delivery patterns, and missing data. Measure interaction sparsity and repeat-purchase prevalence.

For each plot, explain the observation and its consequence for modeling. Verify findings from the reference notebook against our own processing and data version.

**Output** — EDA plots, descriptive statistics, and modeling decisions supported by evidence.

## Phase 4 Engineer features and define prediction tasks

Construct historical Recency, Frequency, and Monetary features. Add further customer or transaction features only when justified and available at prediction time.

Explore RFM segmentation and K-means as customer analysis tools. Keep the low-dimensional RFM features interpretable. Use PCA only if a later feature representation provides a clear reason for it.

Define repeat purchase as another qualifying order within a future observation window. A 90-day window is a candidate to assess against the data. Define the prediction date, order eligibility rules, and complete follow-up requirement before training. Describe non-return within the window as observed inactivity.

Represent purchases as implicit customer-product interactions for recommendation. Verify available product metadata before selecting content features.

**Output** — Feature definitions, target definitions, customer segments, and documented chronological train, validation, and test partitions.

## Phase 5 Develop and compare models

### Repeat purchase prediction

Start with a dummy baseline and Logistic Regression. Compare KNN, Decision Tree, Naive Bayes, SVM, and Random Forest. One simple boosting comparison is optional. Include compact neural learning exercises and a small ANN with their role and results documented. Explain the library tree as CART and use a separate categorical ID3 learning example for the lab-specific algorithm.

Fit preprocessing and any imbalance handling on the training partition. Tune the strongest two models using validation data.

### Product recommendation

Start with popularity recommendations. Compare content-based recommendations and item-based collaborative filtering using cosine similarity. Evaluate a simple weighted hybrid if it is understood and validation performance supports it. SVD and matrix factorization remain optional additions beyond the explicit syllabus list.

Return up to five cross-sell suggestions for the proposed application, with historical purchases excluded under the stated discovery policy. Provide a documented fallback for customers with little or no history. Evaluate at five recommendations, and include metrics at ten where useful for comparison with the lab reference.

**Output** — Working model pipelines, comparison tables, explanations, and selected candidates for the application.

## Phase 6 Evaluate and demonstrate understanding

Use chronological evaluation and prevent future information from entering historical features. Keep items from the same order together and define a consistent candidate catalog for recommendation comparisons.

- Evaluate repeat purchase using average precision, precision, recall, F1, ROC-AUC, and confusion matrices, with the class prevalence recorded.
- Evaluate recommendations using Precision at K, Recall at K, NDCG at K, eligible customer counts, and catalog coverage.
- Report mean and standard deviation over repeated runs or suitable evaluation windows. Distinguish random-seed variation from variation over time.
- Compare against verified, compatible benchmarks and cite their task and evaluation protocol.
- Treat ROC-AUC of 0.85 from the Gemini notes as an aspiration to assess after the baselines.
- Include the lab's by-hand calculation, isolated leakage demonstration, new-customer and new-item checks, evidence-backed decision log, real bug log, and AI-use log.

**Output** — Honest evaluation results and an understanding pack that can be explained during a demonstration or viva.

## Phase 7 Prepare the application pipeline

After notebook validation, extract reusable data preparation and inference functions. Save the fitted preprocessing, selected models, feature configuration, and identifier mappings together with regeneration instructions.

Define application inputs, outputs, supported actions, and historical data context. Select the interface technology after these needs are clear. Streamlit, a separate API, and a custom frontend remain options to assess.

**Output** — Verified reusable components and an agreed application design.

## Phase 8 Add the conversational assistant

The proposed initial assistant will support these requests.

- Summarize a selected customer's historical behavior and segment.
- Explain the repeat-purchase estimate and its prediction horizon.
- Retrieve five product suggestions and explain the supporting signals.
- Answer supported customer and segment questions using computed data.
- Draft an outreach message using the retrieved recommendations.

Customer figures, predictions, and recommendations will come from the underlying functions. Begin with a small set of supported requests and simple intent rules. Responses will identify missing information and uncertainty. An external language-model API can be considered later as an interface extension after the underlying requests work. Model training, RAG, and agent orchestration are outside the core scope.

**Output** — A conversational interface connected to the verified pipeline.

## Final deliverables

1. A reproducible development notebook, organized into clear sections and smaller notebooks if needed for course submission.
2. Reusable preprocessing and model components with setup instructions.
3. A working application demonstrating recommendations, repeat-purchase prediction, and supported chatbot requests.
4. A README covering the problem, dataset, methods, results, sources, limitations, and how to run the project.
5. A final report and the required understanding checks, model comparisons, and demonstration material.

## Decisions to finalize after data inspection

- Dataset version, filtering policy, and reliable observation period.
- Repeat-purchase horizon and feasible chronological partitions.
- Product-level recommendation coverage and handling of sparse histories.
- Final models and measurable success criteria relative to baselines.
- Application framework, chatbot technology, and deployment arrangement.

## Current status

Data preparation, EDA, historical targets and partitions, and baseline models are implemented. Comparative syllabus models are underway. The notebook, README, and pipeline notes record executed results and current progress. The application follows the verified model comparisons and evaluation.
