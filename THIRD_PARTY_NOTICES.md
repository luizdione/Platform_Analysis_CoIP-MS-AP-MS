# Atribuições de terceiros

A licença do `Platform_Analysis_CoIP-MS-AP-MS` (ver `LICENSE`) **não se aplica**
aos componentes de terceiros listados aqui. Cada um permanece sob a sua própria
licença, que prevalece quanto a esse componente.

Esta plataforma **orquestra** ferramentas de proteômica publicadas e revisadas
por pares — ela não as reimplementa e não as redistribui, salvo as duas
bibliotecas JavaScript abaixo, que acompanham o repositório para que o dashboard
funcione offline.

---

## 1. Bibliotecas incluídas neste repositório (`vendor/`)

Estas são distribuídas junto com o código, em
`bonder/web/static/vendor/`.

| Componente | Versão | Autoria | Licença | Origem |
|---|---|---|---|---|
| **Cytoscape.js** (`cytoscape.min.js`) | 3.30.2 | The Cytoscape Consortium (2016–2024) | MIT | https://js.cytoscape.org/ · https://github.com/cytoscape/cytoscape.js |
| **marked** (`marked.min.js`) | 15.0.12 | Christopher Jeffrey e colaboradores (2011–2025) | MIT | https://marked.js.org/ · https://github.com/markedjs/marked |

Os avisos de copyright e os textos de licença originais estão preservados no
cabeçalho de cada arquivo `.min.js` — não os remova.

Citação do Cytoscape.js (quando a figura de rede for usada em publicação):

> Franz M, Lopes CT, Huck G, Dong Y, Sumer O, Bader GD. *Cytoscape.js: a graph
> theory library for visualisation and analysis.* Bioinformatics. 2016.

### `vendor/bin/` — binários externos (não versionados)

O diretório `vendor/bin/` é uma escotilha para o usuário fornecer o binário do
**SAINTexpress** sem reconstruir a imagem Docker. Nenhum binário é versionado
neste repositório (ver `.gitignore`); quem o colocar lá está sujeito à licença do
próprio SAINTexpress.

---

## 2. Ferramentas de proteômica orquestradas (não redistribuídas)

A plataforma invoca estas ferramentas quando elas estão presentes no ambiente ou
na imagem de contêiner. **Elas não são redistribuídas por este repositório**:
cada uma é obtida da sua própria fonte, sob a sua própria licença e seus próprios
termos. Verifique a licença de cada uma antes de usar, em especial para uso
comercial — várias são livres apenas para uso acadêmico.

### Busca e quantificação (raw → proteína)

| Ferramenta | Licença / termos | Referência |
|---|---|---|
| **MaxQuant** | Gratuito, termos próprios (não-open-source) | Cox & Mann, *Nat Biotechnol* 2008 |
| **FragPipe / MSFragger** | MSFragger: licença acadêmica/não-comercial própria | Kong et al., *Nat Methods* 2017 |
| **DIA-NN** | Termos próprios (uso acadêmico gratuito; comercial sob licença) | Demichev et al., *Nat Methods* 2020 |

### Especificidade isca–presa

| Ferramenta | Licença / termos | Referência |
|---|---|---|
| **SAINTexpress** | Código-fonte distribuído pelos autores (SourceForge) | Teo et al., *J Proteomics* 2014; Choi et al., *Nat Methods* 2011 |
| **MiST** | Método publicado pelos autores | Verschueren et al. 2015; Jäger et al., *Nature* 2011 |

### Estatística quantitativa (R / Bioconductor)

| Ferramenta | Licença | Referência |
|---|---|---|
| **DEP** | Artistic-2.0 (Bioconductor) | Zhang et al., *Nat Protoc* 2018 |
| **limma** | GPL (≥2) (Bioconductor) | Ritchie et al., *NAR* 2015 |
| **MSstats** | Artistic-2.0 (Bioconductor) | Choi et al., *Bioinformatics* 2014 |
| **vsn** | Artistic-2.0 (Bioconductor) | Huber et al., *Bioinformatics* 2002 |

### Bancos, anotação e background

| Recurso | Licença / termos | Referência |
|---|---|---|
| **UniProt** | CC BY 4.0 | The UniProt Consortium, *NAR* |
| **STRING** v12.0 | CC BY 4.0 | Szklarczyk et al., *NAR* |
| **BioGRID** | MIT (dados), termos próprios | Oughtred et al., *Protein Sci* 2021 |
| **cRAP** | Global Proteome Machine (GPMDB) | — |
| **CRAPome** | Termos próprios | Mellacheruvu et al., *Nat Methods* 2013 |
| **g:Profiler** | Serviço web, termos próprios | Kolberg et al., *NAR* 2023 |

### GPU (opcional, suplementar)

| Ferramenta | Licença / termos | Referência |
|---|---|---|
| **MS2Rescore** | Apache-2.0 | Declercq et al. |
| **AlphaPeptDeep** | Apache-2.0 | Zeng et al., *Nat Commun* 2022 |
| **AlphaFold2 / AlphaFold-Multimer** | Código Apache-2.0; pesos CC BY 4.0, condições próprias | Jumper et al., *Nature* 2021; Evans et al. |
| **ColabFold** | MIT | Mirdita et al., *Nat Methods* 2022 |
| **ESM-2** | MIT | Lin et al., *Science* 2023 |

---

## 3. Dependências de software (Python, R, contêineres)

As dependências declaradas em `pyproject.toml`, `requirements.txt`,
`requirements-gpu.txt` e `environment.yml` — entre elas NumPy, pandas, SciPy,
NetworkX, Matplotlib, PyYAML, requests, Flask, Gunicorn, RQ, redis-py,
pyteomics, PyArrow, PyTorch e Transformers — e as imagens-base usadas em
`docker/` (Python, Redis, imagens CUDA da NVIDIA, R/Bioconductor) permanecem sob
as suas próprias licenças, resolvidas na instalação. Nenhuma delas é
redistribuída por este repositório.

---

## 4. Como citar as ferramentas num manuscrito

As referências completas, por etapa do pipeline, estão em
`docs/METODOLOGIA.md`. Cada corrida grava em `manifest.json` as versões das
ferramentas efetivamente usadas — use esse arquivo como fonte para a seção de
métodos, em vez de copiar versões à mão.

Se algum crédito aqui estiver incorreto ou faltando, abra uma *issue*: a
correção é bem-vinda.
