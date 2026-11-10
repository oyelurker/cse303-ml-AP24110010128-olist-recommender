# Manual testing issue log

Review instruction: record the user's reported issues without fixing application code or changing demo data until the user requests fixes.

## MT-001 — Repeated Create shopper clicks create duplicate-looking profiles

- **Status:** Reported by user; not fixed. No application or database changes made.
- **Page:** Shop → Create a fresh shopper.
- **Nickname:** Test User 1.
- **Steps:** Enter the nickname and click Create shopper. Creation was not clear to the user, so they clicked again.
- **Observed result:** Two distinct shopper profiles with the same nickname appeared in Demo customer. Screenshots show Test User 1 · demo-e and Test User 1 · demo-d.
- **User impact:** Unclear completion feedback encourages repeated submission and makes the intended shopper ambiguous.
- **Expected experience:** Creation should be clearly confirmed, and accidental repeated submission should not create another unintended shopper.
- **Evidence:** Two screenshots attached to the user's report. The displayed ID suffixes are partial labels, not full database IDs.
- **Verification:** User-observed behavior; not independently reproduced during this logging step. Root cause is not yet investigated.
- **Fix instruction:** Log only for now. Preserve both existing profiles and postpone implementation decisions.
