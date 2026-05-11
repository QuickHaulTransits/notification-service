# Keycloak Helm Deployment Guide

## 1. Add Bitnami Repo
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

## 2. Install Keycloak
```bash
kubectl create namespace keycloak
helm install keycloak bitnami/keycloak \
  --namespace keycloak \
  -f values.yaml
```

## 3. Configuration (values.yaml)
Create a `values.yaml` for Keycloak:
```yaml
auth:
  adminUser: admin
  adminPassword: admin_password
proxy: edge
ingress:
  enabled: true
  hostname: keycloak.quickhaul.com
  ingressClassName: nginx
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
postgresql:
  enabled: true
  auth:
    database: keycloak
    username: keycloak
    password: keycloak_password
```

## 4. Post-Installation
1. Log in to the Admin Console at `https://keycloak.quickhaul.com/admin`.
2. Create Realm: `QuickHaul`.
3. Create Client: `quickhaul-frontend`.
   - Client Protocol: `openid-connect`.
   - Access Type: `public`.
   - Valid Redirect URIs: `https://app.quickhaul.com/*`.
   - Web Origins: `*`.
4. Create Roles: `admin`, `user`, `operator`.
5. Create a test user and assign a role.
