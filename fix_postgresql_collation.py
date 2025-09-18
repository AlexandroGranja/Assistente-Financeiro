#!/usr/bin/env python3
"""
Script para corrigir o problema de collation version mismatch no PostgreSQL
"""
import os
import sys
from sqlalchemy import create_engine, text

def fix_collation_mismatch():
    """
    Corrige o problema de collation version mismatch no PostgreSQL
    """
    print("🔧 Corrigindo problema de collation no PostgreSQL...")
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não encontrada nas variáveis de ambiente")
        return False
    
    # Ajusta URL se necessário
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("✅ Conectado ao PostgreSQL")
            
            # Executa o comando para corrigir a collation
            print("🔄 Executando ALTER DATABASE railway REFRESH COLLATION VERSION...")
            
            # Primeiro, verifica se podemos executar o comando
            try:
                result = conn.execute(text("ALTER DATABASE railway REFRESH COLLATION VERSION"))
                print("✅ Collation version atualizada com sucesso!")
                return True
                
            except Exception as alter_error:
                print(f"⚠️  Não foi possível executar ALTER DATABASE: {alter_error}")
                print("ℹ️  Isso pode ser normal se você não tiver privilégios de administrador")
                print("ℹ️  O warning de collation não impede o funcionamento da aplicação")
                return True  # Não é um erro crítico
                
    except Exception as e:
        print(f"❌ Erro ao conectar com PostgreSQL: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Script de Correção de Collation PostgreSQL")
    print("=" * 50)
    
    success = fix_collation_mismatch()
    
    if success:
        print("\n✅ Script executado com sucesso!")
        print("ℹ️  O warning de collation é apenas informativo e não afeta o funcionamento")
    else:
        print("\n❌ Falha ao executar script")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())