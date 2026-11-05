# Conclusion

## Function and length

A security conclusion closes the argument in 150-480 words. The corpus median is 478 words over 144 papers with a conclusion, with a p10-p90 range of 152-2,087 words.

State what the paper showed, under which assumptions, and what changes for defenders, operators, or users.

Use the same claim scope as the body. State the tested property, attacker model, deployment setting, and evidence level that support the conclusion.

Give the practical stance: identify the decision, design choice, or defensive action that the results support. A conclusion should leave the reader with a reason to use, compare, deploy, or further test the work.

Write the conclusion after the evidence is stable. It should compress the paper rather than introduce a second abstract.

## Summary and stance

A summary lists what the paper did. A stance states what the evidence means for a security decision.

Good example:

> We presented a nonce-bound verification path for services that cannot trust the client runtime. Under the stated key and freshness assumptions, the protocol rejects replay and context-swapped responses. Across the evaluated workloads, the measured overhead is the cost of binding each response to its request. Deployments that need client-visible evidence should adopt the verification path when those assumptions hold and should retain the listed checks for freshness and context.

This example names the mechanism, assumptions, security property, cost interpretation, and deployment consequence without adding a new result.

Weak example:

> We built a powerful system and obtained excellent results. Our approach is broadly useful and should be adopted by everyone.

The weak version gives no property, assumption, evidence scope, or decision rule. It also makes a new universal adoption claim.

## What to include and exclude

Use a compact four-part structure: restate the security problem, state the method and tested property, state the evidence under its assumptions, and state the defender or user consequence.

Give one sentence to the problem and one sentence to the method when the paper has a simple design. Give more space to the evidence and practical stance when they determine deployment.

Do not add new claims, new numbers, or new citations. Every conclusion sentence should trace to the introduction, method, evaluation, or stated limitation.

Do not turn a future-work list into an unsupported promise. Name a concrete next test only when it follows from a limitation already stated in the paper.

Do not repeat every table value. Refer to the result at the claim level and preserve the detailed operating point in Evaluation.

Use plain language for the defender or user consequence. State who changes what behavior and under which assumptions.

Check each sentence against one source location before finalizing. A sentence with no source location is a candidate for removal or relocation.

## Limitations placement

Place limitations in the last subsection of Evaluation or in a Discussion section. If the paper has no Discussion section, use a final Evaluation subsection named Limitations or Discussion and Limitations.

Mention the conclusion-level consequence of the limitation in one sentence when it changes how the reader should use the result. Keep the detailed tested range, untested case, and cause in the limitation subsection.

## Checklist

- [ ] Is the conclusion between 150 and 480 words, with the corpus median of 478 words over 144 papers used as a planning reference?
- [ ] Does it state what was shown and under which threat, deployment, and security assumptions?
- [ ] Does it state what changes for defenders, operators, or users?
- [ ] Does it express a stance rather than only repeat a summary?
- [ ] Does every claim trace to evidence already presented?
- [ ] Are new claims, new numbers, and new citations absent?
- [ ] Are detailed metrics and operating points left in Evaluation?
- [ ] Are limitations placed in the last Evaluation subsection or Discussion when no Discussion exists?
- [ ] Does the conclusion name a concrete use condition or decision rule?
- [ ] Is the prose direct, impersonal, and free of unsupported universal adoption language?
