#!/usr/bin/env python
"""
Script para testar a API manualmente
Django 4.x + DRF - Sistema de Produtos

Este script testa os endpoints da API usando requests
"""

import requests
import json
from decimal import Decimal

# Configurações
BASE_URL = 'http://localhost:8000'
API_URL = f'{BASE_URL}/api/produtos'
RISCO_URL = f'{BASE_URL}/api/produtos/risco'

def test_get_all_products():
    """Testa GET /api/produtos/"""
    print("🔍 Testando GET /api/produtos/")
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            produtos = response.json()
            print(f"✅ Sucesso! {len(produtos)} produtos retornados")
            
            # Mostrar alguns produtos
            for i, produto in enumerate(produtos[:3], 1):
                print(f"   {i}. {produto['nome']} - THC: {produto['thc_percentual']}% - Risco: {produto['tem_risco']}")
            
            if len(produtos) > 3:
                print(f"   ... e mais {len(produtos) - 3} produtos")
                
        else:
            print(f"❌ Erro! Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

def test_get_risk_products():
    """Testa GET /api/produtos/risco/"""
    print("\n⚠️  Testando GET /api/produtos/risco/")
    try:
        response = requests.get(RISCO_URL)
        if response.status_code == 200:
            produtos_risco = response.json()
            print(f"✅ Sucesso! {len(produtos_risco)} produtos de risco retornados")
            
            for produto in produtos_risco:
                print(f"   • {produto['nome']} - THC: {produto['thc_percentual']}% - {produto['categoria_terapeutica_label']}")
                if produto.get('explicacao_risco'):
                    print(f"     💡 {produto['explicacao_risco']}")
        else:
            print(f"❌ Erro! Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

def test_create_product():
    """Testa POST /api/produtos/ - Produto válido"""
    print("\n➕ Testando POST /api/produtos/ - Produto válido")
    
    produto_valido = {
        'nome': 'Produto Teste Válido',
        'tipo_espectro': 'sativa',
        'thc_percentual': 0.2,
        'cbd_percentual': 10.0,
        'categoria_terapeutica': 'outros',
        'status_anvisa': 'pendente'
    }
    
    try:
        response = requests.post(API_URL, json=produto_valido)
        if response.status_code == 201:
            produto_criado = response.json()
            print(f"✅ Produto criado com sucesso!")
            print(f"   ID: {produto_criado['id']}")
            print(f"   Nome: {produto_criado['nome']}")
            print(f"   THC: {produto_criado['thc_percentual']}%")
            print(f"   Risco: {produto_criado['tem_risco']}")
        else:
            print(f"❌ Erro! Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

def test_create_invalid_product():
    """Testa POST /api/produtos/ - Produto inválido (THC > 0.3% + aprovado)"""
    print("\n❌ Testando POST /api/produtos/ - Produto inválido (THC > 0.3% + aprovado)")
    
    produto_invalido = {
        'nome': 'Produto Teste Inválido',
        'tipo_espectro': 'sativa',
        'thc_percentual': 0.5,  # THC > 0.3%
        'cbd_percentual': 10.0,
        'categoria_terapeutica': 'outros',
        'status_anvisa': 'aprovado'  # Status aprovado
    }
    
    try:
        response = requests.post(API_URL, json=produto_invalido)
        if response.status_code == 400:
            print("✅ Validação funcionando corretamente!")
            print(f"   Erro: {response.json()}")
        else:
            print(f"❌ Validação falhou! Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

def test_frontend_pages():
    """Testa as páginas do frontend"""
    print("\n🌐 Testando páginas do frontend")
    
    pages = [
        ('/', 'Página inicial'),
        ('/cadastro/', 'Página de cadastro'),
        ('/admin/', 'Admin Django')
    ]
    
    for url, desc in pages:
        try:
            response = requests.get(f'{BASE_URL}{url}')
            if response.status_code == 200:
                print(f"✅ {desc}: OK")
            else:
                print(f"❌ {desc}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {desc}: Erro de conexão - {e}")

def main():
    """Função principal"""
    print("🧪 TESTE MANUAL DA API")
    print("=" * 50)
    print("Django 4.x + DRF - Sistema de Produtos")
    print("=" * 50)
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(BASE_URL, timeout=5)
        print("✅ Servidor está rodando!")
    except:
        print("❌ Servidor não está rodando!")
        print("Execute: python manage.py runserver")
        return
    
    # Executar testes
    test_get_all_products()
    test_get_risk_products()
    test_create_product()
    test_create_invalid_product()
    test_frontend_pages()
    
    print("\n" + "=" * 50)
    print("🎉 TESTES CONCLUÍDOS!")
    print("=" * 50)
    print("\n📝 PRÓXIMOS PASSOS:")
    print("1. Acesse http://localhost:8000/ para ver o frontend")
    print("2. Teste criar produtos no formulário")
    print("3. Veja produtos de risco destacados")
    print("4. Teste a validação THC vs Status ANVISA")

if __name__ == '__main__':
    main() 