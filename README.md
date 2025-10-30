# Core User Service – Visiobook# Core User Service – Visiobook

Microservice **User Service** du projet Visiobook.Microservice **User Service** du projet Visiobook.

Développé avec **Python 3.12.6** et **FastAPI**, il gère l'authentification, la gestion des utilisateurs et leurs rôles avec une base de données **PostgreSQL**.Développé avec **Python 3.12.6** et **FastAPI**, il gère l'authentification, la gestion des utilisateurs et leurs rôles avec une base de données **PostgreSQL**.

---

## 🚀 Features## 🚀 Features

- **API REST** en FastAPI avec documentation automatique- **API REST** en FastAPI avec documentation automatique

- **Base de données PostgreSQL** avec migrations Alembic- **Base de données PostgreSQL** avec migrations Alembic

- **Modèles SQLAlchemy 2.0** avec types modernes (Mapped[])- **Modèles SQLAlchemy 2.0** avec types modernes (Mapped[])

- **Gestion des utilisateurs** (CRUD, rôles : admin, user, moderator)- **Gestion des utilisateurs** (CRUD, rôles : admin, user, moderator)

- **Endpoints de healthcheck** (`/health`, `/ready`)- **Endpoints de healthcheck** (`/health`, `/ready`)

- **Authentification JWT** et hashage de mots de passe sécurisé- **Authentification JWT** et hashage de mots de passe sécurisé

- **Configuration externalisée** via `.env`- **Configuration externalisée** via `.env`

- **Tests automatisés** avec pytest et couverture- **Tests automatisés** avec pytest et couverture

- **Qualité de code parfaite** : Pylint 10/10, MyPy strict, Ruff- **Qualité de code parfaite** : Pylint 10/10, MyPy strict, Ruff

- **CI/CD GitHub Actions** complet- **CI/CD GitHub Actions** complet

- **Docker** multi-stage (dev/prod)- **Docker** multi-stage (dev/prod)

---

## 📊 Qualité de Code## 📊 Qualité de Code

Un workflow GitHub Actions est configuré dans `.github/workflows/ci-cd.yml`.Un workflow GitHub Actions est configuré dans `.github/workflows/ci-cd.yml`.

Il s'exécute automatiquement sur chaque **Pull Request vers `dev`** :Il s'exécute automatiquement sur chaque **Pull Request vers `dev`** :

- ✅ **Formatage** : Black (format du code)- ✅ **Formatage** : Black (format du code)

- ✅ **Linting** : Ruff (imports + lint), Pylint (qualité parfaite 10/10)- ✅ **Linting** : Ruff (imports + lint), Pylint (qualité parfaite 10/10)

- ✅ **Types** : Mypy strict (0 erreurs)- ✅ **Types** : Mypy strict (0 erreurs)

- ✅ **Sécurité** : Pas de `print()`, `breakpoint()`, `pdb.set_trace()`- ✅ **Sécurité** : Pas de `print()`, `breakpoint()`, `pdb.set_trace()`

- ✅ **Tests** : Pytest avec couverture- ✅ **Tests** : Pytest avec couverture

- ✅ **Docker** : Build et push vers GitHub Container Registry- ✅ **Docker** : Build et push vers GitHub Container Registry

## 📦 Prérequis### Commandes Make disponibles

- Installer **uv** (installe aussi Python si besoin)````bash

  - macOS / Linux :make help # Affiche toutes les commandes disponibles

    ````bashmake install       # Installation complète (venv + dépendances)

    curl -LsSf https://astral.sh/uv/install.sh | shmake run           # Démarre le serveur de développement

    ```make test          # Lance les tests

    ````

  - Windows (PowerShell) :make coverage # Tests + couverture de code

    ````powershellmake fmt           # Formatage automatique (ruff --fix + black)

    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"make fmt-check     # Vérifie le formatage sans modification

    ```make lint          # Linting complet (ruff + pylint)
    ````

make ruff # Linting ruff uniquement

## 🛠️ Développement localmake typecheck # Vérification des types (mypy)

make security # Scan de sécurité (bandit + safety)

### 🚀 Setup rapidemake clean # Supprime l'environnement virtuel

make clean-all # Nettoyage complet (venv + caches)

`bash`stant, les données utilisateurs sont mockées via un fichier JSON (pas encore de base de données).Visiobook – Core User Service

# Clone et setup

git clone git@github.com:VisioBook-ESP/core-user-service.gitMicroservice **User Service** du projet Visiobook.

cd core-user-serviceDéveloppé avec **Python 3.13** et **FastAPI**, il gère l’authentification, la gestion des utilisateurs et leurs rôles.

