# Manual testing issue log

Review instruction: fixes require the user's request. On 11 November 2026 the user authorized fixing duplicate shopper creation (MT-001). Other findings remain log-only unless requested.

## MT-001 — Repeated Create shopper clicks create duplicate-looking profiles

- **Status:** Fix implemented; automated tests and follow-up UI checks passed. Existing shopper records are preserved.
- **Page:** Shop → Create a fresh shopper.
- **Nickname:** Test User 1.
- **Steps:** Enter the nickname and click Create shopper. Creation was not clear to the user, so they clicked again.
- **Observed result:** Two distinct shopper profiles with the same nickname appeared in Demo customer. Screenshots show Test User 1 · demo-e and Test User 1 · demo-d.
- **User impact:** Unclear completion feedback encourages repeated submission and makes the intended shopper ambiguous.
- **Expected experience:** Creation should be clearly confirmed, and accidental repeated submission should not create another unintended shopper.
- **Evidence:** Two screenshots attached to the user's report. The displayed ID suffixes are partial labels, not full database IDs.
- **Cause:** The form previously generated a fresh ID on every submission, retained the entered nickname and supplied no visible creation confirmation. Empty submissions also defaulted to a new generic shopper.
- **Authorization:** The user requested this fix after the manual review. Preserve the two existing Test User 1 profiles and their histories.

### Implemented behavior

- Successful creation clears the nickname field and visibly confirms the selected new shopper.
- A second empty click creates nothing and keeps the success confirmation.
- Submitting an existing demo nickname selects the earliest matching profile and displays an already-exists message. Case and repeated whitespace do not create variants.
- The lookup and insert run in one immediate SQLite transaction so simultaneous submissions create one profile.
- To intentionally create a separate shopper, use a different nickname. Historical personas are excluded from nickname matching.
- Existing duplicate profiles are not deleted or merged.

### Verification

All 14 tests passed, including normalized-name reuse, concurrent creation, preservation of pre-existing duplicates and the Streamlit form's clearing/confirmation/repeated-click flow. Existing shopping, coupon and checkout tests also passed. Tests used isolated temporary databases; the user's demo database was not edited by the fix process.

**Manual retest:** User screenshots confirmed unique-name creation, field clearing, success feedback and same-name reuse with no new profile. A later assistant-operated UI check explicitly submitted an empty field: it showed Enter a shopper nickname first and retained the selected Loyalty Test profile. The rapid repeat-after-success path also passes the automated UI test. See MANUAL_TEST_RESULTS.md for evidence and scope.
