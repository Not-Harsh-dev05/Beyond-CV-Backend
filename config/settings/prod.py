"""Production settings with mandatory secret and secure transport defaults."""

from .base import *  # noqa: F403

DEBUG = False
if SECRET_KEY == "unsafe-dev-key-change-me":  # noqa: F405
    raise RuntimeError("SECRET_KEY must be set in production")
if not env("DATABASE_URL", default=""):  # noqa: F405
    raise RuntimeError("DATABASE_URL must be configured for production")
if not env("ALLOWED_HOSTS", default=""):  # noqa: F405
    raise RuntimeError("ALLOWED_HOSTS must be configured")
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)  # noqa: F405
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
