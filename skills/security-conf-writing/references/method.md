# Method

## Required order

Present the method in causal order. The reader should see the system-level idea before the components that implement it.

1. Give an overview and point to the anchor figure.
2. Use one subsection per component in causal order.
3. Explain the need for a component before its mechanism.
4. State the security or functional property produced by the mechanism.
5. Give the security argument and complexity argument after the components.

The corpus median for Method or Design is 2,569 words over 137 papers with that section, with a p10-p90 range of 463-5,351 words. Use this range as a planning reference.

## Overview and anchor figure

Open with the system goal, actors, inputs, outputs, and the path from input to protected result. Point to Figure 1 while explaining the path.

State the attacker-visible interfaces in the overview. The threat model should make the allowed attacker actions concrete before the security argument relies on them.

Use one sentence to preview each component in the order in which information or control flows through the system.

## Need before mechanism

For every component, state the design need first. The need names a failure mode, attacker capability, or required property that the preceding component leaves unresolved.

Then describe the mechanism that addresses that need. End the subsection by stating the property that follows from the mechanism under the stated assumptions.

A short worked skeleton is:

- Need: the verifier must distinguish a forged response from a response produced by the enrolled service.
- Mechanism: the service binds the response to a nonce and an authenticated context before returning it.
- Property: replayed or context-swapped responses fail verification under the key-compromise and freshness assumptions stated in the threat model.

Use this pattern for every nontrivial component. It prevents a list of mechanisms whose security role is implicit.

Do not open a subsection with an unexplained data structure, equation, or implementation name. Give the reader the reason for the object before its construction.

## Notation

Introduce notation immediately before its first use. Define each symbol once and use the same symbol in prose, equations, figures, and proofs.

Keep notation to symbols that carry an argument. Plain-language names are preferable for incidental implementation values.

A notation table is justified when the method has several interacting sets, roles, keys, or indexed objects that recur across at least two subsections. The table should define symbols and domains; it should not duplicate the method narrative.

Place a short notation table after the overview or at the start of the first formal subsection. Put a long symbol glossary in an appendix.

Explain the operating meaning of every security parameter. A symbol without a domain, unit, or role makes the later argument hard to check.

## Security and complexity arguments

State the security claim in terms of the threat model, attacker capability, and protected property. Map each premise to a component or protocol step already described.

Give the complexity argument after the causal design description. Report asymptotic cost and the measured cost used in Evaluation when both matter.

Move full reductions, long algebraic derivations, and exhaustive case analysis to an appendix when they interrupt the main design argument. Keep the claim, assumptions, proof idea, and a pointer in the body.

Put full protocol listings in an appendix when the main text can specify the message flow, state transitions, and validation conditions precisely without the complete listing.

Keep a protocol excerpt in the body when a single step determines the security property or when omitting it would make the claim uncheckable.

## Cut these items

Cut restated motivation from every subsection. Refer back to the need sentence and advance the mechanism.

Cut standard derivations that a security reader can verify from a cited definition or familiar primitive. State the instantiated result and cite the standard source when needed.

Move implementation details such as thread counts, storage layout, compiler flags, and logging choices to the Evaluation setup unless they define the security mechanism.

Cut code-level narration that does not alter an attacker capability, a security property, or a measured cost.

## Checklist

- [ ] Does the section open with an overview and an anchor figure?
- [ ] Are components ordered by causal information or control flow?
- [ ] Does every component state need, mechanism, and resulting property?
- [ ] Is the need stated before the mechanism?
- [ ] Are attacker-visible interfaces and assumptions explicit?
- [ ] Is notation introduced before use and kept consistent across text, figures, and proofs?
- [ ] Is a notation table included only when recurring interacting symbols justify it?
- [ ] Does the body retain each security claim, its assumptions, and its proof idea?
- [ ] Are full proofs and full protocol listings placed in an appendix when they interrupt the main argument?
- [ ] Were standard derivations, repeated motivation, and evaluation-only implementation details cut from the method?
- [ ] Is the draft length compared with 2,569 words and the 463-5,351-word p10-p90 range for 137 papers?
