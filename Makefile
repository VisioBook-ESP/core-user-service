# ====== Config ======
PYTHON_VERSION := 3.12.6
VENV_DIR := .venv

# Binaries selon l'OS
PY := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
UVICORN := $(VENV_DIR)/bin/uvicorn
PYTEST := $(VENV_DIR)/bin/pytest
RUFF := $(VENV_DIR)/bin/ruff
BLACK := $(VENV_DIR)/bin/black
PYLINT := $(VENV_DIR)/bin/pylint
MYPY := $(VENV_DIR)/bin/mypy
BANDIT := $(VENV_DIR)/bin/bandit
SAFETY := $(VENV_DIR)/bin/safety

ifeq ($(OS),Windows_NT)
	PY := .\.venv\Scripts\python.exe
	PIP := .\.venv\Scripts\pip.exe
	UVICORN := .\.venv\Scripts\uvicorn.exe
	PYTEST := .\.venv\Scripts\pytest.exe
	RUFF := .\.venv\Scripts\ruff.exe
	BLACK := .\.venv\Scripts\black.exe
	PYLINT := .\.venv\Scripts\pylint.exe
	MYPY := .\.venv\Scripts\mypy.exe
	BANDIT := .\.venv\Scripts\bandit.exe
	SAFETY := .\.venv\Scripts\safety.exe
endif

# ====== Phonies ======
.PHONY: help venv install run test coverage fmt fmt-check lint lint-fix ruff ruff-fix typecheck security clean clean-all check-uv

help:
	@echo "Targets:"
	@echo "  make install   -> venv (Python $(PYTHON_VERSION)) + deps"
	@echo "  make run       -> lance FastAPI (uvicorn app.main:app)"
	@echo "  make test      -> pytest"
	@echo "  make coverage  -> pytest + couverture"
	@echo "  make fmt       -> ruff --fix + black"
	@echo "  make fmt-check -> vérifie format"
	@echo "  make lint      -> ruff + pylint"
	@echo "  make lint-fix  -> ruff --fix"
	@echo "  make ruff      -> ruff check ."
	@echo "  make ruff-fix  -> ruff check . --fix"
	@echo "  make typecheck -> mypy"
	@echo "  make security  -> bandit (+ safety si requirements.txt)"
	@echo "  make clean     -> supprime .venv"
	@echo "  make clean-all -> .venv + caches"

# ====== Setup ======
venv: check-uv
	@echo ">> Creating venv with Python $(PYTHON_VERSION)"
	uv venv --clear --python $(PYTHON_VERSION) $(VENV_DIR)
	$(PY) -m ensurepip --upgrade
	$(PY) -m pip install --upgrade pip setuptools wheel
	@echo "✅ venv ready: $$($(PY) --version)"


install: venv
	@if [ -f requirements.txt ]; then \
		echo ">> Installing deps from requirements.txt"; \
		$(PIP) install -r requirements.txt; \
	else \
		echo ">> Installing minimal dev deps"; \
		$(PIP) install fastapi \"uvicorn[standard]\" pytest pytest-cov ruff black mypy pylint bandit safety python-dotenv; \
	fi

# ====== Run / Test ======
run:
	@echo ">> Starting FastAPI on http://0.0.0.0:8000  (docs: /docs)"
	@if [ -f .env ]; then \
		$(PY) -m dotenv -f .env run -- $(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000; \
	else \
		$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000; \
	fi

test:
	@echo ">> Running tests..."
	$(PYTEST) -v

coverage:
	@echo ">> Running tests with coverage..."
	$(PYTEST) --cov=app --cov-report=term-missing

# ====== Qualité de code ======
fmt:
	@echo ">> ruff --fix + black"
	$(RUFF) check . --fix
	$(BLACK) .

fmt-check:
	$(RUFF) check .
	$(BLACK) --check .

lint:
	@echo ">> Ruff"
	$(RUFF) check .
	@echo ">> Pylint (app/)"
	PYTHONPATH=$(shell pwd) $(PYLINT) app

lint-fix:
	$(RUFF) check . --fix

ruff:
	$(RUFF) check .

ruff-fix:
	$(RUFF) check . --fix

typecheck:
	$(MYPY) app

security:
	@echo ">> Bandit (code security)"
	$(BANDIT) -q -r app
	@if [ -f requirements.txt ]; then \
		echo ">> Safety (dependency vulnerabilities)"; \
		$(SAFETY) scan -r requirements.txt || true; \
	else \
		echo ">> Safety skipped (no requirements.txt)"; \
	fi

# ====== Clean ======
clean:
	rm -rf $(VENV_DIR)

clean-all: clean
	find . -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache .ruff_cache .pytest_cache .coverage htmlcov

# ====== Utils ======
check-uv:
	@command -v uv >/dev/null 2>&1 || { \
		echo "❌ 'uv' non trouvé."; \
		echo "Installe-le : https://docs.astral.sh/uv/install/"; \
		exit 1; \
	}
