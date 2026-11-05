# Ethics and disclosure

This is the section that most distinguishes a security-conference submission from a journal paper in
another field, and the one reviewers use to decide whether the authors understand what they built.
USENIX Security requires it; S&P and NDSS expect it whenever the work involves people, other people's
traffic or live systems.

## 1. What the corpus does

| | S&P (86) | USENIX (104) | NDSS (51) |
|---|---|---|---|
| A heading that names ethics | 5 | 15 | 7 |
| Ethics discussed somewhere in the text | 57 | 89 | 32 |
| Named as its own section in the annotated sample | rare | common | occasional |

So most papers do not give ethics a section, and most papers still discuss it. Two places work:
a short subsection before the conclusion, or a paragraph inside the introduction ("we disclosed ... ").
A paper that touches human subjects, real users' traffic, live services or malware gets a heading,
because reviewers look for one.

## 2. What has to be stated, by kind of work

| Kind of work | What the reviewer needs |
|---|---|
| Human subjects (interviews, surveys, user studies) | IRB or ethics-board approval, consent procedure, what was recorded, how it was stored, compensation |
| Measurement of live infrastructure (scanning, crawling, censorship probes) | rate limits and scanning etiquette, which hosts were touched, why no harm followed, what was excluded |
| Real-user traffic or logs | consent or a legal basis, minimisation, anonymisation, retention, who has access |
| Attacks on deployed systems or products | responsible disclosure: whom, when, which channel, embargo length, whether a fix shipped |
| Malware, botnets, illicit-market data | how it was obtained without participating, what was not collected, containment, law-enforcement contact if any |
| LLM and agent security | model versions and providers, prompts that produce harmful content, whether outputs are released, dual-use of the attack |
| Any attack paper | dual-use statement: what the release enables, and what is withheld (code, prompts, exploit details) |

## 3. How it reads in the corpus

A disclosure sentence names the party, the date and the outcome:

> Finally, we disclosed the identified messenger vulnerabilities to Signal and Telegram, following
> responsible disclosure guidelines. — S&P 2023

> For the implementations that turned out to be not compliant with the specification, and therefore are
> prone to exploits, we informed the developers in a responsible disclosure. — NDSS 2023

An IRB sentence names the board and the reason:

> Due to the sensitive nature of this work, we approached our institution's IRB with our detailed
> research plan for review. — USENIX 2023

> For the small-scale user interview study, we design a questionnaire with open-ended questions to
> serve as the framework for each interview, and obtain approval from our Institutional Review Board
> (IRB). — USENIX 2023

A dual-use sentence is honest rather than defensive:

> Like any other responsible disclosure, we acknowledge that we cannot remove the harms altogether and
> that an actor with malicious intent might follow similar workflow to perform privacy attacks.
> — USENIX 2023

Note what these have in common: a named actor, a named process, and a stated limit. Adjectives about
being ethical are absent, and that is what makes them credible.

## 4. Placement

```text
Abstract        nothing; ethics belongs to the body
Introduction    one sentence if the work has a disclosure story worth telling
Section 3-4     the threat model states what the attacker may do, which bounds the experiment
Before Conclusion
                a subsection: "Ethics Considerations" (USENIX), "Ethical Considerations and
                Responsible Disclosure" (scanning work), "Ethics and Data Handling" (measurement)
Appendix        consent forms, IRB approval number, scanning configuration, disclosure timeline
```

A separate ethics section placed after the conclusion reads as an afterthought; before the conclusion
it reads as part of the argument.

## 5. The five failures reviewers cite

1. **No approval, no mention.** A user study without a statement of IRB review, or a sentence that
   says "no IRB was required" without saying why.
2. **Disclosure theatre.** "We disclosed to the vendor" with no date, no response, and no indication
   that anything changed.
3. **Scanning without etiquette.** Internet-scale measurement with no statement of rate limits,
   blacklists or opt-out handling.
4. **Dual-use by omission.** An attack released in full with no discussion of what it enables.
5. **Data handling by implication.** "We use publicly available data" as the whole of the data
   statement, when the data are user-generated and personal.

## 6. Checklist

- [ ] The kind of work is matched to the row in §2, and every item in that row is answered.
- [ ] Disclosure names party, date, channel and outcome, or says explicitly that nothing is live.
- [ ] IRB approval is named, or its absence is justified in one sentence.
- [ ] Data provenance, minimisation and retention are stated for anything not public and synthetic.
- [ ] A dual-use sentence says what is released and what is withheld.
- [ ] The subsection sits before the conclusion, not after it.
- [ ] Nothing in this section is a claim of virtue; every sentence is a fact.
