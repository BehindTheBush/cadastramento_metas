# 🗄️ Guia de Migrations com Alembic

## O que é Alembic?

Alembic é uma ferramenta de versionamento de banco de dados para SQLAlchemy. Ele permite:
- Criar e aplicar alterações no banco de forma controlada
- Gerar migrations automaticamente a partir dos models
- Fazer rollback de alterações
- Manter histórico de mudanças no schema

---

## 📝 Comandos Principais

### 1. Criar uma nova migration (automática)

Depois de criar ou modificar seus models em `app/models/`, gere a migration:

```bash
# Dentro do container backend
alembic revision --autogenerate -m "descrição da mudança"
```

**Exemplo:**
```bash
alembic revision --autogenerate -m "create users table"
alembic revision --autogenerate -m "add gerentes and objetivos tables"
```

### 2. Aplicar migrations (upgrade)

```bash
# Aplicar todas as migrations pendentes
alembic upgrade head

# Aplicar até uma revisão específica
alembic upgrade <revision_id>

# Aplicar próxima migration
alembic upgrade +1
```

### 3. Reverter migrations (downgrade)

```bash
# Reverter última migration
alembic downgrade -1

# Reverter até uma revisão específica
alembic downgrade <revision_id>

# Reverter tudo
alembic downgrade base
```

### 4. Ver histórico de migrations

```bash
# Ver histórico completo
alembic history

# Ver migrations aplicadas
alembic current

# Ver migrations pendentes
alembic history --verbose
```

---

## 🔧 Workflow de Desenvolvimento

### Passo 1: Criar/Editar Models

Crie ou edite seus models em `backend/app/models/`:

```python
# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    nome = Column(String)
    senha_hash = Column(String)
    nivel_acesso = Column(String)  # 'admin' ou 'cadastrador'
    ativo = Column(Boolean, default=True)
```

### Passo 2: Importar no env.py

Edite `backend/alembic/env.py` e descomente/adicione o import:

```python
# Import all models here
from app.models.user import User
from app.models.gerente_negocio import GerenteNegocio
from app.models.objetivo import Objetivo
# ...
```

### Passo 3: Gerar Migration

```bash
# Entre no container
docker-compose exec backend bash

# Gere a migration
alembic revision --autogenerate -m "create users table"
```

### Passo 4: Revisar Migration

Alembic cria o arquivo em `backend/alembic/versions/`. **SEMPRE revise** o arquivo gerado!

### Passo 5: Aplicar Migration

```bash
alembic upgrade head
```

---

## 🐳 Uso com Docker

### Migrations são aplicadas automaticamente!

O `entrypoint.sh` executa `alembic upgrade head` toda vez que o backend inicia.

### Comandos úteis no Docker:

```powershell
# Ver logs do backend (migrations incluídas)
docker-compose logs backend

# Entrar no container backend
docker-compose exec backend bash

# Dentro do container, rodar comandos alembic:
alembic history
alembic current
alembic revision --autogenerate -m "nova migration"
```

### Forçar recriação das migrations:

```powershell
# Parar containers
docker-compose down

# Limpar volumes (CUIDADO: apaga dados!)
docker-compose down -v

# Subir novamente (migrations serão aplicadas)
docker-compose up --build
```

---

## 📚 Exemplos Práticos

### Criar tabela de usuários:

```bash
# 1. Criar model em app/models/user.py
# 2. Importar em alembic/env.py
# 3. Gerar migration
alembic revision --autogenerate -m "create users table"

# 4. Aplicar
alembic upgrade head
```

### Adicionar coluna em tabela existente:

```bash
# 1. Editar model (adicionar Column)
# 2. Gerar migration
alembic revision --autogenerate -m "add phone column to users"

# 3. Aplicar
alembic upgrade head
```

### Reverter última alteração:

```bash
alembic downgrade -1
```

---

## ⚠️ Boas Práticas

1. **Sempre revise migrations geradas** - Alembic nem sempre detecta tudo perfeitamente
2. **Nunca edite migrations já aplicadas** - Crie uma nova migration para corrigir
3. **Use mensagens descritivas** - `alembic revision -m "add index to email column"`
4. **Teste antes de production** - Faça downgrade/upgrade para garantir que funciona
5. **Commits separados** - Commite migrations separadamente do código

---

## 🆘 Troubleshooting

### "Target database is not up to date"

```bash
alembic upgrade head
```

### "Can't locate revision identified by..."

```bash
# Limpar histórico e recomeçar
alembic stamp head
```

### Migrations não detectam mudanças

- Verifique se o model foi importado em `alembic/env.py`
- Verifique se está usando `Base` corretamente
- Tente migration manual: `alembic revision -m "manual migration"`

---

## 📖 Documentação Oficial

- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Auto Generating Migrations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
