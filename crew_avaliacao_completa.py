#!/usr/bin/env python3
"""
🚀 CrewAI Avaliação Completa de Codebase
========================================

Sistema plug-and-play para análise profissional de codebase usando Gemini 2.5 Flash.
Gera relatórios ultra-profissionais para devs juniores e seniores.

Fluxo: Codebase → Script Python → Relatório → CrewAI → Relatório Ultra-Profissional
"""

from crewai import Agent, Task, Crew, Process
try:
    import crewai_tools
    HAVE_CREWAI_TOOLS = True
except Exception:
    crewai_tools = None
    HAVE_CREWAI_TOOLS = False
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

class CodebaseAnalysisCrew:
    """
    🤝 CrewAI para Avaliação Completa de Codebase
    
    Roles especializados:
    📐 Arquiteto de Software
    🧪 Engenheiro de Qualidade  
    📄 Documentador Técnico
    🚀 Product Manager
    ⚖️ Especialista Legal
    🤖 Engenheiro de IA
    """
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        """Inicializa a crew com configuração Gemini 2.5 Flash"""
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("❌ GEMINI_API_KEY não encontrada! Configure no .env ou passe como parâmetro")
        
        # Remove espaços em branco da API key se houver
        self.gemini_api_key = self.gemini_api_key.strip()
        
        logger.info(f"✅ GEMINI_API_KEY carregada: {self.gemini_api_key[:10]}...")
        
        # Set environment variables for CrewAI's built-in LLM handling
        # Following the pattern from latest_ai_development example
        os.environ["GEMINI_API_KEY"] = self.gemini_api_key
        if "MODEL" not in os.environ:
            os.environ["MODEL"] = "gemini/gemini-2.5-flash"
        
        # CrewAI will automatically handle LLM instantiation from env vars
        # No need for manual LLM() instantiation
        self.llm = None
        
        # Tools para leitura de arquivos (só instanciaremos ferramentas reais se disponíveis)
        if HAVE_CREWAI_TOOLS and crewai_tools is not None:
            try:
                self.file_tool = crewai_tools.FileReadTool()
                self.dir_tool = crewai_tools.DirectoryReadTool()
            except Exception:
                # se qualquer erro ao instanciar, caímos para None e usamos leitura direta
                self.file_tool = None
                self.dir_tool = None
        else:
            self.file_tool = None
            self.dir_tool = None
        
        # Cria agentes especializados
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        
    def _create_agents(self) -> Dict[str, Agent]:
        """🎭 Cria todos os agentes especializados"""
        tools_list = [self.file_tool, self.dir_tool] if (self.file_tool is not None and self.dir_tool is not None) else None

        agents = {
            # 📐 Arquiteto de Software
            "arquiteto": Agent(
                role="🏗️ Arquiteto de Software Sênior",
                goal=("Analisar profundamente a arquitetura da aplicação, identificando:\n"
                      "- Padrões arquiteturais usados (MVC, Clean Architecture, etc.)\n"
                      "- Qualidade das integrações com APIs externas\n"
                      "- Escalabilidade e manutenibilidade do código\n"
                      "- Pontos de falha e gargalos potenciais\n"
                      "- Sugestões concretas de refatoração"),
                backstory=("Arquiteto de software com 10+ anos de experiência em sistemas distribuídos,\n"
                          "APIs de redes sociais e automação. Especialista em Instagram Graph API v23, WhatsApp Business API\n"
                          "e arquiteturas para SaaS. Conhece profundamente padrões como Repository, Factory, Observer e\n"
                          "estratégias de rate limiting para APIs."),
                tools=tools_list,
                verbose=True,
                max_iter=3,
                allow_delegation=False,
            ),

            # 🧪 Engenheiro de Qualidade
            "qa_engineer": Agent(
                role="🔬 Engenheiro de Qualidade e Testes",
                goal=("Avaliar rigorosamente a qualidade do código:\n"
                      "- Cobertura de testes (unitários, integração, E2E)\n"
                      "- Análise estática de código (complexity, duplication)\n"
                      "- Práticas de CI/CD e deployment\n"
                      "- Identificação de bugs e vulnerabilidades\n"
                      "- Estratégias de monitoramento e observabilidade"),
                backstory=("Engenheiro de QA com expertise em automação de testes, análise estática\n"
                          "e pipelines CI/CD. Experiência com pytest, bandit, ruff e ferramentas de segurança.\n"
                          "Especialista em testes de APIs, mock de serviços externos e estratégias de teste para\n"
                          "sistemas que integram redes sociais."),
                tools=tools_list,
                verbose=True,
                max_iter=3,
                allow_delegation=False,
            ),

            # 📄 Documentador Técnico
            "documentador": Agent(
                role="📚 Documentador Técnico Sênior",
                goal=("Garantir documentação de classe mundial:\n"
                      "- Clareza para onboarding de desenvolvedores\n"
                      "- Completude da documentação de APIs\n"
                      "- Guias de instalação e configuração\n"
                      "- Exemplos práticos e troubleshooting\n"
                      "- Documentação de arquitetura e decisões técnicas"),
                backstory=("Documentador técnico especializado em projetos open-source e SaaS.\n"
                          "Expert em criar documentação que funciona para diferentes níveis técnicos,\n"
                          "desde devs juniores até arquitetos seniores. Conhece ferramentas como Sphinx,\n"
                          "MkDocs e padrões de documentação de APIs REST."),
                tools=tools_list,
                verbose=True,
                max_iter=3,
                allow_delegation=False,
            ),

            # 🚀 Product Manager
            "product_manager": Agent(
                role="🎯 Product Manager Estratégico",
                goal=("Avaliar viabilidade comercial e estratégica:\n"
                      "- Prontidão para lançamento como SaaS\n"
                      "- Análise competitiva e diferenciação\n"
                      "- Roadmap de features e priorização\n"
                      "- Estratégia de monetização\n"
                      "- Riscos de adoção e go-to-market"),
                backstory=("Product Manager com 8+ anos em produtos de automação e marketing digital.\n"
                          "Experiência em lançar SaaS para redes sociais, conhece profundamente o mercado de\n"
                          "automação Instagram/WhatsApp. Expert em definir MVP, pricing strategy e user journey\n"
                          "para produtos B2B."),
                tools=tools_list,
                verbose=True,
                max_iter=3,
                allow_delegation=False,
            ),

            # ⚖️ Especialista Legal
            "especialista_legal": Agent(
                role="⚖️ Consultor Jurídico de Tecnologia",
                goal=("Assegurar conformidade legal total:\n"
                      "- Compliance com termos das APIs (Instagram, WhatsApp)\n"
                      "- Conformidade LGPD/GDPR para dados pessoais\n"
                      "- Riscos legais de automação em redes sociais\n"
                      "- Políticas de uso e termos de serviço\n"
                      "- Estratégias de mitigação de riscos legais"),
                backstory=("Advogado especializado em direito digital com foco em APIs de redes sociais.\n"
                          "Expert em LGPD, GDPR e regulamentações de automação. Experiência em revisar contratos\n"
                          "de APIs, políticas de uso de dados e compliance para startups de tecnologia."),
                tools=tools_list,
                verbose=True,
                max_iter=3,
                allow_delegation=False,
            ),

            # 🤖 Engenheiro de IA
            "engenheiro_ia": Agent(
                role="🧠 Engenheiro de IA Especialista",
                goal=("Otimizar componentes de inteligência artificial:\n"
                      "- Análise do pipeline de geração de legendas\n"
                      "- Otimização de prompts e modelos LLM\n"
                      "- Estratégias de personalização por usuário\n"
                      "- Performance e custos de APIs de IA\n"
                      "- Implementação de RAG e fine-tuning"),
                backstory=("Engenheiro de IA com especialização em NLP, visão computacional e LLMs.\n"
                          "Experiência com Google Gemini, OpenAI GPT, e modelos de visão para análise de imagens.\n"
                          "Expert em otimização de prompts, RAG systems e estratégias de personalização de conteúdo\n"
                          "para redes sociais."),
                tools=tools_list,
                verbose=True,
                max_iter=3,
                allow_delegation=False,
            ),
        }

        return agents

    
    def _create_tasks(self) -> List[Task]:
        """📋 Cria tasks específicas para cada agente"""
        
        tasks = [
            # Task do Arquiteto
            Task(
                description="""📐 ANÁLISE ARQUITETURAL COMPLETA
                
                Leia o arquivo 'relatorio_codebase_turbinado.md' e conduza uma análise arquitetural profunda:
                
                1. **Arquitetura Atual**: Descreva o padrão arquitetural identificado
                2. **Integrações**: Analise as integrações com APIs externas (Instagram, WhatsApp, Gemini)
                3. **Fluxo de Dados**: Mapeie o fluxo de dados de ponta a ponta
                4. **Escalabilidade**: Identifique gargalos e pontos de falha
                5. **Padrões de Design**: Liste padrões usados e ausentes
                6. **Refatorações Sugeridas**: Proponha melhorias concretas com priorização
                
                Foque em aspectos técnicos profundos e seja específico nas recomendações.""",
                expected_output="""Análise arquitetural estruturada em seções:
                - Resumo da arquitetura atual
                - Qualidade das integrações
                - Pontos críticos identificados
                - Recomendações priorizadas (Alta/Média/Baixa)
                - Diagrama conceitual em texto
                """,
                agent=self.agents["arquiteto"]
            ),
            
            # Task do QA Engineer
            Task(
                description="""🧪 AVALIAÇÃO DE QUALIDADE E TESTES
                
                Analise o relatório focando em qualidade de código e estratégias de teste:
                
                1. **Cobertura de Testes**: Avalie testes existentes (unitários, integração, E2E)
                2. **Qualidade do Código**: Analise complexity, duplicação, code smells
                3. **Segurança**: Identifique vulnerabilidades e riscos de segurança
                4. **CI/CD Pipeline**: Avalie práticas de deployment e automação
                5. **Monitoramento**: Analise estratégias de logging e observabilidade
                6. **Plano de Testes**: Sugira estratégia completa de testes
                
                Seja específico em métricas e ferramentas recomendadas.""",
                expected_output="""Relatório de qualidade estruturado:
                - Score de qualidade atual (0-100)
                - Gaps críticos em testes
                - Vulnerabilidades identificadas
                - Estratégia de testes recomendada
                - Ferramentas e métricas sugeridas
                - Roadmap de melhorias em qualidade
                """,
                agent=self.agents["qa_engineer"]
            ),
            
            # Task do Documentador
            Task(
                description="""📄 AUDITORIA DE DOCUMENTAÇÃO
                
                Avalie a completude e qualidade da documentação existente:
                
                1. **Documentação de Usuário**: Avalie clareza para usuários finais
                2. **Documentação Técnica**: Analise docs para desenvolvedores
                3. **API Documentation**: Verifique documentação de endpoints
                4. **Onboarding**: Avalie facilidade de setup para novos devs
                5. **Exemplos Práticos**: Analise qualidade dos exemplos
                6. **Manutenção**: Avalie processo de atualização da documentação
                
                Priorize aspectos que impactam adoção e produtividade.""",
                expected_output="""Auditoria de documentação:
                - Score de completude (0-100)
                - Gaps críticos identificados
                - Sugestões de reorganização
                - Templates recomendados
                - Estratégia de manutenção
                - Roadmap de melhorias documentais
                """,
                agent=self.agents["documentador"]
            ),
            
            # Task do Product Manager
            Task(
                description="""🚀 ANÁLISE DE VIABILIDADE COMERCIAL
                
                Avalie a prontidão do produto para o mercado:
                
                1. **Market Readiness**: Analise maturidade para lançamento SaaS
                2. **Competitive Analysis**: Compare com soluções existentes
                3. **Value Proposition**: Identifique diferenciadores únicos
                4. **User Journey**: Mapeie jornada do usuário ideal
                5. **Monetization**: Sugira modelos de precificação
                6. **Go-to-Market**: Proponha estratégia de lançamento
                
                Foque em aspectos que impactam success comercial.""",
                expected_output="""Análise comercial estratégica:
                - Score de prontidão para mercado (0-100)
                - Análise competitiva resumida
                - Proposta de valor única
                - Roadmap de lançamento em fases
                - Modelo de monetização sugerido
                - Riscos comerciais e mitigações
                """,
                agent=self.agents["product_manager"]
            ),
            
            # Task do Especialista Legal
            Task(
                description="""⚖️ ANÁLISE DE CONFORMIDADE LEGAL
                
                Conduza uma auditoria legal completa do projeto:
                
                1. **API Terms Compliance**: Analise conformidade com termos das APIs
                2. **Data Privacy**: Avalie conformidade LGPD/GDPR
                3. **Automation Risks**: Identifique riscos legais de automação
                4. **Terms of Service**: Sugira política de uso adequada
                5. **Liability Issues**: Mapeie responsabilidades e riscos
                6. **Compliance Strategy**: Proponha plano de conformidade
                
                Priorize riscos que podem impactar operação ou lançamento.""",
                expected_output="""Relatório de conformidade legal:
                - Score de compliance (0-100)
                - Riscos legais críticos
                - Não conformidades identificadas
                - Plano de adequação legal
                - Políticas necessárias
                - Roadmap de compliance
                """,
                agent=self.agents["especialista_legal"]
            ),
            
            # Task do Engenheiro de IA
            Task(
                description="""🤖 OTIMIZAÇÃO DO PIPELINE DE IA
                
                Analise e otimize os componentes de inteligência artificial:
                
                1. **LLM Integration**: Avalie uso atual do Gemini e outros LLMs
                2. **Prompt Engineering**: Analise qualidade dos prompts
                3. **Performance**: Avalie latência e custos de APIs de IA
                4. **Personalization**: Sugira estratégias de personalização
                5. **Model Selection**: Avalie adequação dos modelos escolhidos
                6. **AI Strategy**: Proponha roadmap de melhorias em IA
                
                Foque em otimizações que impactam UX e custos operacionais.""",
                expected_output="""Análise de IA estratégica:
                - Score de otimização IA (0-100)
                - Bottlenecks identificados
                - Oportunidades de melhoria
                - Estratégia de personalização
                - Otimizações de custo sugeridas
                - Roadmap de evolução IA
                """,
                agent=self.agents["engenheiro_ia"]
            )
        ]
        
        return tasks
    
    def create_final_report_task(self) -> Task:
        """📑 Cria task final para consolidação do relatório"""
        
        return Task(
            description="""🎯 CONSOLIDAÇÃO DO RELATÓRIO FINAL
            
            Com base em todas as análises anteriores, crie um relatório ultra-profissional com:
            
            ## 📊 ESTRUTURA DO RELATÓRIO FINAL:
            
            ### 🎯 EXECUTIVE SUMMARY
            - Score geral do projeto (0-100)
            - Principais forças e fraquezas
            - Recomendação de go/no-go
            
            ### 👶 SEÇÃO PARA DEVS JUNIORES
            - Explicação simples da arquitetura
            - Conceitos técnicos com analogias
            - Passos claros para contribuir
            - Recursos de aprendizado
            
            ### 🚀 SEÇÃO PARA DEVS SENIORES
            - Análise técnica profunda
            - Diagramas e fluxos detalhados
            - Decisões arquiteturais críticas
            - Trade-offs e justificativas
            
            ### 📈 ROADMAP ESTRATÉGICO
            - Fase 1: Correções críticas (0-3 meses)
            - Fase 2: Melhorias estruturais (3-6 meses)  
            - Fase 3: Expansão e otimização (6-12 meses)
            
            ### ⚡ QUICK WINS
            - Ações de alto impacto e baixo esforço
            - Implementações imediatas
            
            ### 🚨 RISCOS CRÍTICOS
            - Top 5 riscos priorizados
            - Planos de mitigação
            
            Use markdown profissional com emojis, tabelas e formatação clara.""",
            expected_output="""Relatório final em markdown com:
            - Executive summary executivo
            - Seções para diferentes públicos
            - Roadmap detalhado e priorizado
            - Métricas e scores quantitativos
            - Recomendações acionáveis
            - Formatação profissional
            """,
            agent=self.agents["arquiteto"],  # Arquiteto como consolidador final
            # NOTE: não passamos `context=self.tasks` aqui porque o modelo Task pode não aceitar objetos complexos.
            # O contexto completo será anexado textualmente à `description` antes da execução final.
        )
    
    def  run_analysis(self, report_path: str = "relatorio_codebase_turbinado.md",
                     max_files: int = 300,
                     max_size_bytes: int = 2 * 1024 * 1024) -> str:
        """🚀 Percorre a codebase lendo arquivos e gerando relatório por arquivo, depois consolida.

        Comportamento:
        - Se `report_path` existe como arquivo: usa o fluxo original (usa o relatório como insumo).
        - Caso contrário: trata `report_path` como diretório (se for) ou usa cwd como root e
          analisa arquivos da codebase gerando relatórios por arquivo.
        - Para evitar custos/overload, existe um limite `max_files` e um limite de tamanho por arquivo.
        """
        logger.info("🚀 Iniciando análise completa da codebase (análise por arquivo)...")

        # Se for arquivo existente, mantemos o comportamento original (usa o relatório como insumo)
        if os.path.exists(report_path) and os.path.isfile(report_path):
            logger.info(f"📄 Relatório de entrada encontrado: {report_path} — executando fluxo padrão.")
            # Reutiliza o fluxo original: verifica e executa crew com as tasks definidas mais a task final
            all_tasks = self.tasks + [self.create_final_report_task()]

            crew = Crew(
                agents=list(self.agents.values()),
                tasks=all_tasks,
                process=Process.sequential,
                verbose=True,
                # Avoid initializing persistent memory here to prevent external
                # dependencies (e.g. Chroma) from being required in minimal runs.
                # Per-file runs use memory=False already.
                memory=False,
            )

            try:
                logger.info("🔄 Executando análise com CrewAI (fluxo padrão)...")
                result = crew.kickoff()

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"relatorio_final_startup_{timestamp}.md"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(str(result))

                metadata = {
                    "timestamp": timestamp,
                    "input_file": report_path,
                    "output_file": output_file,
                    "agents_used": list(self.agents.keys()),
                    "total_tasks": len(all_tasks),
                    "llm_model": "gemini-2.5-flash"
                }
                metadata_file = f"metadata_analise_{timestamp}.json"
                with open(metadata_file, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)

                logger.info("✅ Análise concluída (fluxo padrão)!")
                logger.info(f"📄 Relatório salvo em: {output_file}")
                logger.info(f"📊 Metadados salvos em: {metadata_file}")
                return output_file

            except Exception as e:
                logger.error(f"❌ Erro durante análise (fluxo padrão): {e}")
                raise

        # Caso contrário, tratamos report_path como diretório ou usamos cwd
        if os.path.isdir(report_path):
            root_dir = report_path
            logger.info(f"📁 Usando diretório informado como root da codebase: {root_dir}")
        else:
            # report_path não existe como arquivo nem diretório -> usamos cwd como fallback
            root_dir = os.getcwd()
            logger.warning(f"⚠️ '{report_path}' não encontrado como arquivo; usando root: {root_dir}")

        # filtros e extensões de interesse
        skip_dirs = {".git", "__pycache__", "node_modules", "venv", ".venv", ".idea", ".env", ".venv"}
        allowed_exts = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".ini", ".cfg", ".sh", ".tsx", ".ts", ".js"}

        per_file_reports = []
        reports_dir = os.path.join(os.getcwd(), "reports_by_file")
        os.makedirs(reports_dir, exist_ok=True)

        files_analyzed = 0

        # Percorre arquivos
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # pular diretórios indesejados
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]

            for fname in filenames:
                if files_analyzed >= max_files:
                    logger.info(f"ℹ️ Limite de arquivos alcançado ({max_files}). Parando análise por arquivo.")
                    break

                _, ext = os.path.splitext(fname)
                if ext.lower() not in allowed_exts:
                    continue

                file_path = os.path.join(dirpath, fname)

                # evitar arquivos binários grandes
                try:
                    size = os.path.getsize(file_path)
                    if size > max_size_bytes:
                        logger.info(f"⏭️ Pulando arquivo grande (>{max_size_bytes} bytes): {file_path}")
                        continue
                except Exception:
                    logger.warning(f"⚠️ Não foi possível ler tamanho do arquivo, pulando: {file_path}")
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except Exception as e:
                    logger.warning(f"⚠️ Falha ao ler {file_path}: {e}")
                    continue

                # Trunca conteúdo muito grande para colocar no prompt
                max_chars = 50000
                snippet = content if len(content) <= max_chars else content[:max_chars] + "\n\n... (truncated)"

                logger.info(f"🔎 Gerando análise para: {file_path}")

                # Cria task dedicada para o arquivo (usando arquiteto como analista por arquivo)
                per_file_task = Task(
                    description=f"""ANÁLISE DO ARQUIVO: {os.path.relpath(file_path, root_dir)}

Leia atentamente o conteúdo do arquivo abaixo e gere um relatório focado em:
- Função do arquivo no projeto (responsabilidade)
- Pontos de acoplamento e dependências externas
- Complexidade e sugestões de refatoração
- Riscos de segurança ou má práticas
- Recomendações de testes (unitários/integração)

Conteúdo do arquivo (até {max_chars} chars):
```
{snippet}
```""",
                    expected_output="""Relatório por arquivo em markdown com:
- Resumo (1-3 linhas)
- Pontos críticos e recomendações
- Sugestões de testes
- Linha de ação rápida (quick win)
""",
                    agent=self.agents["arquiteto"]
                )

                # Executa uma execução rápida da crew apenas para este arquivo
                result = None
                try:
                    crew_single = Crew(
                        agents=[self.agents["arquiteto"]],
                        tasks=[per_file_task],
                        process=Process.sequential,
                        verbose=False,
                        memory=False,
                    )
                    result = crew_single.kickoff()
                except Exception as e:
                    logger.error(f"❌ Erro ao analisar {file_path}: {e}")
                    # registramos o erro no resultado para posterior salvamento
                    result = f"❌ Erro ao analisar {file_path}: {e}"

                # Salva relatório por arquivo (sempre tentamos salvar, mesmo que a análise falhe)
                safe_name = os.path.relpath(file_path, root_dir).replace(os.sep, "_").replace("..", "")
                if not safe_name:
                    safe_name = fname
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                out_name = f"{safe_name}_{timestamp}.md"
                out_path = os.path.join(reports_dir, out_name)
                try:
                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(f"# Análise do arquivo: {os.path.relpath(file_path, root_dir)}\n\n")
                        f.write(str(result) if result is not None else "(sem resultado)")
                    per_file_reports.append({"file": os.path.relpath(file_path, root_dir), "report_path": out_path})
                    files_analyzed += 1
                    logger.info(f"✅ Relatório salvo: {out_path} ({files_analyzed}/{max_files})")
                except Exception as e:
                    logger.error(f"❌ Falha ao salvar relatório para {file_path}: {e}")
                    # mesmo se salvar falhar, continuamos com os próximos arquivos
                    continue

            if files_analyzed >= max_files:
                break

        if not per_file_reports:
            logger.error("❌ Nenhum arquivo foi analisado. Verifique permissões, filtros e paths.")
            raise FileNotFoundError("Nenhum arquivo elegível encontrado para análise.")

        # Cria task final de consolidação incluindo lista de relatórios por arquivo
        final_task = self.create_final_report_task()
        # Anexa sumário dos relatórios por arquivo na descrição para fornecer contexto
        reports_summary_lines = [f"- {r['file']}: {r['report_path']}" for r in per_file_reports]
        reports_summary = "\n".join(reports_summary_lines)
        final_task.description += f"\n\n\n\n**Relatórios por arquivo (resumo):**\n{reports_summary}\n"

        # Executa a consolidação final usando toda a crew
        try:
            logger.info("🔄 Executando consolidação final com todos os agentes...")
            crew_all = Crew(
                agents=list(self.agents.values()),
                tasks=[final_task],
                process=Process.sequential,
                verbose=True,
                # disable memory to avoid requiring Chroma or other external
                # vectorstore env vars during light-weight consolidation runs
                memory=False,
            )
            final_result = crew_all.kickoff()

            # Salva resultado final consolidado
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"relatorio_final_startup_{timestamp}.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(str(final_result))

            # Salva metadados
            metadata = {
                "timestamp": timestamp,
                "root_dir": root_dir,
                "per_file_reports": per_file_reports,
                "output_file": output_file,
                "agents_used": list(self.agents.keys()),
                "total_files_analyzed": len(per_file_reports),
                "llm_model": "gemini-2.5-flash",
            }
            metadata_file = f"metadata_analise_{timestamp}.json"
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            logger.info("✅ Consolidação concluída!")
            logger.info(f"📄 Relatório final: {output_file}")
            logger.info(f"📁 Relatórios por arquivo em: {reports_dir}")
            logger.info(f"📊 Metadados salvos em: {metadata_file}")

            return output_file
        except Exception as e:
            # Se a consolidação com a Crew falhar (por exemplo, validação de env vars
            # de memória vetorial), geramos um fallback: concatenamos todos os
            # relatórios por arquivo salvos e produzimos um relatório final simples.
            logger.error(f"❌ Erro durante consolidação com Crew (usando fallback): {e}")
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                fallback_output = f"relatorio_final_fallback_{timestamp}.md"
                with open(fallback_output, "w", encoding="utf-8") as out_f:
                    out_f.write("# Relatório Consolidado (fallback)\n\n")
                    out_f.write("_A consolidação automática com a Crew falhou; este é um fallback que concatena os relatórios por arquivo gerados previamente._\n\n")

                    for r in per_file_reports:
                        try:
                            out_f.write(f"\n---\n\n## Arquivo: {r['file']}\n\n")
                            with open(r["report_path"], "r", encoding="utf-8", errors="ignore") as in_f:
                                out_f.write(in_f.read())
                                out_f.write("\n\n")
                        except Exception as inner_e:
                            out_f.write(f"\n(Erro ao incluir {r['file']}: {inner_e})\n")

                metadata = {
                    "timestamp": timestamp,
                    "root_dir": root_dir,
                    "per_file_reports": per_file_reports,
                    "output_file": fallback_output,
                    "agents_used": list(self.agents.keys()),
                    "total_files_analyzed": len(per_file_reports),
                    "llm_model": "gemini-2.5-flash",
                    "fallback": True,
                    "error": str(e),
                }
                metadata_file = f"metadata_analise_{timestamp}.json"
                with open(metadata_file, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)

                logger.info("✅ Fallback de consolidação concluído")
                logger.info(f"📄 Relatório final (fallback): {fallback_output}")
                logger.info(f"📁 Relatórios por arquivo em: {reports_dir}")
                logger.info(f"📊 Metadados salvos em: {metadata_file}")

                return fallback_output
            except Exception as final_e:
                logger.error(f"❌ Falha ao gerar fallback de consolidação: {final_e}")
                # Re-raise o erro original para que o caller saiba que algo deu errado
                raise


def main():
    """🎯 Função principal para execução direta"""
    
    print("🚀 CrewAI - Análise Completa de Codebase")
    print("=" * 50)
    
    try:
        # Inicializa a crew
        crew_analyzer = CodebaseAnalysisCrew()

        # Executa análise (se o relatório não existir, run_analysis fará a varredura da codebase)
        report_path = "relatorio_codebase_turbinado.md"
        # Use max_files=3 for quick testing with a valid API key
        output_file = crew_analyzer.run_analysis(report_path, max_files=3)

        print("\n🎉 Análise concluída com sucesso!")
        print(f"📄 Relatório final: {output_file}")
        print("\n👀 Visualize o relatório com:")
        print(f"   cat {output_file}")

    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
