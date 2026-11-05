# Threat model and problem formulation

The threat model is where a security reviewer decides whether the evaluation tests what the abstract
claims. In the fit set, 157 of 241 papers mention a threat model somewhere; only 47 give it a section
heading. The rest state the attacker in a paragraph of the introduction, in a subsection of the problem
formulation, or in the design section (medians: 10–22 per venue for an explicit section).

## 1. Six items

Every threat model answers these six, in this order.

1. **Goal.** What the adversary wants, in the terms of the system: the account visited, the key
   recovered, the record identified, the prompt executed.
2. **Knowledge.** Black-box or white-box; whether the defense, the model, the training distribution or
   the deployment is known; whether the adversary has historical data.
3. **Capability.** What the adversary can do, and, more importantly, what it cannot. Capabilities
   without limits cannot be refuted and therefore cannot be reviewed.
4. **Observables.** The signals available: packet sizes, timings, cache state, syscalls, model outputs,
   query counts, logs.
5. **Setting.** Closed or open world, adaptive or static, one victim or many, offline or online, with
   the data split and the time window stated.
6. **Out of scope.** The attacks the work does not cover, named. This protects the claim and signals
   that the authors thought about it.

## 2. The two-sentence version, for the introduction

Most papers state the model twice: one sentence in the introduction, the full version later.

> We consider a passive adversary observing encrypted traffic at an ISP, a router or a public Wi-Fi
> gateway, who sees packet sizes, directions and timing but cannot decrypt, modify or drop traffic.

That sentence gives goal, capability and observables. The section later expands it.

## 3. Where the model goes

| Placement | When | Corpus evidence |
|---|---|---|
| Own section (often 3 or 4, "Threat Model" or "Problem Formulation and Threat Model") | defense and attack papers with several attacker variants | 47 of 241 have a heading |
| Subsection of the design or background section | single-attacker papers, systems papers | common at S&P and NDSS |
| Paragraph in the introduction only | measurement papers, where the "attacker" is the phenomenon | the majority |

A paper whose abstract claims a defense against adaptive attackers, and whose experiments run only a
static baseline, is rejected on substance regardless of where the section sits.

## 4. Write the attacker as a bounded agent

Weak:

> The attacker can observe network traffic and may have access to the model.

Strong:

> The adversary observes ciphertext metadata for the victim's session and may query its own copy of the
> model an unlimited number of times; it has no access to the victim's device, cannot decrypt traffic,
> and does not know the detector's weights.

The second version is falsifiable, and it tells the reviewer exactly which experiments are required.

## 5. Tie the model to the evaluation

- Every capability in the model appears in at least one experiment.
- Every experiment stays inside the model, or the paper says which assumption it relaxes.
- An adaptive evaluation is the test of the model: if the attacker knows the defense, does the number
  survive?
- The limitations section names the attacker the paper does not defend against.

## 6. For each paper type

| Type | What the model must add |
|---|---|
| A1 attack | the victim population, the observation window, what "success" means operationally |
| A2 defense | the attacker the defense is evaluated against, including adaptivity |
| A3 measurement | the population sampled, the consent or public-data basis, the ethics boundary |
| A4 system | the deployment assumptions: who runs it, with which privileges, at what cost |
| A5 analysis | the formal model, the assumptions on primitives, what the bound does not cover |
| A6 SoK | the inclusion criteria and the threat-model taxonomy used to organise prior work |
| A7 dataset | what is represented, what is not, and how labels were obtained |

## 7. What gets a paper rejected on this section

- A single-sentence model for a claim of robustness.
- Capabilities listed without limits.
- Closed-world evaluation presented as an open-world defense.
- The threat model changing between introduction and evaluation.
- "The attacker does not know our defense" with no argument for why that is realistic.

## Checklist

- [ ] Goal, knowledge, capability, observables, setting, out of scope: all six present.
- [ ] The capability that the headline result depends on is stated before the result.
- [ ] Adaptive evaluation reported, or its absence explained in one sentence.
- [ ] Every capability appears in an experiment; every experiment stays inside the model.
- [ ] The introduction's one-sentence attacker matches this section.
- [ ] Out-of-scope attacks named explicitly.
