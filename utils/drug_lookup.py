"""
Drug lookup utility using OpenFDA.
Version aligned with V07.1 – kept focused and robust.
"""

from __future__ import annotations

import logging
from typing import Any

import requests

from config import OPENFDA_LABEL_URL, OPENFDA_TIMEOUT

logger = logging.getLogger(__name__)


def search_drug(name: str) -> dict[str, Any] | None:
    """
    Perform a basic OpenFDA drug label search.

    Returns a compact dictionary of useful fields or an error structure.
    Never raises – always returns a dict or None.
    """
    cleaned = (name or "").strip()
    if len(cleaned) < 2:
        return {"error": "Drug name too short"}

    try:
        params = {
            "search": f'openfda.brand_name:"{cleaned}" OR openfda.generic_name:"{cleaned}"',
            "limit": 1,
        }
        response = requests.get(
            OPENFDA_LABEL_URL,
            params=params,
            timeout=OPENFDA_TIMEOUT,
        )

        if response.status_code != 200:
            logger.warning("OpenFDA returned status %s", response.status_code)
            return {"error": f"API returned status {response.status_code}"}

        payload = response.json()
        results = payload.get("results") or []
        if not results:
            return {"message": "No matching drug label found"}

        item = results[0]
        openfda = item.get("openfda") or {}

        def first(field: str) -> str:
            values = openfda.get(field)
            if isinstance(values, list) and values:
                return str(values[0])
            return "N/A"

        result: dict[str, Any] = {
            "brand_name": first("brand_name"),
            "generic_name": first("generic_name"),
            "manufacturer": first("manufacturer_name"),
            "route": first("route"),
        }

        # Optional longer fields (truncated for readability)
        if "indications_and_usage" in item and item["indications_and_usage"]:
            text = item["indications_and_usage"][0]
            result["indications_snippet"] = text[:320] + ("..." if len(text) > 320 else "")

        if "warnings" in item and item["warnings"]:
            text = item["warnings"][0]
            result["warnings_snippet"] = text[:320] + ("..." if len(text) > 320 else "")

        return result

    except requests.Timeout:
        logger.warning("OpenFDA request timed out")
        return {"error": "Request timed out"}
    except Exception as exc:
        logger.exception("Unexpected error in drug lookup")
        return {"error": str(exc)}
