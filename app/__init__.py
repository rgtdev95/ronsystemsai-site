"""Ron Systems AI website."""
import hashlib
import os
from datetime import date

from flask import Flask, render_template, request, url_for

from .config import CONFIGS


def create_app(env=None):
    env = env or os.environ.get("APP_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(CONFIGS.get(env, CONFIGS["development"]))
    # Flask's default: /about redirects (308) to /about/, so each page has one URL for search engines.

    from .routes import content, pages, seo

    app.register_blueprint(pages.bp)
    app.register_blueprint(content.bp)
    app.register_blueprint(seo.bp)

    _register_template_helpers(app)
    _register_headers(app)
    _register_errors(app)
    return app


def _register_template_helpers(app):
    hashes = {}

    def asset(filename):
        """Static URL with a content hash, so files can be cached for a year."""
        if filename not in hashes or app.debug:
            path = os.path.join(app.static_folder, filename)
            with open(path, "rb") as fh:
                hashes[filename] = hashlib.sha256(fh.read()).hexdigest()[:10]
        return url_for("static", filename=filename, v=hashes[filename])

    def absolute(endpoint, **values):
        return app.config["SITE_URL"] + url_for(endpoint, **values)

    @app.context_processor
    def inject():
        cfg = app.config
        return {
            "asset": asset,
            "absolute": absolute,
            "site_name": cfg["SITE_NAME"],
            "contact_email": cfg["CONTACT_EMAIL"],
            "booking_url": cfg["BOOKING_URL"],
            "social": cfg["SOCIAL"],  # every network; the footer links only those with a URL
            "umami": (cfg["UMAMI_SCRIPT_URL"], cfg["UMAMI_WEBSITE_ID"])
            if cfg["UMAMI_SCRIPT_URL"] and cfg["UMAMI_WEBSITE_ID"] and cfg["ALLOW_INDEXING"]
            else None,
            "current_year": date.today().year,
            "canonical": cfg["SITE_URL"] + request.path,
        }


def _register_headers(app):
    @app.after_request
    def headers(resp):
        cfg = app.config
        script_src = ["'self'"]
        connect_src = ["'self'"]
        if cfg["UMAMI_SCRIPT_URL"]:
            origin = "/".join(cfg["UMAMI_SCRIPT_URL"].split("/")[:3])
            script_src.append(origin)
            connect_src.append(origin)
        resp.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; "
            f"script-src {' '.join(script_src)}; "
            f"connect-src {' '.join(connect_src)}; "
            "style-src 'self'; img-src 'self' data:; font-src 'self'; "
            "frame-src https://www.youtube-nocookie.com; "
            "frame-ancestors 'none'; base-uri 'self'; form-action 'self'",
        )
        if not cfg["ALLOW_INDEXING"]:
            resp.headers["X-Robots-Tag"] = "noindex, nofollow"
        return resp


def _register_errors(app):
    @app.errorhandler(404)
    def not_found(_e):
        return render_template("pages/404.html"), 404
