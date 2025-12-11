# Core User Service – Visiobook

Microservice **User Service** du projet Visiobook.

Développé avec **Python 3.12.6** et **FastAPI**, il gère l'authentification, la gestion des utilisateurs et leurs rôles avec une base de données **PostgreSQL**.

---

## 🚀 Features

- **API REST** en FastAPI avec documentation automatique
- **Base de données PostgreSQL** avec migrations Alembic
- **Modèles SQLAlchemy 2.0** avec types modernes (Mapped[])
- **Gestion des utilisateurs** (CRUD, rôles : admin, user, moderator)
- **Endpoints de healthcheck** (`/health`, `/ready`, `/health-db`)
- **Authentification JWT** et hashage de mots de passe sécurisé
- **Configuration externalisée** via `.env`
- **Tests automatisés** avec pytest et couverture
- **Qualité de code parfaite** : Pylint 10/10, MyPy strict, Ruff
- **CI/CD GitHub Actions** complet
- **Docker** multi-stage (dev/prod)

---

## 📦 Prérequis

- Installer **uv** (installe aussi Python si besoin)
  - macOS / Linux :
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
  - Windows (PowerShell) :
    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

---

## 🛠️ Développement local

### 🚀 Setup rapide

```bash
# Clone et setup
git clone git@github.com:VisioBook-ESP/core-user-service.git
cd core-user-service

# Installation + démarrage
make install
make run
```

L'API sera disponible sur : http://localhost:8080
- Documentation : http://localhost:8080/api/docs
- Health check : http://localhost:8080/health
- Database health : http://localhost:8080/health-db

### 🧪 Validation complète avant push

```bash
# Installation des dépendances
make install

# Formatage automatique
make fmt

# Vérification de la qualité (doit être 10/10)
make lint

# Vérification des types (doit être 0 erreurs)
make typecheck

# Tests avec couverture
make test

# Scan de sécurité
make security
```

### 📋 Commandes Make disponibles

```bash
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
```

---

## 🐳 Docker & Déploiement

### Développement avec Docker Compose

```bash
# Démarrer avec PostgreSQL
docker compose up --build

# Voir les logs
docker compose logs -f

# Arrêter
docker compose down
```

### 🚢 Déploiement Production (DevOps)

#### 1. Build de l'image de production

```bash
docker build -f docker/Dockerfile.prod -t core-user-service:latest .
```

#### 2. Variables d'environnement requises

```bash
DATABASE_URL=postgresql://user:password@host:5432/database_name
```

#### 3. Exécuter les migrations de base de données

**IMPORTANT** : Les migrations doivent être exécutées **AVANT** le premier démarrage de l'application et à chaque déploiement d'une nouvelle version.

```bash
# Option A : Commande Docker directe
docker run --rm \
  -e DATABASE_URL=postgresql://user:pass@host:5432/dbname \
  core-user-service:latest \
  alembic upgrade head

# Option B : Kubernetes initContainer
# Voir exemple ci-dessous
```

**Exemple de configuration Kubernetes avec initContainer :**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: core-user-service
spec:
  template:
    spec:
      initContainers:
      - name: migrations
        image: core-user-service:latest
        command: ["alembic", "upgrade", "head"]
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: database-url
      containers:
      - name: app
        image: core-user-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: database-url
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
```

#### 4. Lancer l'application

```bash
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/dbname \
  core-user-service:latest
```

#### 5. Vérifier le déploiement

```bash
# Health check de l'application
curl http://localhost:8080/health

# Health check de la base de données
curl http://localhost:8080/health-db

# Documentation API
curl http://localhost:8080/api/docs
```

#### 6. Commandes Alembic utiles

```bash
# Appliquer toutes les migrations
alembic upgrade head

# Voir l'état actuel des migrations
alembic current

# Voir l'historique des migrations
alembic history --verbose

# Revenir en arrière d'une migration
alembic downgrade -1

# Créer une nouvelle migration
alembic revision --autogenerate -m "Description"
```

#### 7. Debugging dans le container

Les outils suivants sont disponibles dans l'image de production pour le debugging :

```bash
# Entrer dans le container
docker exec -it <container-id> bash

# Tester la connectivité réseau
ping postgres
ping google.com

# Tester les endpoints HTTP
curl http://localhost:8080/health
curl http://localhost:8080/health-db

