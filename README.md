# 🧩 Visiobook – Core User Service

Microservice **User Service** du projet Visiobook.  
Développé avec **Python 3.13** et **FastAPI**, il gère l’authentification, la gestion des utilisateurs et leurs rôles.  
Pour l’instant, les données utilisateurs sont mockées via un fichier JSON (pas encore de base de données).

---

## 🚀 Features

- API REST en **FastAPI**
- Gestion des **utilisateurs** (CRUD, rôles : admin, user, etc.)
- Endpoints de **healthcheck** (`/health`, `/ready`)
- **Configuration externalisée** via `.env`
- **Tests automatisés** (unitaires + linting)
- **Linting & Typage strict** : Black, isort, Pylint, Mypy
- **CI/CD GitHub Actions** (lint + tests + coverage)
- **Dockerfile multi-stage** + `docker-compose.yml`

---

## 📦 Installation

### 1. Cloner le repo

```bash
git clone git@github.com:VisioBook-ESP/core-user-service.git
cd core-user-service
```

### macOS / Linux (bash/zsh)

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .

```

### Windows(PowerShell)

```bash
py -3.13 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -U pip
pip install -e .
```

### Windows(CMD)

```bash
py -3.13 -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install -U pip
pip install -e .
```

### 3. Installer les dépendances

```bash
pip install -U pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Configuration

Copier `.env.example` vers `.env` et ajuster les variables :

```bash
cp .env.example .env
```

## ▶️ Démarrage

### Mode développement

```bash
uvicorn app.main:app --reload --port 8080
```

### Mode production (Docker)

```bash
docker build -t core-user-service:dev .
docker run -p 8080:8080 core-user-service:dev
```

### Avec docker-compose

```bash
docker compose up --build
```

## 🧪 Tests

### Lancer tous les tests

```bash
pytest
```

### Lancer avec couverture

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

### Vérifier les lints manuellement

```bash
black app .tests
isort app .tests
pylint app
mypy app
```

## ⚡ CI/CD

Un workflow GitHub Actions est configuré dans .github/workflows/ci-cd.yml.
Il s’exécute automatiquement sur chaque push et pull request :

- Installe les dépendances
- Vérifie le formatage (Black, isort)
- Vérifie le linting (Pylint)
- Vérifie le typage (Mypy)
- Lance les tests Pytest avec couverture
- Fait un scan de sécurité (Bandit, Safety)

## 📚 API Documentation

## Endpoints disponibles (MVP)

- GET /health → Vérifie l’état du service
- GET /ready → Vérifie si le service est prêt
- GET /api/v1/users → Récupère la liste des utilisateurs (mock JSON)
- POST /api/v1/users → Crée un utilisateur (mock JSON)
- POST /api/v1/auth/login → Authentifie un utilisateur (mock JSON + JWT futur)

## 🗂 Structure du projet

app/
├── api/v1/ # Routers / Controllers (endpoints FastAPI)
├── services/ # Logique métier
├── schemas/ # Pydantic models (DTO)
├── middleware/ # Middlewares (ex: auth, logs)
├── utils/ # Fonctions utilitaires
├── core/ # Settings, config, logging
├── types/ # Types partagés
└── main.py # Entrée principale FastAPI
.tests/
├── unit/ # Tests unitaires
└── integration/ # Tests d’intégration (futurs)
.github/
└── workflows/ci-cd.yml # CI/CD GitHub Actions
Dockerfile
docker-compose.yml
requirements.txt
requirements-dev.txt
.env.example
README.md

## 🔒 Sécurité

Variables sensibles jamais en dur dans le code

Vérifications automatiques avec :

- bandit
- safety
- Config CORS et JWT (à venir)
- Pas de logs sensibles

## 👩‍💻 Contributeurs

- **Marine** (Core Developer, User Service)
