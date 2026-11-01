from datetime import date

import httpx

API_URL = "https://api.dane.gov.pl/1.4/datasets/{dataset_id}/resources"

# names to keys:
FILES = {
    "rejestr podstawowy": "basic",
    "rejestr kart": "cards",
}


def latest_version(client: httpx.Client, dataset_id: str) -> tuple[date, dict[str, str]]:
    resp = client.get(API_URL.format(dataset_id=dataset_id),
                      params={"sort": "-data_date", "per_page": 50})
    resp.raise_for_status()
    resources = [r["attributes"] for r in resp.json()["data"]]
    published = resources[0]["data_date"]
    urls = {}
    for attrs in resources:
        if attrs["data_date"] != published:
            continue
        base = attrs["title"].split(" - ")[0].strip().lower()
        if base in FILES:
            urls[FILES[base]] = attrs["download_url"]
    missing = set(FILES.values()) - urls.keys()
    if missing:
        raise RuntimeError(f"version {published} is missing files: {sorted(missing)}")
    return date.fromisoformat(published), urls


def download_all(client: httpx.Client, urls: dict[str, str]) -> dict[str, bytes]:
    files = {}
    for key, url in urls.items():
        resp = client.get(url, follow_redirects=True)
        resp.raise_for_status()
        files[key] = resp.content
    return files
