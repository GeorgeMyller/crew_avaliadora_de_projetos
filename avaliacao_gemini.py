#!/usr/bin/env python3
"""
🚀 CrewAI Simplificado - Gemini Integration
==========================================

Versão simplificada que funciona com Google Gemini 2.5 Flash
"""

import os
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def setup_gemini():
    """🔧 Configura Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não encontrada no .env")
    
    # Remove espaços em branco da chave
    api_key = api_key.strip()
    genai.configure(api_key=api_key)
    
    return genai.GenerativeModel('gemini-2.5-flash')

def load_report(file_path="relatorio_codebase_turbinado.md"):
    """📄 Carrega relatório base"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Relatório não encontrado: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def analyze_architecture(model, report_content):
    """🏗️ Análise Arquitetural"""
    
    prompt = f"""Como um Arquiteto de Software Sênior experiente, analise o seguinte relatório de codebase e forneça uma análise arquitetural profunda:

RELATÓRIO DA CODEBASE:
{report_content}

Por favor, forneça uma análise estruturada cobrindo:

1. **ARQUITETURA ATUAL**: Descreva o padrão arquitetural identificado
2. **INTEGRAÇÕES**: Analise as integrações com APIs externas (Instagram, WhatsApp, Gemini)
3. **FLUXO DE DADOS**: Mapeie o fluxo de dados de ponta a ponta
4. **ESCALABILIDADE**: Identifique gargalos e pontos de falha
5. **PADRÕES DE DESIGN**: Liste padrões usados e ausentes
6. **REFATORAÇÕES SUGERIDAS**: Proponha melhorias concretas com priorização

Seja específico e técnico nas recomendações."""

    try:
        response = model.generate_content(prompt)
        return f"# 🏗️ ANÁLISE ARQUITETURAL\n\n{response.text}"
    except Exception as e:
        return f"❌ Erro na análise arquitetural: {str(e)}"

def analyze_quality(model, report_content):
    """🧪 Análise de Qualidade"""
    
    prompt = f"""Como um Engenheiro de Qualidade sênior, analise o seguinte relatório e forneça uma avaliação de qualidade:

RELATÓRIO DA CODEBASE:
{report_content}

Por favor, analise:

1. **COBERTURA DE TESTES**: Avalie testes unitários, integração, E2E
2. **QUALIDADE DO CÓDIGO**: Analise complexity, duplicação, code smells
3. **SEGURANÇA**: Identifique vulnerabilidades e riscos
4. **CI/CD PIPELINE**: Avalie práticas de deployment
5. **MONITORAMENTO**: Analise logging e observabilidade
6. **PLANO DE TESTES**: Sugira estratégia completa

Dê um score de 0-100 para qualidade geral."""

    try:
        response = model.generate_content(prompt)
        return f"# 🧪 ANÁLISE DE QUALIDADE\n\n{response.text}"
    except Exception as e:
        return f"❌ Erro na análise de qualidade: {str(e)}"

def analyze_documentation(model, report_content):
    """📄 Análise de Documentação"""
    
    prompt = f"""Como um Documentador Técnico especialista, analise este relatório:

RELATÓRIO DA CODEBASE:
{report_content}

Avalie a documentação em:

1. **DOCUMENTAÇÃO DE USUÁRIO**: Clareza para usuários finais
2. **DOCUMENTAÇÃO TÉCNICA**: Para desenvolvedores
3. **API DOCS**: Documentação de endpoints
4. **ONBOARDING**: Facilidade de setup para novos devs
5. **EXEMPLOS**: Qualidade dos exemplos práticos
6. **MANUTENÇÃO**: Processo de atualização

Score de completude: 0-100"""

    try:
        response = model.generate_content(prompt)
        return f"# 📄 ANÁLISE DE DOCUMENTAÇÃO\n\n{response.text}"
    except Exception as e:
        return f"❌ Erro na análise de documentação: {str(e)}"

def analyze_business(model, report_content):
    """🚀 Análise de Negócio"""
    
    prompt = f"""Como um Product Manager estratégico, analise a viabilidade comercial:

RELATÓRIO DA CODEBASE:
{report_content}

Avalie:

1. **PRONTIDÃO PARA MERCADO**: Maturidade para lançamento SaaS
2. **ANÁLISE COMPETITIVA**: Compare com soluções existentes
3. **VALUE PROPOSITION**: Identifique diferenciadores únicos
4. **USER JOURNEY**: Mapeie jornada do usuário ideal
5. **MONETIZAÇÃO**: Sugira modelos de precificação
6. **GO-TO-MARKET**: Proponha estratégia de lançamento

Score de market readiness: 0-100"""

    try:
        response = model.generate_content(prompt)
        return f"# 🚀 ANÁLISE DE VIABILIDADE COMERCIAL\n\n{response.text}"
    except Exception as e:
        return f"❌ Erro na análise comercial: {str(e)}"

