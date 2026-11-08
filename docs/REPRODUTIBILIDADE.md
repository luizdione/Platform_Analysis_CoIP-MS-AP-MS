# Reproducibility

Principles: nothing silent, everything traceable.

## 1. Databases pinned by version + checksum

`config/databases.yaml` pins the version, URL and sha256 of each source (UniProt
release, STRING v12.0, BioGRID build, cRAP). The downloader:

- writes to a content-addressed cache (`data/`, or `BONDER_DATA_ROOT`);
- keeps `data/registry.json` with url, sha256, size and timestamp;
- **fails** if the checksum diverges (it does not silently re-download);
- supports **offline mode** (`BONDER_OFFLINE=1`): cache only.

On the first `bonder db sync`, fill in the `sha256_*` fields in `databases.yaml`
with the observed hashes and commit them — pinning the versions for good.

## 2. One manifest per run

Each `runs/<run_id>/manifest.json` records:

- the platform version, Python version and host platform;
- the external tools available (SAINTexpress, Rscript, DIA-NN, ColabFold);
- the device decision (GPU/CPU) and the reason for it;
- the ingestion provenance (engine, acquisition, quant type, source files);
- the status of every step (ok/skipped/error) — honest coverage.

## 3. No silent installation

`bonder/_deps.py`: missing dependencies raise a clear error; auto-pip only with
`BONDER_AUTO_PIP=1`. The containers pin the versions (conda env + wheels).

## 4. Determinism

- Missing = NaN (never 0); DIA-NN MaxLFQ is never re-normalised.
- The ESM2 embedding cache (when used) is keyed by (sequence sha256, model).
- Seeds are fixed where applicable.

## 5. Data deposition (reviewers will ask)

- Deposit the **.raw** files and search results in **ProteomeXchange via PRIDE**
  (https://www.ebi.ac.uk/pride/).
- Include: search parameters, the search FASTA (`data/search_db.fasta`), FDR
  criteria, the replicate/control design and the **versions** (from
  `manifest.json`).
- For AP-MS, report SAINT/MiST BFDR and the thresholds used to call interactors.

## 6. Submission checklist

- [ ] `.raw` files + search outputs in PRIDE (ProteomeXchange identifier)
- [ ] `manifest.json` for each contrast attached as supplementary material
- [ ] versions of MaxQuant/FragPipe/DIA-NN, SAINTexpress, DEP/limma/MSstats
- [ ] interactor table with SAINT score/BFDR and, where available, log2FC/FDR
- [ ] interaction network (GraphML) and, if applicable, AF2-Multimer validations
