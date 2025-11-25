#!/bin/bash

echo "🔄 Aguardando PostgreSQL..."

# Wait for PostgreSQL to be ready
while ! pg_isready -h postgres -p 5432 -U metas_user > /dev/null 2>&1; do
    sleep 1
done

echo "✅ PostgreSQL está pronto!"
echo "🔄 Executando migrations..."

# Run Alembic migrations
cd /app
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migrations aplicadas com sucesso!"
else
    echo "❌ Erro ao aplicar migrations!"
    exit 1
fi

echo "🚀 Iniciando servidor FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
