#!/usr/bin/env python3
"""
Script de teste para verificar se a API está funcionando
"""

import requests
import json

# Configurações
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/produtos/"

def test_api():
    """Testa a API de produtos"""
    print("🧪 Testando API de Produtos...")
    
    try:
        # Teste 1: GET - Listar produtos
        print("\n1. Testando GET /api/produtos/")
        response = requests.get(API_URL)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            produtos = response.json()
            print(f"Produtos encontrados: {len(produtos)}")
            print("✅ GET /api/produtos/ funcionando!")
        else:
            print(f"❌ Erro: {response.text}")
            return False
        
        # Teste 2: POST - Criar produto válido
        print("\n2. Testando POST /api/produtos/ (produto válido)")
        produto_valido = {
            "nome": "Produto Teste 1",
            "tipo_espectro": "sativa",
            "thc_percentual": 0.2,
            "cbd_percentual": 1.5,
            "categoria_terapeutica": "neurologia",
            "status_anvisa": "pendente"
        }
        
        response = requests.post(API_URL, json=produto_valido)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            produto_criado = response.json()
            print(f"✅ Produto criado com ID: {produto_criado['id']}")
            print(f"   Nome: {produto_criado['nome']}")
            print(f"   Tem risco: {produto_criado['tem_risco']}")
        else:
            print(f"❌ Erro: {response.text}")
            return False
        
        # Teste 3: POST - Tentar criar produto inválido (THC > 0.3% com status aprovado)
        print("\n3. Testando POST /api/produtos/ (produto inválido)")
        produto_invalido = {
            "nome": "Produto Teste 2",
            "tipo_espectro": "indica",
            "thc_percentual": 0.5,
            "cbd_percentual": 2.0,
            "categoria_terapeutica": "pediatria",
            "status_anvisa": "aprovado"  # Deve falhar
        }
        
        response = requests.post(API_URL, json=produto_invalido)
        print(f"Status: {response.status_code}")
        if response.status_code == 400:
            print("✅ Validação funcionando - produto rejeitado corretamente")
            print(f"   Erro: {response.json()}")
        else:
            print(f"❌ Validação falhou - produto foi aceito incorretamente")
            return False
        
        # Teste 4: GET - Produtos com risco
        print("\n4. Testando GET /api/produtos/risco/")
        response = requests.get(f"{BASE_URL}/api/produtos/risco/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            produtos_risco = response.json()
            print(f"Produtos com risco encontrados: {len(produtos_risco)}")
            print("✅ GET /api/produtos/risco/ funcionando!")
        else:
            print(f"❌ Erro: {response.text}")
            return False
        
        # Teste 5: GET - Listar produtos novamente
        print("\n5. Testando GET /api/produtos/ (após criação)")
        response = requests.get(API_URL)
        if response.status_code == 200:
            produtos = response.json()
            print(f"Total de produtos: {len(produtos)}")
            print("✅ Listagem atualizada funcionando!")
        else:
            print(f"❌ Erro: {response.text}")
            return False
        
        print("\n🎉 Todos os testes passaram!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor")
        print("   Certifique-se de que o servidor Django está rodando em http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_frontend():
    """Testa o frontend"""
    print("\n🌐 Testando Frontend...")
    
    try:
        # Teste 1: Página inicial
        print("\n1. Testando página inicial")
        response = requests.get(BASE_URL)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Página inicial carregando!")
        else:
            print(f"❌ Erro: {response.status_code}")
            return False
        
        # Teste 2: Página de cadastro
        print("\n2. Testando página de cadastro")
        response = requests.get(f"{BASE_URL}/cadastro/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Página de cadastro carregando!")
        else:
            print(f"❌ Erro: {response.status_code}")
            return False
        
        print("\n🎉 Frontend funcionando!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes do Sistema de Produtos")
    print("=" * 50)
    
    # Testar API
    api_ok = test_api()
    
    # Testar Frontend
    frontend_ok = test_frontend()
    
    print("\n" + "=" * 50)
    print("📊 Resumo dos Testes:")
    print(f"   API: {'✅ OK' if api_ok else '❌ FALHOU'}")
    print(f"   Frontend: {'✅ OK' if frontend_ok else '❌ FALHOU'}")
    
    if api_ok and frontend_ok:
        print("\n🎉 Sistema funcionando perfeitamente!")
        print("\n📝 URLs disponíveis:")
        print(f"   Frontend: {BASE_URL}")
        print(f"   API: {API_URL}")
        print(f"   Admin: {BASE_URL}/admin/")
    else:
        print("\n❌ Alguns testes falharam. Verifique os logs acima.") 