from flask import Blueprint, render_template, request
from .config import settings
from .db import run_query, verify_connection
from .queries import (
    LIST_ROLES,
    LIST_SKILLS,
    ROLE_DETAIL,
    MATCH_ROLES_BY_SKILLS,
    DISCOVER_CAREER_PATHS,
    SEARCH_ROLES,
)

bp = Blueprint("main", __name__)

DEMO_PROFILE = {
    "id": "person_sushank",
    "name": "Sushank",
    "skills": ["Python", "SQL", "Machine Learning", "Deep Learning"],
}
DEMO_ROLES = [
    {"id": "ml_engineer", "title": "Machine Learning Engineer", "company_type": "Product / AI", "description": "Build, evaluate and deploy ML models.", "skills": ["Python", "Machine Learning", "SQL"]},
    {"id": "data_scientist", "title": "Data Scientist", "company_type": "Analytics", "description": "Turn data into experiments, insights and predictive models.", "skills": ["Python", "SQL", "Machine Learning"]},
    {"id": "backend_python", "title": "Python Backend Engineer", "company_type": "Software", "description": "Design APIs and data-backed services with Python.", "skills": ["Python", "SQL"]},
    {"id": "ai_engineer", "title": "AI Engineer", "company_type": "AI Platform", "description": "Build applied AI features using deep learning and NLP.", "skills": ["Python", "Deep Learning", "Machine Learning"]},
]
DEMO_COMPANIES = {
    "ml_engineer": ["Nova AI Labs", "GraphWorks"],
    "data_scientist": ["Signal Analytics"],
    "backend_python": ["CraftCloud"],
    "ai_engineer": ["Nova AI Labs"],
}


def _demo_enabled() -> bool:
    return settings.demo_mode or not settings.cognodb_uri or not settings.cognodb_password


@bp.get("/")
def index():
    q = request.args.get("q", "").strip()
    if _demo_enabled():
        roles = DEMO_ROLES
        if q:
            roles = [r for r in roles if q.lower() in r["title"].lower() or q.lower() in r["description"].lower()]
        return render_template("index.html", roles=roles, profile=DEMO_PROFILE, connected=False, demo=True, q=q)
    try:
        roles = run_query(SEARCH_ROLES, {"q": q}) if q else run_query(LIST_ROLES)
        profile = {"id": "person_sushank", "name": "Candidate", "skills": []}
        return render_template("index.html", roles=roles, profile=profile, connected=verify_connection(), demo=False, q=q)
    except Exception:
        return render_template("index.html", roles=[], profile=DEMO_PROFILE, connected=False, demo=False, q=q, error="Database is unreachable. Check your CognoDB settings.")


@bp.get("/role/<role_id>")
def role_detail(role_id: str):
    if _demo_enabled():
        role = next((r for r in DEMO_ROLES if r["id"] == role_id), None)
        if not role:
            return render_template("role.html", role=None), 404
        role = {**role, "companies": DEMO_COMPANIES.get(role_id, [])}
        paths = [{"role": role["title"], "company": c, "path": ["Person:Sushank", "Skill:Python", f"Role:{role['title']}", f"Company:{c}"]} for c in role["companies"]]
        return render_template("role.html", role=role, paths=paths, demo=True)
    try:
        rows = run_query(ROLE_DETAIL, {"role_id": role_id})
        if not rows:
            return render_template("role.html", role=None), 404
        role = rows[0]
        paths = run_query(DISCOVER_CAREER_PATHS, {"person_id": "person_sushank", "current_role_id": role_id})
        return render_template("role.html", role=role, paths=paths, demo=False)
    except Exception:
        return render_template("role.html", role=None, error="Database is unreachable."), 503


@bp.get("/api/recommendations")
def recommendations():
    if _demo_enabled():
        return {"profile": DEMO_PROFILE, "recommendations": [
            {"title": "Machine Learning Engineer", "fit": 75.0, "matched_skills": 3, "total_skills": 4},
            {"title": "Data Scientist", "fit": 100.0, "matched_skills": 3, "total_skills": 3},
            {"title": "Python Backend Engineer", "fit": 100.0, "matched_skills": 2, "total_skills": 2},
            {"title": "AI Engineer", "fit": 66.7, "matched_skills": 2, "total_skills": 3},
        ]}
    try:
        rows = run_query(MATCH_ROLES_BY_SKILLS, {"person_id": "person_sushank"})
        return {"profile": {"id": "person_sushank"}, "recommendations": rows}
    except Exception as exc:
        return {"error": str(exc)}, 503


@bp.get("/health")
def health():
    if _demo_enabled():
        return {"status": "ok", "mode": "demo"}
    return ({"status": "ok"}, 200) if verify_connection() else ({"status": "degraded"}, 503)
