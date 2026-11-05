# Claim calibration

A security reviewer separates three kinds of claim: what was **measured**, what is **guaranteed**, and
what is **assumed**. The same sentence is legitimate in one category and an overclaim in another.

## 1. The evidence ladder

| Evidence | Strongest wording allowed | Wording to avoid |
|---|---|---|
| Measured on k datasets, one attacker, one operating point | "reduces ASR from X to Y under <condition> on <datasets>" | "robust", "effective in general" |
| Measured on static and adaptive attackers | "holds above X under the static and adaptive attacks we evaluate" | "robust against adaptive attackers" (unnamed family) |
| Measured over seeds with a test | "improves <metric> by X points (p < 0.05, n = 5)" | "significantly better" with no test |
| Proven under stated assumptions | "guarantees <property> under <assumptions>" | "secure" unqualified |
| Proven for a restricted model | "guarantees <property> for attackers making at most q queries" | "secure against any attacker" |
| Argued informally | "we argue that ...", "the design makes ... expensive" | "proves", "guarantees" |
| Not evaluated | "we leave <case> to future work" or `[TODO]` | anything implying it was tested |

Move down the ladder freely; never up. A measured result presented as a guarantee is the most common
reason a security paper loses a reviewer.

## 2. Quantities that travel together

| With | Also report |
|---|---|
| attack success rate | false-positive rate and the operating point |
| detection rate | the benign sample it was measured on |
| overhead in ms | hardware and batch size |
| "works in the open world" | the unknown-class ratio |
| "handles adaptive attacks" | which adaptation, how many rounds |
| "scales to N" | memory or time at N |
| a gain over a baseline | whether the baseline was re-run or quoted |

## 3. Scoping sentences

- "under the threat model in Section 3"
- "on the four datasets in Table 2"
- "for attackers restricted to the observables in Section 3"
- "at the 1 % false-positive operating point"

A scoped claim survives review; an unscoped one invites a counter-example the authors cannot answer.

## 4. Overclaims the checker notes

"state-of-the-art" without a benchmark in the same sentence; "first" without a scope; "robust" without
the attack families; "efficient" without the reference point; "secure" or "privacy-preserving" without
the property and its assumptions; "eliminates"; "generalises" without a cross-dataset or cross-model
experiment; "significantly" without a test.

## 5. Output

For each claim in the claim map, write the rung of the ladder its evidence sits on and the strongest
wording that rung allows. Put the table in `report.md`; the abstract, introduction and contributions must
then use the same rung for the same claim.
