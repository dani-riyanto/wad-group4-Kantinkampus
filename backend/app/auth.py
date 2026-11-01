import hashlib
import hmac
import os
import secrets
import time

from fastapi import Cookie, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app import database, models
from app.database import get_db

DEMO_PASSWORD = os.getenv("INITIAL_ADMIN_PASSWORD", "12345")
TOKEN_LIFETIME_SECONDS = 3600
PASSWORD_HASH_ITERATIONS = 310_000
ACCESS_COOKIE_NAME = "access_token"
CSRF_COOKIE_NAME = "csrf_token"
COOKIE_SECURE = os.getenv(
    "AUTH_COOKIE_SECURE",
    "true" if os.getenv("ENVIRONMENT", "development") == "production" else "false",
).lower() == "true"


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_HASH_ITERATIONS
    )
    return f"{PASSWORD_HASH_ITERATIONS}${salt.hex()}${password_hash.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        iterations, salt_hex, expected_hash = stored_hash.split("$")
        actual_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
        ).hex()
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(actual_hash, expected_hash)


DUMMY_PASSWORD_HASH = hash_password("invalid-login-placeholder")


def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_access_token(db: Session, user: models.User) -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    csrf_token = secrets.token_urlsafe(32)
    db.add(
        models.AuthToken(
            user_id=user.id,
            token_hash=token_digest(token),
            csrf_token_hash=token_digest(csrf_token),
            expires_at=int(time.time()) + TOKEN_LIFETIME_SECONDS,
        )
    )
    db.commit()
    return token, csrf_token


def get_current_user(
    request: Request,
    access_token: str | None = Cookie(default=None, alias=ACCESS_COOKIE_NAME),
    csrf_token: str | None = Cookie(default=None, alias=CSRF_COOKIE_NAME),
    csrf_header: str | None = Header(default=None, alias="X-CSRF-Token"),
    db: Session = Depends(get_db),
) -> models.User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau sudah kedaluwarsa",
    )
    if not access_token or not csrf_token:
        raise unauthorized

    auth_token = (
        db.query(models.AuthToken)
        .filter(
            models.AuthToken.token_hash == token_digest(access_token),
            models.AuthToken.expires_at > int(time.time()),
        )
        .first()
    )
    if (
        auth_token is None
        or not auth_token.csrf_token_hash
        or not hmac.compare_digest(
            auth_token.csrf_token_hash, token_digest(csrf_token)
        )
    ):
        raise unauthorized

    if request.method not in {"GET", "HEAD", "OPTIONS"} and (
        not csrf_header or not hmac.compare_digest(csrf_token, csrf_header)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token CSRF tidak valid",
        )

    user = db.query(models.User).filter(models.User.id == auth_token.user_id).first()
    if user is None:
        raise unauthorized
    return user


def require_admin(user: models.User = Depends(get_current_user)) -> models.User:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat melakukan tindakan ini",
        )
    return user


def create_initial_admin() -> None:
    db = database.SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if admin is None:
            db.add(
                models.User(
                    username="admin",
                    display_name="Administrator",
                    password_hash=hash_password(DEMO_PASSWORD),
                    role="admin",
                )
            )
            db.commit()
    finally:
        db.close()


def migrate_order_ownership() -> None:
    inspector = database.inspect(database.engine)
    tables = set(inspector.get_table_names())
    with database.engine.begin() as connection:
        if "auth_tokens" in tables:
            token_columns = {
                column["name"] for column in inspector.get_columns("auth_tokens")
            }
            if "csrf_token_hash" not in token_columns:
                connection.exec_driver_sql(
                    "ALTER TABLE auth_tokens ADD COLUMN csrf_token_hash VARCHAR(64)"
                )
                connection.exec_driver_sql("DELETE FROM auth_tokens")

        if "orders" not in tables:
            return

        order_columns = {
            column["name"] for column in inspector.get_columns("orders")
        }
        if "owner_id" not in order_columns:
            connection.exec_driver_sql(
                "ALTER TABLE orders ADD COLUMN owner_id INTEGER REFERENCES users(id)"
            )

    db = database.SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if admin is None:
            raise RuntimeError("Akun admin awal tidak ditemukan saat migrasi pesanan")
        db.query(models.Order).filter(models.Order.owner_id.is_(None)).update(
            {models.Order.owner_id: admin.id},
            synchronize_session=False,
        )
        db.commit()
        owner_index = next(
            index
            for index in models.Order.__table__.indexes
            if index.name == "ix_orders_owner_id"
        )
        owner_index.create(bind=database.engine, checkfirst=True)
    finally:
        db.close()