Pour l’instant, les données utilisateurs sont mockées via un fichier JSON (pas encore de base de données).

# Installation + démarrage

make install---

make run

````## 🚀 Features



L'API sera disponible sur : http://localhost:8080- API REST en **FastAPI**

- Documentation : http://localhost:8080/api/docs- Gestion des **utilisateurs** (CRUD, rôles : admin, user, etc.)

- Health check : http://localhost:8080/health- Endpoints de **healthcheck** (`/health`, `/ready`)

- **Configuration externalisée** via `.env`

### 🧪 Validation complète avant push- **Tests automatisés** (unitaires + linting)

- **Linting & Typage strict** : Black, Ruff (lint + imports), Pylint, Mypy

```bash- **CI/CD GitHub Actions** (lint + tests + coverage)

# Installation des dépendances- **Dockerfile multi-stage** + `docker-compose.yml`

make install

---

# Formatage automatique

make fmt## 📦 Prérequis



# Vérification de la qualité (doit être 10/10)- Installer **uv** (installe aussi Python si besoin)

make lint  - macOS / Linux :

    ```bash

# Vérification des types (doit être 0 erreurs)    curl -LsSf https://astral.sh/uv/install.sh | sh

make typecheck      ```

  - Windows (PowerShell) :

# Tests avec couverture    ```powershell

make test    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

    ```

# Scan de sécurité

make security## 🛠️ Développement local

````

### 🚀 Setup rapide

## 📋 Commandes Make disponibles

````bash

```bash# Clone et setup

make help          # Affiche toutes les commandes disponiblesgit clone git@github.com:VisioBook-ESP/core-user-service.git

make install       # Installation complète (venv + dépendances)cd core-user-service

make run           # Démarre le serveur de développement

make test          # Lance les tests# Installation + démarrage

make coverage      # Tests + couverture de codemake install

make fmt           # Formatage automatique (ruff --fix + black)make run

make fmt-check     # Vérifie le formatage sans modification```

make lint          # Linting complet (ruff + pylint)

make ruff          # Linting ruff uniquementL'API sera disponible sur : http://localhost:8080

make typecheck     # Vérification des types (mypy)- Documentation : http://localhost:8080/api/docs

make security      # Scan de sécurité (bandit + safety)- Health check : http://localhost:8080/health

make clean         # Supprime l'environnement virtuel

make clean-all     # Nettoyage complet (venv + caches)### 🧪 Validation complète avant push

````

```````bash

## 📚 API Documentation# Installation des dépendances

make install

Une fois le service démarré, la documentation interactive est disponible :

# Formatage automatique

- **Swagger UI** : http://localhost:8080/api/docsmake fmt

- **ReDoc** : http://localhost:8080/api/redoc

- **OpenAPI Schema** : http://localhost:8080/api/openapi.json# Vérification de la qualité (doit être 10/10)

make lint

### Endpoints disponibles

# Vérification des types (doit être 0 erreurs)

| Endpoint | Méthode | Description |make typecheck

|----------|---------|-------------|

| `/health` | GET | Health check du service |# Tests avec couverture

| `/ready` | GET | Readiness check |make test

| `/api/v1/users/` | GET | Liste des utilisateurs |

| `/api/v1/users/` | POST | Créer un utilisateur |# Scan de sécurité

| `/api/v1/users/{user_id}` | GET | Récupérer un utilisateur |make security

| `/api/v1/users/{user_id}` | PUT | Modifier un utilisateur |```

| `/api/v1/users/{user_id}` | DELETE | Supprimer un utilisateur |

## 📋 Commandes Make disponibles

## 🏗️ Architecture technique

```bash

### Stack technologiquemake help          # Affiche toutes les commandes disponibles

make install       # Installation complète (venv + dépendances)

- **Framework** : FastAPI 0.115+make run           # Démarre le serveur de développement

- **Base de données** : PostgreSQL 15make test          # Lance les tests

- **ORM** : SQLAlchemy 2.0 avec syntaxe modernemake coverage      # Tests + couverture de code

- **Migrations** : Alembicmake fmt           # Formatage automatique (ruff --fix + black)

- **Tests** : Pytest + Coveragemake fmt-check     # Vérifie le formatage sans modification

- **Sécurité** : JWT + bcryptmake lint          # Linting complet (ruff + pylint)

- **Conteneurisation** : Docker + Docker Composemake ruff          # Linting ruff uniquement

make typecheck     # Vérification des types (mypy)

### Structure du projetmake security      # Scan de sécurité (bandit + safety)

make clean         # Supprime l'environnement virtuel

```make clean-all     # Nettoyage complet (venv + caches)

