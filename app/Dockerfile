# Usar imagem base Python oficial
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (para cache de layers)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app.py .

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expor porta
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando para executar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "30", "app:app"]
