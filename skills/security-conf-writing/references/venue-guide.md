# The four venues: what changes and what does not

Two of these venues are close cousins (S&P and NDSS both use IEEE-style two-column proceedings);
USENIX Security has its own house style and its own mandatory sections; CCS uses the ACM class and adds
a CCS Concepts block. The corpus behind this skill contains 241 fit papers from S&P (86), USENIX (104)
and NDSS (51). **It contains no CCS papers**, so every CCS number here is a convention rather than a
measurement; Section 6 says exactly which parts of the skill are corpus-fitted and which are not.

## 1. Measured differences (fit set)

| Observation | S&P (86) | USENIX (104) | NDSS (51) |
|---|---|---|---|
| Pages, median (min–max) | 19 (15–20) | 21 (18–21) | 18 (14–20) |
| Abstract words, median | **275** | 212 | 227 |
| Abstract sentence count | 12 | 9 | 9 |
| Introduction words, median | 993 | 1162 | 1168 |
| Figures / tables, median | 9 / 8 | 8 / 8 | 11 / 9 |
| Floats per page | 1.05 | 0.81 | 1.17 |
| Explicit threat-model section | 15 / 86 | 22 / 104 | 10 / 51 |
| Threat model anywhere | 47 / 86 | 73 / 104 | 37 / 51 |
| Ethics section | 5 / 86 | 15 / 104 | 7 / 51 |
| Ethics mentioned in the text | 57 / 86 | 89 / 104 | 32 / 51 |
| Open-science section | 3 / 86 | 9 / 104 | 8 / 51 |
| Title with a colon | 74 % | 76 % | 69 % |

Three things follow, and they are the reason a single set of rules cannot serve all four venues:

1. **The abstract has a different budget.** An S&P abstract runs 275 words; a USENIX abstract runs 212.
   A 270-word abstract written for S&P reads long at USENIX, and a 200-word abstract written for USENIX
   leaves the S&P reader without the comparison they expect.
2. **USENIX expects the ethics and open-science statements.** 89 of 104 USENIX papers discuss ethics and
   78 of 104 state artefact availability somewhere; S&P and NDSS do it when the work involves people,
   traffic or live systems.
3. **NDSS papers are the densest.** 11 figures and 9 tables on 18 pages, and the longest introductions.

## 2. House rules that are not in the corpus

| Venue | Class | Columns | Section numbering | Body limit | Anonymised review |
|---|---|---|---|---|---|
| IEEE S&P | IEEE two-column (IEEEtran conference) | 2 | arabic since 2023 | 13 pages + unlimited references | yes |
| USENIX Security | usenix2019 style | 2 | arabic | 13 pages including everything | yes, with a separate artefact statement |
| NDSS | IEEE-like two-column | 2 | arabic | 13 pages + references | yes |
| ACM CCS | `acmart` `sigconf` | 2 | arabic, ACM style | 12 pages + references | yes (`anonymous,review`) |

Check the call for papers of the specific edition: page limits and mandatory sections move between
years, and a draft built to last year's rules is rejected on form.

## 3. Mandatory or expected sections

| Section | S&P | USENIX | NDSS | CCS |
|---|---|---|---|---|
| Abstract | required | required | required | required + CCS Concepts + keywords |
| Introduction | required | required | required | required |
| Background / Related work | expected | expected | expected | expected |
| Threat model | for attack and defense papers | for attack and defense papers | for attack and defense papers | for attack and defense papers |
| Ethics Considerations | when humans, traffic or live systems are involved | **required** | when relevant | when humans or live systems are involved |
| Open Science / Artefact availability | expected when code or data is released | **required** (statement of what is released and where) | expected | expected (ACM artefact badges) |
| Discussion / Limitations | expected | expected | expected | expected |
| Conclusion | expected | expected | expected | expected |

## 4. Artefact badges

USENIX and CCS run artefact evaluation with badges (Available, Functional, Reusable, Results
Reproduced). The badges are images in the proceedings PDFs, which is why the text-level census reports
zero: their presence is a submission-time process, not a writing convention. What the writing has to do
is state, in one short section, what is released, under which licence, where, and what is withheld.

## 5. Where the venues agree

The argument structure is shared across all four: threat landscape, what prior work assumes, the
assumption that breaks, the attacker, the idea, the mechanism, the evidence, the limits. The exemplar
bank in this skill mixes the three measured venues on purpose, because at this level of abstraction the
differences are stylistic rather than structural.

## 6. What is fitted and what is extrapolated

| Part of the skill | Basis |
|---|---|
| Style ranges, abstract and introduction budgets, figure and table counts | fitted on the 241-paper fit set, per venue |
| Rhetorical tiers, move tags, exemplar bank | 120 annotated papers from the three measured venues |
| Ethics, open-science and artefact guidance | fitted on the three venues, plus their published policies |
| CCS template and CCS Concepts guidance | ACM class and CCS conventions; **not** corpus-fitted |
| CCS page limit, anonymity rules | ACM policy; verify against the current call for papers |
