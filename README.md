# Sistema de Cadastramento de Metas

Sistema completo para cadastramento e gerenciamento de metas e objetivos de negócio.

## 🚀 Stack Tecnológica

### Backend
- **FastAPI** - Framework Python moderno e rápido
- **SQLAlchemy** - ORM para PostgreSQL
- **PostgreSQL** - Banco de dados relacional
- **JWT** - Autenticação e autorização
- **Pandas** - Processamento de arquivos Excel/CSV

### Frontend
- **Angular 17** - Framework TypeScript
- **PrimeNG** - Biblioteca de componentes UI
- **PrimeFlex** - Sistema de grid CSS
- **RxJS** - Programação reativa

### DevOps
- **Docker** - Containerização completa
- **Docker Compose** - Orquestração de containers

## 📋 Pré-requisitos

- **Docker** (versão 20.10 ou superior)
- **Docker Compose** (versão 2.0 ou superior)

**Apenas isso!** Não é necessário instalar Python, Node.js, Angular CLI ou PostgreSQL localmente.

## 🔧 Instalação e Execução

### 1. Clone o repositório (ou já está na pasta)

```bash
cd cadastramento_metas
```

### 2. Iniciar todos os serviços

```bash
docker-compose up --build
```

**Aguarde alguns minutos na primeira vez** (download de imagens e instalação de dependências).

### 3. Acessar a aplicação

Após todos os containers iniciarem:

- **Frontend Angular**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **Documentação API (Swagger)**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

### 4. Parar os serviços

```bash
docker-compose down
```

### 5. Parar e limpar volumes (dados do banco)

```bash
docker-compose down -v
```

## 🛠️ Desenvolvimento

### Editar Código

Você pode editar os arquivos normalmente no VS Code:

- **Backend**: Edite arquivos em `backend/` - O servidor reinicia automaticamente (hot reload)
- **Frontend**: Edite arquivos em `frontend/src/` - O Angular recompila automaticamente (hot reload)

**Não precisa reiniciar os containers!** As alterações são refletidas automaticamente.

### Estrutura do Projeto

```
cadastramento_metas/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── api/               # Rotas da API
│   │   ├── models/            # Modelos SQLAlchemy (tabelas)
│   │   ├── schemas/           # Schemas Pydantic (validação)
│   │   ├── services/          # Lógica de negócio
│   │   └── core/              # Configurações
│   │       ├── config.py      # Variáveis de ambiente
│   │       ├── database.py    # Conexão com banco
│   │       └── security.py    # JWT e senhas
│   ├── main.py                # Arquivo principal FastAPI
│   ├── requirements.txt       # Dependências Python
│   └── Dockerfile
│
├── frontend/                   # Frontend Angular
│   ├── src/
│   │   ├── app/               # Componentes Angular
│   │   ├── assets/            # Imagens, arquivos estáticos
│   │   ├── environments/      # Configurações de ambiente
│   │   ├── index.html
│   │   ├── main.ts
│   │   └── styles.scss
│   ├── angular.json
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
│
├── docker-compose.yml         # Orquestração dos containers
├── .gitignore
└── README.md
```

## 📝 Próximos Passos para Desenvolvimento

### 1. Criar Models (Backend)

Edite `backend/app/models/` e crie suas tabelas:

- `user.py` - Usuários do sistema
- `gerente_negocio.py` - Gerentes de negócio
- `objetivo.py` - Objetivos
- `indicador.py` - Indicadores

### 2. Criar Schemas (Backend)

Edite `backend/app/schemas/` para validação de dados.

### 3. Criar Rotas da API (Backend)

Edite `backend/app/api/` e crie endpoints REST.

### 4. Criar Componentes (Frontend)

```bash
# Entre no container do frontend
docker-compose exec frontend sh

# Gere componentes Angular
ng generate component components/login
ng generate component components/dashboard
ng generate service services/auth
```

### 5. Instalar Bibliotecas Adicionais

**Backend (Python):**

Edite `backend/requirements.txt` e adicione a biblioteca, depois:

