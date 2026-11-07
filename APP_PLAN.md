# Application plan: personalized shopping and customer rewards

Status: first local version implemented and verified on 7 November 2026. See APP_REFERENCE.md for actual modules, setup, tests and viva notes. This plan records the intended behavior; the completed notebook experiments remain unchanged.

## Product concept

Build a small shopping assistant with personalized product shelves, a demo cart, simulated orders, transparent rewards and a conversational helper. A customer-insights view provides the academic explanation of history, recommendation sources, RFM segments and experimental repeat scores.

The central demo loop is: browse or express interest, see updated suggestions, place a simulated order, return later, and see history-aware recommendations and any eligible reward. The application demonstrates behavior using the Olist historical catalog and explicitly recorded demo activity.

## Public examples and what they support

| Public source | Documented idea | Application adaptation |
|---|---|---|
| [Amazon Science: recommendation history](https://www.amazon.science/the-history-of-amazons-recommendation-algorithm) | Historical item-to-item recommendations connect products through purchase patterns | A secondary evidence-backed Other shoppers also bought shelf |
| [Amazon: product bundling](https://sell.amazon.com/blog/product-bundling) | Frequently bought together suggests complementary co-purchases | A later same-order pair feature, kept separate from generic similarity |
| [Blinkit engineering, May 2018](https://blinkit.com/blog/data-and-bid-simplify-grocery/) | Previously bought, cart-responsive suggestions and last-minute additions | Buy again and cart-aware suggestions, adapted to our sparse non-grocery dataset |
| [Amazon seller announcement, August 2023](https://sell.amazon.com/blog/announcements/brand-tailored-promotions) | Promotions can target customer audiences including loyalty-related groups | Simple transparent audience rules for demo coupons |
| [Blinkit promotional terms](https://blinkit.com/terms) | Offers have campaign eligibility and conditions such as order value, validity and cancellation treatment | Explicit eligibility, caps, expiry and redemption rules |

These sources document public patterns. The 2018 and 2023 articles are historical examples, not specifications of current proprietary ranking or discount formulas. We do not claim to reproduce either company's internal systems, results or discount thresholds.

## Shopping experience

| Surface | Behavior | Evidence or implementation source |
|---|---|---|
| Popular now | Show historical popular items when personalization has insufficient evidence | Existing popularity model |
| Recommended for you | Rank unseen products from historical purchases; incorporate explicitly selected session interests as a separately labeled extension | Existing content model plus proposed activity-profile handling |
| Similar to this product | Match the selected product's category and historical price band | Existing content representation |
| Other shoppers also bought | Show products with actual shared historical buyers for the selected item | Existing collaborative concepts; application adds a minimum-support display rule |
| Your familiar categories | Display category shares from the customer's own purchase history and category-filtered discovery | Descriptive history aggregation; category labels do not define a permanent customer identity |
| Buy again | List the user's own earlier purchases with an add-to-cart shortcut | Direct history, intentionally separate from discovery recommendations |
| Complete your cart | Suggest related unseen items that are not already in the cart | Cart-context application extension with a source-specific label |
| Rewards | Explain one eligible demo coupon, its reason and checkout conditions | Explicit business rules, not a learned discount optimizer |

Do not merge these meanings. Category similarity does not establish that two products were bought together. Shared buyers across separate orders do not establish same-basket co-purchases. Buy again intentionally includes purchased products, while the main discovery shelf excludes them.

## Collaborative and basket evidence

The notebook already evaluated item-based collaborative filtering, but it required popularity fills for about 77 percent of validation top-five positions. Content remains the primary selected recommendation method. The secondary co-purchase shelf should appear only where actual history supports its description.

For an initial display rule, require at least two distinct historical buyers shared by a product pair. Rank eligible neighbors using the existing similarity approach and retain support counts for explanations. This minimum support is a proposed application rule, not a previously evaluated improvement.

When support is absent, hide the shelf or show a separately labeled Popular in this category shelf. Do not relabel popularity or content matches as Customers also bought. Do not reveal individual shoppers' identities.

Frequently bought together is optional for a later small increment: calculate distinct-order pair counts from multi-product historical baskets, require a stated support threshold and report coverage. It is not already implemented by the user-product cosine model. Never infer accessory compatibility solely from a broad category.

## Activity and profile updates

Track product views, explicit interests, cart additions/removals, simulated completed orders and offer redemptions. Keep their event types and timestamps separate.

- A product view adds to Recently viewed; it is not automatically a purchase or reward event.
- Explicit interest adds a saved preference for the selected demo customer until removed, used by the clearly labeled activity-based shelf.
- Cart activity supplies temporary shopping context; removing an item removes that cart context.
- A simulated completed order updates demo purchase history, discovery exclusions and reward counters.
- Changing the customer or resetting a demo clears the appropriate session context and does not mix identities.

No model retraining is needed after each action. The fitted content representation is reused while the customer's eligible profile is rebuilt and candidates reranked. Interest/cart handling is a new app behavior and must be checked separately from the notebook's purchase-based evaluation.

## Returning-customer rewards

Returning means coming back to shop. Page refreshes, repeated logins and browsing alone do not earn order-frequency rewards. Count distinct qualifying completed orders and distinct order dates, rather than product quantities or number of clicks. Historical orders count only if completion is known by the demo reference time. Demo cancellations or refunded orders do not create qualifying rewards.

The following are illustrative defaults for a simulated store, not learned rates, verified profitability or Amazon/Blinkit policies. Retain BRL because source prices are Brazilian historical values.

| Rule, checked in this order | Proposed eligibility | Demo benefit | Constraints |
|---|---|---|---|
| Welcome | No qualifying completed orders | 5% off | Minimum merchandise subtotal BRL 100, cap BRL 20; one redemption per demo account |
| Welcome back | At least one qualifying order and last qualifying purchase more than 60 days ago | 8% off | Minimum BRL 150, cap BRL 30; one redemption in 60 days |
| Frequent shopper | At least three qualifying orders in the preceding 90 days, on at least two distinct dates | 7% off | Minimum BRL 150, cap BRL 25; one redemption in 30 days |
| Other customers | No rule above applies | No automatic loyalty coupon | Normal product browsing and recommendations remain available |

Issue an eligible coupon with a seven-day validity and one redemption, subject to the stated cooldown. Apply at most one coupon to a cart. Show the qualifying reason before redemption. Recheck eligibility, account ownership, expiry, minimum value and cap at checkout. Use deterministic currency rounding; repeated checkout clicks must not duplicate orders or redemption.

Do not raise an individual's base product price because of customer category. Keep the catalog base price shared and show the discount separately. Model-predicted repeat probability does not decide coupon eligibility: its held-out discrimination is weak. RFM groups describe historical behavior, while these separate rules specify reward policy.

Olist does not provide a randomized discount experiment, reliable item profit margins or offer-response labels for this design. Therefore this app cannot claim that these discounts improve retention or maximize profit. It can demonstrate consistent eligibility and log simulated outcomes.

## Screens

1. Shopping home: customer/guest selection, category and price filters, popular/personalized shelves, familiar categories and a visible reward explanation when eligible.
2. Product details: category, anonymized/demo label, historical reference price, Similar items, evidence-backed Other shoppers also bought, interest/cart actions.
3. Cart and demo checkout: selected items, clearly labeled contextual suggestions, subtotal, eligible discount/cap and simulated order confirmation.
4. Purchase history and rewards: earlier purchases, Buy again, saved reward conditions and redemption history.
5. Customer insights: descriptive RFM profile, recommendation reasons, evidence/source labels and the experimental repeat score at its valid prediction context.
6. Shopping assistant: supported requests such as Recommend similar items, Why this suggestion, What did I buy before and Am I eligible for an offer. Responses call the underlying functions.

The assistant starts with bounded intents and deterministic replies. It cannot invent coupon eligibility, pair counts, compatibility or model confidence. External LLM integration remains optional after the functions work.

## Data, time and presentation rules

Use an explicit historical demo reference date and an optional controlled advance-date action. Historical interactions and completion facts must be available by that date. Use the same clock for recency and offer expiry. A simulated order timestamp belongs to the demo timeline. Do not compare 2018 purchase dates directly with today's date and call every shopper inactive.

Keep original CSVs and notebook evaluation outputs immutable. Store demo events in a separate local database with an is_simulated marker. Simulated orders do not become evidence that other real customers bought a pair and do not alter the frozen reported model metrics.

Olist lacks full product titles, photos, stock and current sale prices. Use visibly labeled demo product names, category icons and historical reference prices. Same-price-per-product and the discount policy are demo rules. Avoid claims about live inventory or delivery speed.

The retention pipeline's score applies at 30 days after a first observed item-bearing order, with a next-90-day placed-order target. Do not recompute it at arbitrary customer ages and present it as validated. Show the original-context score only where available, and mark it experimental. Dynamic activity personalization and coupon decisions are separate capabilities.

## Proposed implementation stack

For the first course application, use Python, Streamlit, pandas/scikit-learn and SQLite. Streamlit session state holds immediate UI context; SQLite persists demo identities, events, carts, simulated orders and coupons across reruns. Package the notebook-selected artifacts separately from serving code. A larger frontend/API can be considered only if the UI requirement justifies it.

The first implementation uses this stack. Eleven automated tests and the independent notebook-parity check pass. No additional ML family is introduced.

## Bounded build sequence and acceptance

| Contribution | Work | Acceptance evidence |
|---|---|---|
| 1. Extract reference pipeline | Preparation, frozen content/popularity helpers, RFM and experimental classifier artifacts | Match notebook output IDs/scores on fixed reference examples; preserve historical cutoffs |
| 2. Activity and shopping flow | Catalog cards, customer context, event storage, cart and simulated checkout | Profile changes update the correct shelf; switching identity isolates history; checkout is idempotent |
| 3. Co-purchase and history shelves | Product neighbors with support gating, familiar categories and Buy again | Never show a co-purchase claim without qualifying pairs; discovery excludes seen/cart items as defined; reorder shelf remains separate |
| 4. Reward engine | Rule-based eligibility, coupon records and capped checkout discount | Boundary tests for 0/1/3 orders, dates, expiry, minimum spend, cap, cooldown, cancellation and duplicate redemption |
| 5. Assistant and insights | Function-backed answers, visible reasons and academic model explanations | Replies agree with recommendation/offer functions; unavailable or weak evidence is stated |
| 6. Demo and documentation | A new user, an existing customer, a frequent shopper, an inactive shopper and a sparse-history example | Complete one end-to-end demo for each; update reference notes and setup instructions together |

Frequently bought together from same-order pairs is a stretch feature after the main flow works. New app behaviors need separate fixture/coverage checks. Do not reuse the opened notebook test as a new tuning set or overwrite its benchmark numbers with simulated app activity.

## Example demonstration

A guest starts with popular products, marks a stationery product as interesting and sees activity-based matches. They add an item and see clearly labeled cart suggestions, then complete a simulated order. A later session shows that purchase in Buy again and excludes it from discovery. With sufficient qualifying orders on distinct dates, a frequent-shopper reward becomes available with a visible explanation and capped checkout discount. An existing historical customer also demonstrates the evidence-backed co-purchase shelf wherever shared-buyer support exists.

## Definition of a successful first version

The app makes its recommendation sources understandable, responds correctly to actual demo activity, preserves separate customer histories and applies transparent reward rules consistently. It demonstrates the course methods and their limits. It does not claim Amazon-scale recommendation quality, live grocery logistics or experimentally proven retention uplift.
