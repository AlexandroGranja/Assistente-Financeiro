#!/usr/bin/env python3
"""
Script para verificar a configuração do Railway antes do deploy
"""
import os
import sys

def check_environment_variables():
    """Verifica se as variáveis de ambiente necessárias estão configuradas"""
    print("🔍 Verificando variáveis de ambiente...")
    
    required_vars = {
        'DATABASE_URL': 'URL de conexão do banco PostgreSQL',
        'SECRET_KEY': 'Chave secreta da aplicação Flask',
        'PORT': 'Porta do servidor (opcional, padrão: 8080)'
    }
    
    missing_vars = []
    
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if var == 'PORT':  # PORT é opcional
            print(f"  ✅ {var}: {'Configurada' if value else 'Não configurada (usará padrão)'}")
        elif value:
            if var == 'DATABASE_URL':
                # Mostra apenas parte da URL por segurança
                safe_url = value.split('@')[1] if '@' in value else '***'
                print(f"  ✅ {var}: ...@{safe_url}")
            else:
                print(f"  ✅ {var}: Configurada")
        else:
            print(f"  ❌ {var}: NÃO CONFIGURADA - {description}")
            missing_vars.append(var)
    
    return missing_vars

def check_database_connection():
    """Tenta conectar com o banco de dados"""
    print("\n🔗 Testando conexão com banco de dados...")
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("  ❌ DATABASE_URL não configurada")
        return False
    
    try:
        # Importa SQLAlchemy para testar conexão
        from sqlalchemy import create_engine, text
        
        # Ajusta URL se necessário
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        
        # Cria engine e testa conexão
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("  ✅ Conexão com banco de dados bem-sucedida!")
            return True
            
    except ImportError:
        print("  ⚠️  SQLAlchemy não instalada - não é possível testar conexão")
        return None
    except Exception as e:
        print(f"  ❌ Erro ao conectar com banco: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Verificação de Configuração do Railway")
    print("=" * 50)
    
    # Verifica variáveis de ambiente
    missing_vars = check_environment_variables()
    
    # Testa conexão com banco
    db_connection = check_database_connection()
    
    # Relatório final
    print("\n📊 RELATÓRIO FINAL")
    print("-" * 30)
    
    if missing_vars:
        print(f"❌ Variáveis não configuradas: {', '.join(missing_vars)}")
    else:
        print("✅ Todas as variáveis de ambiente estão configuradas")
    
    if db_connection is True:
        print("✅ Conexão com banco de dados funcionando")
    elif db_connection is False:
        print("❌ Problema na conexão com banco de dados")
    else:
        print("⚠️  Não foi possível testar conexão com banco")
    
    # Instruções para correção
    if missing_vars or db_connection is False:
        print("\n🔧 AÇÕES NECESSÁRIAS NO RAILWAY:")
        print("1. Acesse seu projeto no Railway")
        print("2. Vá em 'Variables' ou 'Settings'")
        print("3. Configure as seguintes variáveis:")
        
        if 'DATABASE_URL' in missing_vars or db_connection is False:
            print("   - DATABASE_URL: Adicione um serviço PostgreSQL no Railway")
        if 'SECRET_KEY' in missing_vars:
            print("   - SECRET_KEY: Uma string aleatória segura")
        
        print("\n4. Para adicionar PostgreSQL:")
        print("   - Clique em 'New' > 'Database' > 'PostgreSQL'")
        print("   - O Railway criará automaticamente a DATABASE_URL")
        
        return 1
    
    print("\n🎉 Configuração parece estar correta!")
    return 0

if __name__ == "__main__":
    sys.exit(main())