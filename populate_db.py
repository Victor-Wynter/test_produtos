#!/usr/bin/env python
"""
Script para popular o banco de dados com dados de exemplo
Django 4.x + DRF - Sistema de Produtos

Este script cria produtos de exemplo que demonstram:
- Produtos com diferentes tipos de espectro
- Produtos com e sem risco (THC > 0.3% + categoria específica)
- Diferentes status ANVISA
- Validações do sistema
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.produtos.models import Produto
from django.core.management import execute_from_command_line

def clear_database():
    """Limpa todos os produtos existentes"""
    print("🗑️  Limpando banco de dados...")
    Produto.objects.all().delete()
    print("✅ Banco de dados limpo!")

def create_sample_products():
    """Cria produtos de exemplo"""
    print("🌱 Criando produtos de exemplo...")
    
    # Lista de produtos de exemplo
    produtos_data = [
        # === PRODUTOS SEM RISCO ===
        {
            'nome': 'Óleo CBD Premium',
            'tipo_espectro': 'sativa',
            'thc_percentual': Decimal('0.1'),
            'cbd_percentual': Decimal('15.0'),
            'categoria_terapeutica': 'neurologia',
            'status_anvisa': 'aprovado',
            'descricao': 'Produto seguro com baixo THC e alto CBD'
        },
        {
            'nome': 'Creme Terapêutico',
            'tipo_espectro': 'indica',
            'thc_percentual': Decimal('0.05'),
            'cbd_percentual': Decimal('8.5'),
            'categoria_terapeutica': 'dermatologia',
            'status_anvisa': 'aprovado',
            'descricao': 'Creme para uso tópico com baixo teor de THC'
        },
        {
            'nome': 'Suplemento Pediátrico',
            'tipo_espectro': 'hibrida',
            'thc_percentual': Decimal('0.2'),
            'cbd_percentual': Decimal('12.0'),
            'categoria_terapeutica': 'pediatria',
            'status_anvisa': 'aprovado',
            'descricao': 'Suplemento seguro para uso pediátrico'
        },
        {
            'nome': 'Medicamento Oncológico',
            'tipo_espectro': 'sativa',
            'thc_percentual': Decimal('0.15'),
            'cbd_percentual': Decimal('20.0'),
            'categoria_terapeutica': 'oncologia',
            'status_anvisa': 'pendente',
            'descricao': 'Medicamento para tratamento oncológico'
        },
        
        # === PRODUTOS COM RISCO (THC > 0.3% + categoria específica) ===
        {
            'nome': 'Óleo Neurológico Forte',
            'tipo_espectro': 'sativa',
            'thc_percentual': Decimal('0.8'),
            'cbd_percentual': Decimal('5.0'),
            'categoria_terapeutica': 'neurologia',
            'status_anvisa': 'pendente',
            'descricao': 'PRODUTO DE RISCO: Alto THC para neurologia'
        },
        {
            'nome': 'Medicamento Pediátrico Especial',
            'tipo_espectro': 'hibrida',
            'thc_percentual': Decimal('0.5'),
            'cbd_percentual': Decimal('10.0'),
            'categoria_terapeutica': 'pediatria',
            'status_anvisa': 'pendente',
            'descricao': 'PRODUTO DE RISCO: Alto THC para pediatria'
        },
        {
            'nome': 'Tratamento Neurológico Avançado',
            'tipo_espectro': 'indica',
            'thc_percentual': Decimal('1.2'),
            'cbd_percentual': Decimal('3.0'),
            'categoria_terapeutica': 'neurologia',
            'status_anvisa': 'reprovado',
            'descricao': 'PRODUTO DE RISCO: THC muito alto para neurologia'
        },
        
        # === PRODUTOS COM THC ALTO MAS CATEGORIA DIFERENTE (SEM RISCO) ===
        {
            'nome': 'Óleo Dermatológico Forte',
            'tipo_espectro': 'sativa',
            'thc_percentual': Decimal('0.6'),
            'cbd_percentual': Decimal('8.0'),
            'categoria_terapeutica': 'dermatologia',
            'status_anvisa': 'pendente',
            'descricao': 'Alto THC mas categoria dermatologia (sem risco)'
        },
        {
            'nome': 'Medicamento Oncológico Especial',
            'tipo_espectro': 'hibrida',
            'thc_percentual': Decimal('0.9'),
            'cbd_percentual': Decimal('15.0'),
            'categoria_terapeutica': 'oncologia',
            'status_anvisa': 'pendente',
            'descricao': 'Alto THC mas categoria oncologia (sem risco)'
        },
        
        # === PRODUTOS DIVERSOS ===
        {
            'nome': 'Óleo CBD Puro',
            'tipo_espectro': 'sativa',
            'thc_percentual': Decimal('0.0'),
            'cbd_percentual': Decimal('25.0'),
            'categoria_terapeutica': 'outros',
            'status_anvisa': 'aprovado',
            'descricao': 'Produto 100% CBD sem THC'
        },
        {
            'nome': 'Creme Relaxante',
            'tipo_espectro': 'indica',
            'thc_percentual': Decimal('0.3'),
            'cbd_percentual': Decimal('12.0'),
            'categoria_terapeutica': 'outros',
            'status_anvisa': 'aprovado',
            'descricao': 'Produto no limite do THC permitido'
        },
        {
            'nome': 'Medicamento Experimental',
            'tipo_espectro': 'hibrida',
            'thc_percentual': Decimal('0.4'),
            'cbd_percentual': Decimal('18.0'),
            'categoria_terapeutica': 'outros',
            'status_anvisa': 'pendente',
            'descricao': 'Produto experimental com THC moderado'
        }
    ]
    
    # Criar produtos
    produtos_criados = []
    for i, data in enumerate(produtos_data, 1):
        try:
            produto = Produto.objects.create(
                nome=data['nome'],
                tipo_espectro=data['tipo_espectro'],
                thc_percentual=data['thc_percentual'],
                cbd_percentual=data['cbd_percentual'],
                categoria_terapeutica=data['categoria_terapeutica'],
                status_anvisa=data['status_anvisa']
            )
            produtos_criados.append(produto)
            print(f"✅ {i:2d}. {produto.nome} - THC: {produto.thc_percentual}% - Risco: {'SIM' if produto.tem_risco else 'NÃO'}")
            
        except Exception as e:
            print(f"❌ Erro ao criar produto {data['nome']}: {e}")
    
    return produtos_criados

def show_statistics(produtos):
    """Mostra estatísticas dos produtos criados"""
    print("\n📊 ESTATÍSTICAS DOS PRODUTOS:")
    print("=" * 50)
    
    # Total de produtos
    total = len(produtos)
    print(f"📦 Total de produtos: {total}")
    
    # Produtos por tipo de espectro
    espectros = {}
    for p in produtos:
        espectros[p.tipo_espectro] = espectros.get(p.tipo_espectro, 0) + 1
    
    print("\n🌿 Por tipo de espectro:")
    for espectro, count in espectros.items():
        print(f"   • {espectro.title()}: {count}")
    
    # Produtos por categoria
    categorias = {}
    for p in produtos:
        categorias[p.categoria_terapeutica] = categorias.get(p.categoria_terapeutica, 0) + 1
    
    print("\n🏥 Por categoria terapêutica:")
    for categoria, count in categorias.items():
        print(f"   • {categoria.title()}: {count}")
    
    # Produtos por status ANVISA
    status = {}
    for p in produtos:
        status[p.status_anvisa] = status.get(p.status_anvisa, 0) + 1
    
    print("\n📋 Por status ANVISA:")
    for st, count in status.items():
        print(f"   • {st.title()}: {count}")
    
    # Produtos com risco
    produtos_risco = [p for p in produtos if p.tem_risco]
    print(f"\n⚠️  Produtos com risco: {len(produtos_risco)}")
    for p in produtos_risco:
        print(f"   • {p.nome} - THC: {p.thc_percentual}% - {p.get_categoria_terapeutica_display()}")
    
    # Produtos sem risco
    produtos_sem_risco = [p for p in produtos if not p.tem_risco]
    print(f"\n✅ Produtos sem risco: {len(produtos_sem_risco)}")
    
    # Produtos com THC alto mas sem risco (categoria diferente)
    thc_alto_sem_risco = [p for p in produtos if p.thc_percentual > 0.3 and not p.tem_risco]
    if thc_alto_sem_risco:
        print(f"\n🔍 Produtos com THC > 0.3% mas sem risco (categoria diferente): {len(thc_alto_sem_risco)}")
        for p in thc_alto_sem_risco:
            print(f"   • {p.nome} - THC: {p.thc_percentual}% - {p.get_categoria_terapeutica_display()}")

def test_api_endpoints():
    """Testa os endpoints da API"""
    print("\n🔗 TESTANDO ENDPOINTS DA API:")
    print("=" * 50)
    
    # Teste 1: Listar todos os produtos
    print("1️⃣  Testando GET /api/produtos/")
    try:
        from django.test import Client
        client = Client()
        response = client.get('/api/produtos/')
        if response.status_code == 200:
            produtos_api = response.json()
            print(f"   ✅ Sucesso! {len(produtos_api)} produtos retornados")
        else:
            print(f"   ❌ Erro! Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 2: Listar produtos com risco
    print("\n2️⃣  Testando GET /api/produtos/risco/")
    try:
        response = client.get('/api/produtos/risco/')
        if response.status_code == 200:
            produtos_risco = response.json()
            print(f"   ✅ Sucesso! {len(produtos_risco)} produtos de risco retornados")
            for p in produtos_risco:
                print(f"      • {p['nome']} - THC: {p['thc_percentual']}%")
        else:
            print(f"   ❌ Erro! Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

def main():
    """Função principal"""
    print("🚀 SCRIPT DE POPULAÇÃO DO BANCO DE DADOS")
    print("=" * 60)
    print("Django 4.x + DRF - Sistema de Produtos")
    print("=" * 60)
    
    try:
        # Limpar banco
        clear_database()
        
        # Criar produtos
        produtos = create_sample_products()
        
        # Mostrar estatísticas
        show_statistics(produtos)
        
        # Testar API
        test_api_endpoints()
        
        print("\n" + "=" * 60)
        print("🎉 POPULAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("\n📝 PRÓXIMOS PASSOS:")
        print("1. Acesse http://localhost:8000/ para ver o frontend")
        print("2. Acesse http://localhost:8000/admin/ para o admin Django")
        print("3. Teste a API em http://localhost:8000/api/produtos/")
        print("4. Veja produtos de risco em http://localhost:8000/api/produtos/risco/")
        print("\n💡 DICAS:")
        print("• Produtos com risco são destacados em vermelho no frontend")
        print("• Teste criar produtos com THC > 0.3% e status 'aprovado' (será rejeitado)")
        print("• Use o admin Django para gerenciar produtos")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 