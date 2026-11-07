# Olist Project Syllabus Comparison and Viva Walkthrough

## Recommended scope

Build the recommendation and repeat-purchase application around the algorithms taught in CSE303. Retain the existing preparation and baseline work, develop the syllabus model comparisons with one shared pipeline, and add a small customer-segmentation and neural-learning section. Keep the application interface and chatbot focused on explaining those results.

Some project-specific techniques are needed to turn the course algorithms into a working system. Each should have a short explanation and a small example. Advanced statistical or software additions can be supplementary or deferred.

This is the working course-aligned scope and learning path. It distinguishes what is already implemented from future work. Model choices, current scores, and operating assumptions remain visible in the project notebook and reference notes.

## Sources and how to interpret the comparison

- The official source is `SOURCE FILES/ML_CSE303_Syllabus.docx`, including the theory unitization and lab experiments.
- The kickoff guide and project catalog add capstone expectations, including a comparative algorithm ladder and working deployment.
- The Week 10 starter is a reference for recommender methods and understanding checks. Its content includes additions beyond the explicit theory list.
- The public Kaggle notebook supplies implementation examples. Methods appearing there require separate syllabus and project justification.
- The original comparison reviewed `PROJECT_PLAN.md`, the Gemini project notes, and 43 executed notebook code cells. The Unit II, Unit III and Random Forest implementations have since extended the notebook to 69 executed cells.

An algorithm being covered by the syllabus makes it suitable to study and use when it fits the task. It does not mean every lecture topic must become a separate application feature. The model comparisons and small learning demonstrations can live in the notebook, while the application uses the selected models.

Difficulty labels below are estimates for this project and its viva preparation. Familiarity from your lectures may change them.

## What the official syllabus contains

| Course section | Explicitly listed topics relevant to this review |
|---|---|
| Unit I | ML types, models and learning algorithms, hypothesis space and inductive bias, training/testing/validation, cross-validation, overfitting and underfitting, simple/multiple linear regression, polynomial regression, and evaluating regression fit |
| Unit II | Decision trees and ID3, KNN, dimensionality, feature selection, PCA, Linear Discriminant Analysis, content-based recommendation, and collaborative filtering |
| Unit III | Probability, Bayesian learning, Bayes-optimal decisions, Naive Bayes, SVM, maximum margin, nonlinear SVM, and kernels |
| Unit IV | Neural-network representation, McCulloch-Pitts neuron, Perceptron, gradient descent, ADALINE, delta rule, MADALINE, multilayer networks, backpropagation, radial-basis-function networks, sample complexity, and VC dimension |
| Unit V | Bagging, boosting, Random Forest, fixed and trained rule fusion, K-means, and hierarchical clustering |
| Lab | Python packages, regression, distance measures, KNN, ID3, covariance/correlation, PCA, Naive Bayes, SVM, Perceptron, ADALINE/MADALINE, backpropagation ANN, K-means, and hierarchical clustering |

Logistic Regression is not explicitly named in the supplied theory or lab topic list. The kickoff guide and catalog explicitly include Linear/Logistic Regression in the project progression. We should describe Logistic Regression as a small capstone-supported addition, with its sigmoid and probability interpretation taught clearly.

## Planned methods directly supported by the syllabus

