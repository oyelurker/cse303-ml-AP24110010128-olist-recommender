# Application pipeline and viva reference

The first local shopping application implements the agreed recommendation, activity, cart, rewards, history, insights and bounded-assistant flow. It runs against a frozen June 2018 historical catalog plus separately stored simulated activity. The completed notebook remains unchanged.

## Run it

Use Python 3.12, verified with 3.12.14. From the repository root:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-app-lock.txt
.\.venv\Scripts\python.exe scripts/build_artifacts.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Open http://127.0.0.1:8501. If artifacts are missing, the app also provides a Prepare local demo action. It builds once. Subsequent starts load the fitted bundle rather than rerunning or retraining the notebook.

`requirements-app-lock.txt` records the tested complete environment. `requirements-app.txt` describes the app's direct dependencies. The original notebook lock is preserved.

## Modules and data flow

| File | Responsibility |
|---|---|
| `olist_shop/data.py` | Load the six CSVs needed by the selected features, prepare order/item/product tables, select first eligible reviews, reproduce historical retention features and common-date RFM. |
| `olist_shop/recommendations.py` | Build the frozen category/price vectors and historical interaction matrix, rank personalized/popular/cart suggestions, compute product similarity and display-gated shared-buyer pairs. |
| `olist_shop/artifacts.py` | Fit the frozen reduced logistic model and RFM model, build the catalog, verify all nine source hashes and save the local artifact bundle. |
| `olist_shop/rewards.py` | Declare the three illustrative reward rules and deterministic capped discount calculation. |
| `olist_shop/store.py` | Persist customer identities, active interests, carts, events, demo orders and coupons in SQLite; enforce checkout transactions and idempotency. |
| `olist_shop/service.py` | Combine historical and simulated customer context; expose shared functions to UI and assistant. |
| `app.py` | Render shopping, product details, cart, orders/rewards, insights and conversational pages. |
| `scripts/verify_notebook_parity.py` | Independently compare extracted data/model/recommendation behavior with the notebook. It is a QA tool, not an app runtime dependency. |

The six runtime preparation inputs are customers, orders, order items, reviews, products and category translation. Payments, seller coordinates and geolocation are not selected classifier inputs. Their full audits remain in the notebook. Before saving artifacts, hashes of all nine original files are verified against the notebook manifest.

## Preparation and saved artifacts

Review answers before purchase are excluded. Eligible reviews are sorted by availability/creation/ID to select the first review per order. Items are aggregated once per order before customer joins. Source line-item events retain their original grain. Customer identifiers remain stable across order-specific customer IDs.

The retention data builder reproduces the original fixed-age snapshots and next-90-day placed-order labels. Only the original 14,362 training customers fit imputation, scaling, encoding and Logistic Regression C=0.1. Log average order value is excluded from the classifier. The selected model is not retuned for the application.

The recommendation artifact uses history strictly before 1 June 2018. It contains 26,895 candidate products, category/price-band vectors, historical distinct-buyer counts, user-product history and shared-buyer counts. Prices are historical medians, converted to integer cents using explicit half-up rounding. Categories and price bands retain weights two and one.

The RFM scaler and K=2 model fit the original November 2017 historical snapshot. Current demo profiles can be assigned descriptively; their assignments are not a new held-out evaluation.

The ignored `artifacts/shop.joblib` contains these fitted objects and historical tables. `artifacts/shop.json` records the build context. Only locally built, trusted artifacts are loaded; there is no uploaded-pickle interface. Normal Streamlit reruns reuse the cached artifact. SQLite data lives separately in ignored `.app_data/shop.sqlite`.

## Recommendation and activity meanings

| Interaction or shelf | Behavior |
|---|---|
| New shopper | Historical popularity supplies initial suggestions. |
| Save interest | Persists an explicit preference for that demo customer until removed; profile rebuilding reranks the content shelf. |
| Product view | Adds a recently viewed event; does not count as a purchase or automatically earn rewards. |
| Cart | Persists selected quantities; cart-context suggestions exclude cart and previously purchased items. |
| Simulated completed order | Updates demo purchase history, removes the checked-out cart and changes discovery exclusions and reward eligibility. |
| Main discovery | Uses distinct historical/demo purchases and saved interests; excludes bought and cart items. |
| Similar products | Uses category and historical price-band cosine for the selected product. |
| Other shoppers also bought | Requires at least two distinct historical shoppers with both products in order records; ranks eligible pairs by cosine. |
| Buy again | Displays the customer's historical products only after completion is known by the demo clock, plus completed demo products, intentionally including purchased items. |
| Familiar categories | Counts distinct purchased products by category, rather than assigning a permanent customer identity. |

The shared-buyer shelf describes recorded orders across time, not necessarily one basket or completed sales. If evidence is insufficient, the app says so and labels a separate popular-alternatives shelf. It never labels those fallback items as proven co-purchases. Same-order Frequently bought together remains a stretch feature and is not claimed to be implemented.

Saved-interest and cart-context reranking are application extensions, not newly measured notebook model improvements. Simulated activity never alters the original CSVs, artifact shared-buyer counts or reported held-out metrics.

## Rewards and checkout

Rules use qualifying completed orders. Historical delivery must be known by the demo clock and not precede purchase. Simulated cancellations do not count toward qualification. Quantity and page-refresh counts do not increase order frequency.

