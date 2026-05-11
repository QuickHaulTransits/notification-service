# Keycloak Standalone Docker Setup

This setup is intended for your new dedicated Keycloak instance.

## 1. Prerequisites
- Docker and Docker Compose installed.
- Port 8080 (or 443 with a proxy) open.

## 2. Docker Compose File
```yaml
version: '3.8'

services:
  keycloak:
    image: quay.io/keycloak/keycloak:24.0.0
    command: start-dev --http-relative-path /auth
    environment:
      KC_BOOTSTRAP_ADMIN_USERNAME: admin
      KC_BOOTSTRAP_ADMIN_PASSWORD: your_secure_password
      KC_PROXY: edge
      KC_HOSTNAME: auth.quickhaul.com # Replace with your domain
    ports:
      - "8080:8080"
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: keycloak_password
    volumes:
      - keycloak_data:/var/lib/postgresql/data

volumes:
  keycloak_data:
```

## 3. Deployment
```bash
docker-compose up -d
```

## 4. Configuration
1. Login at `http://<INSTANCE_IP>:8080/auth/admin`.
2. Import the [keycloak_realm.json](file:///C:/Users/ASUS/.gemini/antigravity/brain/48d12dfe-51ae-43e5-88f5-d55b230a9c2c/keycloak_realm.json).
