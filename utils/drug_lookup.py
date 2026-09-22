"""OpenFDA drug-label lookup with stable results and source provenance."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import requests

from config import OPENFDA_LABEL_URL, OPENFDA_TIMEOUT
from utils.validation import validate_drug_name

logger = logging.getLogger(__name__)
SOURCE_NAME = "U.S. FDA OpenFDA drug labeling API"


def _first(value: Any, default: str = "N/A") -> str:
    if isinstance(value, list) and value:
        return str(value[0]).strip()
    if isinstance(value, str) and value.strip():
        return value.strip()
    return default


def _truncate(text: str, limit: int = 350) -> str:
    text = str(text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."


def _provenance(query: str) -> dict[str, str]:
    return {
        "source": SOURCE_NAME,
        "source_type": "retrieved",
        "source_url": OPENFDA_LABEL_URL,
        "query": query,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def search_drug(name: str) -> dict[str, Any]:
    validation = validate_drug_name(name)
    if not validation.valid:
        return {"status": "error", "message": validation.error}

    cleaned = validation.value
    if not cleaned:
        return {"status": "empty", "message": "No drug name provided."}

    escaped = cleaned.replace('"', '\\\"')
    search_query = (
        f'openfda.brand_name:"{escaped}" OR '
        f'openfda.generic_name:"{escaped}" OR '
        f'openfda.substance_name:"{escaped}"'
    )

    try:
        response = requests.get(
            OPENFDA_LABEL_URL,
            params={"search": search_query, "limit": 1},
            timeout=OPENFDA_TIMEOUT,
        )
        provenance = _provenance(cleaned)

        if response.status_code == 404:
            return {
                "status": "not_found",
                "message": f"No drug label found for '{cleaned}'.",
                **provenance,
            }

        response.raise_for_status()

        try:
            payload = response.json()
        except ValueError:
            logger.warning("OpenFDA returned malformed JSON for '%s'", cleaned)
            return {
                "status": "error",
                "message": "The drug information service returned an invalid response.",
                **provenance,
            }

        if not isinstance(payload, dict):
            return {
                "status": "error",
                "message": "The drug information service returned an unexpected response.",
                **provenance,
            }

        results = payload.get("results")
        if not isinstance(results, list) or not results:
            return {
                "status": "not_found",
                "message": f"No drug label found for '{cleaned}'.",
                **provenance,
            }

        item = results[0]
        if not isinstance(item, dict):
            return {
                "status": "error",
                "message": "The drug information service returned an unexpected record.",
                **provenance,
            }

        openfda = item.get("openfda")
        if not isinstance(openfda, dict):
            openfda = {}

        result: dict[str, Any] = {
            "status": "success",
            **provenance,
            "brand_name": _first(openfda.get("brand_name")),
            "generic_name": _first(openfda.get("generic_name")),
            "substance_name": _first(openfda.get("substance_name")),
            "manufacturer": _first(openfda.get("manufacturer_name")),
            "route": _first(openfda.get("route")),
            "product_type": _first(openfda.get("product_type")),
        }

        fields = (
            ("indications_and_usage", "indications_snippet", 350),
            ("warnings", "warnings_snippet", 350),
            ("boxed_warning", "boxed_warning_snippet", 300),
            ("dosage_and_administration", "dosage_snippet", 280),
        )
        for source_key, result_key, limit in fields:
            value = item.get(source_key)
            if isinstance(value, list) and value and value[0]:
                result[result_key] = _truncate(value[0], limit=limit)

        if openfda.get("package_ndc"):
            result["example_ndc"] = _first(openfda.get("package_ndc"))

        return result

    except requests.Timeout:
        logger.warning("OpenFDA timeout for '%s'", cleaned)
        return {
            "status": "error",
            "message": "Request timed out. Please try again.",
            **_provenance(cleaned),
        }
    except requests.HTTPError as exc:
        logger.warning("OpenFDA HTTP error for '%s': %s", cleaned, exc)
        return {
            "status": "error",
            "message": "The drug information service could not complete the request.",
            **_provenance(cleaned),
        }
    except requests.RequestException as exc:
        logger.warning("OpenFDA request error for '%s': %s", cleaned, exc)
        return {
            "status": "error",
            "message": "Network or drug-information service request failed.",
            **_provenance(cleaned),
        }
    except Exception:
        logger.exception("Unexpected error in drug lookup")
        return {
            "status": "error",
            "message": "Unexpected error occurred while retrieving drug information.",
            **_provenance(cleaned),
        }
