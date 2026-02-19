"""
FastAPI dependencies for authentication and authorization.
"""

from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User, UserRole
from app.schemas.auth import TokenData

# HTTP Bearer token security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> TokenData:
    """Extract and validate the current user from JWT token, fetch roles from DB."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification requis",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable",
        )

    roles = ["admin", "user"] if user.role == UserRole.ADMIN else ["user"]

    return TokenData(user_id=user_id, roles=roles)


def require_role(required_role: UserRole) -> Any:
    """Factory function to create role-based access control dependencies."""

    async def role_checker(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        """Check if the current user has the required role."""
        if required_role.value not in current_user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès refusé. Rôle requis : {required_role.value}",
            )

        return current_user

    return role_checker


# Common role dependencies
require_admin = require_role(UserRole.ADMIN)
require_user = require_role(UserRole.USER)
