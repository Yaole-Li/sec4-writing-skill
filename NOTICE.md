# Notice and attribution

## Corpus
The rules, bands and exemplars in this skill were fitted on 268 papers published at IEEE S&P, USENIX
Security and NDSS (2023–2026), downloaded from the venues' open-access proceedings by the repository
owner. **No paper PDF or full text is redistributed.** `PAPER_LIST.md` lists the papers and marks the 27
held-out ones. The corpus contains no ACM CCS papers; every CCS statement in the skill is a convention
and is labelled as such.

## Quoted sentences
`skills/security-conf-writing/references/exemplars/` contains short verbatim sentences and 117 whole
abstracts from those papers, each with its identifier, quoted for commentary and teaching. Copyright
remains with the original authors; they are not licensed under CC BY 4.0 and must not be copied into a
manuscript. If you are an author and want an excerpt adjusted or removed, open an issue.

## Method
The construction method — corpus, sentence-level annotation, percentile bands per venue, reference
documents, checkers, held-out evaluation — follows the pattern of
[Best-Paper-Writing-Skill](https://github.com/gulucaptain/Best-Paper-Writing-Skill) (CC BY 4.0) and of the
TIFS skill built with it. No text or data from those projects is copied here.

## Tooling
`template/SP` and `template/NDSS` use `IEEEtran.cls`; `template/CCS` uses `acmart.cls`; the USENIX folder
ships a local `usenixlike.sty` stand-in because `usenix2019_v3.sty` is not in TeX Live. Replace it with
the official kit before submitting.
