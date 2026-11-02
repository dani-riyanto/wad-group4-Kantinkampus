from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models
from app.auth import (
    ACCESS_COOKIE_NAME,
    COOKIE_SECURE,
    CSRF_COOKIE_NAME,
    TOKEN_LIFETIME_SECONDS,
    create_access_token,
    DUMMY_PASSWORD_HASH,
    get_current_user,
    token_digest,
    verify_password,
)
from app.database import get_db
from app.schemas import AuthSessionResponse, LoginRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=AuthSessionResponse)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    stored_hash = user.password_hash if user is not None else DUMMY_PASSWORD_HASH
    if not verify_password(payload.password, stored_hash) or user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
        )

    token, csrf_token = create_access_token(db, user)
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=TOKEN_LIFETIME_SECONDS,
        path="/",
    )
    response.set_cookie(
        key=CSRF_COOKIE_NAME,
        value=csrf_token,
        httponly=False,
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=TOKEN_LIFETIME_SECONDS,
        path="/",
    )
    return AuthSessionResponse(user=user)


@router.get("/session", response_model=AuthSessionResponse)
def get_session(
    csrf_token: str | None = Cookie(default=None, alias=CSRF_COOKIE_NAME),
    user: models.User = Depends(get_current_user),
):
    if not csrf_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesi tidak valid",
        )
    return AuthSessionResponse(user=user)


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    access_token: str | None = Cookie(default=None, alias=ACCESS_COOKIE_NAME),
    _user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.query(models.AuthToken).filter(
        models.AuthToken.token_hash == token_digest(access_token)
    ).delete()
    db.commit()
    response.delete_cookie(
        key=ACCESS_COOKIE_NAME,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    response.delete_cookie(
        key=CSRF_COOKIE_NAME,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
