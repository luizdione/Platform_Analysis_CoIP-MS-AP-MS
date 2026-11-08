#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docs.py - registro de documentos de ajuda/tutoriais servidos pela web.

Serve arquivos .md (e a licenca) de dentro do projeto para a aba "Ajuda e
Tutoriais". Seguranca: apenas caminhos em whitelist/descobertos sob PROJECT_ROOT
sao servidos (sem path traversal). Novos .md em docs/ aparecem automaticamente.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from bonder.config import PROJECT_ROOT

# Documentos curados (ordem e titulos amigaveis). path relativo a PROJECT_ROOT.
CURATED: List[Dict[str, str]] = [
    {"id": "visao-geral", "title": "Overview", "category": "Start", "path": "README.md"},
    {"id": "como-rodar", "title": "How to run (tutorial)", "category": "Tutorials", "path": "docs/COMO_RODAR.md"},
    {"id": "sequencias", "title": "Bait sequences", "category": "Tutorials", "path": "config/sequences/README.md"},
    {"id": "metodologia", "title": "Methodology and citations", "category": "Science", "path": "docs/METODOLOGIA.md"},
    {"id": "reprodutibilidade", "title": "Reproducibility", "category": "Science", "path": "docs/REPRODUTIBILIDADE.md"},
    {"id": "versionamento", "title": "Changelog", "category": "Project", "path": "CHANGELOG.md"},
    {"id": "licenca", "title": "Licence", "category": "Project", "path": "LICENSE"},
    {"id": "terceiros", "title": "Third-party notices", "category": "Project", "path": "THIRD_PARTY_NOTICES.md"},
    {"id": "citacao", "title": "How to cite", "category": "Project", "path": "CITATION.cff"},
]


def _slug(name: str) -> str:
    return name.lower().replace(".md", "").replace("_", "-").replace(" ", "-")


def _registry() -> List[Dict[str, str]]:
    """Curados + auto-descoberta de docs/*.md ainda nao listados."""
    reg = list(CURATED)
    known = {d["path"] for d in reg}
    docs_dir = PROJECT_ROOT / "docs"
    if docs_dir.exists():
        for md in sorted(docs_dir.glob("*.md")):
            rel = "docs/%s" % md.name
            if rel not in known:
                reg.append({"id": _slug(md.name), "title": md.stem.replace("_", " ").title(),
                            "category": "Documentos", "path": rel})
    return reg


def _resolve(rel_path: str) -> Optional[Path]:
    """Resolve com seguranca: precisa ficar sob PROJECT_ROOT e existir."""
    root = PROJECT_ROOT.resolve()
    p = (PROJECT_ROOT / rel_path).resolve()
    if root != p and root not in p.parents:
        return None  # tentativa de sair da raiz -> negado
    return p if p.exists() and p.is_file() else None


def list_docs() -> List[Dict[str, str]]:
    out = []
    for d in _registry():
        if _resolve(d["path"]) is not None:
            out.append({"id": d["id"], "title": d["title"], "category": d["category"]})
    return out


def get_doc(doc_id: str) -> Optional[Dict[str, Any]]:
    for d in _registry():
        if d["id"] == doc_id:
            p = _resolve(d["path"])
            if p is None:
                return None
            return {
                "id": d["id"], "title": d["title"], "category": d["category"],
                "path": d["path"], "markdown": p.read_text(encoding="utf-8", errors="replace"),
            }
    return None
