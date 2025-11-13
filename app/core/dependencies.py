"""
FastAPI dependencies for authentication and authorization.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import verify_token
from app.models.user import UserRole
from app.schemas.auth import TokenData

# HTTP Bearer token security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security)
) -> TokenData:
    """
    Extract and validate the current user from JWT token.
    
    Args:
        credentials: Bearer token from Authorization header
        
    Returns:
        TokenData: User information from the token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
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
    
    return TokenData(
        user_id=payload.get("sub"),
        email=payload.get("email"),
        role=payload.get("role"),
    )


def require_role(required_role: UserRole) -> callable:
    """
    Factory function to create role-based access control dependencies.
    
    Args:
        required_role: The minimum role required to access the endpoint
        
    Returns:
        Dependency function that validates user role
    """
    async def role_checker(
        current_user: TokenData = Depends(get_current_user)
    ) -> TokenData:
        """
        Check if the current user has the required role.
        
        Args:
            current_user: Current authenticated user
            
        Returns:
            TokenData: User information if authorized
            
        Raises:
            HTTPException: If user doesn't have required role
        """
        if not current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Rôle utilisateur manquant",
            )
        
        try:
            user_role = UserRole(current_user.role)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Rôle utilisateur invalide",
            ) from exc
        
        # Check role hierarchy: ADMIN > MODERATOR > USER
        role_hierarchy = {
            UserRole.USER: 1,
            UserRole.MODERATOR: 2,
            UserRole.ADMIN: 3,
        }
        
        if role_hierarchy.get(user_role, 0) < role_hierarchy.get(required_role, 999):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès refusé. Rôle requis : {required_role.value}",
            )
        
        return current_user
    
    return role_checker


# Common role dependencies
require_admin = require_role(UserRole.ADMIN)
require_moderator = require_role(UserRole.MODERATOR)
require_user = require_role(UserRole.USER)