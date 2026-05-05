# 💰 FinanceOS — Personal Finance Management System

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?style=flat-square&logo=django)
![DRF](https://img.shields.io/badge/DRF-REST%20API-red?style=flat-square)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=flat-square&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black?style=flat-square&logo=githubactions)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

> A robust, scalable and decoupled personal finance management system — built with professional engineering practices for real-world portfolio demonstration.

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Layer Responsibilities](#-layer-responsibilities)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Running Tests](#-running-tests)
- [CI/CD Pipeline](#-cicd-pipeline)
- [API Documentation](#-api-documentation)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📌 About the Project

**FinanceOS** is a personal finance management system designed with a focus on clean architecture, maintainability, and scalability. The system provides a financial dashboard, spending rules, goal tracking, and reporting tools — all accessible via a REST API consumed by a modern SPA frontend.

This project follows industry-standard engineering practices:

- **Feature-Based Layered Architecture** — each feature is fully isolated
- **Separation of Concerns** — data, business logic, and presentation never mix
- **Test-Driven mindset** — each layer is independently testable
- **CI/CD** — automated linting, testing, and deployment on every push
- **MVP-first, iterative delivery** — built in incremental, documented layers

---

## ✨ Features

### ✅ MVP — Layer 1 (Foundation)
- [x] Project scaffold (Django + DRF + PostgreSQL + Docker)
- [x] JWT Authentication (register, login, token refresh)
- [x] CI/CD pipeline with GitHub Actions
- [x] Swagger API documentation

### 🚧 Layer 2 — Core Finance
- [ ] Transactions (income & expenses)
- [ ] Custom categories and subcategories
- [ ] Filtering, sorting, and pagination

### 📊 Layer 3 — Dashboard & Reports
- [ ] Monthly summary (balance, income, expenses)
- [ ] Interactive charts
- [ ] PDF / CSV export

### 🔔 Layer 4 — Rules & Intelligence
- [ ] Spending rules per category (e.g. max 30% on leisure)
- [ ] Budget limit alerts
- [ ] Financial goals with visual progress

### 🎨 Layer 5 — Polish
- [ ] Dark / Light mode
- [ ] Financial projections
- [ ] Notifications system

---

## 🏗️ Architecture

This project follows a **Feature-Based Layered Architecture** — both on the backend and frontend. Each feature (transactions, dashboard, goals, etc.) owns its own isolated layers. Changing one layer never requires touching another.

### Request Flow (End-to-End)

```
[User Action on UI]
        ↓
[Page Component]          → Composes UI
        ↓
[Custom Hook]             → Manages local state
        ↓
[API Layer]               → HTTP calls only (Axios)
        ↓
[Django URL Router]       → urls.py
        ↓
[View]                    → Receives request, returns response
        ↓
[Service]                 → Business rules & validations
        ↓
[Repository]              → Database queries
        ↓
[PostgreSQL]              → Persisted data
```

### Golden Rules

> - The **View** never queries the database directly.
> - The **Service** never knows about the HTTP request.
> - The **Repository** never contains business logic.
> - The **Component** never calls the API directly.
> - The **API layer** never manages state.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.12, Django 5, Django REST Framework |
| **Frontend** | JavaScript, React 18, Axios |
| **Database** | PostgreSQL 16 |
| **Auth** | JWT via `djangorestframework-simplejwt` |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **API Docs** | Swagger via `drf-spectacular` |
| **Testing (back)** | Pytest, pytest-django, factory-boy |
| **Testing (front)** | Jest, React Testing Library |
| **Linting** | flake8, black (back) · ESLint, Prettier (front) |

---

## 📁 Project Structure

```
financeos/
├── backend/
│   ├── apps/
│   │   ├── transactions/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── services.py
│   │   │   ├── repositories.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── tests/
│   │   ├── dashboard/
│   │   ├── goals/
│   │   ├── rules/
│   │   └── reports/
│   ├── core/
│   │   ├── permissions.py
│   │   ├── pagination.py
│   │   ├── exceptions.py
│   │   └── base_repository.py
│   └── config/
│       ├── settings/
│       │   ├── base.py
│       │   ├── development.py
│       │   └── production.py
│       ├── urls.py
│       └── wsgi.py
│
├── frontend/
│   └── src/
│       ├── features/
│       │   ├── transactions/
│       │   │   ├── api/
│       │   │   ├── hooks/
│       │   │   ├── components/
│       │   │   └── pages/
│       │   ├── dashboard/
│       │   ├── goals/
│       │   └── rules/
│       ├── shared/
│       │   ├── components/
│       │   ├── hooks/
│       │   └── services/
│       └── app/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
│
├── docs/
│   ├── architecture.md
│   └── adr/                  # Architecture Decision Records
│
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
└── README.md
```

---

## ⚙️ Layer Responsibilities

### Backend

| Layer | File | Responsibility |
|---|---|---|
| Model | `models.py` | Database schema, field validations |
| Repository | `repositories.py` | All database queries and filters |
| Service | `services.py` | Business rules, calculations, orchestration |
| Serializer | `serializers.py` | Input validation and data transformation |
| View | `views.py` | Handle request/response, call service |
| URL | `urls.py` | Route mapping |

### Frontend

| Layer | Location | Responsibility |
|---|---|---|
| API | `features/x/api/` | HTTP calls only, no state |
| Hook | `features/x/hooks/` | State management, calls API |
| Component | `features/x/components/` | Pure UI, receives props |
| Page | `features/x/pages/` | Composes components + hooks |
| Shared | `shared/` | Reusable across all features |

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- [Git](https://git-scm.com/)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/financeos.git
cd financeos
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your local values
```

### 3. Start the application

```bash
docker-compose up --build
```

### 4. Apply migrations and create superuser

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

### 5. Access

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/api/ |
| Swagger Docs | http://localhost:8000/api/docs/ |
| Django Admin | http://localhost:8000/admin/ |

---

## 🔐 Environment Variables

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=financeos
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# JWT
JWT_ACCESS_TOKEN_LIFETIME=5       # minutes
JWT_REFRESH_TOKEN_LIFETIME=1440   # minutes (1 day)

# Frontend
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## 🧪 Running Tests

### Backend

```bash
# All tests
docker-compose exec backend pytest

# With coverage report
docker-compose exec backend pytest --cov=apps --cov-report=term-missing

# Specific feature
docker-compose exec backend pytest apps/transactions/tests/
```

### Frontend

```bash
# All tests
docker-compose exec frontend npm test

# With coverage
docker-compose exec frontend npm run test:coverage
```

---

## 🔄 CI/CD Pipeline

Every push and pull request triggers the pipeline automatically via **GitHub Actions**.

### On Pull Request (`ci.yml`)

```
1. Lint backend   → flake8, black --check
2. Lint frontend  → ESLint, Prettier
3. Test backend   → pytest with coverage
4. Test frontend  → Jest
5. Build Docker   → ensures build doesn't break
```

### On merge to `main` (`cd.yml`)

```
1. All CI checks pass
2. Build production Docker images
3. Deploy to production (Railway / Render / VPS)
```

### Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Production — protected, requires PR + CI green |
| `develop` | Integration branch |
| `feature/x` | Feature development |
| `fix/x` | Bug fixes |
| `chore/x` | Config, tooling, docs |

### Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add transaction listing endpoint
fix: correct balance calculation in dashboard service
chore: update docker-compose volumes
docs: add architecture decision record for JWT
test: add unit tests for transaction service
refactor: extract query logic to repository layer
```

---

## 📖 API Documentation

Interactive Swagger UI available at `/api/docs/` when running locally.

### Auth Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Create new user |
| POST | `/api/auth/login/` | Obtain JWT tokens |
| POST | `/api/auth/refresh/` | Refresh access token |

### Transactions (coming in Layer 2)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/transactions/` | List transactions |
| POST | `/api/transactions/` | Create transaction |
| GET | `/api/transactions/{id}/` | Get transaction |
| PUT | `/api/transactions/{id}/` | Update transaction |
| DELETE | `/api/transactions/{id}/` | Delete transaction |

---

## 🗺️ Roadmap

- [x] **Layer 1** — Project scaffold, Auth, Docker, CI/CD
- [ ] **Layer 2** — Transactions, Categories
- [ ] **Layer 3** — Dashboard, Charts, Reports
- [ ] **Layer 4** — Spending Rules, Goals, Alerts
- [ ] **Layer 5** — Dark mode, Projections, Notifications

---

## 🤝 Contributing

This is a personal portfolio project, but feedback and suggestions are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes following [Conventional Commits](#commit-convention)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request against `develop`

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  Built with 💙 by <a href="https://github.com/your-username">your-username</a>
</div>