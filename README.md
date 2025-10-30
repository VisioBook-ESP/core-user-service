# Microservice **User Service** Développé avec **Python 3.12.6** et **FastAPI**, il gère l'authentification, la gestion des utilisateurs et leurs rôles.u projet Visiobook.

Développé avec **Python 3.12.6** et **FastAPI**, il gère l'authentification, la gestion des utilisateurs et leurs rôles.  
Un workflow GitHub Actions est configuré dans `.github/workflows/ci-cd.yml`.
Il s'exécute automatiquement sur chaque **Pull Request vers `dev`** :

- ✅ **Formatage** : Black (format du code)
- ✅ **Linting** : Ruff (imports + lint), Pylint (qualité)
- ✅ **Types** : Mypy (vérification de types)
- ✅ **Sécurité** : Pas de `print()`, `breakpoint()`, `pdb.set_trace()` dans le code
- ✅ **Tests** : Pytest avec couverture (temporairement désactivé)
- ✅ **Docker** : Build et push vers GitHub Container Registry

### Commandes Make disponibles

````bash
make help          # Affiche toutes les commandes disponibles
make install       # Installation complète (venv + dépendances)
make run           # Démarre le serveur de développement
make test          # Lance les tests
make coverage      # Tests + couverture de code
make fmt           # Formatage automatique (ruff --fix + black)
make fmt-check     # Vérifie le formatage sans modification
make lint          # Linting complet (ruff + pylint)
make ruff          # Linting ruff uniquement
make typecheck     # Vérification des types (mypy)
make security      # Scan de sécurité (bandit + safety)
make clean         # Supprime l'environnement virtuel
make clean-all     # Nettoyage complet (venv + caches)
```stant, les données utilisateurs sont mockées via un fichier JSON (pas encore de base de données).Visiobook – Core User Service

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
- **Linting & Typage strict** : Black, Ruff (lint + imports), Pylint, Mypy
- **CI/CD GitHub Actions** (lint + tests + coverage)
- **Dockerfile multi-stage** + `docker-compose.yml`

---

## Prérequis

- Installer **uv** (installe aussi Python si besoin)
  - macOS / Linux :
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
  - Windows (PowerShell) :
    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

## Version de Python

Le projet force **Python 3.12.6** via `uv` et le `Makefile`.

## Setup & run

```bash
make install
make run
````

## 📦 Installation

### 1. Cloner le repo

```bash
git clone git@github.com:VisioBook-ESP/core-user-service.git
cd core-user-service
```

### macOS / Linux (bash/zsh)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

### Windows (CMD)

```cmd
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -U pip
pip install -r requirements.txt
```

### 3. Configuration

Copier `.env.example` vers `.env` et ajuster les variables :

```bash
cp .env.example .env
```

## ▶️ Démarrage

### Option 1 : Avec le Makefile (recommandé)

```bash
# Installation complète + démarrage
make install
make run
```

### Option 2 : Mode développement manuel

```bash
# Activer l'environnement virtuel
source .venv/bin/activate  # Linux/macOS
# ou .venv\Scripts\activate.bat  # Windows

# Démarrer le serveur de développement
uvicorn app.main:app --reload --port 8080
```

### Option 3 : Avec Docker

```bash
# Build et run en mode développement
docker compose up --build

# Ou en mode production
docker compose -f docker-compose-prod.yml up --build
```

## 🧪 Tests & Qualité de code

### Tests

```bash
# Lancer tous les tests
make test
# ou
pytest

# Tests avec couverture de code
make coverage
# ou
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

### Formatage et linting

```bash
# Formatage automatique (ruff + black)
make fmt

# Vérification sans modification
make fmt-check

# Linting complet (ruff + pylint)
make lint

# Correction automatique des erreurs ruff
make ruff-fix

# Vérification des types
make typecheck

# Scan de sécurité
make security
```

### Commandes individuelles

```bash
# Formatage
black app
ruff check app --fix

# Linting
ruff check app
pylint app
mypy app

# Sécurité
bandit -r app
safety scan -r requirements.txt
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
.env.example
README.md

## 🔒 Sécurité

- **Variables sensibles** jamais en dur dans le code (utilisation de `.env`)
- **Vérifications automatiques** avec :
  - `bandit` : Analyse du code source pour les vulnérabilités
  - `safety` : Scan des dépendances pour les CVE connus
  - `pip-audit` : Audit moderne des packages
- **Pas de debug** en production (interdiction de `print()`, `breakpoint()`, etc.)
- **Configuration CORS** et **JWT** (à venir)

## 🚀 Contribution

### Workflow de développement

1. **Clone** le repository
2. **Crée une branche** : `git checkout -b feature/ma-feature`
3. **Configure** l'environnement : `make install`
4. **Code** avec les outils de qualité : `make fmt`, `make lint`
5. **Teste** tes modifications : `make test`
6. **Commit** et **push** vers ta branche
7. **Crée une Pull Request** vers `dev`

### Avant de commit

```bash
# Formatage + linting + tests
make fmt
make lint
make test
make security
```

### Standards de qualité

- **Couverture de code** : minimum 80%
- **Formatage** : Black + Ruff
- **Linting** : Ruff + Pylint (score > 8/10)
- **Types** : Mypy strict mode
- **Sécurité** : Bandit + Safety sans vulnérabilité

## 👩‍💻 Contributeurs

- **Marine** (Core Developer, User Service)

## 📝 Licence

Ce projet est développé dans le cadre du projet Epitech T-ESP Visiobook.
