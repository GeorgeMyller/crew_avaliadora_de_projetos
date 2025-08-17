# crewavaliadora

Projeto: ferramentas de análise de codebase e relatórios automatizados usando CrewAI + Google Gemini.

Descrição
---------
Este repositório contém scripts que geram análises detalhadas (arquitetura, qualidade, documentação, negócio, compliance e IA) a partir de um relatório base ou examinando a codebase arquivo-a-arquivo. O fluxo principal usa a API do Google Gemini para gerar conteúdo via LLMs.

Principais scripts
------------------
- `avaliacao_gemini.py`: versão simplificada que carrega um relatório (`relatorio_codebase_turbinado.md`) e gera um relatório final usando Google Gemini 2.5 Flash.
- `crew_avaliacao_completa.py`: fluxo mais completo plug-and-play que usa abstrações CrewAI (Agents/Tasks/Crew) para produzir análises por arquivo e uma consolidação final.

Requisitos
----------
- Python >= 3.12 (definido em `pyproject.toml`)
- Dependências listadas em `pyproject.toml`:
  - crewai>=0.157.0
  - crewai-tools>=0.60.0
  - google-generativeai>=0.8.5
  - python-dotenv>=1.1.1

Configuração (rápida)
---------------------
1. Crie um ambiente virtual e ative-o (recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale dependências (pip):

```bash
pip install -r requirements.txt  # se criar um requirements.txt
# ou instale diretamente conforme pyproject.toml
pip install crewai crewai-tools google-generativeai python-dotenv
```

3. Configure a variável de ambiente para a API do Gemini criando um arquivo `.env` na raiz do projeto com:

```env
GEMINI_API_KEY=seu_segredo_aqui
# Exemplo (NÃO comente a chave no repositório):
# GEMINI_API_KEY=ya29.a0AfH6SMA...
```

Uso
---

Executar a análise simplificada (avaliacao_gemini.py):

```bash
python avaliacao_gemini.py
```

Executar a avaliação completa (crew_avaliacao_completa.py):

```bash
python crew_avaliacao_completa.py
```

Observações
-----------
- Os scripts esperam encontrar um arquivo `relatorio_codebase_turbinado.md` na raiz para o fluxo padrão. Se não existir, o `crew_avaliacao_completa.py` irá varrer a codebase e gerar relatórios por arquivo na pasta `reports_by_file/`.
- Custos de API: chamadas ao Google Gemini podem gerar custos — use limites (`max_files`) em `crew_avaliacao_completa.py` durante testes.
- Segurança: nunca commite o `.env` com chaves reais. O `.gitignore` do projeto já ignora `.env`.

Contribuindo
------------
- Sinta-se livre para abrir issues e PRs. Para desenvolvimento local, mantenha chaves e segredos fora do repositório.

Licença
-------
Adicione informações de licença conforme necessário.
