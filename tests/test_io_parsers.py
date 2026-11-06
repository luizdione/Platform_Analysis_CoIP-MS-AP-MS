#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testes do nucleo de ingestao (CPU, sem GPU, sem R)."""
import numpy as np
import pandas as pd
import pytest

from bonder.io import load_search_output
from bonder.io.parsers import parse_maxquant, parse_diann, parse_fragpipe, _leading_accession


SAMPLES_CFG = [
    {"sample": "NCAP_IP_1", "condition": "IP_NCAP", "bait_id": "NCAP_SARS2", "role": "bait", "replicate": 1, "raw_file": "NCAP_IP_1.raw"},
    {"sample": "NCAP_IP_2", "condition": "IP_NCAP", "bait_id": "NCAP_SARS2", "role": "bait", "replicate": 2, "raw_file": "NCAP_IP_2.raw"},
    {"sample": "NCAP_CTRL_1", "condition": "CTRL_NCAP", "bait_id": "control", "role": "control", "replicate": 1, "raw_file": "NCAP_CTRL_1.raw"},
    {"sample": "NCAP_CTRL_2", "condition": "CTRL_NCAP", "bait_id": "control", "role": "control", "replicate": 2, "raw_file": "NCAP_CTRL_2.raw"},
]

BAITS_CFG = {
    "baits": [
        {"id": "NCAP_SARS2", "source": "viral", "uniprot_accession": None,
         "search_db_header": "bait|NCAP_SARS2|Nucleoprotein"},
        {"id": "TP53_HUMAN", "source": "human", "uniprot_accession": "P04637",
         "search_db_header": "sp|P04637|LEG3_HUMAN",
         "ortholog": {"mouse_gene": "Trp53", "mouse_accession": "P02340"}},
    ]
}


def _write_maxquant(path):
    df = pd.DataFrame({
        "Majority protein IDs": ["P02340;Q9Z0", "NCAP_SARS2", "P12345", "CON__P00761", "Q8R1;Q8R2"],
        "Gene names": ["Trp53", "NCAP", "Prey1", "Trypsin", "Prey2"],
        "Peptides": ["8", "12", "5", "3", "6"],
        "Razor + unique peptides": ["6", "10", "4", "2", "5"],
        "Q-value": ["0.001", "0.0", "0.01", "0.2", "0.005"],
        "Reverse": ["", "", "", "", ""],
        "Potential contaminant": ["", "", "", "+", ""],
        "Only identified by site": ["", "", "", "", "+"],
        "LFQ intensity NCAP_IP_1": ["1000", "50000", "800", "300", "0"],
        "LFQ intensity NCAP_IP_2": ["1100", "52000", "0", "0", "0"],
        "LFQ intensity NCAP_CTRL_1": ["0", "100", "700", "320", "0"],
        "LFQ intensity NCAP_CTRL_2": ["0", "0", "750", "0", "0"],
    })
    df.to_csv(path, sep="\t", index=False)


def _write_diann(path):
    df = pd.DataFrame({
        "Protein.Group": ["P02340", "P12345", "Q8R1"],
        "Protein.Ids": ["P02340", "P12345", "Q8R1"],
        "Genes": ["Trp53", "Prey1", "Prey2"],
        "First.Protein.Description": ["p53 mouse", "Prey one", "Prey two"],
        "/data/NCAP_IP_1.raw": ["1000", "800", "0"],
        "/data/NCAP_IP_2.raw": ["1100", "", "500"],
        "/data/NCAP_CTRL_1.raw": ["", "700", "480"],
        "/data/NCAP_CTRL_2.raw": ["", "750", ""],
    })
    df.to_csv(path, sep="\t", index=False)


def _write_fragpipe(path):
    df = pd.DataFrame({
        "Protein ID": ["P02340", "P12345", "contam_sp|P00761|TRYP"],
        "Protein": ["sp|P02340|LEG3_MOUSE", "sp|P12345|PREY1", "contam_sp|P00761|TRYP"],
        "Gene": ["Trp53", "Prey1", "Trypsin"],
        "Combined Total Peptides": ["8", "5", "3"],
        "Combined Unique Peptides": ["6", "4", "2"],
        "NCAP_IP_1 MaxLFQ Intensity": ["1000", "800", "300"],
        "NCAP_IP_2 MaxLFQ Intensity": ["1100", "0", "0"],
        "NCAP_CTRL_1 MaxLFQ Intensity": ["0", "700", "320"],
        "NCAP_CTRL_2 MaxLFQ Intensity": ["0", "750", "0"],
    })
    df.to_csv(path, sep="\t", index=False)


def test_leading_accession():
    assert _leading_accession("sp|P04637|LEG3_HUMAN") == "P04637"
    assert _leading_accession("P02340;Q9Z0") == "P02340"
    assert _leading_accession("CON__P00761") == "P00761"
    assert _leading_accession("") == ""


