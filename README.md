# IDEEZA Analytics API

Backend API for analytics-focused endpoints with efficient aggregation, dynamic filtering, and optimized performance.

## Tech Stack

- **Django 5.2**: Web framework
- **Django REST Framework**: REST API framework
- **PostgreSQL**: Database
- **Docker Compose**: Development environment
- **uv**: Fast Python package manager

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [uv](https://github.com/astral-sh/uv) package manager
- Python 3.12+

### Setup

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ideeza-analytics-api
    ```

2. **Install dependencies:**
    ```bash
    make install
    ```

3. **Start Docker services:**
    ```bash
    docker-compose -f docker/development/docker-compose.yml up -d
    ```

4. **Run migrations:**
    ```bash
    uv run python manage.py migrate
    ```

5. **Start development server:**
    ```bash
    uv run python manage.py runserver 8001
    ```

## Development

- API endpoints are available at `/api/`
- API documentation available at `/swagger/`
- Development server runs on `http://localhost:8001`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
