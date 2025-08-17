#!/usr/bin/env python3
"""
🧹 Script para Limpeza de Relatórios
==================================

Remove relatórios antigos e inconsistentes para evitar confusão.
"""

import os
import shutil
import glob

def main():
    print("🧹 Limpeza de Relatórios Antigos")
    print("=" * 40)
    
    # Remove relatórios finais antigos
    final_reports = glob.glob("relatorio_final_*.md")
    if final_reports:
        print(f"📄 Removendo {len(final_reports)} relatórios finais antigos:")
        for report in final_reports:
            print(f"  - {report}")
            os.remove(report)
    
    # Remove metadados antigos
    metadata_files = glob.glob("metadata_analise_*.json")
    if metadata_files:
        print(f"📊 Removendo {len(metadata_files)} arquivos de metadados antigos:")
        for metadata in metadata_files:
            print(f"  - {metadata}")
            os.remove(metadata)
    
    # Remove diretório reports_by_file antigo (sem timestamp)
    old_reports_dir = "reports_by_file"
    if os.path.exists(old_reports_dir):
        print(f"📁 Removendo diretório antigo: {old_reports_dir}")
        shutil.rmtree(old_reports_dir)
    
    # Remove diretórios reports_by_file com timestamp antigos (opcional)
    timestamped_dirs = glob.glob("reports_by_file_*")
    if timestamped_dirs:
        print(f"📁 Encontrados {len(timestamped_dirs)} diretórios de relatórios com timestamp:")
        for dir_name in timestamped_dirs:
            print(f"  - {dir_name}")
        
        if input("💬 Deseja remover os diretórios com timestamp também? (s/N): ").lower().startswith('s'):
            for dir_name in timestamped_dirs:
                print(f"  🗑️ Removendo: {dir_name}")
                shutil.rmtree(dir_name)
    
    print("\n✅ Limpeza concluída!")
    print("\n📋 Próximos passos:")
    print("1. Execute uma nova análise com:")
    print("   python crew_avaliacao_completa.py --path /caminho/do/projeto")
    print("2. Ou analise um repositório GitHub com:")
    print("   python github_analyzer.py https://github.com/user/repo")
    print("3. Os relatórios individuais e finais agora serão consistentes!")

if __name__ == "__main__":
    main()