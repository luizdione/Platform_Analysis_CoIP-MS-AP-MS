# How to run the platform (step by step)

## Prerequisites

- Docker Desktop (Windows 11 + WSL2) or Docker Engine (Linux).
- For GPU: NVIDIA Container Toolkit + a driver compatible with CUDA 12.4.
- Without Docker: conda/miniforge with the project environment
  (`conda env create -f environment.yml`, creates the `bonder` env).

## 1. Prepare baits and databases

```bash
# bait sequences for the public example (see config/sequences/README.md)
curl -L "https://rest.uniprot.org/uniprotkb/P0DTC9.fasta" -o config/sequences/NCAP_SARS2.fasta
curl -L "https://rest.uniprot.org/uniprotkb/P04637.fasta" -o config/sequences/TP53_HUMAN.fasta
# (for YOUR baits: edit config/baits.yaml and download/write the matching FASTA files)

# download the version-pinned mouse databases (once)
python -m bonder.cli db sync
# validate the baits and build the combined search FASTA
python -m bonder.cli baits check
```

## 2. (Optional) Produce the search output from .raw files

If all you have are the raw files:

- **DDA:** run MaxQuant or FragPipe using `data/search_db.fasta` -> you get
  `proteinGroups.txt` (MaxQuant) or `combined_protein.tsv` (FragPipe).
- **DIA:** run DIA-NN (GPU) -> you get `report.pg_matrix.tsv` (+ `report.tsv`).
  Inside the GPU container:
  ```bash
  docker compose -f docker/docker-compose.yml -f docker/docker-compose.gpu.yml \
    run --rm gpu python -m bonder.gpu.tools   # DIA-NN/rescoring wrappers
  ```

Put the output in `./inputs/`.

## 3. Start the platform

```bash
# CPU (always works)
docker compose -f docker/docker-compose.yml up --build
# GPU (NVIDIA)
docker compose -f docker/docker-compose.yml -f docker/docker-compose.gpu.yml up --build
```

Open **http://localhost:8080**.

## 4. Run an analysis (dashboard)

1. Give the path to the search output, e.g. `/inputs/proteinGroups.txt`.
2. Pick the contrast (e.g. `NCAP_vs_CTRL` or `TP53_vs_CTRL`).
3. Click **Rodar analise**. Follow the status.
4. Inspect **Resumo/QC**, **Interatores** (table ranked by BFDR/FDR),
   **Volcano** (if DEP ran) and **Rede** (cytoscape).

## 4b. Run from the CLI (headless / CI)

```bash
python -m bonder.cli run --input inputs/proteinGroups.txt --contrast NCAP_vs_CTRL
# outputs in runs/<run_id>/: interactors.tsv, network.graphml, volcano.png,
#                            results.json, manifest.json
```

## 5. Outputs

- `interactors.tsv` — ranked table (prey, gene, SAINT/BFDR, log2FC/FDR,
  background, confidence).
- `network.graphml` / `network.json` — interaction network (Cytoscape/cytoscape.js).
- `volcano.png` — volcano plot from DEP/limma.
- `manifest.json` — reproducibility (versions/tools/device/steps).

## Validating the full stack (SAINT + R actually running)

After starting with Docker, run the self-test INSIDE the analysis container
(the one that has R/Bioconductor and SAINTexpress):

```bash
docker compose -f docker/docker-compose.yml run --rm worker bonder selftest
```

Expected output with the full stack:

```
AUTOTESTE: PASSOU | candidatos: ~248
passos: {... 'saint': 'ok', 'dep': 'ok', ...}
```

- `dep: ok`  -> R/Bioconductor (DEP/limma) really ran.
- `saint: ok` -> SAINTexpress really ran.
- If you see `saint: pulado` ("skipped"), SAINTexpress did not compile during the
  build. Manual install (the official release is a tar.gz and builds with GSL):
  ```bash
  # inside a Linux container/host with g++ and libgsl-dev installed:
  curl -fL -o saint.tgz "https://sourceforge.net/projects/saint-apms/files/SAINTexpress_v3.6.3__2018-03-09.tar.gz/download"
  tar xzf saint.tgz
  cd SAINTexpress_v3.6.3__2018-03-09/SAINTexpress-int && bash compile
  # copy the resulting 'SAINTexpress-int' binary into a directory on PATH
  # (e.g. mount a host volume at /opt/bonder/bin, which is already on PATH).
  ```
  The pipeline then picks it up automatically. DEP/limma do NOT depend on this.

On plain CPU (conda, no Docker) the same `python -m bonder.cli selftest` reports
`saint`/`dep` as `pulado` ("skipped") — expected, since SAINT and R live in the
container.

## Maintenance tab (audit + self-test)

In the dashboard, the **Manutencao** ("Maintenance") tab runs a sanity audit:

- Python dependencies (core vs optional) and their versions;
- external tools on PATH (SAINTexpress, Rscript, DIA-NN, ColabFold, nvidia-smi);
- gold-standard R packages (DEP/limma/MSstats) when Rscript is present;
- GPU (chosen device + free VRAM) and config (baits/contrasts/warnings);
- cached reference databases + `search_db.fasta`; writable paths; recorded runs.

The **Rodar autoteste** ("Run self-test") button executes the pipeline on
synthetic data (in a temporary directory) and reports the status of every stage
and check — the sanity check of the scripts and processes, with no dependency on
GPU or R. Also available through the API:

```bash
curl http://localhost:8080/api/health/full
curl -X POST http://localhost:8080/api/health/selftest
```

## GPU tips (sharing the card with a local LLM)

`gpu_gate` waits for free VRAM and for the absence of an LLM process
(Ollama/llama) before loading GPU stages. Tune the thresholds in
`config/gpu.yaml`.
