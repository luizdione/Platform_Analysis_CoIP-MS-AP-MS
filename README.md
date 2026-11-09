# Platform_Analysis_CoIP-MS-AP-MS

**A local platform (browser + Docker) for CoIP-MS / AP-MS analysis and
identification of protein–protein interaction partners in the mouse proteome**
(*Mus musculus*, taxid 10090).

This platform **does not reinvent the wheel**: it **orchestrates established,
peer-reviewed tools** from the proteomics community inside reproducible
containers, with a Flask dashboard served at `http://localhost:8080`. The result
is rigour and reproducibility compatible with publication, running **on your own
server**, with no closed or paid software.

> **This repository contains no experimental data.** The files under `config/`
> are a **public example** built only from UniProt reference sequences, meant as a
> template. Your data stays on your machine, in a folder you point to (see
> [Where your data lives](#where-your-data-lives)) — it is never versioned and
> never enters the container image.

> The Python package and its modules are named `bonder`, the project's internal
> name. The platform's name is the repository's.

---

## Why does open source have the rigour to publish?

High-impact interaction proteomics runs mostly on **open** software. What makes
work publishable is not the brand, but: using **validated and citable** methods,
proper **FDR** control, a design with replicates and controls, and **depositing
the raw data** (PRIDE/ProteomeXchange). The SARS-CoV-2 host–pathogen interactome
(Gordon et al., *Nature* 2020) and BioPlex were built with these same tools.

## Orchestrated tools (every one has a published paper)

| Stage | Tool (open) |
|---|---|
| Search/quantification (raw → protein) | **MaxQuant** (DDA) · **FragPipe/MSFragger** · **DIA-NN** (DIA, GPU) |
| **Bait–prey specificity** | **SAINTexpress** (all baits) · **MiST** (host–pathogen, exogenous baits) |
| Differential quantification | **DEP / limma / MSstats** (R/Bioconductor) |
| Background / contaminants | internal **CRAPome** (controls) + cRAP |
| Annotation / networks | **UniProt, STRING, BioGRID**, GO (g:Profiler), Cytoscape |
| GPU (NVIDIA, optional) | **DIA-NN**, **MS2Rescore + AlphaPeptDeep** (rescoring), **AlphaFold2-Multimer/ColabFold** (structural validation) |

> ESM2 (embeddings) is used only as **supplementary exploratory prioritisation**,
> never as the basis of the confidence score that goes into the main figure.

Licences and citations for each tool: [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)
and [`docs/METODOLOGIA.md`](docs/METODOLOGIA.md).

## Architecture

```
 browser (localhost:8080)
        |
   [web] Flask ---- queue (Redis/RQ) ----> [worker]
                                             |
   io -> db -> scoring(SAINT/MiST) -> stats(DEP/limma R) -> annotate -> pipeline -> report
                                             |
                        [gpu] (optional) DIA-NN / rescoring / AlphaFold / ESM2
```

- **One-way flow** `io -> db -> scoring/stats -> gpu -> pipeline -> web`.
- The **scientific core is testable on CPU**, with no GPU and no R (see `tests/`).
- Stages whose external tools are missing are **skipped and recorded in the
  manifest** — the pipeline never claims coverage it did not have.

---

## How to run

### Option 1 — ready-made image from GHCR (no build)

```bash
docker pull ghcr.io/luizdione/platform_analysis_coip-ms-ap-ms:latest
```

Run it pointing at your own data folder (nothing is sent off your machine):

```bash
docker run --rm -p 8080:8080 -v "/path/to/your/data:/inputs:ro" ghcr.io/luizdione/platform_analysis_coip-ms-ap-ms:latest
```

On Windows PowerShell, use your folder's path:

```powershell
docker run --rm -p 8080:8080 -v "C:\my_data\coip:/inputs:ro" ghcr.io/luizdione/platform_analysis_coip-ms-ap-ms:latest
```

Then open `http://localhost:8080`. This image brings the dashboard up on its own
(in-thread queue, no Redis) — enough for individual use. For the full stack with
Redis and a separate worker, use option 2.

### Option 2 — compose from source (full stack)

```bash
# CPU (works on any machine):
docker compose -f docker/docker-compose.yml up --build
#    -> open http://localhost:8080

# With an NVIDIA GPU (requires the NVIDIA Container Toolkit):
docker compose -f docker/docker-compose.yml -f docker/docker-compose.gpu.yml up --build
```

Put your search outputs in `./inputs`. In the dashboard: give the path
(`/inputs/proteinGroups.txt`), pick the contrast (bait vs control) and run.
The **search engine and acquisition mode (DDA/DIA) are detected automatically**.

### Option 3 — without Docker (conda)

```bash
conda env create -f environment.yml      # creates the 'bonder' env
conda activate bonder
pip install -e .
python -m bonder.cli list-contrasts
python -m bonder.web.app                 # dashboard at 127.0.0.1:8080
```

To install into an environment you already have:
`conda env update -n YOUR_ENV -f environment.yml`.

On Windows there are also `run.ps1` (Docker, CPU), `run-gpu.ps1` (Docker, GPU) and
`iniciar_bonder.ps1` (no Docker). If the `python` on your PATH is not the one with
the dependencies, set `BONDER_PYTHON` to the full path of `python.exe`.

---

## Where your data lives

The platform reads and writes **only where you tell it to**. Nothing leaves your
machine.

| What | Environment variable | Default |
|---|---|---|
| Search outputs you want to analyse | `BONDER_INPUTS_DIR` | `./inputs` (in Docker: mounted at `/inputs`) |
| Downloaded reference databases (UniProt/STRING/BioGRID/cRAP) | `BONDER_DATA_ROOT` | `./data` (in Docker: `/data`, volume `bonder-data`) |
| Run results | `BONDER_RUNS_DIR` | `./runs` (in Docker: `/runs`, volume `bonder-runs`) |
| Configuration files (the YAMLs) | `BONDER_CONFIG_DIR` | `./config` |

```bash
export BONDER_DATA_ROOT=/my/disk/coip/data
export BONDER_RUNS_DIR=/my/disk/coip/runs
export BONDER_INPUTS_DIR=/my/disk/coip/inputs
```

Two more useful variables: `BONDER_OFFLINE=1` uses only the already-downloaded
database cache (no network calls), and `BONDER_REDIS_URL` enables the RQ/Redis
queue — without it a run executes in a thread of the process itself, which is
enough for individual use.

In a plain `docker run`, `/data` and `/runs` live **inside** the container and are
lost when it is removed. To keep results, mount volumes:

```bash
docker run --rm -p 8080:8080 \
  -v "/path/to/your/data:/inputs:ro" \
  -v "coip-data:/data" -v "coip-runs:/runs" \
  ghcr.io/luizdione/platform_analysis_coip-ms-ap-ms:latest
```

## Configuration (declarative)

The four files below define the analysis. The first two ship with a **public
example** that you are meant to replace:

- `config/baits.yaml` — the baits. The example covers the two cases the pipeline
  treats differently: a bait **exogenous** to the host with no mouse orthologue
  (host–pathogen), and a bait from another species **with** a mouse orthologue,
  which is kept **distinct** from the bait.
- `config/samples.yaml` — samples, replicates and bait-vs-control **contrasts**.
  The names must match the columns of your search output.
- `config/databases.yaml` — mouse databases **pinned by version** + checksums.
- `config/gpu.yaml` — device, `gpu_gate` and toggles for the GPU stages.
- `config/sequences/` — bait FASTA files (see the README there). Not versioned.

## CLI

```bash
bonder db sync            # download/verify UniProt/STRING/contaminants (mouse)
bonder baits check        # validate baits and build search_db.fasta
bonder qc --input F       # QC summary of a search output
bonder run --input F --contrast NCAP_vs_CTRL
```

## Reproducibility

Every run writes `manifest.json` (versions, available tools, device, provenance,
steps) and `results.json`. Databases are **pinned by version** and verified by
sha256. See [`docs/REPRODUTIBILIDADE.md`](docs/REPRODUTIBILIDADE.md) and the PRIDE
deposition guide.

## Tests

```bash
python -m pytest -q     # CPU core (IO, SAINT formatting, end-to-end pipeline, web jobs)
```

## Requirements

- **Minimum:** Docker (Desktop on Windows/macOS, Engine on Linux). Nothing else.
- **Without Docker:** Python 3.10+ (tested on 3.11) and conda/miniforge.
- **GPU (optional):** an NVIDIA card with CUDA 12.4, a compatible driver and the
  NVIDIA Container Toolkit. Every GPU stage has a **guaranteed CPU fallback**.
- **R (optional):** provided by the analysis image; without it, differential
  quantification is skipped and recorded in the manifest.

Developed and tested on Windows 11 + WSL2 and on Linux.

---

## Licence

**The licence changed in version 1.0.0.** See [`LICENSE`](LICENSE) for the terms
that apply.

| Use | Condition |
|---|---|
| **Personal** (on your machine, no economic purpose) | Free, no need to ask |
| **Teaching** (classes, courses, training, student coursework) | Free, no need to ask |
| **Research** (generating/analysing data for a thesis, article, preprint, poster, project) | **Only with the author's prior authorisation, by e-mail:** luiz.melo@ifrj.edu.br |
| **Commercial** (paid services, consulting, SaaS, business use) | Not allowed — contact the author for a specific licence |
| **Redistribution, modification, derivative works** | Not allowed without written authorisation |

Running the platform merely to get to know or evaluate it, without producing
research results, counts as personal use and does **not** require authorisation.

The `LICENSE` file is **bilingual**: an English translation followed by the
Portuguese text. **In case of any divergence, the Portuguese text prevails** — it
is the version the author adopted, it refers to Brazilian Law no. 9.609/98 and no.
9.610/98 and elects the courts of Rio de Janeiro, and it is the text published
with version 1.0.0.

### About the previous MIT licence

Up to version 1.0.0 this platform was released under **MIT**. The new licence
applies **from that version onwards** and **does not revoke the MIT grant for what
was already published**: anyone who obtained a copy while it was under MIT keeps,
over **that copy**, all the rights MIT granted — including using, modifying and
redistributing it. A licence already granted is not withdrawn.

### Third parties

The orchestrated tools and the libraries bundled under
`bonder/web/static/vendor/` (**Cytoscape.js**, **marked** — both MIT) keep their
own licences, which **prevail** over this one with respect to them. See
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## How to cite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24063134.svg)](https://doi.org/10.5281/zenodo.24063134)

See [`CITATION.cff`](CITATION.cff) — the **Cite this repository** button at the top
of the GitHub page produces a ready-made reference in APA or BibTeX.

> De-Melo, L.D.B. (2026). *Platform_Analysis_CoIP-MS-AP-MS: a local, reproducible
> platform for CoIP-MS / AP-MS interaction partner identification in the mouse
> proteome*. Federal Institute of Education, Science and Technology of Rio de
> Janeiro (IFRJ). Zenodo. https://doi.org/10.5281/zenodo.24063134

**Which DOI to use:**

| DOI | When |
|---|---|
| `10.5281/zenodo.24063134` | **Concept.** Always resolves to the most recent deposited version. The default choice, and the one in `CITATION.cff`. |
| `10.5281/zenodo.24063135` | **Version 1.0.0.** Use it in an article when you need to pin exactly the code you ran, which is what a reviewer needs to be able to inspect. |

Release 1.0.1 was not deposited separately: it changed only the language of the
public documentation, so the archive under the version DOI stays the faithful
snapshot of 1.0.0 as published. To pin the exact code behind a result, cite the
version DOI **and** report the platform version from that run's `manifest.json`.

Also cite the **tools you actually used** — the versions for each run are in its
`manifest.json`, and the per-stage references are in
[`docs/METODOLOGIA.md`](docs/METODOLOGIA.md).

## Author

**Luiz Dione Barbosa De-Melo** (De-Melo, L.D.B.)
Federal Institute of Education, Science and Technology of Rio de Janeiro (IFRJ),
Rio de Janeiro, Brazil
ORCID [0000-0003-2445-9943](https://orcid.org/0000-0003-2445-9943) ·
luiz.melo@ifrj.edu.br

---

*Documentation filenames are kept in Portuguese (`docs/COMO_RODAR.md`,
`docs/METODOLOGIA.md`, `docs/REPRODUTIBILIDADE.md`) because they are referenced by
the dashboard and are part of the archive already deposited under the DOI above.
Their contents are in English.*
