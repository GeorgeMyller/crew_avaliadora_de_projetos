# 🤖 CrewAI Codebase Evaluator | Avaliador de Codebase CrewAI

**English** | [Português](#português)

Automated codebase analysis and reporting tools using CrewAI + Google Gemini.

## 📋 Description

This repository contains scripts that generate detailed analyses (architecture, quality, documentation, business, compliance, and AI) from a base report or by examining the codebase file-by-file. The main workflow uses Google Gemini API to generate content via LLMs.

## 🚀 Main Scripts

- **`avaliacao_gemini.py`**: Simplified version that loads a report (`relatorio_codebase_turbinado.md`) and generates a final report using Google Gemini 2.5 Flash.
- **`crew_avaliacao_completa.py`**: Complete plug-and-play workflow that uses CrewAI abstractions (Agents/Tasks/Crew) to produce per-file analyses and a final consolidation.
- **`github_analyzer.py`**: Automated GitHub repository analyzer that clones and analyzes public repositories.
- **`limpar_relatorios.py`**: Cleanup script to remove old and inconsistent reports.

## 🛠️ Requirements

- Python >= 3.12 (defined in `pyproject.toml`)
- Dependencies listed in `pyproject.toml`:
  - `crewai>=0.157.0`
  - `crewai-tools>=0.60.0`
  - `google-generativeai>=0.8.5`
  - `python-dotenv>=1.1.1`

## ⚡ Quick Setup

### 1. Create and activate virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install dependencies:

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install crewai crewai-tools google-generativeai python-dotenv
```

### 3. Configure environment variables:

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
# Example (DO NOT commit real keys):
# GEMINI_API_KEY=AIzaSyC...
```

## 🎯 Usage

### Basic Analysis

**Simplified analysis** (avaliacao_gemini.py):
```bash
python avaliacao_gemini.py
```

**Complete evaluation** (crew_avaliacao_completa.py):
```bash
python crew_avaliacao_completa.py
```

### Analyzing Specific Folders

**Current folder:**
```bash
python crew_avaliacao_completa.py
```

**Specific folder (relative path):**
```bash
python crew_avaliacao_completa.py --path ./my-project
python crew_avaliacao_completa.py --path ../other-project
```

**Specific folder (absolute path):**
```bash
python crew_avaliacao_completa.py --path "/Users/user/projects/my-app"
python crew_avaliacao_completa.py --path "/Volumes/EXTERNAL-HD/workspace/project-x"
```

**Limit number of files (useful for testing):**
```bash
python crew_avaliacao_completa.py --path ./large-project --max-files 10
```

**Control maximum file size:**
```bash
python crew_avaliacao_completa.py --path ./project --max-size 1048576  # 1MB
```

### 🐙 GitHub Repository Analysis

**Basic analysis:**
```bash
python github_analyzer.py https://github.com/facebook/react
```

**Limited analysis (cost control):**
```bash
python github_analyzer.py https://github.com/vercel/next.js --max-files 30
```

**Keep clone for later analysis:**
```bash
python github_analyzer.py https://github.com/microsoft/vscode --keep-clone
```

### 🧹 Cleanup Old Reports

```bash
python limpar_relatorios.py
```

## 📊 Output Structure (v2.0)

Each execution creates isolated outputs with consistent timestamps:

```
project-folder/
├── reports_by_file_YYYYMMDD_HHMMSS/    # Individual file reports
│   ├── file1.py_YYYYMMDD_HHMMSS.md
│   ├── file2.js_YYYYMMDD_HHMMSS.md
│   └── ...
├── relatorio_final_startup_YYYYMMDD_HHMMSS.md  # Consolidated report (LLM)
├── relatorio_final_concat_YYYYMMDD_HHMMSS.md   # Literal concatenation
└── metadata_analise_YYYYMMDD_HHMMSS.json       # Execution metadata
```

## 💡 Important Notes

- **First run**: Use `--max-files 5` to test if everything is working
- **Large projects**: Gradually increase `--max-files` as needed
- **API costs**: Each file generates a Gemini API call - be mindful of costs
- **Execution time**: Large projects may take several minutes
- **Security**: Never commit `.env` with real keys. The project `.gitignore` already ignores `.env`

## 🔧 Project Types Examples

**Node.js project:**
```bash
python crew_avaliacao_completa.py --path ./my-node-app --max-files 20
```

**Python/Django project:**
```bash
python crew_avaliacao_completa.py --path ./django-project --max-files 30
```

**Large monorepo (limited analysis):**
```bash
python crew_avaliacao_completa.py --path ./monorepo --max-files 50 --max-size 1000000
```

## 🤝 Contributing

Feel free to open issues and PRs. For local development, keep keys and secrets out of the repository.

## 📄 License

Add license information as needed.

---

# Português

**[English](#-crewai-codebase-evaluator--avaliador-de-codebase-crewai)** | Português

Ferramentas de análise de codebase e relatórios automatizados usando CrewAI + Google Gemini.

## 📋 Descrição

Este repositório contém scripts que geram análises detalhadas (arquitetura, qualidade, documentação, negócio, compliance e IA) a partir de um relatório base ou examinando a codebase arquivo-a-arquivo. O fluxo principal usa a API do Google Gemini para gerar conteúdo via LLMs.

## 🚀 Scripts Principais

- **`avaliacao_gemini.py`**: Versão simplificada que carrega um relatório (`relatorio_codebase_turbinado.md`) e gera um relatório final usando Google Gemini 2.5 Flash.
- **`crew_avaliacao_completa.py`**: Fluxo mais completo plug-and-play que usa abstrações CrewAI (Agents/Tasks/Crew) para produzir análises por arquivo e uma consolidação final.
- **`github_analyzer.py`**: Analisador automatizado de repositórios GitHub que clona e analisa repositórios públicos.
- **`limpar_relatorios.py`**: Script de limpeza para remover relatórios antigos e inconsistentes.

## 🛠️ Requisitos

- Python >= 3.12 (definido em `pyproject.toml`)
- Dependências listadas em `pyproject.toml`:
  - `crewai>=0.157.0`
  - `crewai-tools>=0.60.0`
  - `google-generativeai>=0.8.5`
  - `python-dotenv>=1.1.1`

## ⚡ Configuração Rápida

### 1. Crie e ative um ambiente virtual (recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

### 2. Instale as dependências:

```bash
# Usando uv (recomendado)
uv sync

# Ou usando pip
pip install crewai crewai-tools google-generativeai python-dotenv
```

### 3. Configure as variáveis de ambiente:

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_api_aqui
# Exemplo (NÃO commite chaves reais):
# GEMINI_API_KEY=AIzaSyC...
```

## 🎯 Uso

### Análise Básica

**Análise simplificada** (avaliacao_gemini.py):
```bash
python avaliacao_gemini.py
```

**Avaliação completa** (crew_avaliacao_completa.py):
```bash
python crew_avaliacao_completa.py
```

### Analisando Pastas Específicas

**Pasta atual:**
```bash
python crew_avaliacao_completa.py
```

**Pasta específica (caminho relativo):**
```bash
python crew_avaliacao_completa.py --path ./meu-projeto
python crew_avaliacao_completa.py --path ../outro-projeto
```

**Pasta específica (caminho absoluto):**
```bash
python crew_avaliacao_completa.py --path "/Users/usuario/projetos/meu-app"
python crew_avaliacao_completa.py --path "/Volumes/HD-EXTERNO/workspace/projeto-x"
```

**Limitar número de arquivos (útil para testes):**
```bash
python crew_avaliacao_completa.py --path ./projeto-grande --max-files 10
```

**Controlar tamanho máximo dos arquivos:**
```bash
python crew_avaliacao_completa.py --path ./projeto --max-size 1048576  # 1MB
```

### 🐙 Análise de Repositórios GitHub

**Análise básica:**
```bash
python github_analyzer.py https://github.com/facebook/react
```

**Análise limitada (controle de custos):**
```bash
python github_analyzer.py https://github.com/vercel/next.js --max-files 30
```

**Manter clone para análise posterior:**
```bash
python github_analyzer.py https://github.com/microsoft/vscode --keep-clone
```

### 🧹 Limpeza de Relatórios Antigos

```bash
python limpar_relatorios.py
```

## 📊 Estrutura de Saída (v2.0)

Cada execução cria saídas isoladas com timestamps consistentes:

```
pasta-do-projeto/
├── reports_by_file_YYYYMMDD_HHMMSS/    # Relatórios individuais
│   ├── arquivo1.py_YYYYMMDD_HHMMSS.md
│   ├── arquivo2.js_YYYYMMDD_HHMMSS.md
│   └── ...
├── relatorio_final_startup_YYYYMMDD_HHMMSS.md  # Relatório consolidado (LLM)
├── relatorio_final_concat_YYYYMMDD_HHMMSS.md   # Concatenação literal
└── metadata_analise_YYYYMMDD_HHMMSS.json       # Metadados da execução
```

## 💡 Observações Importantes

- **Primeira execução**: Use `--max-files 5` para testar se está funcionando
- **Projetos grandes**: Aumente gradualmente o `--max-files` conforme necessário
- **Custos de API**: Cada arquivo gera uma chamada para o Gemini - cuidado com custos
- **Tempo de execução**: Projetos grandes podem demorar vários minutos
- **Segurança**: Nunca commite o `.env` com chaves reais. O `.gitignore` do projeto já ignora `.env`

## 🔧 Exemplos para Diferentes Tipos de Projeto

**Projeto Node.js:**
```bash
python crew_avaliacao_completa.py --path ./meu-app-node --max-files 20
```

**Projeto Python/Django:**
```bash
python crew_avaliacao_completa.py --path ./projeto-django --max-files 30
```

**Monorepo grande (análise limitada):**
```bash
python crew_avaliacao_completa.py --path ./monorepo --max-files 50 --max-size 1000000
```

## 🤝 Contribuindo

Sinta-se livre para abrir issues e PRs. Para desenvolvimento local, mantenha chaves e segredos fora do repositório.

## 📄 Licença

Adicione informações de licença conforme necessário.
