"""JSON-LD structured data for search engines and AI answer engines."""
from flask import current_app, url_for

AREA_SERVED = ["US", "CA", "GB", "IE", "EU", "AU", "NZ", "SG"]


def _site():
    return current_app.config["SITE_URL"]


def _abs(endpoint, **values):
    return _site() + url_for(endpoint, **values)


def _logo():
    return {"@type": "ImageObject", "url": _abs("static", filename="img/ron-mark.svg"), "width": 300, "height": 215}


def _same_as():
    return [v for v in current_app.config["SOCIAL"].values() if v]


def person():
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": _site() + "/#person",
        "name": "Rolando Tactay",
        "alternateName": "Ron Tactay",
        "jobTitle": "IT systems, automation and AI consultant",
        "url": _abs("pages.about"),
        "image": _abs("static", filename="img/ron-profile.webp"),
        "worksFor": {"@id": _site() + "/#org"},
        "homeLocation": {"@type": "Place", "name": "Manila, Philippines"},
        "knowsAbout": [
            "Workflow automation", "n8n", "Zapier", "Make", "Microsoft Power Automate",
            "AI agents", "Retrieval-augmented generation", "Systems architecture",
            "Application support", "Microsoft 365", "AWS", "PostgreSQL", "Self-hosting",
        ],
    }
    if _same_as():
        data["sameAs"] = _same_as()
    return data


def organization():
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": _site() + "/#org",
        "name": current_app.config["SITE_NAME"],
        "url": _site() + "/",
        "email": current_app.config["CONTACT_EMAIL"],
        "description": (
            "IT systems, automation and AI consulting for small and medium businesses: "
            "tech check-ups and roadmaps, workflow automation, practical AI, software selection, "
            "systems setup, custom tools and ongoing support."
        ),
        "logo": _logo(),
        "image": _logo()["url"],
        "founder": {"@id": _site() + "/#person"},
        "areaServed": AREA_SERVED,
        "knowsLanguage": "en",
    }
    if _same_as():
        data["sameAs"] = _same_as()
    return data


def website():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": _site() + "/#website",
        "name": current_app.config["SITE_NAME"],
        "url": _site() + "/",
        "publisher": {"@id": _site() + "/#org"},
        "inLanguage": "en-US",
    }


def service(s):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["name"],
        "serviceType": s["name"],
        "description": s["answer"],
        "url": _abs("pages.service", slug=s["slug"]),
        "provider": {"@id": _site() + "/#org"},
        "areaServed": AREA_SERVED,
    }


def faq(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }


def breadcrumbs(items):
    elements = [{"@type": "ListItem", "position": 1, "name": "Home", "item": _site() + "/"}]
    for i, (name, endpoint, values) in enumerate(items, start=2):
        elements.append({"@type": "ListItem", "position": i, "name": name, "item": _abs(endpoint, **values)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements}


def article(item, endpoint):
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting" if endpoint == "content.resource" else "VideoObject",
        "headline" if endpoint == "content.resource" else "name": item["title"],
        "description": item["description"],
        "url": _abs(endpoint, slug=item["slug"]),
        "author": {"@id": _site() + "/#person"},
        "publisher": {"@id": _site() + "/#org"},
    }
    if endpoint == "content.resource":
        data["datePublished"] = item["published"]
        data["dateModified"] = item.get("updated") or item["published"]
    else:
        data["uploadDate"] = item["published"]
        if item.get("youtube_id"):
            data["embedUrl"] = f"https://www.youtube-nocookie.com/embed/{item['youtube_id']}"
            data["thumbnailUrl"] = f"https://i.ytimg.com/vi/{item['youtube_id']}/hqdefault.jpg"
    return data
