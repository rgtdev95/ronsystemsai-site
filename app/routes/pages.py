from flask import Blueprint, abort, redirect, render_template, url_for

from .. import site_content as C
from ..services import schema

bp = Blueprint("pages", __name__)


@bp.get("/")
def home():
    return render_template(
        "pages/home.html",
        C=C,
        jsonld=[schema.organization(), schema.person(), schema.website(), schema.faq(C.FAQS)],
    )


@bp.get("/services/")
def services():
    return render_template(
        "pages/services.html",
        C=C,
        jsonld=[schema.organization(), schema.breadcrumbs([("Services", "pages.services", {})])],
    )


@bp.get("/services/<slug>/")
def service(slug):
    item = C.service_by_slug(slug)
    if not item:
        abort(404)
    others = [s for s in C.SERVICES if s["slug"] != slug]
    return render_template(
        "pages/service.html",
        C=C,
        s=item,
        others=others,
        jsonld=[
            schema.service(item),
            schema.faq(item["faqs"]),
            schema.breadcrumbs([("Services", "pages.services", {}), (item["name"], "pages.service", {"slug": slug})]),
        ],
    )


@bp.get("/process/")
def process():
    return render_template(
        "pages/process.html",
        C=C,
        jsonld=[schema.organization(), schema.breadcrumbs([("How it works", "pages.process", {})])],
    )


@bp.get("/work/")
def work():
    return render_template(
        "pages/work.html",
        C=C,
        jsonld=[schema.organization(), schema.breadcrumbs([("Work", "pages.work", {})])],
    )


@bp.get("/about/")
def about():
    return render_template(
        "pages/about.html",
        C=C,
        jsonld=[schema.person(), schema.breadcrumbs([("About", "pages.about", {})])],
    )


@bp.get("/faq/")
def faq():
    return render_template(
        "pages/faq.html",
        C=C,
        jsonld=[schema.faq(C.FAQS), schema.breadcrumbs([("FAQ", "pages.faq", {})])],
    )


@bp.get("/book/")
def book():
    return render_template(
        "pages/book.html",
        C=C,
        jsonld=[schema.breadcrumbs([("Book a call", "pages.book", {})])],
    )


@bp.get("/contact/")
def contact():
    """The contact form was dropped; email and the booking page replace it. Keeps old links working."""
    return redirect(url_for("pages.book"), code=301)


@bp.get("/privacy/")
def privacy():
    return render_template("pages/privacy.html")


@bp.get("/terms/")
def terms():
    return render_template("pages/terms.html")
