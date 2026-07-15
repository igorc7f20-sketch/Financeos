# 💰 FinanceOS — Business Finance Management System

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?style=flat-square&logo=django)
![DRF](https://img.shields.io/badge/DRF-REST%20API-red?style=flat-square)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=flat-square&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black?style=flat-square&logo=githubactions)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

> A robust, scalable and decoupled finance management system for small businesses — built with professional engineering practices for real-world portfolio demonstration.

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

**FinanceOS** is a finance management system for small businesses, built with a focus on clean architecture, maintainability, and scalability. It centers on a daily cash register flow (income and expenses broken down by payment method — cash, card, boleto, installments), a financial dashboard with period summaries and monthly evolution charts, and general transaction/category tracking — all accessible via a REST API consumed by a modern SPA frontend.

Each user account represents a single business today. The data model is intentionally kept simple at this stage (no premature abstraction — see [ADR-001](docs/adr/ADR-001-product-over-engineering.md)), but is positioned to evolve into full multi-tenant support (multiple businesses per account) later without a rewrite.

This project follows industry-standard engineering practices:

- **Feature-Based Layered Architecture** — each feature is fully isolated
- **Separation of Concerns** — data, business logic, and presentation never mix
- **Test-Driven mindset** — each layer is independently testable
- **CI/CD** — automated linting, testing, and deployment on every push
- **MVP-first, iterative delivery** — built in incremental, documented layers
- **Product over Engineering** — behavior and usability drive new development, not structure ([ADR-001](docs/adr/ADR-001-product-over-engineering.md))

---

## ✨ Features

### ✅ Layer 1 — Foundation (completed)
- [x] Project scaffold (Django + DRF + PostgreSQL + Docker)
- [x] Custom User model with email-based authentication
- [x] JWT Authentication (register, login, token refresh, profile)
- [x] Feature-based layered architecture (model → repository → service → serializer → view)
- [x] Core layers: pagination, exceptions, base repository, permissions
- [x] Unit and integration tests — 90% coverage
- [x] CI/CD pipeline with GitHub Actions (lint → test → docker build)
- [x] Swagger / OpenAPI documentation

### ✅ Layer 2 — Core Finance (completed)
- [x] `Category` model with user ownership and type (income/expense)
- [x] `Transaction` model with amount, date, notes and category relation
- [x] Full CRUD endpoints for transactions and categories
- [x] Filters by type, category, date range and search
- [x] Pagination on all list endpoints
- [x] Category/transaction type mismatch validation
- [x] Tests for all layers — models, services, views

### ✅ Layer 3 — Cash Register MVP (completed)
- [x] React + Vite frontend scaffold
- [x] Tailwind CSS + dark/light mode support
- [x] HTTP client with JWT refresh interceptor
- [x] Auth store (Zustand)
- [x] Login and Register pages
- [x] Cash entries (income/expense) with payment method (cash, card, boleto, installment)
- [x] Current balance view — persisted, updated in real time on every movement
- [x] Movement history with period filters (date range, backend-driven)
- [x] Sidebar navigation shell shared across authenticated pages

### 🚧 Layer 4 — Dashboard & Reports (in progress)
- [x] Current balance and period summary (today / this week / this month)
- [x] Monthly evolution charts — income and expenses, last 12 months, with hover tooltips
- [ ] Spending breakdown by category
- [ ] CSV / PDF export
- [ ] Aggregate reports combining multiple data sources (cash register + general transactions)

### 🔲 Layer 5 — Rules & Intelligence
- [ ] Spending rules per category
- [ ] Budget limit alerts
- [ ] Financial goals with visual progress

### 🔲 Layer 6 — Polish & Observability
- [ ] Structured logs and tracing
- [ ] Health checks and metrics
- [ ] Financial projections
- [ ] Notifications system

---

## 🏗️ Architecture

This project follows a **Feature-Based Layered Architecture** — both on the backend and frontend. Each feature (cash, transactions, dashboard, etc.) owns its own isolated layers. Changing one layer never requires touching another.

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
| **Frontend** | JavaScript, React 18, Axios, Recharts, lucide-react |
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
│   │   ├── users/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── services.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   ├── transactions/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── services.py
│   │   │   ├── repositories.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── tests/
│   │   ├── cash/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── services.py
│   │   │   ├── repositories.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── tests/
│   │   ├── dashboard/
│   │   │   ├── repositories.py
│   │   │   ├── serializers.py
│   │   │   ├── services.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   └── (goals/, rules/, reports/ — planned for Layer 5–6)
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
│       │   ├── auth/
│       │   │   ├── api/
│       │   │   ├── hooks/
│       │   │   └── pages/
│       │   ├── cash/
│       │   │   ├── api/
│       │   │   ├── hooks/
│       │   │   └── pages/
│       │   └── dashboard/
│       │       ├── api/
│       │       ├── hooks/
│       │       ├── components/
│       │       └── pages/
│       ├── shared/
│       │   ├── components/     # AppLayout (sidebar) and other shared UI
│       │   ├── hooks/
│       │   ├── services/
│       │   └── store/
│       └── App/
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
| Shared | `shared/` | Reusable across all features (layout, theme, auth store) |

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- [Git](https://git-scm.com/)

### 1. Clone the repository

```bash
git clone https://github.com/igorc7f20-sketch/Financeos.git
cd Financeos
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
docker-compose exec backend pytest apps/cash/tests/
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
3. Deploy to production (Render)
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
feat: add cash movement period filter
fix: correct monthly aggregation key in dashboard service
chore: update docker-compose volumes
docs: update README for business-management pivot
test: add unit tests for cash service
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
| GET | `/api/users/profile/` | Get authenticated user's profile |

### Transactions

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/transactions/` | List transactions |
| POST | `/api/transactions/` | Create transaction |
| GET | `/api/transactions/{id}/` | Get transaction |
| PUT | `/api/transactions/{id}/` | Update transaction |
| DELETE | `/api/transactions/{id}/` | Delete transaction |

### Cash Register

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/cash/status/` | Current cash balance |
| GET | `/api/cash/movements/` | List movements (period filter + pagination + totals) |
| POST | `/api/cash/movements/` | Create a cash movement (income/expense + payment method) |
| POST | `/api/cash/close/` | Close today's cash register |

### Dashboard

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/dashboard/period-summary/` | Income/expense totals for today, this week, this month |
| GET | `/api/dashboard/monthly-income/` | Income by month, last 12 months |
| GET | `/api/dashboard/monthly-expense/` | Expenses by month, last 12 months |

---

## 🗺️ Roadmap

- [x] **Layer 1** — Project scaffold, Auth, Docker, CI/CD ✅
- [x] **Layer 2** — Transactions, Categories, Filters, Pagination ✅
- [x] **Layer 3** — Cash Register MVP, Frontend Base ✅
- [ ] **Layer 4** — Dashboard, Charts, Reports 🚧
- [ ] **Layer 5** — Spending Rules, Goals, Alerts
- [ ] **Layer 6** — Polish, Observability, Projections

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
  Built with 💙 by <a href="https://github.com/igorc7f20-sketch">Igor Crisóstomo</a>
</div>