def analyze_legal(model, report_content):
    """⚖️ Análise Legal"""
    
    prompt = f"""Como um Consultor Jurídico de Tecnologia, analise os aspectos legais:

RELATÓRIO DA CODEBASE:
{report_content}

Avalie:

1. **COMPLIANCE COM APIs**: Conformidade com termos das APIs
2. **DATA PRIVACY**: Conformidade LGPD/GDPR
3. **RISCOS DE AUTOMAÇÃO**: Riscos legais de automação
4. **TERMOS DE SERVIÇO**: Política de uso adequada
5. **RESPONSABILIDADES**: Responsabilidades e riscos
6. **ESTRATÉGIA DE COMPLIANCE**: Plano de conformidade

Score de compliance: 0-100"""

    try:
        response = model.generate_content(prompt)
        return f"# ⚖️ ANÁLISE DE CONFORMIDADE LEGAL\n\n{response.text}"
    except Exception as e:
        return f"❌ Erro na análise legal: {str(e)}"

def analyze_ai(model, report_content):
    """🤖 Análise de IA"""
    
    prompt = f"""Como um Engenheiro de IA especialista, analise os componentes de inteligência artificial:

RELATÓRIO DA CODEBASE:
{report_content}

Avalie:

1. **INTEGRAÇÃO LLM**: Avalie uso do Gemini e outros LLMs
2. **PROMPT ENGINEERING**: Analise qualidade dos prompts
3. **PERFORMANCE**: Avalie latência e custos APIs IA
4. **PERSONALIZAÇÃO**: Estratégias de personalização
5. **SELEÇÃO DE MODELOS**: Adequação dos modelos escolhidos
6. **ESTRATÉGIA IA**: Roadmap de melhorias em IA

Score de otimização IA: 0-100"""

    try:
        response = model.generate_content(prompt)
        return f"# 🤖 ANÁLISE DE OTIMIZAÇÃO IA\n\n{response.text}"
    except Exception as e:
        return f"❌ Erro na análise de IA: {str(e)}"

def generate_final_report(model, analyses):
    """📑 Gera relatório final consolidado"""
    
    combined_analysis = "\n\n".join(analyses)
    
    prompt = f"""Como um Arquiteto de Software Sênior, consolide as seguintes análises em um relatório final ultra-profissional:

ANÁLISES ESPECIALIZADAS:
{combined_analysis}

Crie um relatório final estruturado com:

## 🎯 EXECUTIVE SUMMARY
- Score geral do projeto (0-100)
- Principais forças e fraquezas
- Recomendação de go/no-go

## 👶 SEÇÃO PARA DEVS JUNIORES
- Explicação simples da arquitetura
- Conceitos técnicos com analogias
- Passos claros para contribuir

## 🚀 SEÇÃO PARA DEVS SENIORES
- Análise técnica profunda
- Diagramas e fluxos detalhados
- Decisões arquiteturais críticas

## 📈 ROADMAP ESTRATÉGICO
- Fase 1: Correções críticas (0-3 meses)
- Fase 2: Melhorias estruturais (3-6 meses)
- Fase 3: Expansão e otimização (6-12 meses)

## ⚡ QUICK WINS
- Ações de alto impacto e baixo esforço

## 🚨 RISCOS CRÍTICOS
- Top 5 riscos priorizados
- Planos de mitigação

Use markdown profissional com emojis e formatação clara."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Erro na consolidação final: {str(e)}"

def main():
    """🎯 Função principal"""
    
    print("🚀 CrewAI Simplificado - Análise com Gemini")
    print("=" * 50)
    
    try:
        # Setup
        print("🔧 Configurando Gemini...")
        model = setup_gemini()
        
        print("📄 Carregando relatório...")
        report_content = load_report()
        
        # Análises especializadas
        print("🏗️ Executando análise arquitetural...")
        arch_analysis = analyze_architecture(model, report_content)
        
        print("🧪 Executando análise de qualidade...")
        quality_analysis = analyze_quality(model, report_content)
        
        print("📄 Executando análise de documentação...")
        doc_analysis = analyze_documentation(model, report_content)
        
        print("🚀 Executando análise de negócio...")
        business_analysis = analyze_business(model, report_content)
        
        print("⚖️ Executando análise legal...")
        legal_analysis = analyze_legal(model, report_content)
        
        print("🤖 Executando análise de IA...")
        ai_analysis = analyze_ai(model, report_content)
        
        # Consolidação final
        print("📑 Gerando relatório final...")
        analyses = [
            arch_analysis,
            quality_analysis, 
            doc_analysis,
            business_analysis,
            legal_analysis,
            ai_analysis
        ]
        
        final_report = generate_final_report(model, analyses)
        
        # Salva resultado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"relatorio_final_gemini_{timestamp}.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            header = f"""# 🚀 RELATÓRIO ULTRA-PROFISSIONAL - ANÁLISE DE CODEBASE
## Agent Social Media - Automação WhatsApp→Instagram

**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  
**Modelo**: Google Gemini 2.5 Flash  
**Versão**: CrewAI Simplificado v1.0

---

"""
            f.write(header + final_report)
        
        print("\n✅ Análise concluída com sucesso!")
        print(f"📄 Relatório salvo: {output_file}")
        
        # Preview
        print("\n👀 Preview do relatório:")
        print("-" * 40)
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')[:30]
            for line in lines:
                print(line)
            print("...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    exit(0 if main() else 1)