| Method or activity | Syllabus location | Project use | Current position | Recommendation and viva depth |
|---|---|---|---|---|
| Data handling and ML pipeline | Course objectives, CLO1, package labs | Load, inspect, clean, prepare and validate Olist tables | Implemented | Keep. Explain table grain, identifiers, missing values, and join checks |
| Correlation and descriptive exploration | Lab 7 and ML pipeline objectives | EDA and initial feature reasoning | Implemented | Keep. Explain what each plot measures and what correlation establishes |
| Training, validation, testing and overfitting | Unit I | Separate learning, model selection, and final evaluation | Implemented | Keep. Explain the role of each partition |
| KNN | Unit II, Lab 5 | A retention classification comparison | Implemented in Section 7 | Keep. Explain K, distance, scaling, and majority voting |
| Decision trees | Unit II | Interpretable retention classifier | Implemented in Section 7 | Keep. Explain splits, depth, impurity, and overfitting |
| ID3 | Unit II, Lab 6 | A small learning example accompanying the tree comparison | Implemented in Section 7 | Explain entropy and information gain, with a genuinely identified ID3 example |
| Feature selection | Unit II | Examine usefulness and redundancy of predictors | Preliminary EDA only | Keep a simple training-only feature-analysis exercise |
| Content-based recommendation | Unit II | Recommend products using available item attributes and customer history | Implemented in Section 8 | Core project method. Explain item vectors and similarity |
| Collaborative filtering | Unit II | Recommend from customer-product purchase patterns | Implemented in Section 8 | Core project method. Start with item-based similarity |
| Naive Bayes | Unit III, Lab 9 | A retention comparison with stated assumptions | Implemented in Section 9 | Keep a justified variant. Explain conditional independence and feature assumptions |
| SVM | Unit III, Lab 10 | A retention classifier comparison | Implemented in Section 9 | Keep a simple configuration. Explain margin, C, scaling, and the kernel used |
| Random Forest | Unit V | A retention ensemble comparison | Implemented in Section 10 | Keep as the primary ensemble. Explain tree diversity, bagging, and feature subsets |
| Basic boosting | Unit V | An optional additional ensemble comparison | Planned option | One simple example is enough if useful after Random Forest |
| Small ANN and backpropagation | Unit IV, Lab 13 | Neural learning and a small retention comparison | Planned | Keep one small hidden-layer network and learning curves |
| Perceptron, ADALINE and MADALINE | Unit IV, Labs 11 and 12 | Small learning demonstrations in the required neural progression | Planned | Keep the demonstrations compact and explain their updates. App deployment can use the selected model |
| K-means | Unit V, Lab 14 | Explore historical RFM customer segments | Planned | Keep a small interpretable analysis with a justified K |
| Hierarchical clustering | Unit V, Lab 15 | Compare customer-group structure on a documented manageable sample | Planned | Keep a compact illustration when it provides a useful comparison |
| Simple score fusion | Unit V covers fixed and trained rule fusion | Optional content/CF score blend | Planned option | A fixed weighted blend is manageable after individual models work. Its specific recommendation design is an application of the general fusion idea |

### Decision tree and ID3 accuracy in the viva

