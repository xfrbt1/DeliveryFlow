from fastapi import HTTPException, status

from app.domain.exceptions import (
    DomainError,
    InvalidCredentialsError,
    InvalidStatusTransitionError,
    OrderAccessDeniedError,
    OrderConflictError,
    OrderNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


def domain_error_handler(exc: DomainError) -> HTTPException:
    if isinstance(exc, UserNotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    if isinstance(exc, OrderNotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    if isinstance(exc, OrderAccessDeniedError):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message)
    if isinstance(exc, UserAlreadyExistsError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)
    if isinstance(exc, OrderConflictError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)
    if isinstance(exc, InvalidCredentialsError):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.message,
        )
    if isinstance(exc, InvalidStatusTransitionError):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
