# Related Work

## Purpose and placement

Related work tells the reader which prior design families solve the same security problem and which assumption separates the present work from each family.

Use Section 2 as the default location. This placement follows the common conference-paper structure and gives the introduction room to state the problem and contribution.

Some papers fold related work into the introduction and retain a short Background section later. Use that arrangement when terminology or system context is needed before the method.

The corpus contains a related-work section in 185 of 241 papers. The measured length subset contains 183 papers, with a median of 1,017 words and a p10-p90 range of 352-4,414 words.

Treat 1,017 words as a planning reference, not as a target. A paper with two sharply different prior-work families can justify more space; a paper with one close family should be shorter.

## Group prior work by security assumption

Group prior work by the assumption or threat model that each family adopts. Chronological ordering hides the security distinction that lets the reader compare systems.

For each family, use this three-sentence pattern:

1. Name the family and state what it does, with citations attached to the concrete claims.
2. State the family\'s security, deployment, data, or attacker assumption.
3. State the cost of that assumption for the problem addressed by the paper.

A useful paragraph therefore has the form: "Family A uses mechanism X [citations]. It assumes Y. That assumption costs Z in the target setting." Replace the placeholders with checkable facts.

Start a new paragraph when the assumption changes. Keep systems in one family when they share the same security premise even when their publication years differ.

Describe a family before listing its individual papers. Mention an individual paper separately only when its mechanism, scope, or evidence changes the comparison.

Use citations for prior-work facts and reserve evaluative language for a stated comparison dimension. A citation cluster without a comparison leaves the reader to perform the synthesis.

## Position against the closest work

Choose one closest work or one closest family and state one checkable dimension of difference.

Useful dimensions are mechanism, scope, cost, assumption, input, output, and evaluation.

Name the dimension explicitly: "Relative to X, this paper changes the input from ..." or "Relative to family Y, this design removes assumption Z at the cost of ...".

Tie the distinction to an artifact or measurement that the reader can inspect. Examples include a protocol step, an attacker capability, a supported input type, a measured runtime, or an evaluation workload.

Do not claim general superiority when the evidence covers one dimension. State the comparison at the same operating point used in the evaluation.

Keep the contribution claim in the introduction and use related work to establish the precise gap. Repeating the full contribution list increases length without improving the comparison.

## Length discipline

The corpus median is 1,017 words for 183 papers with a measurable related-work section; the p10-p90 range is 352-4,414 words.

Draft a compact version near the median, then expand only when a distinct assumption family or close comparison requires it.

Cut first: historical chronology, duplicate descriptions of the same mechanism, citations that add no new family or comparison, and broad claims with no checkable dimension.

Cut second: implementation detail that belongs in Method, benchmark detail that belongs in Evaluation, and motivation already established in the introduction.

Retain the sentence that states each family\'s assumption and cost. Those sentences carry the security comparison.

## Checklist

- [ ] Is the section placed in Section 2, or is the alternative introduction-plus-Background structure justified?
- [ ] Are families grouped by assumption or threat model rather than publication year?
- [ ] Does every family follow the three-sentence pattern: family and citations, assumption, cost?
- [ ] Does every citation support a concrete description of prior work?
- [ ] Is the closest work compared on one named checkable dimension?
- [ ] Does the comparison identify an input, output, mechanism, scope, cost, assumption, or evaluation point?
- [ ] Are broad superiority claims removed or tied to evidence?
- [ ] Is the draft length compared with 1,017 words and the 352-4,414-word p10-p90 range for 183 papers?
- [ ] Were chronology, duplicate descriptions, and non-comparative citations cut first?
- [ ] Does each remaining paragraph help the reader locate the paper's security contribution?
