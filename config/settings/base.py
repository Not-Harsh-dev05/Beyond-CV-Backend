"""Shared production-safe Django settings."""

from pathlib import Path
import environ
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parents[2]
env = environ.Env(DEBUG=(bool, False), ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]))
environ.Env.read_env(BASE_DIR / ".env")
SECRET_KEY = env("SECRET_KEY", default="unsafe-dev-key-change-me")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "apps.core",
    "apps.accounts",
    "apps.candidates",
    "apps.ingestion",
    "apps.scoring",
    "apps.jobs",
    "apps.ranking",
    "apps.insights",
    "django_prometheus",
]
MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "apps.core.cors.CORSMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.middleware.RequestMetadataMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="postgres://beyondcv:beyondcv@localhost:5432/beyondcv"
    )
}
AUTH_USER_MODEL = "accounts.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_THROTTLE_CLASSES": ["apps.core.throttling.RoleRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {
        "candidate": "120/hour",
        "recruiter": "300/hour",
        "admin": "600/hour",
        "anon": "20/hour",
        "auth": "10/minute",
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.core.exceptions.api_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.DefaultPagination",
    "PAGE_SIZE": 20,
}
SIMPLE_JWT = {
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
SPECTACULAR_SETTINGS = {
    "TITLE": "BeyondCV API",
    "DESCRIPTION": "Pedigree-blind talent discovery API",
    "VERSION": "1.0.0",
}
CELERY_BROKER_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TASK_TIME_LIMIT = 300
CELERY_TASK_SOFT_TIME_LIMIT = 240
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_ALWAYS_EAGER = False
CELERY_BEAT_SCHEDULE = {
    "reap-stale-ingestion-jobs": {
        "task": "apps.ingestion.tasks.reap_stale_ingestion_jobs",
        "schedule": crontab(minute="*/5"),
    },
}
SIGNAL_TTL_HOURS = env.int("SIGNAL_TTL_HOURS", default=24)
INGESTION_STALE_MINUTES = env.int("INGESTION_STALE_MINUTES", default=30)
INGESTION_MIN_REFRESH_MINUTES = env.int("INGESTION_MIN_REFRESH_MINUTES", default=10)
UNVERIFIED_SIGNAL_WEIGHT = env.float("UNVERIFIED_SIGNAL_WEIGHT", default=0.65)
VERIFICATION_ALLOWED_DOMAINS = env.list(
    "VERIFICATION_ALLOWED_DOMAINS",
    default=["nptel.ac.in", "archive.nptel.ac.in", "coursera.org", "www.coursera.org"],
)
INSIGHTS_MIN_GROUP_SIZE = env.int("INSIGHTS_MIN_GROUP_SIZE", default=5)
RANKING_W_FIT = env.float("RANKING_W_FIT", default=0.7)
RANKING_W_DELTA = env.float("RANKING_W_DELTA", default=0.3)
EMBEDDING_BACKEND = env("EMBEDDING_BACKEND", default="local")
EMBEDDING_MODEL = env(
    "EMBEDDING_MODEL", default="sentence-transformers/all-MiniLM-L6-v2"
)
EMBEDDING_API_URL = env("EMBEDDING_API_URL", default="")
EMBEDDING_API_KEY = env("EMBEDDING_API_KEY", default="")
GITHUB_TOKEN = env("GITHUB_TOKEN", default="")
KAGGLE_USERNAME = env("KAGGLE_USERNAME", default="")
KAGGLE_KEY = env("KAGGLE_KEY", default="")
PEDIGREE_MODEL_PATH = env(
    "PEDIGREE_MODEL_PATH", default=str(BASE_DIR / "var" / "pedigree_model_v1.joblib")
)
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "standard"}
    },
    "root": {"handlers": ["console"], "level": env("LOG_LEVEL", default="INFO")},
}