```bash
docker-compose restart backend
```

**Frontend (Node):**

Edite `frontend/package.json` e adicione a biblioteca, depois:

```bash
docker-compose restart frontend
```

## 🗄️ Banco de Dados

### Migrations com Alembic

O projeto usa **Alembic** para gerenciar alterações no banco de dados de forma versionada.

**Migrations são aplicadas automaticamente** quando o backend inicia!

#### Criar nova migration:

```bash
# Entre no container backend
docker-compose exec backend bash

# Depois de criar/editar models em app/models/
alembic revision --autogenerate -m "descrição da mudança"

# Aplicar migrations
alembic upgrade head
```

#### Comandos úteis:

```bash
# Ver histórico
alembic history

# Ver migration atual
alembic current

# Reverter última migration
alembic downgrade -1
```

**📖 Guia completo:** Veja `backend/MIGRATIONS.md` para tutorial detalhado

### Acessar PostgreSQL

```bash
docker-compose exec postgres psql -U metas_user -d cadastramento_metas
```

### Credenciais do Banco

- **Host**: localhost (ou `postgres` dentro dos containers)
- **Porta**: 5432
- **Usuário**: metas_user
- **Senha**: metas_password
- **Database**: cadastramento_metas

### Workflow: Criar Models e Aplicar no Banco

1. **Crie o model** em `backend/app/models/`:
   ```python
   # app/models/user.py
   from sqlalchemy import Column, Integer, String
   from app.core.database import Base
   
   class User(Base):
       __tablename__ = "users"
       id = Column(Integer, primary_key=True)
       nome = Column(String)
   ```

2. **Importe no Alembic** (`backend/alembic/env.py`):
   ```python
   from app.models.user import User
   ```

3. **Gere a migration**:
   ```bash
   docker-compose exec backend bash
   alembic revision --autogenerate -m "create users table"
   alembic upgrade head
   ```

Pronto! Tabela criada no PostgreSQL.

### Migrations (Alembic)

Para criar migrations:

```bash
# Entre no container do backend
docker-compose exec backend sh

# Inicialize Alembic (apenas uma vez)
alembic init alembic

# Crie uma migration
alembic revision --autogenerate -m "create initial tables"

# Execute migrations
alembic upgrade head
```

## 🔐 Autenticação

O sistema está preparado para JWT. Exemplos em `backend/app/core/security.py`.

## 📊 Upload de Arquivos Excel/CSV

Bibliotecas já instaladas:
- `pandas` - Processar dados
- `openpyxl` - Ler Excel (.xlsx)
- `xlrd` - Ler Excel antigo (.xls)

## 🐛 Troubleshooting

### Porta já em uso

Se alguma porta (4200, 8000, 5432) já estiver em uso, edite `docker-compose.yml` e altere:

```yaml
ports:
  - "NOVA_PORTA:PORTA_CONTAINER"
```

### Limpar tudo e recomeçar

```bash
docker-compose down -v
docker-compose up --build
```

### Ver logs de um serviço

```bash
# Backend
docker-compose logs -f backend

# Frontend
docker-compose logs -f frontend

# Banco
docker-compose logs -f postgres
```

### Executar comandos dentro dos containers

```bash
# Backend (Python)
docker-compose exec backend sh

# Frontend (Node)
docker-compose exec frontend sh

# PostgreSQL
docker-compose exec postgres psql -U metas_user -d cadastramento_metas
```

## 📦 Deploy (Produção)

Para produção, ajuste:

1. Altere `SECRET_KEY` em `docker-compose.yml`
2. Configure `DEBUG: "False"` no backend
3. Use build de produção do Angular (edite `frontend/Dockerfile`)
4. Configure HTTPS com proxy reverso (Nginx)

## 🤝 Suporte

Documentação das tecnologias:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Angular](https://angular.io/docs)
- [PrimeNG](https://primeng.org/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Docker](https://docs.docker.com/)

---

**Desenvolvido com 💙 usando FastAPI + Angular + PostgreSQL**