Scikit-learn uses an optimized CART tree implementation. Its entropy criterion does not turn the algorithm into ID3. We should name the library model correctly and use a separate small ID3 example for the lab-specific concept. [Scikit-learn tree algorithms](https://scikit-learn.org/stable/modules/tree.html#tree-algorithms-id3-c4-5-c5-0-and-cart).

### Neural learning scope

A small multilayer perceptron is consistent with Unit IV. Scikit-learn's MLPClassifier trains by backpropagation. The viva should cover a weighted sum, bias, activation, loss, learning rate, forward pass, and backward update. If the full-data comparison uses MLPClassifier, accompany it with a small from-scratch forward and backward update demonstration to support Lab 13's implementation emphasis. [Scikit-learn neural-network documentation](https://scikit-learn.org/stable/modules/neural_networks_supervised.html).

## Syllabus topics that need selective project use

| Topic | Official status | Recommended treatment |
|---|---|---|
| Linear and polynomial regression | Explicit in Unit I and regression lab | Study their concepts for viva. Our binary repeat-order target supports a classifier. An unrelated numerical-prediction task would add scope, so include a separate small lab illustration only if needed for the instructor's project expectations |
| PCA | Explicit in Unit II and Lab 8 | Keep the concept in viva preparation. Add a small training-only demonstration if the lab requirement needs it or a feature experiment justifies it. Explain retained variance and interpretability before selecting it for a model |
| Linear Discriminant Analysis | Explicit in Unit II as feature reduction | Understand its supervised dimensionality-reduction purpose. Optional comparison if there is a clear need |
| RBF neural networks | Explicit in Unit IV | Understand the basic architecture for syllabus viva. Additional implementation is optional because our neural comparison can use a small MLP |
| Hypothesis space, inductive bias, sample complexity and VC dimension | Explicit in Units I and IV | Prepare conceptual answers tied to our models. These topics support explanations of capacity and generalization |
| Speech and object recognition examples | Mentioned in the course outcomes | Our selected domain is e-commerce. Keep the project focused on its recommendation and classification tasks |

PCA was earlier described as something we might omit for interpretability. The syllabus confirms that it is a course topic. Its use in the main feature pipeline should follow a measured reason, while its basic mathematics can remain part of study and lab demonstration.

## Manageable additions supporting the project

These terms are not explicitly named in the official topic list, or their exact implementation goes beyond the listed wording. They have a direct project purpose and can be explained with small examples.

| Addition | Why it appears | Learning burden | Recommendation |
|---|---|---|---|
| Logistic Regression | Explicitly called for by the capstone guide and useful for binary outcomes | Modest. Linear score, sigmoid, probability, threshold | Keep the implemented baseline and teach these ideas |
| Prior or dummy baseline | Establishes what happens when the model uses only the training class rate | Small | Keep. It helps explain why an apparent accuracy can be misleading |
| RFM terminology | Names ordinary recency, distinct-order counts, and spending summaries | Small | Keep. Memorize each formula and the prediction-date rule |
| Median imputation, one-hot encoding and StandardScaler | Practical implementations of preprocessing using Python ML packages | Modest | Keep. Explain each operation and why its fitted values use training only |
| Pipeline and ColumnTransformer | Organize the learned preprocessing and classifier | Small after the operations are understood | Keep as software structure. Explain the sequence and selected columns |
| Chronological splits and maturation gaps | Apply Unit I's train/validation/test concepts to future-order labels | Modest | Essential for this task. Explain with a dated example |
| Historical purchase and review availability | Prevents future information from entering earlier customer features | Modest | Keep. Explain exactly when a contributing event was recorded |
| Cosine similarity | A similarity choice supporting the distance lab and the recommender methods | Small | Keep. Learn dot product divided by vector lengths and one worked example |
| Implicit feedback | Treats observed purchases as interaction evidence | Small | Keep. Explain why an unobserved pair has unknown preference |
| Popularity and cold-start fallback | Supplies baseline recommendations when history is limited | Small | Keep. Explain historical buyer counts and seen-item exclusion |
| Precision, recall, F1 and ROC-AUC | Concrete evaluation choices under the syllabus's general evaluation topic | Modest | Keep the formulas, confusion matrix, threshold interpretation, and ranking intuition |
| Precision at K and Recall at K | Supplied by the Week 10 starter and directly evaluate recommendations | Small | Keep. Work through a five-product example |
| NDCG at K | Supplied by the starter and rewards correct products near the top | Moderate | Keep as a limited extension. Learn the rank-discount idea and one hand calculation |
| Average precision | Supports evaluation when repeat orders are rare | Moderate | Keep as a supporting metric with a short precision-recall explanation. Focus viva preparation on why accuracy alone is inadequate |
| Mean and standard deviation across suitable runs | Required by the kickoff benchmark section | Small to moderate | Keep. Distinguish training randomness and temporal-window variation |
| Sparse representations | Avoid impractically large customer-product matrices | Small conceptual burden | Explain storing observed interactions. Advanced sparse linear-algebra derivations can be supplementary |

## Additions to simplify defer or exclude from the core scope

| Addition | Official syllabus relationship | Current position | Recommendation |
|---|---|---|---|
| Bootstrap confidence intervals | Not explicitly listed | Retained in Appendix A | Use as supplementary evaluation material. Primary study focuses on the guide's repeated-run mean and standard deviation |
| Brier score and probability-calibration theory | Not explicitly listed | Brier score is already reported. Calibration models are pending | Treat Brier as supplementary. Calibration methods can be deferred |
| TruncatedSVD and matrix factorization | Not explicitly named in the official syllabus; SVD appears in the Week 10 reference | Planned | Defer from the core method set. Include a small version only if the instructor expects that starter section and its extra linear algebra is understood |
| XGBoost-specific machinery | General boosting is in Unit V; this library and its internals are not named | Earlier plan option | Prefer Random Forest for the main ensemble. Defer XGBoost-specific tuning and derivations |
| CatBoost and LightGBM | Named implementations are not in the supplied syllabus | Present in the Kaggle source, outside our implemented models | Do not inherit these extra models from the reference automatically |
| SMOTE and synthetic oversampling | Not explicitly listed | Used by the Kaggle source, outside our current baseline | Defer. Begin with original data and, if needed, a clearly explained training-only class-weight comparison |
| SHAP and advanced fairness toolkits | Not explicitly listed | Earlier optional analysis ideas | Defer. Explain a small tree, coefficients with their limitations, feature importance, and subgroup error counts where useful |
| Portuguese review NLP, embeddings and transformers | Not explicit in this ML syllabus | Review-text NLP exists in the Kaggle source | Defer as a separate extension. Numeric review features already support our core pipeline |
| Deep recommendation networks or implicit ALS | Not explicit in the supplied syllabus | Possible extensions discussed earlier | Exclude from the core recommendation comparison |
| Large hyperparameter searches and automated ML | Not explicit requirements | Planned tuning is limited | Tune a few understandable settings on the strongest two models |
| LLM training, fine-tuning, RAG and multi-agent workflows | Not in the syllabus | Outside implemented work | Exclude from the core application |
| FastAPI plus a separate custom frontend and complex infrastructure | Software extensions outside the ML topics | Earlier Gemini architecture option | Start with one simple interface. Revisit a separate backend or custom frontend only for a concrete need |

Existing optional evaluation outputs remain part of the execution record and are grouped in Appendix A. Core and supplementary study paths are explicit. Pending methods are identified separately from implemented work.

## Proposed final model scope

### Repeat order prediction

Use the existing prior and Logistic Regression baselines. Compare KNN, a correctly named library decision tree, a justified Naive Bayes variant, SVM, Random Forest, and one small ANN. Explain the ID3 and neural lab concepts through compact learning demonstrations.

One simple boosting comparison is optional within Unit V. Each model reuses the established validation design. Tune the strongest two with a small set of parameters that can be explained.

The models belong to one comparison topic, with one result table and concise model-specific notes. The final application uses the selected validated model.

### Product recommendation

Use popularity as the baseline and fallback. Add content-based similarity and item-based collaborative filtering. Both main recommender approaches are explicitly in Unit II.

Compare recommendations at five products, with ten as a secondary reporting value. Add a simple weighted hybrid only if the individual models and score combination are understood and validation evidence supports it.

### Customer segmentation and course learning

Explore a small interpretable RFM feature set with K-means. A compact hierarchical comparison on a documented sample can support Lab 15. Fit any required scaling using the permitted training data.

Keep Perceptron, ADALINE/MADALINE, PCA and backpropagation learning demonstrations compact and connected to the course exercises. Existing completed lab material can be referenced where appropriate. These demonstrations support viva understanding without expanding the application's responsibilities.

## Application and chatbot walkthrough

1. Select a customer and show the historical snapshot and available order history.
2. Compute the same verified features used by the selected classifier.
3. Show the repeat-order estimate, its 90-day meaning, and the fixed 30-day customer-age operating context.
4. Return five product suggestions from the selected recommender with short explanations.
5. Let the conversational interface handle a small documented set of requests, such as customer summary, repeat estimate, and recommendations.

The first conversational implementation can use simple intent rules and call the existing functions. An external language-model API can be considered later for wording or request parsing, with its role explained as an application extension. Model training or agent architecture is outside the proposed core scope.

Keep the interface framework decision separate from the ML syllabus comparison. A local Streamlit or Gradio app can satisfy the guide's deployment requirement. A larger frontend is a later product choice.

## Learning and implementation order

| Topic contribution | Work to complete together | Viva preparation |
|---|---|---|
| Existing foundation review | Review current cleaning, EDA, targets and baselines; mark supplementary evaluation clearly | Explain row grain, historical availability, RFM, splits, sigmoid, imbalance and baseline limitations |
| Neighbors and trees | KNN and decision tree comparisons, with a small ID3 explanation | Distance and K, entropy/information gain, CART distinction, depth and overfitting |
| Syllabus recommenders | Content-based and item-based collaborative methods with baseline comparison | Product vectors, interaction vectors, cosine similarity, top-K metrics, cold start |
| Probabilistic and margin models | Naive Bayes and SVM with appropriate preprocessing | Conditional independence, Bayes reasoning, margin, kernel and scaling |
| Neural learning | Compact course demonstrations and a small ANN comparison | Weighted sums, activation, learning rule, forward pass, loss, backpropagation and learning curves |
| Ensembles and segmentation | Random Forest, optional simple boosting, K-means and a compact hierarchical analysis | Bagging versus boosting, tree diversity, centroids, K and linkage |
| Final evaluation and application | Limited tuning, locked test results, report, interface and bounded chatbot | Model selection, thresholds, honest performance limits and the complete input-to-output flow |

Each topic includes its notebook sections, measured outputs, explanations, and reference notes in one contribution. Core concepts should be understandable before increasing model complexity.

## Essential viva questions for the current notebook

1. What does one row represent in each original CSV, and why can an unrestricted join inflate spending?
2. Why is `customer_unique_id` used to connect customer histories?
3. How are recency, frequency and monetary value calculated at a historical snapshot?
4. What does our repeat label mean, and why are incomplete follow-up windows excluded?
5. Why must training outcomes mature before the next prediction period?
6. Why does Logistic Regression use a sigmoid, and what does the classification threshold change?
7. Why do the current models predict no positive cases at 0.5 despite assigning different probabilities?
8. Why is accuracy alone inadequate for a target with very few repeat orders?
9. How does popularity ranking work, and how will content and collaborative filtering differ?
10. What do Precision at 5, Recall at 5 and NDCG at 5 measure?
11. What happens for a new customer or an unseen product?
12. How does the application reuse the fitted preprocessing and models?

Current Logistic Regression validation ROC-AUC is about 0.516. It is an initial weak baseline. Model comparisons and an honest discussion of data limitations matter more than reaching the earlier aspirational score of 0.85.

## Recommended next action

Review this scope, then continue with the neighbors-and-trees topic and the syllabus recommender methods. Keep the next implementation centered on explainable course concepts and update the viva notes alongside the code.