def test_maxquant_invariants(tmp_path):
    p = tmp_path / "proteinGroups.txt"
    _write_maxquant(p)
    ds = parse_maxquant(p, samples_cfg=SAMPLES_CFG, baits_cfg=BAITS_CFG)
    # 'only identified by site' removido -> 4 linhas restantes
    assert ds.intensity.shape == (4, 4)
    # ausente (0) virou NaN, nunca 0
    assert (ds.intensity.fillna(-1) != 0).all().all()
    assert ds.intensity.isna().sum().sum() > 0
    # chave = acesso lider
    assert "P02340" in ds.intensity.index
    # isca marcada e nao-contaminante
    assert bool(ds.features.loc["NCAP_SARS2", "is_bait"])
    assert ds.features.loc["NCAP_SARS2", "species"] == "bait"
    # contaminante flaggeado
    assert bool(ds.features.loc["P00761", "is_contaminant"])
    # ortologo murino da isca humana sinalizado
    assert bool(ds.features.loc["P02340", "shared_with_bait"])
    # colunas reconciliadas para sample ids
    assert list(ds.intensity.columns) == ["NCAP_IP_1", "NCAP_IP_2", "NCAP_CTRL_1", "NCAP_CTRL_2"]
    ds.validate()


def test_maxquant_observed_counts(tmp_path):
    p = tmp_path / "proteinGroups.txt"
    _write_maxquant(p)
    ds = parse_maxquant(p, samples_cfg=SAMPLES_CFG, baits_cfg=BAITS_CFG)
    oc = ds.observed_counts("IP_NCAP")
    assert oc.loc["NCAP_SARS2"] == 2   # isca vista nas 2 replicas IP
    assert ds.observed_counts("CTRL_NCAP").loc["NCAP_SARS2"] == 1


def test_diann_not_zeroed(tmp_path):
    p = tmp_path / "report.pg_matrix.tsv"
    _write_diann(p)
    ds = parse_diann(p, samples_cfg=SAMPLES_CFG, baits_cfg=BAITS_CFG)
    assert ds.provenance["acquisition"] == "DIA"
    assert ds.provenance["quant_type"] == "maxlfq"
    assert ds.intensity.shape == (3, 4)
    assert list(ds.intensity.columns) == ["NCAP_IP_1", "NCAP_IP_2", "NCAP_CTRL_1", "NCAP_CTRL_2"]


def test_fragpipe_contaminant_prefix(tmp_path):
    p = tmp_path / "combined_protein.tsv"
    _write_fragpipe(p)
    ds = parse_fragpipe(p, samples_cfg=SAMPLES_CFG, baits_cfg=BAITS_CFG)
    assert bool(ds.features.loc["P00761", "is_contaminant"])
    clean = ds.drop_contaminants_decoys()
    assert "P00761" not in clean.intensity.index


def test_autodetect(tmp_path):
    mq = tmp_path / "proteinGroups.txt"
    _write_maxquant(mq)
    ds = load_search_output(mq, samples_cfg=SAMPLES_CFG, baits_cfg=BAITS_CFG)
    assert ds.provenance["engine"] == "maxquant"
    dn = tmp_path / "report.pg_matrix.tsv"
    _write_diann(dn)
    ds2 = load_search_output(dn, samples_cfg=SAMPLES_CFG, baits_cfg=BAITS_CFG)
    assert ds2.provenance["engine"] == "diann"


def test_parquet_roundtrip(tmp_path):
    from bonder.io import MSDataset
    p = tmp_path / "proteinGroups.txt"
    _write_maxquant(p)
    ds = parse_maxquant(p, samples_cfg=SAMPLES_CFG, baits_cfg=BAITS_CFG)
    outdir = tmp_path / "run"
    ds.to_parquet(outdir)
    ds2 = MSDataset.from_parquet(outdir)
    pd.testing.assert_frame_equal(ds.intensity, ds2.intensity)
    assert ds2.provenance["engine"] == "maxquant"


def test_parquet_fallback_to_pickle(tmp_path, monkeypatch):
    # simula pyarrow/fastparquet indisponiveis (caso Windows/conda quebrado):
    # a serializacao intermediaria deve cair para pickle e o roundtrip funcionar.
    from bonder.io import schema
    monkeypatch.setattr(schema, "_parquet_available", lambda: False)
    p = tmp_path / "proteinGroups.txt"
    _write_maxquant(p)
    ds = parse_maxquant(p, samples_cfg=SAMPLES_CFG, baits_cfg=BAITS_CFG)
    outdir = tmp_path / "run_pkl"
    ds.to_parquet(outdir)
    assert (outdir / "intensity.pkl").exists()
    assert not (outdir / "intensity.parquet").exists()
    ds2 = schema.MSDataset.from_parquet(outdir)
    pd.testing.assert_frame_equal(ds.intensity, ds2.intensity)
    assert ds2.provenance.get("_storage_format") == "pickle"


def test_unmatched_sample_raises(tmp_path):
    p = tmp_path / "proteinGroups.txt"
    _write_maxquant(p)
    bad_cfg = [{"sample": "X", "condition": "c", "bait_id": "b", "role": "bait", "replicate": 1, "raw_file": "totally_other.raw"}]
    with pytest.raises(ValueError):
        parse_maxquant(p, samples_cfg=bad_cfg, baits_cfg=BAITS_CFG)
