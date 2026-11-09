# Changelog

Notable changes to **Platform_Analysis_CoIP-MS-AP-MS**. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows
[SemVer](https://semver.org/).

## [1.0.2] - 2026-11-09

Documentation only, again: no change to the code, the pipeline or the results.

### Changed

- The remaining public files are now in **English** too: `THIRD_PARTY_NOTICES.md`
  (which was entirely in Portuguese, not just one section) and the guidance
  comments in `config/databases.yaml` and `config/gpu.yaml`.
- The **internal development files** follow the same policy, by the author's
  decision: `.gitignore`, `.dockerignore`, `.gitattributes`, `Makefile`, both
  workflows, `requirements.txt`, `requirements-gpu.txt`, `environment.yml`,
  `docker/environment-analysis.yml`, both Dockerfiles and both compose files.
  This includes the output a user actually sees: the `make` help, the CI data
  guard's error messages, and the warning the build prints when SAINTexpress
  does not compile.
- Only comments, messages and labels changed. Nothing in the logic: the 28
  ignore rules are byte-for-byte identical, the dependency specifications are
  unchanged, and the compose and environment files parse to the same structures.

### Fixed

- Two docstrings pointed at files that do not exist. `bonder/stats/runner.py`
  claimed the R scripts live in `bonder/R/` and run in a `Dockerfile.r`
  container; they live in `R/` at the repository root (which is what the code
  itself resolves) and run in `docker/Dockerfile.analysis`.
  `bonder/scoring/saint.py` referred to a "scoring container" and
  `bonder/docker/Dockerfile.scoring`; SAINTexpress is compiled in
  `docker/Dockerfile.analysis`. Comments only — no behaviour changed.

### Note on the container image

Release 1.0.1 shipped the image before the documentation above was translated,
so `:1.0.1` carries the Portuguese `THIRD_PARTY_NOTICES.md`. That tag is left as
it is, because it correctly pins what 1.0.1 was. From this release on,
`:latest`, `:1.0` and `:1.0.2` carry the English documentation.

### Not deposited separately

As with 1.0.1, this release was not deposited in Zenodo: it changes only the
language of the public documentation. `CITATION.cff` cites the **concept DOI**
([10.5281/zenodo.24063134](https://doi.org/10.5281/zenodo.24063134)).

## [1.0.1] - 2026-11-08

Documentation only: no change to the code, the pipeline or the results.

### Changed

- Public-facing documentation is now in **English**, following the author's
  policy for public repositories: README, the three documents under `docs/`, the
  guidance comments in `config/baits.yaml` and `config/samples.yaml`,
  `config/sequences/README.md`, this changelog and the help-tab labels in the
  dashboard.
- `LICENSE` is now **bilingual**: an English translation followed by the
  Portuguese text, with an explicit clause stating that **the Portuguese text
  prevails** in case of divergence — it is the version the author adopted, it
  refers to Brazilian Law no. 9.609/98 and no. 9.610/98 and elects the courts of
  Rio de Janeiro, and it is the text published with version 1.0.0.
- Documentation **filenames stay in Portuguese** (`docs/COMO_RODAR.md`,
  `docs/METODOLOGIA.md`, `docs/REPRODUTIBILIDADE.md`): they are referenced by the
  dashboard and are part of the archive already deposited under
  [10.5281/zenodo.24063135](https://doi.org/10.5281/zenodo.24063135). Only their
  contents changed.
- Code comments and commit messages remain in Portuguese, unchanged.

### Note on the container image tags

The image tag `1.0.0` was briefly overwritten with content newer than release
1.0.0, because a manual workflow run builds from the default branch rather than
from the release tag. It has been restored to the digest built from `v1.0.0`, so
that `ghcr.io/luizdione/platform_analysis_coip-ms-ap-ms:1.0.0` matches the
`v1.0.0` git tag and the archive deposited under
[10.5281/zenodo.24063135](https://doi.org/10.5281/zenodo.24063135). The publish
workflow now refuses to tag a version from a moving ref.

### Not deposited separately

This release was not deposited in Zenodo: it changes only the language of the
public documentation, and the archive under the version DOI above remains the
faithful snapshot of 1.0.0 as published. `CITATION.cff` therefore cites the
**concept DOI** ([10.5281/zenodo.24063134](https://doi.org/10.5281/zenodo.24063134)),
which always resolves to the most recent deposited version.

## [1.0.0] - 2026-11-06

**DOI:** [10.5281/zenodo.24063135](https://doi.org/10.5281/zenodo.24063135)
(concept: [10.5281/zenodo.24063134](https://doi.org/10.5281/zenodo.24063134))

First release published as an **open scientific platform**. The repository now
contains only the platform: no experimental data, no real targets and no working
notes.

> The archive deposited under the DOI above is the Portuguese-language snapshot
> of 1.0.0, which is what was published at the time.

### Changed — LICENCE (read before updating)

- The licence changed from **MIT** to the author's **own licence** in `LICENSE`:
  personal use and use in teaching are free, **use in research requires the
  author's prior authorisation by e-mail** (luiz.melo@ifrj.edu.br), commercial
  use is not allowed, and neither are redistribution or derivative works.
- **The change applies from this version onwards.** It **does not revoke the MIT
  grant** for what had already been published: anyone who obtained a copy while
  the program was under MIT keeps, over **that copy**, every right MIT granted —
  including using, modifying and redistributing it. A licence already granted is
  not withdrawn. Versions before this one remain MIT for whoever received them.
- Added `THIRD_PARTY_NOTICES.md`: the two JavaScript libraries bundled under
  `bonder/web/static/vendor/` (**Cytoscape.js** 3.30.2 and **marked** 15.0.12,
  both MIT) and the orchestrated proteomics tools, each under its own licence —
  which prevails over this platform's licence with respect to it.
- Added `CITATION.cff` (De-Melo, L.D.B.; ORCID 0000-0003-2445-9943; IFRJ).

### Changed — configuration is now a public example

- `config/baits.yaml` and `config/samples.yaml` now ship a **minimal public
  example** built only from UniProt reference sequences, as a template for users
  to fill in. The example covers the two cases the pipeline treats differently: a
  bait **exogenous** to the host with no mouse orthologue (host–pathogen,
  SARS-CoV-2 nucleoprotein N, P0DTC9) and a bait from another species **with** a
  mouse orthologue kept distinct (human p53, P04637, orthologue `Trp53` P02340).
  The file headers state explicitly that these are examples.
- `config/sequences/README.md` rewritten: how to download the example FASTA files
  and how to declare a bait with no public accession (construct, tag, own
  isolate). The FASTA files remain outside version control.
- `config/gpu.yaml` no longer assumes a specific graphics card; `min_capability`
  and the residue ceiling are user parameters.

### Changed — portability

- `iniciar_bonder.ps1` no longer contains any machine-specific path: it uses
  `$env:BONDER_PYTHON` when set and otherwise the `python` on PATH, **with an
  explicit error message** saying what to set when neither exists.
- The documented conda environment is now the project's own (`bonder`, in
  `environment.yml`) instead of a personal one: `conda env create -f
  environment.yml`.
- Documentation and scripts no longer name a specific GPU model; the GPU is
  described by capability (NVIDIA CUDA, with a guaranteed CPU fallback).
- `.dockerignore` hardened: the container image carries no input data, downloaded
  databases, run outputs, bait FASTA files, credentials or working notes.

### Removed

- All of the author's internal working notes (project memory, session
  instructions, decisions, tasks and archived sessions) and the real targets and
  samples from their experiments. **This repository contains no research data.**
- The repository's previous history was archived in a private repository; this
  release starts a new history, so that the removed content is no longer
  reachable through old commits.

### Added

- A public container image on **GHCR**, linked to this repository, to run the
  platform without a local build (see the README).

---

## Earlier history (technical summary)

The versions below circulated under the MIT licence. The summary is kept to give
context to the code; the description of the biological systems the author was
studying has been removed, as it is not part of the platform.

### [0.3.0] - 2026-07

- Exporter that renders a run's results as a **static HTML page**, publishable on
  any web host (the analyses keep running on localhost).
- **cRAP** contaminant database built from the public source, with a checksum.
- Dashboard: input-file selector, **STRING/BioGRID** network and locally served
  assets (works offline).
- **Help and Tutorials** tab: serves the `.md` documents (tutorials, methodology,
  reproducibility) and the licence, rendered in the browser. Endpoints
  `GET /api/docs` and `GET /api/docs/<id>`.

### [0.2.0] - 2026-07

- In-silico digestion of the mouse proteome and the subtractive methodology.

### [0.1.0] - 2026-07-02

First release of the CoIP-MS / AP-MS platform.

- **Ingestion (`bonder.io`)**: MaxQuant/DIA-NN/FragPipe/generic parsers into a
  unified `MSDataset`; automatic detection of engine and acquisition (DDA/DIA);
  missing = NaN (never 0); keyed by the leading UniProt accession; exogenous
  baits flagged and kept distinct from the host orthologue.
- **Specificity (`bonder.scoring`)**: input formatting plus wrappers for
  **SAINTexpress** (all baits) and **MiST** (exogenous baits, host–pathogen).
- **Quantification (`bonder.stats`)**: R wrappers for **DEP/limma/MSstats**
  (Bioconductor) via Rscript; QC in Python (no inferential value). DIA-NN MaxLFQ
  is never re-normalised.
- **Databases (`bonder.db`)**: mouse UniProt/STRING/BioGRID/cRAP with a
  reproducible cache (checksum, offline mode) + assembly of `search_db.fasta`.
- **GPU (`bonder.gpu`)**: DIA-NN / MS2Rescore / AlphaPeptDeep / AlphaFold and ESM2
  (supplementary), with a CPU fallback and a cooperative `gpu_gate`.
- **Pipeline + web**: orchestrator, report (table/volcano/network), Flask
  dashboard + RQ/Redis queue (thread fallback).
- **Docker**: analysis image (Python + R + SAINT) and GPU image (CUDA 12.4 +
  torch); `docker compose` on CPU by default plus a GPU overlay.
- **Maintenance tab**: audit (dependencies, tools, R, GPU, config, databases,
  paths, runs) plus a pipeline self-test on synthetic data.
- Documentation and core tests (CPU, no GPU/R).

#### Fixed across the 0.x series

- `saint` does not exist as a conda package: removed from the environment;
  SAINTexpress is now compiled from source in the Dockerfile, best-effort and
  non-fatal.
- DIA-NN peptide/q-value mapping now uses the original `Protein.Group`.
- The SAINT gene fallback wrote the literal `nan` (NaN is truthy) → it now falls
  back to the accession.
- Dashboard: an empty log2fc column without R → uses `log2fc_descriptive`; the
  polling now stops at a terminal status (done/error).
- CI: the `requests` dependency was missing from the test job.
