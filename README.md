# 🌿 Sistema de Monitoramento de Produtos Canabinoides

> **Painel interno para cadastrar e monitorar produtos medicinais à base de canabinoides conforme regras da ANVISA**

Este projeto veio de um teste para criar um sistema interno para empresas farmacêuticas que trabalham com produtos à base de canabinoides (THC/CBD). O objetivo é facilitar o cadastro, monitoramento e controle de produtos que precisam seguir rigorosas regulamentações da ANVISA, especialmente aqueles com alto teor de THC destinados a grupos sensíveis como neurologia e pediatria.

## 📌 Sobre o Projeto

### 🎯 Propósito Real

O sistema foi desenvolvido para atender um caso em especifico: **monitorar produtos canabinoides que podem representar risco quando destinados a certos grupos**. 

**Problema que resolve:**
- Produtos com THC > 0.3% não podem ter status "Aprovado" na ANVISA
- Produtos para neurologia e pediatria com alto THC precisam de atenção especial
- Necessidade de um painel visual para identificar rapidamente produtos de risco
- Controle centralizado de todos os produtos canabinoides da empresa

**Solução implementada:**
- Sistema web completo com backend robusto e frontend simples
- Validações automáticas baseadas nas regras da ANVISA
- Destaque visual para produtos que precisam de análise especial
- API REST para integração com outros sistemas da empresa

### 🏗️ Arquitetura Escolhida

Optei por uma arquitetura **monolítica com Django** por alguns motivos específicos:

1. **Simplicidade de Deploy**: Uma única aplicação é mais fácil de manter e deployar
2. **Integração Perfeita**: DRF + Django Templates funcionam bem juntas
3. **Manutenibilidade**: Tudo em um lugar, fácil de debugar e modificar

## 🛠 Tecnologias Utilizadas

### Backend
- **Django**: Framework web robusto e maduro
- **Django REST Framework**: Para APIs REST
- **SQLite**: Banco simples para desenvolvimento (fácil de trocar para PostgreSQL em produção)
- **python-decouple**: Para gerenciar variáveis de ambiente

### Frontend
- **Django Templates**: Renderização server-side rápida e SEO-friendly
- **Bootstrap 5**: Framework CSS responsivo
- **JavaScript Puro**: Sem frameworks complexos
- **Font Awesome**: Ícones profissionais

### Por que essas escolhas?

**Django REST Framework:**
- Serializers com validação customizada integrada
- Auto-documentação da API
- Perfeita integração com Django ORM
- Fácil extensão para novos endpoints

**Templates Django (não SPA):**
- Não precisa de build tools complexos
- SEO melhor que aplicações SPA
- Carregamento mais rápido
- Manutenção mais simples

**Bootstrap 5:**
- Grid system responsivo nativo
- Componentes prontos (tabelas, formulários, badges)
- Design system consistente
- Suporte mobile-first

## 📦 Estrutura do Projeto

```
PROVA_BACKEND/
├── apps/
│   └── produtos/                    # App principal do sistema
│       ├── migrations/              # Migrações do banco
│       ├── templates/
│       │   └── produtos/
│       │       ├── base.html        # Template base com navbar
│       │       ├── index.html       # Lista de produtos
│       │       └── cadastro.html    # Formulário de cadastro
│       ├── static/
│       │   └── produtos/
│       │       ├── css/
│       │       │   └── styles.css   # Estilos customizados
│       │       └── js/
│       │           └── main.js       # JavaScript principal
│       ├── admin.py                 # Configuração do admin Django
│       ├── models.py                # Modelo Produto com validações
│       ├── serializers.py           # Serializers DRF
│       ├── views.py                 # Views (API + Templates)
│       ├── urls.py                  # URLs do app
│       └── tests.py                 # Testes unitários
├── setup/                           # Configurações do projeto Django
│   ├── settings.py                  # Configurações principais
│   ├── urls.py                      # URLs principais
│   └── wsgi.py                      # WSGI para deploy
├── .env                             # Variáveis de ambiente
├── manage.py                        # Script de gerenciamento Django
├── requirements.txt                 # Dependências Python
├── populate_db.py                   # Script para popular banco
├── test_api_manual.py               # Script para testar API
└── README.md                        # Este arquivo
```

## ⚙️ Como Rodar Localmente

### Pré-requisitos
- Python 3.11+
- pip (gerenciador de pacotes Python)

### Passos para Configuração