# Vérifier les migrations
alembic current
alembic history
```

---

## 📚 API Documentation

Une fois le service démarré, la documentation interactive est disponible :

- **Swagger UI** : http://localhost:8080/api/docs
- **ReDoc** : http://localhost:8080/api/redoc
- **OpenAPI Schema** : http://localhost:8080/api/openapi.json

### Endpoints disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/health` | GET | Health check du service |
| `/ready` | GET | Readiness check |
| `/health-db` | GET | Health check de la base de données |
| `/api/v1/users/` | GET | Liste des utilisateurs |
| `/api/v1/users/` | POST | Créer un utilisateur |
| `/api/v1/users/{user_id}` | GET | Récupérer un utilisateur |
| `/api/v1/users/{user_id}` | PUT | Modifier un utilisateur |
| `/api/v1/users/{user_id}` | DELETE | Supprimer un utilisateur |
| `/api/v1/auth/register` | POST | Inscription |
| `/api/v1/auth/login` | POST | Connexion (JWT) |

---

## 🏗️ Architecture technique

### Stack technologique

- **Framework** : FastAPI 0.115+
- **Base de données** : PostgreSQL 15
- **ORM** : SQLAlchemy 2.0 avec syntaxe moderne
- **Migrations** : Alembic
- **Tests** : Pytest + Coverage
- **Sécurité** : JWT + bcrypt
- **Conteneurisation** : Docker + Docker Compose

### Structure du projet

```
app/
├── api/v1/              # API routes et controllers
├── core/                # Configuration et settings
│   ├── database.py      # Configuration DB et sessions
│   ├── security.py      # JWT et hash passwords
│   └── settings.py      # Variables d'environnement
├── models/              # Modèles SQLAlchemy
│   ├── base.py          # Modèle de base
│   └── user.py          # User et Profile models
├── schemas/             # Schémas Pydantic (DTOs)
├── services/            # Logique métier
├── middleware/          # Middlewares
├── types/               # Types partagés
├── utils/               # Utilitaires
└── main.py             # Point d'entrée FastAPI

alembic/                 # Migrations de base de données
tests/                   # Tests automatisés
docker/                  # Dockerfiles dev/prod
.github/workflows/       # CI/CD GitHub Actions
```

---

## 📊 Qualité de Code

Un workflow GitHub Actions est configuré dans `.github/workflows/ci-cd.yml`.

Il s'exécute automatiquement sur chaque **Pull Request vers `dev`** :

- ✅ **Formatage** : Black (format du code)
- ✅ **Linting** : Ruff (imports + lint), Pylint (qualité parfaite 10/10)
- ✅ **Types** : Mypy strict (0 erreurs)
- ✅ **Sécurité** : Pas de `print()`, `breakpoint()`, `pdb.set_trace()`
- ✅ **Tests** : Pytest avec couverture
- ✅ **Docker** : Build et push vers GitHub Container Registry

### Standards de qualité

- **Pylint** : Score 10.00/10 (obligatoire)
- **MyPy** : 0 erreurs en mode strict (obligatoire)
- **Ruff** : Aucune erreur de linting (obligatoire)
- **Tests** : Tous les tests passent (obligatoire)
- **Couverture** : Minimum 80%
- **Sécurité** : Aucune vulnérabilité détectée

---

## 🔒 Sécurité

- **Variables sensibles** jamais en dur dans le code (utilisation de `.env`)
- **Vérifications automatiques** avec :
  - `bandit` : Analyse du code source pour les vulnérabilités
  - `safety` : Scan des dépendances pour les CVE connus
  - `pip-audit` : Audit moderne des packages
- **Pas de debug** en production (interdiction de `print()`, `breakpoint()`, etc.)
- **Configuration CORS** et **JWT**

---

## 🚀 Workflow de développement

### Avant de pusher

```bash
# 1. Formatage automatique
make fmt

# 2. Vérification qualité (DOIT être 10/10)
make lint

# 3. Vérification types (DOIT être 0 erreurs)
make typecheck

# 4. Tests (DOIT passer)
make test

# 5. Sécurité (DOIT être clean)
make security

# 6. Si tout est vert ✅
git add .
git commit -m "feat: description du changement"
git push origin ma-branche
```

---

## 👩‍💻 Contributeurs

- **Marine** (Core Developer, User Service)

---

## 📝 Licence

Ce projet est développé dans le cadre du projet Epitech T-ESP Visiobook.
