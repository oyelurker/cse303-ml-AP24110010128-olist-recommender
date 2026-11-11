# Recorded manual review results

Evidence: the user's screenshots and reports during the guided review on 11 November 2026. The assistant interpreted those captures; it did not independently replay the manual actions. Demo dates advanced from 1 June to 8 June 2018. Displayed customer/order suffixes below are partial UI labels.

No application code or demo data was changed while recording the original results. Afterwards, the user authorized MT-001. Its fix passes automated tests and the follow-up UI checks documented below. Original observed results are retained as historical evidence.

## Observed results

| Check | Evidence observed | Result |
|---|---|---|
| Shopper creation feedback / repeat submission | Repeated clicks created Test User 1 · demo-e and Test User 1 · demo-d after creation was unclear | Open issue MT-001 |
| Category search | stationery returned 671 matching products | Pass for search |
| Interest personalization | Saving FB5598 changed the heading to Picked for you and showed stationery suggestions with Interest saved | Pass for observed behavior |
| Below-minimum welcome cart | One FB5598 at R$79; disabled offer and R$21 more required | Pass |
| Quantity and welcome arithmetic | Quantity 2, subtotal R$158, 5% saving R$7.90, total R$150.10 | Pass |
| Checkout and recorded order | One confirmation for order prefix 36EBAF0F, empty cart, saved quantity 2 and correct amounts | Pass |
| Purchase discovery exclusion | FB5598 absent from Picked for you but still in full catalog and Buy again | Pass |
| Familiar category summary | Stationery counted as one distinct product despite quantity 2 | Pass |
| Shared-buyer example | Perfumery 005030 showed 51250F with three shared shoppers and 75C06E with two; separate category/price similarity section | Pass for displayed evidence |
| Loyalty offer display | Frequent shopper showed 7%, R$150 minimum and R$25 cap | Pass |
| Welcome-back display | Returning after a break showed 8%, R$150 minimum, R$30 cap and over-60-day reason | Pass |
| Chat reward answer | Reply matched the selected returning customer's 8% offer, conditions and expiry | Pass |
| Chat identity isolation | Switching to Test User 1 · demo-e showed an empty conversation instead of the other customer's messages | Pass |
| Chat purchase history | Identified Stationery FB5598 from that shopper's completed demo purchase | Pass |
| Insights for new demo shopper | One order, merchandise R$158, segment 1, one distinct stationery product and no evaluated historical repeat snapshot | Pass for displayed values; no independent manual clustering audit |
| Browser refresh persistence | After refresh and customer reselection, interest, Buy again item and order 36EBAF0F remained | Pass |
| Cart isolation and preservation | Test User 1's R$79 cart did not appear for Frequent shopper, and returned when the original shopper was reselected | Pass |
| Remove final cart item | Minus from quantity 1 produced empty cart, zero sidebar total and no checkout control | Pass |
| Loyalty discount cap | F819F0 subtotal R$668, capped saving R$25 and total R$643 | Pass |
| Immediate loyalty reuse | After simulated purchase, item appeared in Buy again and the 7% offer was no longer displayed | Pass for immediate blocking; 30-day requalification not manually checked |
| Cancellation | Order 36EBAF0F remained listed as cancelled; Buy again empty; used welcome offer not restored | Pass |
| Clock and replacement offer | Demo date became 8 June; an eligible unused welcome-back offer was replaced with expiry 15 June | Pass for visible renewal; old-token rejection not manually checked |
| Chat explanation | Named FB5598, category weight 2, price-band weight 1 and similarity rather than purchase probability | Pass |
| Chat recommendation consistency | Chat and Shop both showed FB5598 R$79, D189FB R$59.90 and 944750 R$39.99 for the unchanged returning customer | Pass |

## Review conclusion

The basic guided shopping, reward and assistant walkthrough is complete. The original creation problem MT-001 was fixed and verified by automated tests and follow-up UI checks. No new functional issue was found in the exercised flows. Remaining boundary coverage is listed below.

This does not establish exhaustive manual coverage, production readiness, predictive accuracy or real retention benefit. The previously completed eleven automated tests and notebook parity checks are separate evidence and were not rerun for this recording step.

## Follow-up UI verification

The user's later screenshots confirmed the category dropdown (671 stationery products), Over R$150 filter (129 matches, visible prices above the threshold), normal zero-result search, Recently viewed for 99A478, insufficient-evidence fallback for Perfumery 00066F, unsupported weather-question fallback, and existing-customer historical score 0.0347 at snapshot 2018-04-25 with the experimental warning. These are displayed-behavior passes, not an independent model-accuracy audit.

The parent assistant then operated the app UI directly. The delegated agent could not access the parent browser session and completed no tests. In the existing manual-review database, Loyalty Test already had order 90A90428 on 8 June. The assistant completed order 0A1DCD51 on that date and observed no loyalty offer. After advancing one day, order 75F2099E on 9 June earned the 7% offer for a subsequent purchase. A R$149 cart was below its R$150 minimum; quantity two produced subtotal R$298, saving R$20.86 and total R$277.14. Order 0588D585 recorded that redemption, cleared the cart and removed the immediately available loyalty offer. These checks passed.

An explicitly empty shopper submission showed Enter a shopper nickname first and retained Loyalty Test. Combined with the user's successful unique-name creation and same-name reuse screenshots, MT-001's visible creation and duplicate-name safeguards have been verified. The automated suite separately tests the rapid repeated-click path.

The shared clock is now 9 June 2018. Existing records were preserved; three additional simulated orders were added to Loyalty Test. Evidence: manual-loyalty-verification.png. No application code changed in this follow-up. Fourteen automated tests previously passed; they and notebook parity were not rerun for these documentation-only changes.

## Additional cases not established by this walkthrough

- Exact price-boundary tests (category selection, a price range and empty search passed).
- Requalifying exactly at 30-day or 60-day redemption cooldown boundaries.
- Rejecting the original expired coupon token directly; visible replacement alone does not prove this.
- Quantity maximum, repeated concurrent checkout and wrong-owner coupon attempts through manual interaction.

Some of these boundaries are covered by existing automated tests. They are not relabeled as manual passes here. New issues should be added to MANUAL_TEST_ISSUES.md without implementing fixes until requested.
