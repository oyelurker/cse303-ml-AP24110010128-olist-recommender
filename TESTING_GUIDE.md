# Manual application review

This is the student's reusable manual walkthrough. The guided screenshot review is recorded in MANUAL_TEST_RESULTS.md, and reported issues are in MANUAL_TEST_ISSUES.md. The table below distinguishes observed passes, partial coverage and untested cases. Existing automated results remain separate from manual evidence.

## 1. Start a clean review

Open the VS Code PowerShell terminal at the repository root. Use a separate testing database and port:

```powershell
$env:OLIST_DEMO_DB = Join-Path (Get-Location) ".app_data\manual-review.sqlite"
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502
```

Open http://127.0.0.1:8502. This uses the existing fitted artifacts. If the app presents Prepare local demo, click it once after confirming the CSVs are in data/raw.

A database is persistent. For a completely fresh repeat of the review, choose a new filename such as manual-review-2.sqlite. Creating a fresh shopper resets that customer's history, not the shared clock. The initial clock is 1 June 2018, advances forward only, and ends on 30 August. Do the ordinary persona tests before the date-advance tests.

If the sidebar is collapsed, open it using the upper-left arrow. Record your shopper nickname and demo date before each scenario. Prices and thresholds are in BRL, displayed as R$.

## 2. Main walkthrough, in this order

| Case | Actions | Expected result | Manual result |
|---|---|---|---|
| Fresh shopper | Expand Create a fresh shopper, enter a unique nickname such as Review A, click Create shopper | Cleared nickname, visible success confirmation, selected identity, empty history/cart and welcome offer; repeated submission creates no extra profile | MT-001 fix: automated pass; manual retest pending |
| Browse and filters | Search stationery, choose a category, change the price range, then clear the filters | Displayed catalog items match filters; an empty match shows a normal empty state | Partial — search verified |
| View versus interest | View a product and go back. Save an interest in a category different from the original popular choices | Viewing adds Recently viewed. Saving interest refreshes content suggestions toward that category/price band. Neither action creates a completed order | Partial — interest verified |
| Cart | Add an item, open Cart, use plus/minus, and remove it by reducing quantity to zero | Correct quantities, sidebar item count and subtotal; empty cart cannot submit an order | Pass |
| Welcome minimum | Add a cart below R$100, then raise it to at least R$100 | Welcome checkbox is disabled below the minimum and enabled when it is met | Pass |
| Welcome redemption | Tick Apply this demo offer and place one simulated order | 5% saving capped at R$20; total equals subtotal minus saving; one confirmation, cleared cart and one saved order | Pass |
| Purchase-aware shelves | Open Orders & rewards, then Shop | Completed product appears in Buy again and is excluded from main discovery; the used welcome offer cannot be redeemed again | Pass |
| Co-purchase evidence | Click Try shared-buyer example in the sidebar | Product page includes Other shoppers also bought with at least two historical shoppers per displayed pair; no compatibility or same-basket claim | Pass — displayed evidence |
| Sparse evidence | Open another product with insufficient shared-buyer evidence | Explicit insufficient-evidence message and separately labeled popular alternatives, rather than invented co-purchase claims | Not run |
| Existing personas | Select Frequent shopper, then Returning after a break | On a fresh June 2018 review clock, qualifying personas show 7% loyalty and 8% welcome-back rewards respectively, with their conditions | Pass — offer display |
| Insights | Review a fresh shopper and an existing shopper | Empty history has no RFM assignment; history can produce a descriptive segment. Repeat score appears only where its original dated snapshot exists, with the experimental warning | Pass — new-shopper values |
| Assistant | Ask Recommend products, Why this suggestion, What offer can I use, and What did I buy before | Answers refer to selected customer and agree with page data; absent history/offers/scores are stated | Pass — tested requests |
| Customer isolation | Put an item in Review A's cart, save an interest, switch to a different fresh Review B, then return to A | B does not inherit A's cart/interests/history/chat. A's own saved data remains when selected again | Pass |
| Persistence | Refresh the browser or restart the app and reselect the same named shopper | Their saved cart, interests and orders remain. The active selection/chat can reset because those are session UI state | Pass |

