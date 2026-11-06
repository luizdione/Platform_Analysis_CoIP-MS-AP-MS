# Sequencias das iscas (FASTA)

Quando a isca e **exogena** ao proteoma do hospedeiro, ela precisa entrar no
FASTA de busca (`search_db.fasta`) para ser quantificada como controle positivo.
Coloque aqui **um FASTA por isca**, com o nome apontado em `config/baits.yaml`.

Os FASTA **nao sao versionados** (ver `.gitignore`): a sequencia da sua isca e
sua. Este diretorio sobe vazio, so com este README.

Os comandos abaixo baixam as duas iscas do **exemplo publico** que acompanha
`config/baits.yaml`. Troque os acessos pelos da sua Co-IP.

## 1. Nucleoproteina N do SARS-CoV-2 (`NCAP_SARS2`) — UniProt P0DTC9

Exemplo de isca exogena ao hospedeiro. Baixe a sequencia canonica exata (nao
digite a mao):

```bash
curl -L "https://rest.uniprot.org/uniprotkb/P0DTC9.fasta" -o NCAP_SARS2.fasta
```

## 2. p53 humana (`TP53_HUMAN`) — UniProt P04637

Exemplo de isca de outra especie que **tem** ortologo murino (`Trp53`, P02340);
o ortologo e mantido distinto da isca pelo pipeline.

```bash
curl -L "https://rest.uniprot.org/uniprotkb/P04637.fasta" -o TP53_HUMAN.fasta
```

## Isca sem acesso publico (construto, isolado proprio)

Se a sua isca nao tem acesso no UniProt/GenBank — um construto, uma etiqueta, ou
o isolado do seu laboratorio — grave o FASTA a mao com um cabecalho que combine
com o `search_db_header` declarado em `baits.yaml`:

```
>bait|MINHA_ISCA|descricao curta da isca
MSEQ...   (a sequencia de aminoacidos)
```

Deixe `uniprot_accession: null` nessa entrada do `baits.yaml`.

## Verificacao

Depois de adicionar os arquivos:

```bash
bonder baits check
```

Isso valida as iscas e gera `data/search_db.fasta` (proteoma do hospedeiro +
contaminantes + iscas) para a busca. Sem os FASTAs, o comando apenas avisa
(nao quebra) e o restante do pipeline continua funcionando a partir de uma
saida de busca ja pronta.
