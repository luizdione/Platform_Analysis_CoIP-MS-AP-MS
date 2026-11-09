# Third-party notices

The licence of `Platform_Analysis_CoIP-MS-AP-MS` (see `LICENSE`) does **not**
apply to the third-party components listed here. Each one remains under its own
licence, which prevails with respect to that component.

This platform **orchestrates** published, peer-reviewed proteomics tools — it
does not reimplement them and does not redistribute them, with the exception of
the two JavaScript libraries below, which ship with the repository so that the
dashboard works offline.

---

## 1. Libraries bundled in this repository (`vendor/`)

These are distributed with the code, under
`bonder/web/static/vendor/`.

| Component | Version | Authors | Licence | Source |
|---|---|---|---|---|
| **Cytoscape.js** (`cytoscape.min.js`) | 3.30.2 | The Cytoscape Consortium (2016–2024) | MIT | https://js.cytoscape.org/ · https://github.com/cytoscape/cytoscape.js |
| **marked** (`marked.min.js`) | 15.0.12 | Christopher Jeffrey and contributors (2011–2025) | MIT | https://marked.js.org/ · https://github.com/markedjs/marked |

The original copyright notices and licence texts are preserved in the header of
each `.min.js` file — do not remove them.

Citation for Cytoscape.js (when the network figure is used in a publication):

> Franz M, Lopes CT, Huck G, Dong Y, Sumer O, Bader GD. *Cytoscape.js: a graph
> theory library for visualisation and analysis.* Bioinformatics. 2016.

### `vendor/bin/` — external binaries (not versioned)

The `vendor/bin/` directory is a hatch for the user to supply the **SAINTexpress**
binary without rebuilding the Docker image. No binary is versioned in this
repository (see `.gitignore`); whoever places one there is subject to
SAINTexpress's own licence.

---

## 2. Orchestrated proteomics tools (not redistributed)

The platform invokes these tools when they are present in the environment or in
the container image. **They are not redistributed by this repository**: each one
is obtained from its own source, under its own licence and terms. Check each
licence before use, particularly for commercial use — several are free only for
academic use.

### Search and quantification (raw → protein)

| Tool | Licence / terms | Reference |
|---|---|---|
| **MaxQuant** | Free of charge, own terms (not open source) | Cox & Mann, *Nat Biotechnol* 2008 |
| **FragPipe / MSFragger** | MSFragger: own academic/non-commercial licence | Kong et al., *Nat Methods* 2017 |
| **DIA-NN** | Own terms (free for academic use; commercial under licence) | Demichev et al., *Nat Methods* 2020 |

### Bait–prey specificity

| Tool | Licence / terms | Reference |
|---|---|---|
| **SAINTexpress** | Source distributed by the authors (SourceForge) | Teo et al., *J Proteomics* 2014; Choi et al., *Nat Methods* 2011 |
| **MiST** | Method published by the authors | Verschueren et al. 2015; Jäger et al., *Nature* 2011 |

### Quantitative statistics (R / Bioconductor)

| Tool | Licence | Reference |
|---|---|---|
| **DEP** | Artistic-2.0 (Bioconductor) | Zhang et al., *Nat Protoc* 2018 |
| **limma** | GPL (≥2) (Bioconductor) | Ritchie et al., *NAR* 2015 |
| **MSstats** | Artistic-2.0 (Bioconductor) | Choi et al., *Bioinformatics* 2014 |
| **vsn** | Artistic-2.0 (Bioconductor) | Huber et al., *Bioinformatics* 2002 |

### Databases, annotation and background

| Resource | Licence / terms | Reference |
|---|---|---|
| **UniProt** | CC BY 4.0 | The UniProt Consortium, *NAR* |
| **STRING** v12.0 | CC BY 4.0 | Szklarczyk et al., *NAR* |
| **BioGRID** | MIT (data), own terms | Oughtred et al., *Protein Sci* 2021 |
| **cRAP** | Global Proteome Machine (GPMDB) | — |
| **CRAPome** | Own terms | Mellacheruvu et al., *Nat Methods* 2013 |
| **g:Profiler** | Web service, own terms | Kolberg et al., *NAR* 2023 |

### GPU (optional, supplementary)

| Tool | Licence / terms | Reference |
|---|---|---|
| **MS2Rescore** | Apache-2.0 | Declercq et al. |
| **AlphaPeptDeep** | Apache-2.0 | Zeng et al., *Nat Commun* 2022 |
| **AlphaFold2 / AlphaFold-Multimer** | Code Apache-2.0; weights CC BY 4.0, own conditions | Jumper et al., *Nature* 2021; Evans et al. |
| **ColabFold** | MIT | Mirdita et al., *Nat Methods* 2022 |
| **ESM-2** | MIT | Lin et al., *Science* 2023 |

---

## 3. Software dependencies (Python, R, containers)

The dependencies declared in `pyproject.toml`, `requirements.txt`,
`requirements-gpu.txt` and `environment.yml` — among them NumPy, pandas, SciPy,
NetworkX, Matplotlib, PyYAML, requests, Flask, Gunicorn, RQ, redis-py, pyteomics,
PyArrow, PyTorch and Transformers — and the base images used in `docker/`
(Python, Redis, NVIDIA CUDA images, R/Bioconductor) remain under their own
licences, resolved at install time. None of them is redistributed by this
repository.

---

## 4. How to cite the tools in a manuscript

The full references, by pipeline stage, are in `docs/METODOLOGIA.md`. Every run
records in `manifest.json` the versions of the tools actually used — use that
file as the source for the methods section, rather than copying versions by hand.

If any credit here is incorrect or missing, please open an issue: corrections are
welcome.
