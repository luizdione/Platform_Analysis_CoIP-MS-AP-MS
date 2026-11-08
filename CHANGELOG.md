# Changelog

Mudanças relevantes da plataforma **Platform_Analysis_CoIP-MS-AP-MS**. Formato
baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versionamento [SemVer](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-11-06

Primeira versão publicada como **plataforma científica aberta**. O repositório
passa a conter apenas a plataforma: nenhum dado de experimento, nenhum alvo real
e nenhuma anotação de trabalho.

### Alterado — LICENÇA (leia antes de atualizar)

- A licença mudou de **MIT** para a **licença de uso própria** em `LICENSE`:
  uso pessoal e de ensino livres, **uso em pesquisa somente com autorização
  prévia do autor por e-mail** (luiz.melo@ifrj.edu.br), uso comercial proibido,
  redistribuição e obras derivadas proibidas.
- **A mudança vale desta versão em diante.** Ela **não revoga a MIT** para o que
  já havia sido publicado: quem obteve uma cópia enquanto o programa estava sob
  MIT mantém, sobre **aquela cópia**, todos os direitos que a MIT lhe concedeu —
  inclusive usar, modificar e redistribuir. Uma licença já concedida não se
  retira. Versões anteriores a esta continuam MIT para quem as recebeu.
- Adicionado `THIRD_PARTY_NOTICES.md`: as duas bibliotecas JavaScript incluídas
  em `bonder/web/static/vendor/` (**Cytoscape.js** 3.30.2 e **marked** 15.0.12,
  ambas MIT) e as ferramentas de proteômica orquestradas, cada uma com a sua
  própria licença — que prevalece sobre a desta plataforma quanto a ela.
- Adicionado `CITATION.cff` (De-Melo, L.D.B.; ORCID 0000-0003-2445-9943; IFRJ).

### Alterado — configuração passa a ser exemplo público

- `config/baits.yaml` e `config/samples.yaml` agora trazem um **exemplo público e
  mínimo**, montado só com sequências de referência do UniProt, para servir de
  modelo ao usuário preencher. O exemplo cobre os dois casos que o pipeline trata
  de forma diferente: isca **exógena** ao hospedeiro sem ortólogo murino
  (host–patógeno, nucleoproteína N do SARS-CoV-2, P0DTC9) e isca de outra espécie
  **com** ortólogo murino mantido distinto (p53 humana, P04637, ortólogo `Trp53`
  P02340). Os cabeçalhos dos arquivos dizem explicitamente que são exemplo.
- `config/sequences/README.md` reescrito: como baixar os FASTA do exemplo e como
  declarar uma isca sem acesso público (construto, etiqueta, isolado próprio).
  Os FASTA continuam fora do versionamento.
- `config/gpu.yaml` deixou de assumir um modelo de placa específico; a
  `min_capability` e o teto de resíduos são parâmetros do usuário.

### Alterado — portabilidade

- `iniciar_bonder.ps1` não traz mais caminho de máquina nenhum: usa
  `$env:BONDER_PYTHON` quando definida e, na falta, o `python` do PATH, **com
  mensagem de erro explícita** dizendo o que definir quando nenhum dos dois
  existe.
- O ambiente conda documentado passou a ser o do próprio projeto (`bonder`, em
  `environment.yml`), em vez de um ambiente pessoal: `conda env create -f
  environment.yml`.
- Documentação e scripts deixaram de citar um modelo de GPU específico; a GPU é
  descrita por capacidade (NVIDIA CUDA, fallback CPU garantido).
- `.dockerignore` endurecido: a imagem de contêiner não carrega dados de entrada,
  bancos baixados, saídas de corrida, FASTA de iscas, credenciais nem anotação de
  trabalho.

### Removido

- Toda a anotação de trabalho interna do autor (memória de projeto, instruções de
  sessão, decisões, tarefas e sessões arquivadas) e os alvos e amostras reais dos
  experimentos dele. **Este repositório não contém dados de pesquisa.**
- O histórico anterior do repositório foi arquivado em repositório privado; esta
  versão inicia um histórico novo, para que o conteúdo removido não continue
  acessível via commits antigos.

### Adicionado

- Imagem de contêiner pública no **GHCR**, vinculada a este repositório, para
  rodar a plataforma sem build local (ver o README).

---

## Histórico anterior (resumo técnico)

As versões abaixo circularam sob licença MIT. O resumo é mantido para dar
contexto ao código; a descrição dos sistemas biológicos que o autor estudava foi
retirada, por não fazer parte da plataforma.

### [0.3.0] - 2026-07

- Exportador de resultados como **página HTML estática**, para publicar o
  relatório de uma corrida em qualquer hospedagem (as análises continuam rodando
  em localhost).
- Base de contaminantes **cRAP** a partir da fonte pública, com checksum.
- Dashboard: seletor de arquivos de entrada, rede **STRING/BioGRID** e assets
  servidos localmente (funciona offline).
- Aba **Ajuda e Tutoriais**: serve os documentos `.md` (tutoriais, metodologia,
  reprodutibilidade) e a licença, renderizados no navegador. Endpoints
  `GET /api/docs` e `GET /api/docs/<id>`.

### [0.2.0] - 2026-07

- Digestão in silico do proteoma murino e metodologia subtrativa.

### [0.1.0] - 2026-07-02

Primeira versão da plataforma CoIP-MS / AP-MS.

- **Ingesta (`bonder.io`)**: parsers MaxQuant/DIA-NN/FragPipe/genérico para um
  `MSDataset` unificado; detecção automática de motor e de aquisição (DDA/DIA);
  ausente = NaN (nunca 0); chave por acesso UniProt líder; iscas exógenas
  marcadas e mantidas distintas do ortólogo do hospedeiro.
- **Especificidade (`bonder.scoring`)**: formatação de entrada + wrappers de
  **SAINTexpress** (todas as iscas) e **MiST** (iscas exógenas, host–patógeno).
- **Quantitativo (`bonder.stats`)**: wrappers R para **DEP/limma/MSstats**
  (Bioconductor) via Rscript; QC em Python (sem valor inferencial). MaxLFQ do
  DIA-NN nunca é re-normalizado.
- **Bancos (`bonder.db`)**: UniProt/STRING/BioGRID/cRAP murinos com cache
  reprodutível (checksum, modo offline) + montagem do `search_db.fasta`.
- **GPU (`bonder.gpu`)**: DIA-NN / MS2Rescore / AlphaPeptDeep / AlphaFold e ESM2
  (suplementar), com fallback CPU e `gpu_gate` cooperativo.
- **Pipeline + Web**: orquestrador, relatório (tabela/volcano/rede), dashboard
  Flask + fila RQ/Redis (fallback thread).
- **Docker**: imagem de análise (Python + R + SAINT) e imagem GPU (CUDA 12.4 +
  torch); `docker compose` CPU por padrão + overlay de GPU.
- **Aba Manutenção**: auditoria (deps, ferramentas, R, GPU, config, bancos,
  caminhos, corridas) + autoteste do pipeline em dados sintéticos.
- Documentação PT-BR (metodologia com citações, como rodar, reprodutibilidade) e
  testes do núcleo (CPU, sem GPU/R).

#### Corrigido ao longo da série 0.x

- `saint` não existe como pacote conda: removido do env; SAINTexpress passou a
  ser compilado do código-fonte no Dockerfile, best-effort e não-fatal.
- Mapeamento de peptídeos/q-value do DIA-NN pela `Protein.Group` original.
- Fallback de gene no SAINT gravava o literal `nan` (NaN é truthy) → cai para o
  acesso.
- Dashboard: coluna log2fc vazia sem R → usa `log2fc_descriptive`; o polling
  agora para em status terminal (done/error).
- CI: dependência `requests` faltando no job de testes.
