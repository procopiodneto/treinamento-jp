# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Device management application with a FastAPI backend and Streamlit frontend, running in Docker containers with PostgreSQL database.

## Architecture

```
treinamento-jp/
├── fastapi/          # REST API backend
│   └── main.py       # SQLModel ORM with Device CRUD endpoints
├── streamlit/        # Web UI frontend
│   ├── streamlit_pages.py  # Page navigation entry point
│   ├── home_page.py        # Device listing
│   ├── pagina_cadastro.py  # Device creation form
│   └── pagina_ajustes.py   # Device update/delete
└── docker-compose.yml
```

**Service communication:** Streamlit connects to FastAPI via container name `http://fastAPI_devices:8000`

## Commands

### Start all services
```bash
cd treinamento-jp
docker compose up --build
```

### Access points
- Streamlit UI: http://localhost:8501
- FastAPI: http://localhost:8000
- API docs: http://localhost:8000/docs

### Environment
Requires `.env` file in `treinamento-jp/` with:
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /devices/ | Create device |
| GET | /devices/ | List devices (pagination: offset, limit) |
| GET | /devices/{id} | Get single device |
| PATCH | /devices/{id} | Update device fields |
| DELETE | /devices/{id} | Delete device |

## Data Model

**Device**: `id`, `nome` (indexed), `uptime` (default 0, indexed), `contrato`
