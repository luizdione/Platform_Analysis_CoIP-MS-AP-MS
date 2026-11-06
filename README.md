# Platform_Analysis_CoIP-MS-AP-MS

**Plataforma local (navegador + Docker) para análise de CoIP-MS / AP-MS e
identificação de parceiros de interação no proteoma de camundongo**
(*Mus musculus*, taxid 10090).

A plataforma **não reinventa a roda**: ela **orquestra ferramentas consagradas e
revisadas por pares** da comunidade de proteômica dentro de contêineres
reprodutíveis, com um dashboard Flask acessível em `http://localhost:8080`.
Resultado: rigor e reprodutibilidade compatíveis com publicação, rodando **no seu
servidor**, sem software fechado/pago.

> **Este repositório não contém dados de experimento.** Os arquivos em `config/`
> são um **exemplo público** montado só com sequências de referência do UniProt,
> para servir de modelo. Os seus dados ficam na sua máquina, numa pasta que você
> aponta (ver [Onde ficam os seus dados](#onde-ficam-os-seus-dados)) — e que não é
> versionada nem entra na imagem de contêiner.

> O pacote Python e os módulos se chamam `bonder`, nome interno do projeto. O nome
> da plataforma é o do repositório.

---

## Por que open source tem rigor para publicar?

A proteômica de interação publicada em alto impacto roda majoritariamente em
software **aberto**. O que confere publicabilidade não é a marca, e sim: usar
métodos **validados e citáveis**, controle de **FDR** adequado, desenho com
réplicas + controles, e **depósito dos dados brutos** (PRIDE/ProteomeXchange).
O interactoma host–patógeno do SARS-CoV-2 (Gordon et al., *Nature* 2020) e o
BioPlex foram feitos com estas mesmas ferramentas.

## Ferramentas orquestradas (todas com artigo publicado)

| Etapa | Ferramenta (aberta) |
|---|---|
| Busca/quantificação (raw → proteína) | **MaxQuant** (DDA) · **FragPipe/MSFragger** · **DIA-NN** (DIA, GPU) |
| **Especificidade isca–presa** | **SAINTexpress** (todas as iscas) · **MiST** (host–patógeno, iscas exógenas) |
| Quantitativo diferencial | **DEP / limma / MSstats** (R/Bioconductor) |
| Background / contaminantes | **CRAPome** interno (controles) + cRAP |
| Anotação / redes | **UniProt, STRING, BioGRID**, GO (g:Profiler), Cytoscape |
| GPU (NVIDIA, opcional) | **DIA-NN**, **MS2Rescore + AlphaPeptDeep** (rescoring), **AlphaFold2-Multimer/ColabFold** (validação estrutural) |

> ESM2 (embeddings) entra apenas como **priorização exploratória suplementar**,
> nunca como base do escore de confiança que vai para a figura principal.

Licenças e citações de cada uma: [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)
e [`docs/METODOLOGIA.md`](docs/METODOLOGIA.md).

## Arquitetura

```
 navegador (localhost:8080)
        |
   [web] Flask ---- fila (Redis/RQ) ----> [worker]
                                             |
   io -> db -> scoring(SAINT/MiST) -> stats(DEP/limma R) -> annotate -> pipeline -> relatorio
                                             |
                        [gpu] (opcional) DIA-NN / rescoring / AlphaFold / ESM2
```

- **Fluxo unidirecional** `io -> db -> scoring/stats -> gpu -> pipeline -> web`.
- O **núcleo científico é testável em CPU**, sem GPU e sem R (ver `tests/`).
- Etapas cujas ferramentas externas faltam são **puladas com registro no
  manifesto** — o pipeline nunca finge cobertura que não teve.

---

## Como rodar

### Opção 1 — imagem pronta do GHCR (sem build)

```bash
docker pull ghcr.io/luizdione/platform_analysis_coip-ms-ap-ms:latest
```

Rode apontando a sua pasta de dados para `/inputs` (nada é enviado para fora da
sua máquina):

```bash
docker run --rm -p 8080:8080 -v "/caminho/para/seus/dados:/inputs:ro" ghcr.io/luizdione/platform_analysis_coip-ms-ap-ms:latest
```

No PowerShell (Windows), use o caminho da sua pasta:

```powershell
docker run --rm -p 8080:8080 -v "C:\meus_dados\coip:/inputs:ro" ghcr.io/luizdione/platform_analysis_coip-ms-ap-ms:latest
```

Depois abra `http://localhost:8080`. Essa imagem sobe o dashboard sozinho (fila
em thread, sem Redis) — suficiente para uso individual. Para a pilha completa com
Redis e worker separado, use a opção 2.

### Opção 2 — compose a partir do código (pilha completa)

```bash
# CPU (funciona em qualquer máquina):
docker compose -f docker/docker-compose.yml up --build
#    -> abra http://localhost:8080

# Com GPU NVIDIA (requer NVIDIA Container Toolkit):
docker compose -f docker/docker-compose.yml -f docker/docker-compose.gpu.yml up --build
```

Coloque suas saídas de busca em `./inputs`. No dashboard: informe o caminho
(`/inputs/proteinGroups.txt`), escolha o contraste (isca vs controle) e rode.
O **motor e o modo de aquisição (DDA/DIA) são detectados automaticamente**.

### Opção 3 — sem Docker (conda)

```bash
conda env create -f environment.yml      # cria o env 'bonder'
conda activate bonder
pip install -e .
python -m bonder.cli list-contrasts
python -m bonder.web.app                 # dashboard em 127.0.0.1:8080
```

Para instalar num ambiente que você já tem:
`conda env update -n SEU_ENV -f environment.yml`.

No Windows há ainda `run.ps1` (Docker, CPU), `run-gpu.ps1` (Docker, GPU) e
`iniciar_bonder.ps1` (sem Docker). Se o `python` do PATH não é o que tem as
dependências, defina `BONDER_PYTHON` com o caminho completo do `python.exe`.

---

## Onde ficam os seus dados

A plataforma lê e escreve **só onde você mandar**. Nada sai da sua máquina.

| O quê | Variável de ambiente | Padrão |
|---|---|---|
| Saídas de busca que você vai analisar | `BONDER_INPUTS_DIR` | `./inputs` (no Docker: montada em `/inputs`) |
| Bancos de referência baixados (UniProt/STRING/BioGRID/cRAP) | `BONDER_DATA_ROOT` | `./data` (no Docker: `/data`, volume `bonder-data`) |
| Resultados das corridas | `BONDER_RUNS_DIR` | `./runs` (no Docker: `/runs`, volume `bonder-runs`) |
| Arquivos de configuração (os YAML) | `BONDER_CONFIG_DIR` | `./config` |

```bash
export BONDER_DATA_ROOT=/meu/disco/coip/data
export BONDER_RUNS_DIR=/meu/disco/coip/runs
export BONDER_INPUTS_DIR=/meu/disco/coip/inputs
```

Outras duas variáveis úteis: `BONDER_OFFLINE=1` usa só o cache de bancos já
baixado (nenhuma chamada de rede), e `BONDER_REDIS_URL` liga a fila RQ/Redis —
sem ela, a corrida roda numa thread do próprio processo, o que basta para uso
individual.

Num `docker run` simples, `/data` e `/runs` ficam **dentro** do contêiner e se
perdem ao removê-lo. Para guardar os resultados, monte volumes:

```bash
docker run --rm -p 8080:8080 \
  -v "/caminho/para/seus/dados:/inputs:ro" \
  -v "coip-data:/data" -v "coip-runs:/runs" \
  ghcr.io/luizdione/platform_analysis_coip-ms-ap-ms:latest
```

`data/`, `runs/`, `inputs/` e `config/sequences/*.fasta` estão no `.gitignore` e
no `.dockerignore`: **não são versionados e não entram na imagem**. Os seus dados
de entrada e os resultados pertencem a quem os gerou.

## Configuração (declarativa)

Os quatro arquivos abaixo definem a análise. Os dois primeiros vêm com um
**exemplo público** que você deve substituir:

- `config/baits.yaml` — as iscas. O exemplo cobre os dois casos que o pipeline
  trata de forma diferente: isca **exógena** ao hospedeiro, sem ortólogo murino
  (host–patógeno), e isca de outra espécie **com** ortólogo murino, mantido
  **distinto** da isca.
- `config/samples.yaml` — amostras, réplicas e **contrastes** isca-vs-controle.
  Os nomes precisam casar com as colunas da sua saída de busca.
- `config/databases.yaml` — bancos murinos **fixados por versão** + checksums.
- `config/gpu.yaml` — device, `gpu_gate` e toggles das etapas de GPU.
- `config/sequences/` — FASTA das iscas (veja o README de lá). Não versionado.

## CLI

```bash
bonder db sync            # baixa/verifica UniProt/STRING/contaminantes (murinos)
bonder baits check        # valida iscas e monta o search_db.fasta
bonder qc --input F       # resumo de QC de uma saída de busca
bonder run --input F --contrast NCAP_vs_CTRL
```

## Reprodutibilidade

Cada corrida grava `manifest.json` (versões, ferramentas disponíveis, device,
procedência, passos) e `results.json`. Bancos são **fixados por versão** e
verificados por sha256. Ver [`docs/REPRODUTIBILIDADE.md`](docs/REPRODUTIBILIDADE.md)
e o guia de depósito no PRIDE.

## Testes

```bash
python -m pytest -q     # núcleo CPU (IO, SAINT-format, pipeline e2e, web jobs)
```

## Requisitos

- **Mínimo:** Docker (Desktop no Windows/macOS, Engine no Linux). Nada mais.
- **Sem Docker:** Python 3.10+ (testado em 3.11) e conda/miniforge.
- **GPU (opcional):** placa NVIDIA com CUDA 12.4, driver compatível e NVIDIA
  Container Toolkit. Toda etapa de GPU tem **fallback CPU garantido**.
- **R (opcional):** fornecido pela imagem de análise; sem ele, o quantitativo
  diferencial é pulado com registro no manifesto.

Desenvolvido e testado em Windows 11 + WSL2 e em Linux.

---

## Licença

**A licença mudou na versão 1.0.0.** Ver [`LICENSE`](LICENSE) para o texto que
vale.

| Uso | Condição |
|---|---|
| **Pessoal** (na sua máquina, sem fim econômico) | Livre, não precisa avisar |
| **Ensino** (aulas, disciplinas, treinamentos, trabalho de aluno) | Livre, não precisa avisar |
| **Pesquisa** (gerar/analisar dado para tese, artigo, pré-print, pôster, projeto) | **Só com autorização prévia do autor, por e-mail:** luiz.melo@ifrj.edu.br |
| **Comercial** (serviço remunerado, consultoria, SaaS, uso empresarial) | Proibido — procure o autor para licença específica |
| **Redistribuir, modificar, criar obra derivada** | Proibido sem autorização escrita |

Executar a plataforma apenas para conhecê-la ou avaliá-la, sem gerar resultado de
pesquisa, conta como uso pessoal e **não** precisa de autorização.

### Sobre a licença MIT anterior

Até a versão 1.0.0 esta plataforma foi publicada sob **MIT**. A licença nova vale
**desta versão em diante** e **não revoga a MIT para o que já foi publicado**:
quem obteve uma cópia enquanto ela estava sob MIT mantém, sobre **aquela cópia**,
todos os direitos que a MIT concedeu — inclusive usar, modificar e redistribuir.
Uma licença já concedida não se retira.

### Terceiros

As ferramentas orquestradas e as bibliotecas incluídas em
`bonder/web/static/vendor/` (**Cytoscape.js**, **marked** — ambas MIT) mantêm as
suas próprias licenças, que **prevalecem** sobre esta quanto a elas. Ver
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Como citar

Ver [`CITATION.cff`](CITATION.cff). Em trabalho de pesquisa autorizado, cite a
plataforma com nome, versão e URL, e cite também as ferramentas efetivamente
usadas — as versões de cada corrida estão no `manifest.json` dela.

> De-Melo, L.D.B. *Platform_Analysis_CoIP-MS-AP-MS* (v1.0.0). Instituto Federal
> de Educação, Ciência e Tecnologia do Rio de Janeiro (IFRJ), 2026.
> https://github.com/luizdione/Platform_Analysis_CoIP-MS-AP-MS

## Autor

**Luiz Dione Barbosa De-Melo** (De-Melo, L.D.B.)
Instituto Federal de Educação, Ciência e Tecnologia do Rio de Janeiro (IFRJ),
Rio de Janeiro, Brasil
ORCID [0000-0003-2445-9943](https://orcid.org/0000-0003-2445-9943) ·
luiz.melo@ifrj.edu.br
