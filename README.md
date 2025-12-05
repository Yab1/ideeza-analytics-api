# IDEEZA Analytics API

Backend API for analytics-focused endpoints with efficient aggregation, dynamic filtering, and optimized performance.

## Tech Stack

- **Django 5.2**: Web framework
- **Django REST Framework**: REST API framework
- **PostgreSQL 18**: Database
- **Docker Compose**: Development and production environment
- **uv**: Fast Python package manager
- **Gunicorn + Uvicorn**: ASGI server for production

## Features

- ✅ Three analytics endpoints with proper aggregation
- ✅ Dynamic filtering system with support for complex queries
- ✅ Time-series performance metrics with growth calculations
- ✅ Top-ranked entities (users, countries, blogs)
- ✅ Optimized database queries with proper indexing
- ✅ Automatic fixture loading on container startup
- ✅ Swagger/OpenAPI documentation

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [uv](https://github.com/astral-sh/uv) package manager (optional, for local development)
- Python 3.12+ (optional, for local development)

### Quick Start with Docker

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd ideeza-analytics-api
   ```

2. **Create `.env` file:**

   ```bash
   # Copy and configure your environment variables
   # See .env.example or configure:
   DB_NAME=analysis
   DB_USER=analytics_user
   DB_PASSWORD=analytics_password
   DB_HOST=analytics_api_postgres  
   DB_PORT=5432
   ```

3. **Start Docker services:**

   ```bash
   # Start in detached mode (background)
   make docker-up-detached
   
   # Or start in attached mode (see logs)
   make docker-up
   ```

   This will:
   - Start PostgreSQL database
   - Build and start Django application
   - Run migrations automatically
   - Load test fixtures automatically

4. **Access the API:**
   - API base URL: `http://localhost:8001`
   - Swagger documentation: `http://localhost:8001/swagger/`
   - API endpoints: `http://localhost:8001/api/v1/analytics/`

### Local Development (without Docker)

1. **Install dependencies:**

   ```bash
   make install
   ```

2. **Configure database in `.env`:**

   ```bash
   DB_HOST=localhost  # or your database host
   DB_PORT=5432
   # ... other database settings
   ```

3. **Run migrations:**

   ```bash
   make migrate
   ```

4. **Load fixtures:**

   ```bash
   make load-fixtures
   ```

5. **Start development server:**

   ```bash
   make run
   ```

## API Endpoints

All endpoints are available under `/api/v1/analytics/`:

### 1. Blog Views (`/api/v1/analytics/blog-views/`)

Get grouped blog view metrics by country or user.

**Query Parameters:**

- `object_type` (required): `country` or `user`
- `range` (required): `month`, `week`, or `year`
- `filters` (optional): JSON string for dynamic filtering

**Example:**

```bash
GET /api/v1/analytics/blog-views/?object_type=country&range=month
```

**Response:**

```json
[
  {
    "x": "US",
    "y": 5,
    "z": 100
  }
]
```

### 2. Top Rankings (`/api/v1/analytics/top/`)

Get top 10 ranked entities (users, countries, or blogs).

**Query Parameters:**

- `top` (required): `user`, `country`, or `blog`
- `start_date` (optional): ISO format date (YYYY-MM-DD)
- `end_date` (optional): ISO format date (YYYY-MM-DD)
- `filters` (optional): JSON string for dynamic filtering

**Example:**

```bash
GET /api/v1/analytics/top/?top=user&start_date=2025-02-01&end_date=2025-02-28
```

**Response:**

```json
[
  {
    "x": 10,
    "y": 150,
    "z": 3
  }
]
```

### 3. Performance (`/api/v1/analytics/performance/`)

Get time-series performance metrics with growth percentages.

**Query Parameters:**

- `compare` (required): `day`, `week`, `month`, or `year`
- `user_id` (optional): Filter by specific user's blogs
- `filters` (optional): JSON string for dynamic filtering

**Example:**

```bash
GET /api/v1/analytics/performance/?compare=month
```

**Response:**

```json
[
  {
    "x": "2025-02 (10 blogs)",
    "y": 150,
    "z": 25.5
  }
]
```

## Dynamic Filtering

All endpoints support dynamic filtering via the `filters` query parameter (JSON string).

**Supported Operators:**

- `eq`: equals
- `ne`: not equals
- `gt`: greater than
- `gte`: greater than or equal
- `lt`: less than
- `lte`: less than or equal
- `in`: in array
- `contains`: contains (case-insensitive)

**Logical Operators:**

- `and`: AND conditions
- `or`: OR conditions
- `not`: NOT conditions

**Example:**

```json
{
  "and": [
    {
      "field": "viewed_at",
      "gte": "2025-02-01T00:00:00Z"
    },
    {
      "field": "viewed_at",
      "lte": "2025-02-28T23:59:59Z"
    }
  ]
}
```

URL encoded:

```text
filters=%7B%22and%22%3A%5B%7B%22field%22%3A%22viewed_at%22%2C%22gte%22%3A%222025-02-01T00%3A00%3A00Z%22%7D%5D%7D
```

## Make Commands

```bash
# Development
make install          # Install dependencies
make run              # Run development server
make migrate          # Run migrations
make migrations       # Create migrations
make shell            # Django shell
make load-fixtures    # Load test fixtures

# Docker
make docker-up              # Start containers (attached - shows logs)
make docker-up-detached     # Start containers (detached - background)

# Code Quality
make lint             # Format and lint code
make format           # Format code only
```

## Project Structure

```text
ideeza-analytics-api/
├── core/
│   ├── analytics/        # Analytics app
│   │   ├── apis.py      # API endpoints
│   │   ├── selectors.py # Business logic
│   │   ├── filters.py   # Dynamic filtering
│   │   ├── models/       # Data models
│   │   └── fixtures/     # Test data
│   ├── users/            # User management
│   └── common/           # Shared utilities
├── config/               # Django configuration
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker image definition
├── entrypoint.sh         # Container entrypoint script
└── Makefile             # Development commands
```

## Database

The application uses PostgreSQL. When running with Docker:

- Database is automatically created on first startup
- Migrations run automatically
- Test fixtures are loaded automatically
- Database persists in Docker volume: `analytics_api_postgres_data`

## Testing

Test fixtures are included in:

- `core/analytics/fixtures/` - Analytics data (countries, blogs, blog views)
- `core/users/fixtures/` - User data

Fixtures are automatically loaded when starting Docker containers.

## API Documentation

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8001/swagger/`
- ReDoc: `http://localhost:8001/redoc/`

## Contact

For technical questions or contributions, contact:

- **Developer**: [Yeabsera](https://github.com/Yab1)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
