#!/usr/bin/env python3
"""
🐙 GitHub Repository Analyzer
============================

Script auxiliar para analisar repositórios GitHub com o CrewAI.
Este script automatiza o processo de clone + análise.
"""

import os
import sys
import subprocess
import tempfile
import shutil
import argparse
from urllib.parse import urlparse

def is_github_url(url: str) -> bool:
    """Verifica se a URL é um repositório GitHub válido"""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower() in ['github.com', 'www.github.com']
    except Exception:
        return False

def clone_github_repo(github_url: str) -> str:
    """Clona um repositório GitHub e retorna o caminho local"""
    if not is_github_url(github_url):
        raise ValueError(f"❌ URL inválida. Esperado GitHub URL, recebido: {github_url}")
    
    # Cria diretório temporário
    temp_dir = tempfile.mkdtemp(prefix="crew_github_")
    repo_name = github_url.rstrip('/').split('/')[-1]
    if repo_name.endswith('.git'):
        repo_name = repo_name[:-4]
    
    clone_path = os.path.join(temp_dir, repo_name)
    
    try:
        print(f"🔄 Clonando repositório: {github_url}")
        print(f"📁 Destino: {clone_path}")
        
        # Executa git clone
        subprocess.run([
            'git', 'clone', '--depth', '1', github_url, clone_path
        ], capture_output=True, text=True, check=True)
        
        print("✅ Clone concluído com sucesso!")
        return clone_path
        
    except subprocess.CalledProcessError as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise RuntimeError(f"❌ Erro ao clonar repositório: {e.stderr}")
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise RuntimeError(f"❌ Erro inesperado durante clone: {str(e)}")

def main():
    """Função principal - clone e análise de repositório GitHub"""
    parser = argparse.ArgumentParser(
        description="🐙 Analisador de Repositórios GitHub com CrewAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Análise de repositório público
  python github_analyzer.py https://github.com/usuario/repo
  
  # Análise com controle de arquivos
  python github_analyzer.py https://github.com/usuario/repo --max-files 15
  
  # Manter clone após análise
  python github_analyzer.py https://github.com/usuario/repo --keep-clone
        """
    )
    
    parser.add_argument("github_url", help="URL do repositório GitHub")
    parser.add_argument("--max-files", type=int, default=20, help="Máximo de arquivos a analisar")
    parser.add_argument("--max-size", type=int, default=10_000_000, help="Tamanho máximo por arquivo (bytes)")
    parser.add_argument("--keep-clone", action="store_true", help="Não remove o clone após análise")
    
    args = parser.parse_args()
    
    print("🐙 Analisador de Repositórios GitHub")
    print("=" * 40)
    print(f"🔗 URL: {args.github_url}")
    print(f"📊 Máximo de arquivos: {args.max_files}")
    print(f"💾 Tamanho máximo: {args.max_size:,} bytes")
    print()
    
    cloned_path = None
    
    try:
        # 1. Clone do repositório
        cloned_path = clone_github_repo(args.github_url)
        
        # 2. Importa e executa a análise
        print("\n🚀 Iniciando análise com CrewAI...")
        
        # Importa o módulo de análise
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from crew_avaliacao_completa import CodebaseAnalysisCrew
        
        # Executa análise
        analyzer = CodebaseAnalysisCrew()
        output_file = analyzer.run_analysis(
            report_path=cloned_path,
            max_files=args.max_files,
            max_size_bytes=args.max_size
        )
        
        print("\\n🎉 Análise concluída com sucesso!")
        print(f"📄 Relatório: {output_file}")
        
        if args.keep_clone:
            print(f"📁 Clone mantido em: {cloned_path}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1
        
    finally:
        # Cleanup se necessário
        if not args.keep_clone and cloned_path and os.path.exists(cloned_path):
            try:
                parent_dir = os.path.dirname(cloned_path)
                shutil.rmtree(parent_dir, ignore_errors=True)
                print(f"🧹 Clone temporário removido")
            except Exception as e:
                print(f"⚠️ Erro ao limpar clone: {e}")

if __name__ == "__main__":
    exit(main())