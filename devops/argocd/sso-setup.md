# ArgoCD SSO with Keycloak Integration

## 1. Keycloak Configuration
- Create Client: `argocd`.
- Protocol: `openid-connect`.
- Root URL: `https://argocd.quickhaul.com`.
- Redirect URI: `https://argocd.quickhaul.com/auth/callback`.
- Client Secret: Generate and save.

## 2. ArgoCD ConfigMap (`argocd-cm`)
Update the `argocd-cm` to enable OIDC.
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  url: https://argocd.quickhaul.com
  oidc.config: |
    name: Keycloak
    issuer: https://keycloak.quickhaul.com/realms/QuickHaul
    clientID: argocd
    clientSecret: <YOUR_CLIENT_SECRET>
    requestedScopes: ["openid", "profile", "email", "groups"]
```

## 3. ArgoCD RBAC (`argocd-rbac-cm`)
Map Keycloak roles to ArgoCD roles.
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.csv: |
    g, /admin, role:admin
    g, /operator, role:editor
  policy.default: role:readonly
```