A saved-interest seed can still appear in discovery if it has not been bought or added to the cart. The main exclusion rule concerns historical/demo purchases and cart items. Similar-category products do not automatically qualify for the co-purchase shelf.

## 3. Check reward arithmetic

| Reward | Percentage | Minimum subtotal | Maximum saving |
|---|---|---|---|
| Welcome | 5% | R$100 | R$20 |
| Frequent shopper | 7% | R$150 | R$25 |
| Welcome back | 8% | R$150 | R$30 |

Try an eligible R$500-or-greater cart to exercise the caps. At R$500 the savings should be R$20, R$25 and R$30 respectively, rather than the uncapped percentages. At most one coupon applies. Base catalog prices should stay the same when changing customer.

Qualifying frequency counts distinct completed orders, not items, quantities, refreshes or logins. Loyalty needs three orders in 90 days across at least two dates. Win-back needs a previous completed order and more than 60 days since the last purchase. An inactive shopper can take priority over the frequency rule.

## 4. Independent date and cancellation scenarios

Use separate fresh testing database filenames for independent clock experiments if necessary. The clock is shared and cannot be moved backward through the UI.

### Earn loyalty through actual demo activity

1. Create a fresh shopper and complete two orders on the initial date.
2. Advance one day using Move the demo forward.
3. Complete a third order.
4. A loyalty offer should become available for the next eligible cart. It is not a discount retroactively applied to the third order.
5. Redeem it once. It should not immediately be offered again; its redemption cooldown is 30 days.

### Check the inactive-customer rule

1. In a fresh independent review database, create a shopper and complete one order.
2. Advance 61 days once.
3. Welcome-back eligibility should appear if its rule/cooldown conditions hold.
4. Do not stack large advances past the 30 August demo limit. An out-of-range advance should show a warning and keep the previous date.

### Check expiry

Offers are valid for seven demo days. Advancing the clock can expire an unused coupon. If the customer still qualifies, the app may issue a replacement coupon, so seeing an offer again is not proof the original coupon remains valid. Old-token expiry rejection is covered directly by the automated tests.

### Check cancellation

Use a fresh shopper with a single demo order. Cancel that order in Orders & rewards. It must no longer count as a completed purchase for Buy again or reward qualification. A redeemed coupon is not restored. A product may still remain in Buy again when another completed order independently contains it.

## 5. Expected limitations, not defects

- Product names and category illustrations are demo presentation; source IDs and historical reference prices do not supply real product titles, current inventory or delivery promises.
- Purchases and rewards are simulated. No payment or shipment occurs.
- Main discovery excludes purchased items, whereas Buy again deliberately includes eligible previous purchases.
- New-interest/cart behavior is an app extension. It does not change the notebook's reported held-out metrics.
- Collaborative evidence is sparse. A co-purchase shelf is not guaranteed for every product.
- Repeat prediction is experimental, with test ROC-AUC 0.4746. New shoppers may have no valid original 30-day snapshot score.
- The assistant supports bounded shopping/data requests; it is not a general external LLM.

## 6. Record evidence and report a failure

Capture these useful screenshots: before/after interest recommendations, cart with applied discount, order confirmation/history, co-purchase support counts, reward persona conditions and an assistant response.

For a failure record:

| Field | Your observation |
|---|---|
| Page and shopper nickname/ID | |
| Demo date | |
| Exact steps, product IDs and cart values | |
| Expected behavior | |
| Actual behavior / exact error | |
| Screenshot and terminal traceback, if present | |

Mark each manual case Pass, Fail or Not applicable. A product's lack of sufficient co-purchase evidence is not itself a failure; displaying invented evidence would be.

## 7. Optional automated verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/verify_notebook_parity.py
```

The first command checks the application and store/service/UI flows. The second checks equivalence to the completed notebook. Neither means that every possible user interface case has been manually reviewed.

After reviewing, stop the test server with Ctrl+C. To return to the default demo database in the same terminal:

```powershell
$env:OLIST_DEMO_DB = $null
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```
