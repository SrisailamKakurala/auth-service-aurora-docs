Auth Service
Overview
This is a modular authentication service built with FastAPI, PostgreSQL (via Prisma), JWT, Redis, and Docker.
Setup

Copy .env.example to .env and fill in the values.
Run docker-compose up --build.
Run Prisma migrations: docker exec -it auth-service prisma migrate deploy.

Endpoints

POST /auth/register: Register a new user.
POST /auth/login: Login and get JWT.
POST /auth/logout: Logout (invalidate token).
GET /auth/me: Get current user info.

Notes

Uses Redis for token blacklisting on logout.
Production-ready with logging, dependencies, and configurable settings.
