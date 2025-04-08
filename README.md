# File Analyzer Agent

Um agente CLI para análise de arquivos usando modelos locais de linguagem.

## Instalação

```bash
pip install file-analyzer-agent
```

## Uso

O agente pode ser usado de duas formas:

1. Análise direta de arquivos:
```bash
file-analyzer analyze /caminho/para/arquivos --model mistral
```

2. Indexação de arquivos para análise posterior:
```bash
file-analyzer index /caminho/para/arquivos
```

### Opções disponíveis

- `--model`: Modelo a ser usado (padrão: mistral)
- `--index-path`: Caminho para salvar/carregar o índice (padrão: ./index)
- `--verbose`: Modo verboso para mais detalhes

## Exemplos

1. Analisar arquivos de log:
```bash
file-analyzer analyze /var/log --model mistral
```

2. Indexar documentos para análise posterior:
```bash
file-analyzer index /documentos --index-path ./meu_indice
```

## Requisitos

- Python 3.8+
- Ollama instalado e rodando localmente
- Dependências Python (instaladas automaticamente via pip)

## Licença

MIT 