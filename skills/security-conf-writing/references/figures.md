# Figures and Tables

## Figure 1

Figure 1 in a security paper is usually a system overview or threat scenario. It explains actors, trust relationships, inputs, outputs, and the protected path.

Use Figure 1 to orient the method. A result plot belongs later, after the reader knows the system and the claim being tested.

Label trust boundaries, attacker-controlled inputs, protected state, and the direction of messages when those distinctions affect the security argument.

Use the figure reference in the overview: name the path that the next method subsections will explain.

## Captions

Build a caption in two parts. Start with a noun phrase that names the figure, then state the takeaway or the reading instruction.

A reliable pattern is: "System overview of [system]. [Actor or component] sends [input] through [mechanism] to produce [protected output]; dashed arrows show attacker-controlled actions."

The corpus median caption length is 28.5 words over the measured captions. Figure 1 captions have a median of 53.5 words. Use the longer Figure 1 budget for actor roles, trust, and the takeaway.

A caption should let a reader understand what is being compared, measured, or traced without searching the main text for the object names.

Define symbols and colors in the caption when they are essential to reading the figure. Keep detailed motivation in the body.

## Tables

Use booktabs-style horizontal rules and avoid vertical rules. Align numbers by magnitude or decimal mark when the format permits.

Mark the best value per column and explain the marking in the caption. Define whether best means larger, smaller, or closest to a target.

Report the operating point in the table or its caption. Include thresholds, budgets, workload, sample count, or other fixed conditions that make the values comparable.

Keep units in headers. Include a denominator for rates, percentages, averages, and per-input costs.

Name missing, inapplicable, and failed values explicitly. A blank cell leaves the result uninterpretable.

The corpus median is 8 tables per paper, with a 2-16 range. Use tables for exact comparisons and figures for trends, distributions, and system flows.

## Placeholders and evidence

Never invent curves, screenshots, traces, or numbers. A draft that lacks data should reserve the frame and describe the required evidence.

Keep a result figure as a framed placeholder with its plan in the caption. State the x-axis, y-axis, groups, operating point, uncertainty display, and claim to be tested.

Use a placeholder label that cannot be mistaken for a measured result, such as "RESULT FIGURE PLACEHOLDER: replace after experiment." Remove the label before submission.

Do not draw a plausible curve to suggest an expected trend. Expected direction belongs in the experiment plan and the claim paragraph.

## Float budget

The corpus median is 9 figures per paper, with a 4-16 range, and 8 tables per paper, with a 2-16 range.

The median float density is 0.95 floats per page, with a 0.52-1.39 range. Use this as a layout warning: a page crowded with floats can hide the causal argument and increase reader search cost.

Plan floats against the venue page limit. The venue limits are policy facts: S&P, USENIX, and NDSS use 13-page body targets under the stated submission rules, while CCS uses 12 pages plus references.

Reserve Figure 1 for orientation, then allocate result figures to claims that require visual trends. Put exact values in tables when the claim depends on close comparisons.

## Anti-examples of bad captions

- "Figure showing our system." It names neither the actors nor the security takeaway.
- "Performance results." It omits the metric, operating point, groups, and direction of improvement.
- "Screenshot of the prototype." It gives no purpose, state, or interpretation and can conceal identifying information.

## Checklist

- [ ] Is Figure 1 a system overview or threat scenario rather than a result plot?
- [ ] Does Figure 1 label actors, trust relationships, attacker-controlled inputs, and relevant message flow?
- [ ] Does every caption start with a noun phrase naming the object?
- [ ] Does every caption state a takeaway or reading instruction?
- [ ] Is the Figure 1 caption planned near the 53.5-word median when its roles and trust relations require it?
- [ ] Do tables use booktabs-style rules and mark best-per-column values?
- [ ] Does each table caption explain what best means and state the operating point?
- [ ] Are units and denominators present for reported rates and costs?
- [ ] Are missing and inapplicable values labeled?
- [ ] Are unmeasured result figures framed as placeholders with an explicit plan?
- [ ] Does the float plan respect the corpus medians of 9 figures, 8 tables, and 0.95 floats per page?
- [ ] Were all invented curves, screenshots, and numbers removed before submission?
