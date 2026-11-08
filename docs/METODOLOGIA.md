# Scientific methodology and citations

This document describes the platform's method and the references for the
orchestrated tools. Every score that supports a conclusion comes from a
**published, peer-reviewed** tool — nothing is reimplemented.

## 1. Design

- **Sample:** *Mus musculus* (taxid 10090), cells in vitro.
- **Baits:** declared in `config/baits.yaml`. The pipeline handles two cases: a
  bait **exogenous** to the host, with no mouse orthologue (host–pathogen
  design), and a bait from another species **with** a mouse orthologue, which is
  kept distinct from the bait. Partners = mouse proteins. The repository ships a
  public example (see `config/baits.yaml`), not experimental data.
- **Controls:** IgG/mock/parental cell line, paired per bait.
- **Replicates:** **≥ 3 biological** replicates per group are recommended. With
  n = 2–4, the decision favours specificity (SAINT/MiST) and presence/absence vs
  control, with the quantitative layer (DEP/limma) as support.

## 2. Ingestion and QC

- Per-engine parsers (MaxQuant/DIA-NN/FragPipe/generic) -> a single matrix
  (`MSDataset`), **keyed by the leading UniProt accession**, with **missing =
  NaN** (MaxQuant/FragPipe zeros converted to NaN in DDA; DIA-NN MaxLFQ is
  **not** re-normalised).
- Contaminants/decoys are flagged both by boolean column **and** by prefix
  (`CON__`/`REV__`/`contam_`); baits are never treated as contaminants.
- QC: valid values per sample/condition, correlation between replicates, log2.

## 3. Bait–prey specificity (the core of CoIP)

- **SAINTexpress** (Teo et al., *J Proteomics* 2014; Choi et al., *Nat Methods*
  2011) — SAINT probability + **BFDR** per prey against controls. The de facto
  standard in AP-MS. Exogenous baits are excluded from the mouse prey set.
- **MiST** (Verschueren et al., 2015; Jäger et al., *Nature* 2011) — combines
  reproducibility, abundance and specificity; recommended for the **exogenous
  bait** (host–pathogen paradigm, e.g. Gordon et al., *Nature* 2020).

## 4. Differential quantification

- **DEP** (Zhang et al., *Nat Protoc* 2018) — differential enrichment at protein
  level: filtering, **vsn** normalisation, MNAR imputation (**MinProb**) and
  testing via **limma** (Ritchie et al., *NAR* 2015; empirical Bayes moderated
  t-test). Well suited to proteinGroups matrices.
- **MSstats** (Choi et al., *Bioinformatics* 2014) — when feature-level data are
  available (evidence/report), using the official converters.

## 5. Background / contaminants

- **CRAPome** (Mellacheruvu et al., *Nat Methods* 2013) — background frequency;
  here we give priority to the frequency observed in the user's **own controls**.

## 6. Annotation and network

- **UniProt** (mouse proteome), **STRING v12.0** (Szklarczyk et al.), **BioGRID**
  (Oughtred et al.), GO via **g:Profiler** (Kolberg et al.). The network is
  exported as GraphML/Cytoscape (Shannon et al., *Genome Res* 2003).

## 7. GPU (optional)

- **DIA-NN** (Demichev et al., *Nat Methods* 2020) — accelerated DIA search.
- **MS2Rescore** (Declercq et al.) + **AlphaPeptDeep** (Zeng et al., *Nat Commun*
  2022) — deep-learning rescoring; more IDs at fixed FDR.
- **AlphaFold2-Multimer** (Evans et al.) / **ColabFold** (Mirdita et al., *Nat
  Methods* 2022) — structural validation of the top bait–prey candidates.
- **ESM2** (Lin et al., *Science* 2023) — **exploratory/supplementary**
  prioritisation; never the basis of the confidence score.

## 8. Final ranking

Interactors are ordered by **BFDR (SAINT)**, then by **FDR (DEP/limma)**; the
descriptive measures (fold change of means, observation counts) enter only as QC
or tie-breakers. Confidence label: high (BFDR ≤ 0.05), medium (≤ 0.10), low.

## 9. Reporting for publication

Deposit the raw data in **ProteomeXchange/PRIDE**; report the tool versions (from
`manifest.json`), search parameters, FDR criteria and the replicate/control
design. See `docs/REPRODUTIBILIDADE.md`.
