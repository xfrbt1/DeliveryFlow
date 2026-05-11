from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.application.interfaces.cache import CachePort
from app.core.config import Settings, get_settings
from app.core.security import decode_access_token
from app.domain.value_objects.role import Role
from app.infrastructure.cache.redis_cache import RedisCache
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork

security = HTTPBearer(auto_error=False)


@dataclass(frozen=True, slots=True)
class AuthPrincipal:
    user_id: UUID
    role: Role


def get_app_settings() -> Settings:
    return get_settings()


def get_uow(request: Request) -> SqlAlchemyUnitOfWork:
    session_factory = request.app.state.session_factory
    return SqlAlchemyUnitOfWork(session_factory)


def get_cache_port(request: Request) -> CachePort:
    cache: RedisCache = request.app.state.cache
    return cache


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    settings: Annotated[Settings, Depends(get_app_settings)],
) -> UUID:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_access_token(credentials.credentials, settings)
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return UUID(str(sub))
    except (JWTError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from exc


async def get_current_principal(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    settings: Annotated[Settings, Depends(get_app_settings)],
) -> AuthPrincipal:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_access_token(credentials.credentials, settings)
        sub = payload.get("sub")
        role_raw = payload.get("role")
        if sub is None or role_raw is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        role = Role(str(role_raw).lower())
        return AuthPrincipal(user_id=UUID(str(sub)), role=role)
    except (JWTError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from exc


def require_customer(
    principal: Annotated[AuthPrincipal, Depends(get_current_principal)],
) -> AuthPrincipal:
    if principal.role != Role.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer role required",
        )
    return principal


def require_courier(
    principal: Annotated[AuthPrincipal, Depends(get_current_principal)],
) -> AuthPrincipal:
    if principal.role != Role.COURIER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Courier role required",
        )
    return principal


UoWDep = Annotated[SqlAlchemyUnitOfWork, Depends(get_uow)]
CacheDep = Annotated[CachePort, Depends(get_cache_port)]
SettingsDep = Annotated[Settings, Depends(get_app_settings)]
CurrentUserId = Annotated[UUID, Depends(get_current_user_id)]
CurrentPrincipal = Annotated[AuthPrincipal, Depends(get_current_principal)]
CustomerPrincipalDep = Annotated[AuthPrincipal, Depends(require_customer)]
CourierPrincipalDep = Annotated[AuthPrincipal, Depends(require_courier)]
