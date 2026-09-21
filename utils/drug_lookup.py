import requests

def search_drug(name: str):
    """
    Very basic OpenFDA lookup.
    Returns a small dict with available info or None.
    Kept simple for V-0.7.
    """
    if not name or len(name.strip()) < 2:
        return None

    try:
        # OpenFDA drug label endpoint
        url = "https://api.fda.gov/drug/label.json"
        params = {
            "search": f'openfda.brand_name:"{name}" OR openfda.generic_name:"{name}"',
            "limit": 1
        }
        resp = requests.get(url, params=params, timeout=8)

        if resp.status_code != 200:
            return {"error": f"API returned {resp.status_code}"}

        data = resp.json()
        if "results" not in data or len(data["results"]) == 0:
            return {"message": "No matching drug label found"}

        item = data["results"][0]
        openfda = item.get("openfda", {})

        result = {
            "brand_name": openfda.get("brand_name", ["N/A"])[0] if openfda.get("brand_name") else "N/A",
            "generic_name": openfda.get("generic_name", ["N/A"])[0] if openfda.get("generic_name") else "N/A",
            "manufacturer": openfda.get("manufacturer_name", ["N/A"])[0] if openfda.get("manufacturer_name") else "N/A",
            "route": openfda.get("route", ["N/A"])[0] if openfda.get("route") else "N/A",
        }

        # Add a couple more fields if present
        if "indications_and_usage" in item:
            result["indications_snippet"] = item["indications_and_usage"][0][:300] + "..."
        if "warnings" in item:
            result["warnings_snippet"] = item["warnings"][0][:300] + "..."

        return result

    except Exception as e:
        return {"error": str(e)}
