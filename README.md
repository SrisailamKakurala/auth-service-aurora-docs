# Auth Service

## Overview

This is a modular authentication service built with FastAPI, MongoDB, JWT, Redis, and Docker.
Setup

```bash
Copy .env.example to .env and fill in the values.
Run docker-compose up --build.
```

### Running the Service

```bash
docker-compose up --build.
uvicorn app.main:app --reload
``` 


### Endpoints

`POST /auth/register: Register a new user.`
`POST /auth/login: Login and get JWT.`
`POST /auth/logout: Logout (invalidate token).`
`GET /auth/me: Get current user info.`

### Notes

- Uses Redis for token blacklisting on logout.
- Production-ready with logging, dependencies, and configurable settings.
