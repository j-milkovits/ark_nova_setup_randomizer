FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.8.3 /uv /uvx /bin/

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/ark_nova_setup_randomizer/frontend/entrypoint.py", "--server.port=8501", "--server.address=0.0.0.0"]