1. **Clone o repositório e entre na pasta:**
   ```bash
   git clone <url-do-repositorio>
   cd PROVA_BACKEND
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # Criar ambiente virtual
   python -m venv venv
   
   # Ativar (Windows)
   venv\Scripts\activate
   
   # Ativar (Linux/Mac)
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   ```bash
   # Crie o arquivo .env
   echo "SECRET_KEY=django-insecure-your-secret-key-here-change-in-production" > .env
   ```

5. **Execute as migrações:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Popule o banco com dados de exemplo:**
   ```bash
   python populate_db.py
   ```

7. **Execute o servidor:**
   ```bash
   python manage.py runserver
   ```

8. **Acesse o sistema:**
   - **Frontend**: http://localhost:8000/
   - **Admin Django**: http://localhost:8000/admin/
   - **API**: http://localhost:8000/api/produtos/

## 🚀 Funcionalidades Principais

### Backend (Django + DRF)

#### Modelo de Dados
O sistema trabalha com um modelo `Produto` que inclui:
- **Informações básicas**: Nome, tipo de espectro (Sativa/Indica/Híbrida)
- **Composição**: Percentual de THC e CBD
- **Classificação**: Categoria terapêutica e status ANVISA
- **Controle**: Timestamps automáticos de criação/atualização

#### API REST
- `GET /api/produtos/`: Lista todos os produtos
- `POST /api/produtos/`: Cria novo produto
- `GET /api/produtos/risco/`: Lista produtos que precisam de atenção especial

### Frontend (Templates + JavaScript)

#### Página de Listagem
- Tabela responsiva com todos os produtos
- **Destaque visual** para produtos de risco (linha vermelha)
- Badges coloridos para status e percentuais
- Loading states e tratamento de erros

#### Página de Cadastro
- Formulário completo com validação
- **Validação em tempo real** (THC vs Status ANVISA)
- Feedback visual para erros
- Redirecionamento após sucesso

## 🔍 Regras de Negócio Implementadas

### Validação THC vs Status ANVISA

A regra mais importante do sistema está implementada no serializer:

```python
def validate(self, data):
    thc_percentual = data.get('thc_percentual')
    status_anvisa = data.get('status_anvisa')
    
    if thc_percentual and status_anvisa:
        if thc_percentual > 0.3 and status_anvisa == 'aprovado':
            raise serializers.ValidationError(
                "Produtos com THC superior a 0.3% não podem ter status 'aprovado' na ANVISA."
            )
    
    return data
```

**Por que no serializer?**
- Validação acontece no backend, garantindo integridade
- Mensagem de erro clara para o usuário
- Previne dados inválidos no banco

### Identificação de Produtos de Risco

Um produto é considerado de risco quando:
- **THC > 0.3%** **E**
- **Categoria terapêutica** é "Neurologia" ou "Pediatria"

```python
@property
def tem_risco(self):
    return (
        self.thc_percentual > 0.3 and 
        self.categoria_terapeutica in ['neurologia', 'pediatria']
    )
```

### Rota Especial para Monitoramento

A rota `/api/produtos/risco/` foi criada especificamente para:
- **Monitoramento rápido** de produtos que precisam de atenção
- **Relatórios** para a equipe de compliance
- **Alertas** para produtos sensíveis

## 🖥 Como Funciona o Frontend

### Consumo da API

O frontend usa **JavaScript puro** com `fetch()` para consumir a API:

```javascript
// Carregar produtos
async function loadProdutos() {
    try {
        const response = await fetch('/api/produtos/');
        const produtos = await response.json();
        displayProdutos(produtos);
    } catch (error) {
        showAlert('Erro ao carregar produtos', 'danger');
    }
}

// Criar produto
async function createProduto(formData) {
    try {
        const response = await fetch('/api/produtos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error('Erro ao criar produto');
        }
        
        showAlert('Produto criado com sucesso!', 'success');
    } catch (error) {
        showAlert('Erro: ' + error.message, 'danger');
    }
}
```

### Identificação Visual de Produtos de Risco

Produtos de risco são destacados de várias formas:

1. **Linha vermelha** na tabela (classe `table-danger`)
2. **Badge vermelho** com ícone de alerta
3. **Tooltip** com explicação do risco
4. **Ícone de atenção** ao lado do nome

```javascript
function hasRisk(produto) {
    return produto.thc_percentual > 0.3 && 
           ['neurologia', 'pediatria'].includes(produto.categoria_terapeutica);
}

function getRiskClass(produto) {
    return hasRisk(produto) ? 'table-danger' : '';
}
```

### Separação de Responsabilidades

- **HTML**: Estrutura e conteúdo
- **CSS**: Estilos e responsividade
- **JavaScript**: Interatividade e consumo da API
- **Templates Django**: Renderização server-side

## 🧪 Scripts de Teste e População

### População do Banco de Dados

Para popular o banco com dados de exemplo:

```bash
python populate_db.py
```

Este script cria:
- **12 produtos de exemplo** com diferentes características
- **3 produtos com risco** (THC > 0.3% + categoria específica)
- **Produtos com diferentes status ANVISA**
- **Estatísticas detalhadas** dos produtos criados

### Teste Manual da API

Para testar a API manualmente:

```bash
python test_api_manual.py
```

Este script testa:
- ✅ GET /api/produtos/ (listar todos)
- ✅ GET /api/produtos/risco/ (produtos de risco)
- ✅ POST /api/produtos/ (criar produto válido)
- ✅ Validação THC > 0.3% vs status 'aprovado'
- ✅ Páginas do frontend

### Dados de Exemplo Criados

O script `populate_db.py` cria produtos que demonstram:

1. **Produtos Sem Risco**:
   - Óleo CBD Premium (THC: 0.1%, Neurologia, Aprovado)
   - Creme Terapêutico (THC: 0.05%, Dermatologia, Aprovado)
   - Suplemento Pediátrico (THC: 0.2%, Pediatria, Aprovado)

2. **Produtos Com Risco**:
   - Óleo Neurológico Forte (THC: 0.8%, Neurologia, Pendente)
   - Medicamento Pediátrico Especial (THC: 0.5%, Pediatria, Pendente)
   - Tratamento Neurológico Avançado (THC: 1.2%, Neurologia, Reprovado)

3. **Produtos com THC Alto mas Sem Risco**:
   - Óleo Dermatológico Forte (THC: 0.6%, Dermatologia, Pendente)
   - Medicamento Oncológico Especial (THC: 0.9%, Oncologia, Pendente)

## 👨‍💻 Autor

**Victor Ruiz Scarassati**

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---
