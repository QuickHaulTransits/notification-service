import os
import httpx
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import List, Optional

# Configuration
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://keycloak.quickhaul.svc.cluster.local:8080")
REALM_NAME = os.getenv("KEYCLOAK_REALM", "QuickHaul")
ALGORITHMS = ["RS256"]

# JWKS Endpoint for public keys
JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/certs"

security = HTTPBearer()

class AuthHandler:
    _jwks: Optional[dict] = None

    async def get_jwks(self):
        if not self._jwks:
            async with httpx.AsyncClient() as client:
                response = await client.get(JWKS_URL)
                self._jwks = response.json()
        return self._jwks

    async def validate_token(self, token: str):
        try:
            jwks = await self.get_jwks()
            # Decode the token and verify against JWKS
            payload = jwt.decode(
                token,
                jwks,
                algorithms=ALGORITHMS,
                audience="account", # Adjust based on Keycloak client config
                options={"verify_at_hash": False}
            )
            return payload
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

auth_handler = AuthHandler()

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    return await auth_handler.validate_token(token.credentials)

def require_role(allowed_roles: List[str]):
    def role_checker(user: dict = Depends(get_current_user)):
        # Extract roles from 'realm_access'
        user_roles = user.get("realm_access", {}).get("roles", [])
        
        if not any(role in user_roles for role in allowed_roles):
            raise HTTPException(
                status_code=403, 
                detail=f"Access denied. Required roles: {allowed_roles}"
            )
        return user
    return role_checker
