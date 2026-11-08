"""Configuration, selected by the APP_ENV environment variable."""
import os


def _env(name, default=""):
    return os.environ.get(name, default).strip()


class BaseConfig:
    APP_ENV = "development"
    SECRET_KEY = _env("SECRET_KEY", "dev-only-not-secret")
    # Each environment knows its own address; set SITE_URL only to override it (e.g. local Docker on :8000).
    SITE_URL = _env("SITE_URL", "http://127.0.0.1:5000").rstrip("/")
    SITE_NAME = "Ron Systems AI"

    # Search engines and AI crawlers may index this environment.
    ALLOW_INDEXING = False

    CONTACT_EMAIL = _env("CONTACT_EMAIL", "contactme@ronsystemsai.com")
    BOOKING_URL = _env("BOOKING_URL")  # Proton Calendar booking page; empty = /book/ offers email only

    # Social profiles render only when set.
    SOCIAL = {
        "YouTube": _env("SOCIAL_YOUTUBE"),
        "Facebook": _env("SOCIAL_FACEBOOK"),
        "LinkedIn": _env("SOCIAL_LINKEDIN"),
        "GitHub": _env("SOCIAL_GITHUB"),
    }

    # IndexNow (Bing and others): the site serves /<key>.txt to prove ownership; deploys ping with it.
    INDEXNOW_KEY = _env("INDEXNOW_KEY")

    # Umami analytics renders only when both are set.
    UMAMI_SCRIPT_URL = _env("UMAMI_SCRIPT_URL")
    UMAMI_WEBSITE_ID = _env("UMAMI_WEBSITE_ID")

    CONTENT_DIR = _env("CONTENT_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "content"))

    # The site sets no cookies (the privacy page says so). If a session is ever used, keep it locked down.
    SESSION_COOKIE_SAMESITE = "Lax"
    SEND_FILE_MAX_AGE_DEFAULT = 60 * 60 * 24 * 365  # static URLs are cache-busted by file hash


class DevelopmentConfig(BaseConfig):
    SEND_FILE_MAX_AGE_DEFAULT = 0


class TestConfig(BaseConfig):
    APP_ENV = "test"
    SITE_URL = _env("SITE_URL", "https://test.ronsystemsai.com").rstrip("/")
    SESSION_COOKIE_SECURE = True


class ProductionConfig(BaseConfig):
    APP_ENV = "production"
    SITE_URL = _env("SITE_URL", "https://ronsystemsai.com").rstrip("/")
    ALLOW_INDEXING = True
    SESSION_COOKIE_SECURE = True


class TestingConfig(BaseConfig):
    """Used by pytest."""
    APP_ENV = "testing"
    TESTING = True


CONFIGS = {
    "development": DevelopmentConfig,
    "test": TestConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
