<h1 align="center" id="header">
  Python FastAPI Application (Clean Architecture)
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana">
  <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/Alembic-000000?style=for-the-badge&logo=alembic&logoColor=white" alt="Alembic">
</p>

<p align="center">
  Base FastAPI project for applying general RestAPI Application cases.
</p>

---

<h2 id="table-of-contents">
  Table of Contents
</h2>

- [Tech Stack](#stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation)
- [Usage](#usage)
- [Database Management](#database)
- [Project Structure](#project-structure)
- [Code Quality & Formatting](#code-quality)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Monitoring & Logging](#monitoring)
- [Configuration Files](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

<h2 id="stack">
  Tech Stack
</h2>

<p>
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Python-Dark.svg" width="48" title="Python"> 
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/FastAPI.svg" width="48" title="FastAPI">
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Nginx.svg" width="48" title="Nginx">
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Docker.svg" width="48" title="Docker">
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Grafana-Dark.svg" width="48" title="Grafana">
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/PostgreSQL-Dark.svg" width="48" title="PostgreSQL">
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Redis-Dark.svg" width="48" title="Redis">
</p>

### Core Technologies

- **Python 3.12+** - Modern Python with latest language features and performance improvements
- **FastAPI** - High-performance async web framework with automatic OpenAPI documentation
- **PostgreSQL 17** - Robust, production-grade relational database management system
- **Aio Kafka** - Asynchronous Kafka client for event streaming and producer/consumer workflows
- **Nginx** - High-performance reverse proxy and load balancer
- **Docker** - Containerized, reproducible deployment across environments
- **SQLAlchemy 2.0** - Async ORM and query builder for Python with full PostgreSQL support
- **Redis** - In-memory data store used for caching and session management
- **Alembic** - Lightweight database migration tool for SQLAlchemy schema version control
- **Pytest** - Comprehensive testing framework for unit and integration tests

### Infrastructure & Monitoring

- **Nginx** - Reverse proxy with custom error pages and logging
- **Grafana** - Metrics visualization and monitoring dashboards
- **Loki** - Log aggregation and querying system
- **Promtail** - Log collector and shipper to Loki
- **Docker Compose** - Multi-container orchestration

### Features & Integrations

- **Database Migrations** - Automated schema version control with Alembic
- **PostgreSQL Integration** - Production-ready database with persistent storage
- **Argon2** - Standard secure password hashing
- **Reverse Proxy** - Nginx with environment-based configuration
- **JWT Authentication** - Stateless token-based authentication and authorization
- **Centralized Logging** - Grafana/Loki stack for log aggregation and visualization
- **RESTful API** - Clean and scalable API architecture following Clean Architecture principles
- **Environment-based Configuration** - Separate dev/prod settings with .env files
- **Custom Error Pages** - Branded error handling through Nginx
- **Log Management** - Nginx access and error logs with Promtail collection
- **Hot Reload** - Development mode with automatic code reloading
- **Database Shell Access** - Direct PostgreSQL psql command-line interface
- **Code Quality Tools** - Automated formatting and linting

---

<h2 id="prerequisites">
  Prerequisites
</h2>

Before starting, ensure you have the following installed:

- [Docker](https://www.docker.com/) - Container platform
- [Docker Compose](https://docs.docker.com/compose/) - Multi-container orchestration
- [Make](https://www.gnu.org/software/make/) - Build automation
- [Git](https://git-scm.com/) - Version control

> Optional: [Python 3.12+](https://www.python.org/) if you prefer running the app without Docker.

---

<h2 id="installation">
  Installation & Setup
</h2>

### 1. Clone the Repository

```bash
git clone https://github.com/Victor-Zarzar/fastapi-clean-architecture
cd fastapi-clean-architecture
```

### 2. Open in your editor

```bash
zed .
```

### 3. Environment Configuration

Copy the example environment file and configure your credentials:

```bash
cp .env-example .env.dev
```

**Key configurations needed:**

- **Database**: PostgreSQL credentials (user, password, database)
- **API Settings**: Host, port, and other application settings
- **Environment**: Development or production mode

> **Important:** Never commit your `.env.dev` or `.env.prod` files to version control. They should be in `.gitignore`.

### 4. Build Development Environment

```bash
make build-dev
```

This will:

- Build the Docker image with tag `api-cost-map-web-api:1.0.0`
- Set up the PostgreSQL database container
- Configure networking between services

---

<h2 id="usage">
  Usage
</h2>

### Available Commands

View all available Make commands:

```bash
make help
```

### Local Development

Start the development server (port 8000):

```bash
make up-dev
```

Access the API at:

- **API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### Docker Deployment

#### Development Commands

```bash
make build-dev    # Build development Docker image
make up-dev       # Start development server with hot reload
make down-dev     # Stop development server
make logs-dev     # View development logs in real-time
make test         # Run tests with pytest
make format       # Format code with Ruff
make lint         # Lint code with pylint
make shell        # Access container bash shell
make migrate      # Run database migrations
```

#### Database Management

```bash
make access-db-local  # Access PostgreSQL shell directly
make migrate          # Apply pending database migrations
```

Access database with credentials from your `.env.dev`:

- **Url**: postgresql+psycopg://example...
- **Host**: localhost
- **Port**: 5432
- **Database**: costdb
- **User**: admin
- **Password**: pass

#### Cleanup Commands

```bash
make clean        # Clean local environment and containers
make clean-all    # Remove all containers, volumes, and images
```

#### View Logs

```bash
make logs-dev     # Development logs
make logs-prod    # Production logs
```

Or directly with Docker:

```bash
docker logs -f api-cost-map
docker logs -f postgresql-server
```

---

### Running Tests

```bash
make test
```

Or manually with Docker:

```bash
docker compose -f docker-compose.dev.yaml exec web pytest
```

### API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

<h2 id="database">
  Database Management
</h2>

### Migrations with Alembic

This project uses Alembic for database schema version control.

#### Create a New Migration

```bash
# Inside the container
docker exec -it api-cost-map alembic revision --autogenerate -m "Description of changes"
```

#### Apply Migrations

```bash
make migrate
# or
docker exec -it api-cost-map python -m alembic upgrade head
```

#### Rollback Migration

```bash
docker exec -it api-cost-map python -m alembic downgrade -1
```

### Direct Database Access

Access the PostgreSQL shell:

```bash
make access-db-local
```

This opens an interactive PostgreSQL session where you can run SQL queries directly.

**Example queries:**

```sql
--- List all tables in the current schema
\dt

-- Describe a table structure
\d your_table_name

-- Query data
SELECT * FROM your_table_name LIMIT 10;

-- Quit the session
\q
```

---

<h2 id="project-structure">
  Project Structure
</h2>

```
api-cost-map/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py              # Authentication routes
│   │           ├── user.py              # User management routes
│   │           ├── cost.py              # Cost management routes
│   │           └── ...
│   ├── repository/
│   │   ├── user_repository.py           # User data access layer
│   │   └── cost_repository.py           # Cost data access layer
│   ├── services/
│   │   ├── auth_service.py              # Authentication business logic
│   │   ├── user_service.py              # User business logic
│   │   └── cost_service.py              # Cost business logic
│   ├── schemas/                         # Pydantic request/response models
│   ├── models/                          # SQLAlchemy ORM models
│   ├── core/
│   │   ├── config.py                    # App settings and environment config
│   │   ├── exceptions.py                # Custom exception handlers
│   │   └── security.py                  # Auth utilities (JWT, hashing)
│   └── db/
│       └── database.py                  # Database session and engine setup
├── alembic/                             # Database migrations
│   ├── versions/                        # Auto-generated migration files
│   └── env.py                           # Alembic environment configuration
├── nginx/                               # Nginx reverse proxy
│   ├── nginx.conf.template              # Config template with env vars
│   └── errors/                          # Custom branded error pages
├── grafana/                             # Grafana monitoring
│   └── provisioning/                    # Auto-provisioned datasources & dashboards
├── logs/                                # Application logs (gitignored)
│   └── nginx/                           # Nginx access and error logs
├── tests/                               # Test suite
│   ├── test_api.py                      # API endpoint integration tests
│   └── test_services.py                 # Service layer unit tests
├── docker-compose.dev.yaml              # Development orchestration
├── docker-compose.prod.yaml             # Production orchestration
├── Dockerfile                           # Development image
├── Dockerfile.prod                      # Production image (optimized)
├── entrypoint.sh                        # Container startup & migration script
├── loki-config.yml                      # Loki log aggregation configuration
├── promtail-config.yml                  # Promtail log collection configuration
├── requirements.txt                     # Python dependencies
├── .env.example                         # Environment variables template
├── .env.dev                             # Development environment (not in git)
├── .env.prod                            # Production environment (not in git)
├── alembic.ini                          # Alembic CLI configuration
├── pyproject.toml                       # Ruff, pylint, and project metadata
├── Makefile                             # Build and task automation
└── README.md                            # Project documentation
```

---

<h2 id="code-quality">
  Code Quality & Formatting
</h2>

### Ruff Configuration

This project uses [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and code formatting. The configuration is defined in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP"]
ignore = ["E501"]
fixable = ["ALL"]
unfixable = []
```

**Configuration details:**

- **Line length**: 88 characters (Black compatible)
- **Target version**: Python 3.12
- **Quote style**: Double quotes for strings
- **Linting rules**:
  - `E`, `W` - pycodestyle errors and warnings
  - `F` - Pyflakes
  - `I` - isort (import sorting)
  - `B` - flake8-bugbear
  - `UP` - pyupgrade (modern Python syntax)
- **Ignored rules**: `E501` (line too long)

### Running Code Quality Tools

All code quality tools run inside the Docker container:

```bash
# Format code with Ruff
make format

# Lint code with pylint
make lint
```

Or directly with Docker Compose:

```bash
# Format code
docker compose -f docker-compose.dev.yaml exec web ruff format app

# Lint code
docker compose -f docker-compose.dev.yaml exec web pylint app
```

---

<h2 id="api-endpoints">
  API Endpoints
</h2>

### Core Endpoints

The API provides RESTful endpoints for cost management:

- **GET** `/api/v1/costs` - List all costs
- **POST** `/api/v1/costs` - Create new cost
- **GET** `/api/v1/costs/{id}` - Get cost by ID
- **PUT** `/api/v1/costs/{id}` - Update cost
- **DELETE** `/api/v1/costs/{id}` - Delete cost

### Authentication

Depending on your configuration, endpoints may require authentication. Check the API documentation for details:

- **Development**: `http://localhost:8000/docs`
- **Production (via Nginx)**: `http://localhost/docs`

---

<h2 id="deployment">
  Deployment
</h2>

### Docker Production

Build and run the production container:

```bash
# Start production environment
make up-prod

# Check logs
make logs-prod

# Stop when needed
make down-prod
```

### Production Architecture

The production environment includes:

- **FastAPI Application** - Main API service (port 8006 internal)
- **PostgreSQL Database** - Persistent data storage (port 5432)
- **Nginx** - Reverse proxy (port 80)
- **Grafana** - Monitoring dashboard (port 3000)
- **Loki** - Log aggregation (port 3100)
- **Promtail** - Log collection from Nginx

### Accessing Services

Once deployed, access the services at:

- **API**: `http://localhost` (via Nginx reverse proxy)
- **API Docs**: `http://localhost/docs`
- **Grafana Dashboard**: `http://localhost:3000`
- **PostgreSQL**: `localhost:5432`
- **Loki API**: `http://localhost:3100`

### Production Considerations

- Use strong database credentials
- Configure proper backup strategies for PostgreSQL
- Set up monitoring alerts in Grafana
- Use environment-specific configuration files
- Consider using Docker secrets for sensitive data
- Implement proper SSL/TLS certificates for Nginx
- Configure log retention policies in Loki
- Set up automated database backups

---

<h2 id="monitoring">
  Monitoring & Logging
</h2>

### Grafana Dashboard

Access Grafana at `http://localhost:3000` to visualize metrics and logs.

**Default credentials** (configure in `.env.prod`):

- Check your environment file for credentials

**Features:**

- Pre-configured Loki datasource
- Nginx access and error log visualization
- Real-time log streaming
- Log filtering and searching
- Custom dashboard creation

### Loki Log Aggregation

Loki aggregates logs from multiple sources:

**Log Sources:**

- Nginx access logs (`/var/log/nginx/access.log`)
- Nginx error logs (`/var/log/nginx/error.log`)
- Application logs (via Promtail configuration)

**Querying Logs:**

Access Loki directly at `http://localhost:3100` or through Grafana's Explore interface.

Example LogQL queries:

```logql
# All nginx logs
{job="nginx"}

# Error logs only
{job="nginx"} |= "error"

# Logs from specific time range
{job="nginx"} | json | line_format "{{.timestamp}} {{.message}}"
```

### Promtail Configuration

Promtail collects logs and ships them to Loki. Configuration location:

```
./promtail-config.yml
```

**Monitored paths:**

- `/var/log/nginx` - Nginx logs mounted from host

### Nginx Logging

Nginx logs are stored in:

```
./logs/nginx/access.log  # HTTP access logs
./logs/nginx/error.log   # Nginx error logs
```

These logs are automatically collected by Promtail and sent to Loki.

### Custom Error Pages

Nginx serves custom error pages from:

```
./nginx/errors/
```

Configure error pages in `nginx.conf.template` to maintain branding during errors.

---

<h2 id="configuration">
  Configuration Files
</h2>

### Nginx Configuration

**Location:** `./nginx/nginx.conf.template`

Environment variables used:

- `${BACKEND_HOST}` - FastAPI service hostname (default: `web`)
- `${BACKEND_PORT}` - FastAPI service port (default: `8006`)

Example configuration:

```nginx
upstream backend {
    server ${BACKEND_HOST}:${BACKEND_PORT};
}

server {
    listen 80;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Loki Configuration

**Location:** `./loki-config.yml`

Key settings:

- Log retention period
- Storage configuration
- Ingestion limits

### Promtail Configuration

**Location:** `./promtail-config.yml`

Configure:

- Log file paths
- Labels and metadata
- Loki server endpoint

### Grafana Provisioning

**Location:** `./grafana/provisioning/`

Auto-provisioned:

- Datasources (Loki)
- Dashboards (if configured)
- Alert rules (if configured)

---

<h2 id="troubleshooting">
  Troubleshooting
</h2>

### Database Connection Issues

**Database not accessible:**

- Ensure PostgreSQL container is running: `docker ps`
- Check database credentials in `.env.prod`
- Verify port 5432 is not in use by another service
- Check Docker network connectivity

**Migration errors:**

- Ensure database is initialized: `make access-db-local`
- Check Alembic configuration in `alembic.ini`
- Review migration files in `alembic/versions/`

### Nginx Issues

**502 Bad Gateway:**

- Verify FastAPI container is running: `docker ps | grep web`
- Check backend configuration in `nginx.conf.template`
- Ensure `BACKEND_HOST` and `BACKEND_PORT` are correct
- View Nginx error logs: `cat logs/nginx/error.log`

**Custom error pages not showing:**

- Verify error page files exist in `./nginx/errors/`
- Check Nginx configuration for error_page directives
- Restart Nginx: `docker restart api-cost-map-nginx`

### Logging & Monitoring Issues

**Grafana not accessible:**

- Ensure Grafana container is running: `docker ps | grep grafana`
- Check port 3000 availability: `lsof -i :3000`
- Verify credentials in `.env.prod`

**Logs not appearing in Grafana:**

- Check Promtail is running: `docker ps | grep promtail`
- Verify Loki datasource is configured in Grafana
- Check Promtail configuration: `cat promtail-config.yml`
- Ensure log files exist: `ls -la logs/nginx/`
- Test Loki directly: `curl http://localhost:3100/ready`

**Loki storage issues:**

- Check disk space: `df -h`
- Review Loki configuration for retention settings
- Check Loki logs: `docker logs loki`

### Container Issues

**Port already in use:**

```bash
# Check what's using port 80
lsof -i :80

# Or port 5432 for PostgreSQL
lsof -i :5432

# Or port 3000 for Grafana
lsof -i :3000
```

**Clean restart:**

```bash
make clean
make build-dev
make up-dev
```

### Network Issues

**Containers can't communicate:**

- Verify all containers are on `app-network`: `docker network inspect app-network`
- Check Docker Compose network configuration
- Restart Docker Compose: `make down-prod && make up-prod`

---

<h2 id="contributing">
  Contributing
</h2>

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

Report issues at: https://github.com/Victor-Zarzar/fastapi-clean-architecture

### Development Guidelines

- Write tests for new features
- Follow PEP 8 style guide
- Update documentation as needed
- Ensure all tests pass before submitting PR
- Create migrations for database schema changes
- Run `make format` and `make lint` before committing

---

<h2 id="license">
  License
</h2>

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<h2 id="author">
  Author
</h2>

Victor Zarzar - [@Victor-Zarzar](https://github.com/Victor-Zarzar)

Project Link: [https://github.com/Victor-Zarzar/fastapi-clean-architecture](https://github.com/Victor-Zarzar/fastapi-clean-architecture)

---
