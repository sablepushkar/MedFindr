"""
Drug lookup utility using OpenFDA.
Version: 07.2 / 07.3 major compatible

Improved search, structured safety fields, robust error handling.
"""

from __future__ import annotations

import logging
from typing import Any

import requests

from config import OPENFDA_LABEL_URL, OPENFDA_TIMEOUT

logger = logging.getLogger(__name__)


def _first(value: Any, default: str = "N/A") -> str:
    if isinstance(value, list) and value:
        return str(value[0]).strip()
    if isinstance(value, str) and value.strip():
        return value.strip()
    return default


def _truncate(text: str, limit: int = 350) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."


def search_drug(name: str) -> dict[str, Any]:
    cleaned = (name or "").strip()
    if len(cleaned) < 2:
        return {"status": "error", "message": "Drug name is too short"}

    search_query = (
        f'openfda.brand_name:"{cleaned}" OR '
        f'openfda.generic_name:"{cleaned}" OR '
        f'openfda.substance_name:"{cleaned}"'
    )

    try:
        params = {"search": search_query, "limit": 1}
        response = requests.get(OPENFDA_LABEL_URL, params=params, timeout=OPENFDA_TIMEOUT)

        if response.status_code != 200:
            logger.warning("OpenFDA status %s for query '%s'", response.status_code, cleaned)
            return {"status": "error", "message": f"OpenFDA returned status {response.status_code}"}

        payload = response.json()
        results = payload.get("results") or []

        if not results:
            return {"status": "not_found", "message": f"No drug label found for '{cleaned}'", "query": cleaned}

        item = results[0]
        openfda = item.get("openfda") or {}

        result: dict[str, Any] = {
            "status": "success",
            "query": cleaned,
            "brand_name": _first(openfda.get("brand_name")),
            "generic_name": _first(openfda.get("generic_name")),
            "substance_name": _first(openfda.get("substance_name")),
            "manufacturer": _first(openfda.get("manufacturer_name")),
            "route": _first(openfda.get("route")),
            "product_type": _first(openfda.get("product_type")),
        }

        if "indications_and_usage" in item and item["indications_and_usage"]:
            result["indications_snippet"] = _truncate(item["indications_and_usage"][0])

        if "warnings" in item and item["warnings"]:
            result["warnings_snippet"] = _truncate(item["warnings"][0])

        if "boxed_warning" in item and item["boxed_warning"]:
            result["boxed_warning_snippet"] = _truncate(item["boxed_warning"][0], limit=300)

        if "dosage_and_administration" in item and item["dosage_and_administration"]:
            result["dosage_snippet"] = _truncate(item["dosage_and_administration"][0], limit=280)

        if openfda.get("package_ndc"):
            result["example_ndc"] = _first(openfda.get("package_ndc"))

        return result

    except requests.Timeout:
        logger.warning("OpenFDA timeout for '%s'", cleaned)
        return {"status": "error", "message": "Request timed out. Please try again."}
    except requests.RequestException as exc:
        logger.warning("Request error: %s", exc)
        return {"status": "error", "message": "Network or API request failed"}
    except Exception as exc:
        logger.exception("Unexpected error in drug lookup")
        return {"status": "error", "message": "Unexpected error occurred", "detail": str(exc)}