app/```

├── api/v1/              # API routes et controllers

├── core/                # Configuration et settings## 📦 Installation

│   ├── database.py      # Configuration DB et sessions

│   ├── security.py      # JWT et hash passwords### 1. Cloner le repo

│   └── settings.py      # Variables d'environnement

├── models/              # Modèles SQLAlchemy```bash

│   ├── base.py          # Modèle de basegit clone git@github.com:VisioBook-ESP/core-user-service.git

│   └── user.py          # User et Profile modelscd core-user-service

├── schemas/             # Schémas Pydantic (DTOs)```

├── services/            # Logique métier

│   ├── user_service.py         # Service JSON (mock)### macOS / Linux (bash/zsh)

│   └── database_user_service.py # Service PostgreSQL

├── middleware/          # Middlewares (futures)```bash

├── types/               # Types partagéspython3.12 -m venv .venv

├── utils/               # Utilitairessource .venv/bin/activate

└── main.py             # Point d'entrée FastAPIpip install -U pip

pip install -r requirements.txt

alembic/                 # Migrations de base de données```

tests/                   # Tests automatisés

docker/                  # Dockerfiles dev/prod### Windows (PowerShell)

.github/workflows/       # CI/CD GitHub Actions

``````powershell

py -3.12 -m venv .venv

## 🐳 Docker.\.venv\Scripts\Activate.ps1

python -m pip install -U pip

### Développementpip install -r requirements.txt

```````

````bash

# Démarrer avec PostgreSQL### Windows (CMD)

docker compose up --build

```cmd

# Voir les logspy -3.12 -m venv .venv

docker compose logs -f.venv\Scripts\activate.bat

python -m pip install -U pip

# Arrêterpip install -r requirements.txt

docker compose down```

````

### 3. Configuration

### Production

Copier `.env.example` vers `.env` et ajuster les variables :

````bash

# Build et déploiement production```bash

docker compose -f docker-compose-prod.yml up --build -dcp .env.example .env

````

## 🔒 Sécurité## ▶️ Démarrage

- **Variables sensibles** jamais en dur dans le code (utilisation de `.env`)### Option 1 : Avec le Makefile (recommandé)

- **Vérifications automatiques** avec :

  - `bandit` : Analyse du code source pour les vulnérabilités```bash

  - `safety` : Scan des dépendances pour les CVE connus# Installation complète + démarrage

  - `pip-audit` : Audit moderne des packagesmake install

- **Pas de debug** en production (interdiction de `print()`, `breakpoint()`, etc.)make run

- **Configuration CORS** et **JWT**```

## 🚀 Workflow de développement### Option 2 : Mode développement manuel

### Avant de pusher```bash

# Activer l'environnement virtuel

````bashsource .venv/bin/activate  # Linux/macOS

# 1. Formatage automatique# ou .venv\Scripts\activate.bat  # Windows

make fmt

# Démarrer le serveur de développement

# 2. Vérification qualité (DOIT être 10/10)uvicorn app.main:app --reload --port 8080

make lint```



# 3. Vérification types (DOIT être 0 erreurs)  ### Option 3 : Avec Docker

make typecheck

```bash

# 4. Tests (DOIT passer)# Build et run en mode développement

make testdocker compose up --build



# 5. Sécurité (DOIT être clean)# Ou en mode production

make securitydocker compose -f docker-compose-prod.yml up --build

````

# 6. Si tout est vert ✅

git add .## 🧪 Tests & Qualité de code

git commit -m "feat: description du changement"

git push origin ma-branche### Tests

````

```bash

### Standards de qualité# Lancer tous les tests

make test

- **Pylint** : Score 10.00/10 (obligatoire)# ou

- **MyPy** : 0 erreurs en mode strict (obligatoire)pytest

- **Ruff** : Aucune erreur de linting (obligatoire)

- **Tests** : Tous les tests passent (obligatoire)# Tests avec couverture de code

- **Couverture** : Minimum 30% (en progression)make coverage

- **Sécurité** : Aucune vulnérabilité détectée# ou

pytest --cov=app --cov-report=term-missing --cov-fail-under=80

## 👩‍💻 Contributeurs```



- **Marine** (Core Developer, User Service)### Formatage et linting



## 📝 Licence```bash

# Formatage automatique (ruff + black)

Ce projet est développé dans le cadre du projet Epitech T-ESP Visiobook.make fmt

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
````

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
