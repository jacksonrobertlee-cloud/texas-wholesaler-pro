# Gulf Coast Lead Aggregator — User Guide (Updated)

A Streamlit tool for aggregating, matching, scoring, and grading wholesale real estate leads from public records across **Harris, Fort Bend, Montgomery, Galveston, and Brazoria** counties.

---

## 1. What This Tool Does (and Doesn't Do)

This app does not connect live to every county's records — most Gulf Coast counties don't publish an API for evictions, probate, divorce, or tax delinquency. Each of those lives on its own government portal and usually requires a manual export.

**Two sources are a genuine exception** and are pulled live, no manual export needed:
- **City of Houston Code Enforcement Violations** (Harris/Houston only) — real CKAN open-data feed.
- **HCAD Ownership Data by zip code** (Harris only) — real, public ArcGIS parcel service, queried directly.

Everything else — Fort Bend, Montgomery, Galveston, Brazoria in every category, and Harris's tax delinquency, probate, divorce, eviction, and fire records — is manual-CSV-upload, sourced from the links in the Data Sources tab.

What the app does with whatever data you give it:
1. Matches leads across sources by normalized address, so a property hitting both the tax-delinquent list and the probate index gets flagged as one stacked, high-priority lead.
2. **Scores and letter-grades** every lead (A–D) based on how many, and which, distress signals are attached.
3. Auto-derives a **Multiple Evictions** signal when the same address shows up 2+ times in an eviction filing upload.
4. Flags your **highest-value combination** — out-of-state owner + at least one other distress signal — with a dedicated filter.
5. Tracks **duplicates** and **skip-traced contact info** so your list stays clean and workable.
6. Gives you a working pipeline to move leads from New → Contacted → Under Contract.

Nothing here is legal advice, and generating a lead list doesn't replace SB 2212 wholesale disclosure obligations once you're working a real deal.

---

## 2. Running the App

```bash
pip install streamlit pandas numpy requests openpyxl --break-system-packages
streamlit run lead_aggregator.py
```

Opens at `http://localhost:8501`. Data lives in that browser session — closing the tab clears everything, so export CSVs regularly (every tab has a download button).

---

## 3. The Seven Tabs

### Tab 1 — 📚 Data Sources
A directory of the real portal for each record type in each of the five counties: appraisal district (ownership), tax office (delinquency), county/district clerk (probate, divorce), JP courts (evictions), city open-data (code violations), and fire department records. Sources marked **🔄 AUTOMATED** are the two live feeds described above; everything else is a link to the real government portal you'll export from yourself.

### Tab 2 — 📥 Upload & Normalize
One section per lead category: Tax Delinquent, Code Violation, Probate/Estate, Divorce Filing, Eviction Filing, Out-of-State Owner, Fire.

- **Code Violation** and **Out-of-State Owner** each have a 🔄 auto-fetch button at the top (Harris only) in addition to the manual uploader below.
- The HCAD auto-fetch takes a comma-separated list of zip codes — fetch a handful at a time, not the whole county; each zip is cached 24 hours.
- After any auto-fetch, you'll be asked to **confirm the column mapping** (which column is address, owner, mailing state) before it's added — this protects against a live feed's column names not matching what the app expects.
- Manual CSVs need at minimum an `address` column; see the Upload Guide for the full column spec per category.
- **Multiple Evictions is not a separate upload** — it's derived automatically from repeat addresses in your Eviction Filing data.
- Re-uploading a file **replaces** the previous one for that category; it doesn't append.

### Tab 3 — 🔁 Duplicates
- **Within-file duplicates**: the same address appearing more than once inside one uploaded CSV — usually a bad export, worth cleaning up.
- **Cross-source matches**: the same address appearing across multiple lead-type files — expected, and exactly what drives scoring, shown here so you can sanity-check the matching.

### Tab 4 — ☎️ Skip Trace
County records give you an address and owner name, never a phone or email. Export your leads from the Merged Lead Pipeline tab, run them through a skip-trace provider (BatchSkipTracing, REISkip, IDI, TLOxp), then upload the results here (`address`, `owner_name`, `phone_1`, `phone_2`, `email`). Matched leads get a ☎️ tag elsewhere in the app. This tab also shows a **"Needs Skip Trace"** export — your highest-scored leads still missing contact info.

### Tab 5 — 🎯 Merged Lead Pipeline
The core output — every uploaded address, deduplicated, scored, and graded.

**Scoring weights** (capped at 100):

| Signal | Points |
|---|---|
| Tax Delinquent | 30 |
| Probate / Estate | 30 |
| Multiple Evictions | 25 |
| Eviction Filing | 20 |
| Code Violation | 20 |
| Fire | 20 |
| Divorce Filing | 15 |
| Out-of-State Owner | 15 |

**Letter grade**: A (80+), B (60–79), C (40–59), D (<40).

**Priority Combo filter**: a dedicated toggle for "out-of-state owner + at least one other distress signal" — your single best-value combination, one click instead of stacking sliders manually.

Other controls: minimum score, minimum stacked signals, sort by score/signal count/eviction count, contact-info-only toggle. Click **Add to Working Pipeline** on any lead; export the filtered list anytime.

### Tab 6 — 📋 Working Pipeline
Leads you're actively working. Status (New Lead → Contacted → Negotiating → Under Contract → Dead/Closed), notes, contact info if skip-traced, and a full CSV export.

### Tab 7 — 🏚️ Code Enforcement Focus
A dedicated, zip-filterable view combining code violations with out-of-state ownership (Harris/Houston, since that's the only county with both live feeds):
- **Refresh** button pulls fresh violation data on demand.
- Filter by **zip code**, **out-of-state owners only**, and **minimum violation count** (repeat offenders surface automatically).
- Shows violation count, owner name, mailing state, and out-of-state flag per address; exports to CSV.

---

## 4. A Typical Session (Harris-First Workflow)

1. **Code Enforcement Focus** tab → "Refresh Code Violations (live)."
2. **Upload & Normalize → Out-of-State Owner** → enter your target zip codes → "Fetch HCAD Ownership Data."
3. Back in **Code Enforcement Focus**, filter to those zips + "out-of-state owners only" → export. This alone is your fastest, lowest-effort lead source.
4. Pull manual exports for Tax Delinquent and Probate from the **Data Sources** tab (highest-weighted signals) and upload them in Tab 2.
5. Check **Duplicates** before trusting the numbers.
6. **Merged Lead Pipeline** → filter to score ≥ 60, toggle Priority Combo → export.
7. Skip-trace that list, upload results in Tab 4, pull the "Needs Skip Trace" list for what's left.
8. Move contactable leads into **Working Pipeline** and start calling.
9. Repeat the manual-export steps for Fort Bend, Montgomery, Galveston, and Brazoria one county at a time — there's no automation shortcut for those yet.

---

## 5. Known Limitations

- **Automation is Harris/Houston-only**, and only for two of seven signal types (code violations, ownership). Everything else, everywhere else, is manual export.
- **Code violation coverage is thin outside Houston proper** — most unincorporated areas have no open-data feed at all.
- **Fire data is thin everywhere.** Harris's live feed only shows *currently active* incidents, not historical fires; a real fire-history record requires a paid TPIA request. Other counties have no equivalent feed.
- **Address matching is exact-normalized, not fuzzy.** Clean up unit numbers/abbreviations in source exports if matches seem low.
- **Session-only storage.** Nothing persists after you close the app; export CSVs as you go.

---

*Not legal advice. Consult a licensed Texas real estate attorney for contract and disclosure matters (SB 2212).*

