from __future__ import annotations

from typing import Any
from neo4j import GraphDatabase
from .config import settings

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        if not settings.cognodb_uri or not settings.cognodb_password:
            raise RuntimeError("CognoDB credentials are not configured.")
        _driver = GraphDatabase.driver(
            settings.cognodb_uri,
            auth=(settings.cognodb_user, settings.cognodb_password),
        )
    return _driver


def run_query(query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, params or {})
        return [record.data() for record in result]


def verify_connection() -> bool:
    try:
        get_driver().verify_connectivity()
        return True
    except Exception:
        return False


def close_driver() -> None:
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
