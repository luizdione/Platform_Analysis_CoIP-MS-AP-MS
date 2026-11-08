# Bait sequences (FASTA)

When a bait is **exogenous** to the host proteome, it has to be included in the
search FASTA (`search_db.fasta`) so it can be quantified as a positive control.
Put **one FASTA per bait** here, named as pointed to by `config/baits.yaml`.

The FASTA files are **not versioned** (see `.gitignore`): your bait sequence is
yours. This directory is published empty, with only this README.

The commands below download the two baits of the **public example** that ships
with `config/baits.yaml`. Replace the accessions with those of your own Co-IP.

## 1. SARS-CoV-2 nucleoprotein N (`NCAP_SARS2`) — UniProt P0DTC9

An example of a bait exogenous to the host. Download the exact canonical
sequence (do not type it by hand):

```bash
curl -L "https://rest.uniprot.org/uniprotkb/P0DTC9.fasta" -o NCAP_SARS2.fasta
```

## 2. Human p53 (`TP53_HUMAN`) — UniProt P04637

An example of a bait from another species that **does** have a mouse orthologue
(`Trp53`, P02340); the pipeline keeps the orthologue distinct from the bait.

```bash
curl -L "https://rest.uniprot.org/uniprotkb/P04637.fasta" -o TP53_HUMAN.fasta
```

## A bait with no public accession (construct, your own isolate)

If your bait has no UniProt/GenBank accession — a construct, a tag, or an isolate
from your own laboratory — write the FASTA by hand, with a header matching the
`search_db_header` declared in `baits.yaml`:

```
>bait|MY_BAIT|short description of the bait
MSEQ...   (the amino-acid sequence)
```

Leave `uniprot_accession: null` in that `baits.yaml` entry.

## Verification

Once the files are in place:

```bash
bonder baits check
```

This validates the baits and builds `data/search_db.fasta` (host proteome +
contaminants + baits) for the search. Without the FASTA files the command only
warns (it does not fail) and the rest of the pipeline keeps working from an
already-prepared search output.