| Priority | Eligibility | Benefit | Minimum / cap |
|---|---|---|---|
| Welcome | No completed orders | 5% | BRL 100 / BRL 20 |
| Welcome back | Previous completed order, last purchase over 60 days ago | 8% | BRL 150 / BRL 30 |
| Frequent shopper | Three completed orders in 90 days, on at least two dates | 7% | BRL 150 / BRL 25 |

Only one rule applies. Coupons expire after seven demo days and allow one redemption. Welcome is once per account; welcome-back and frequent rewards have 60-day and 30-day redemption cooldowns respectively. A cancellation does not restore a previously redeemed coupon.

Checkout uses server catalog prices and integer cents. It rechecks offer ownership, expiry, current eligibility, cooldown, minimum amount and cap inside a SQLite transaction. An order, its items, coupon redemption and cart removal commit together. Failure rolls back the operation. A unique customer/request key makes repeated checkout requests return the same order, rather than creating duplicates. Concurrent requests are serialized with an immediate write transaction.

The original price is shared across customers and rewards are displayed as separate discounts. Coupons are illustrative policy rules, not model-learned or proven retention improvements. The weak repeat-purchase model does not set discounts. No real payment, shipment or refund is performed.

## Demo identities and clock

Use a fresh shopper or the prepared existing-customer personas: Frequent shopper, Returning after a break, One-purchase history and the shared-buyer example. These existing personas come from actual historical patterns; their purchases are not fabricated.

The clock starts on 1 June 2018 and can advance by 1, 7, 30 or 61 days, up to 30 August. It is shared across local demo profiles. Historical catalog and purchase inputs remain frozen at their cutoff; new simulated activity is dated on this clock. Clock movement allows recency, expiry and return scenarios to be demonstrated without comparing 2018 orders with today's date.

Create a fresh shopper with a distinct nickname for an independent scenario. Success clears the form and confirms the selected shopper. An existing demo nickname, ignoring case and repeated spaces, switches to the existing shopper. Duplicate submissions are serialized by a SQLite write transaction. Existing duplicate records are preserved. The database persists across app restarts. The UI provides no real sign-in; identities are selectable demo profiles, not a production account/authentication system.

## Assistant and insights

The bounded assistant answers recommendation, explanation, history, segment and reward questions by calling the same service functions as the pages. It uses no external LLM, API key or generated purchase facts. Unsupported requests receive a description of available commands. Chat context is stored separately per selected customer in the session.

Repeat scores are shown only for an available original 30-day customer-age snapshot, with its date and target. They are not recomputed at arbitrary ages or portrayed as current validated risk. The UI states test AP 0.0153 and ROC-AUC 0.4746. No snapshot means no invented score. RFM labels are descriptive and do not establish loyalty.

## Validation commands

```powershell
.\.venv\Scripts\python.exe scripts/verify_notebook_parity.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The parity check compares all 71,105 research feature rows, validation/test probability vectors and 202 top-ten lists with independently executed notebook reference calculations. Matching the previously opened test is a regression check against the frozen implementation, not another selection exercise.

Core tests cover identity isolation, persistence, minimum values, caps, expiry, cooldown, cancellation, coupon ownership, atomic/idempotent checkout and concurrent duplicate requests. Service checks cover activity-driven changes, the known-completion date boundary for Buy again, history/exclusions, real persona rewards, co-purchase support and function-backed chat answers. The Streamlit flow test browses a known-price item, applies a real demo coupon, checks out, views Buy again/insights/chat, opens the co-purchase example and switches identities.

Inside the Codex sandbox, Windows Streamlit's event-loop socket required an approved unsandboxed test process. Ordinary local terminal execution does not use that sandbox. A test-harness path issue was corrected by passing the absolute app file path to AppTest.

## Viva questions

1. Do models retrain on each click? No. The fitted content vectors are reused while the customer's active profile is rebuilt.
2. What is the difference between a click, interest and purchase? Each is a distinct event; only explicit interests and eligible purchases affect their declared profile rules, and only completed orders qualify for rewards.
3. Why does Buy again include purchased items? It is a reorder shortcut rather than the discovery ranking task.
4. What supports Customers also bought? At least two historical shoppers have both products in their order records; this is not proof of same-order buying or compatibility.
5. Are discounts machine learning? These are transparent business rules, evaluated for correctness rather than learned uplift.
6. Why store money in cents? It makes rounding and cap/minimum calculations deterministic.
7. Why is checkout transactional? Partial order/coupon/cart updates would otherwise leave inconsistent state.
8. What is an idempotency key? A request identifier that makes a duplicate checkout return the same result.
9. Why use a demo clock? The source is historical, so recency and offer expiry need one consistent reference timeline.
10. Why are prediction scores labeled experimental? Held-out repeat discrimination is weak and the validated model applies only at its original fixed-age snapshot.

## Verification result and remaining scope

Fourteen automated tests passed, including the actual Streamlit shopping/coupon/checkout/history/assistant flow and two concurrent duplicate checkout requests. The independent notebook-parity script also passed: all 71,105 feature rows, complete validation/test probability vectors and 202 top-ten recommendation lists match. The local browser preview was opened and visually inspected.

The first local shopping flow is implemented and verified for this contribution. Real authentication, real payments, live inventory, real product photography/titles, cloud deployment and external LLM integration are separate product work. Same-order pair recommendations remain optional. The notebook is preserved as the research reference.
