import requests
from config import TRACKER_TOKEN, ORG_ID, ORG_TYPE, BASE_URL


class TrackerClient:
    def __init__(self):
        self.session = requests.Session()
        org_header = "X-Org-ID" if ORG_TYPE == "yandex360" else "X-Cloud-Org-ID"
        self.session.headers.update({
            "Authorization": f"OAuth {TRACKER_TOKEN}",
            org_header: ORG_ID,
            "Content-Type": "application/json",
        })

    def _raise(self, r: requests.Response):
        if not r.ok:
            try:
                detail = r.json()
            except Exception:
                detail = r.text
            raise SystemExit(f"HTTP {r.status_code} {r.url}\n{detail}")

    def token_status(self) -> str:
        r = requests.get(
            f"{BASE_URL}/myself",
            headers={"Authorization": f"OAuth {TRACKER_TOKEN}"},
        )
        if r.status_code == 422:
            return "valid"
        if r.status_code == 401:
            return "invalid"
        return f"unknown ({r.status_code})"

    def get_orgs_360(self) -> list:
        r = requests.get(
            "https://api360.yandex.net/directory/v1/org/",
            headers={"Authorization": f"OAuth {TRACKER_TOKEN}"},
        )
        if r.ok:
            return r.json().get("organizations", [])
        return []

    def get_issue(self, issue_key: str) -> dict:
        r = self.session.get(f"{BASE_URL}/issues/{issue_key}")
        self._raise(r)
        return r.json()

    def get_comments(self, issue_key: str) -> list:
        r = self.session.get(f"{BASE_URL}/issues/{issue_key}/comments")
        self._raise(r)
        return r.json()

    def search_issues(self, sprint: str, queue: str) -> list:
        payload = {"filter": {"queue": queue, "sprint": sprint}}
        issues, page = [], 1
        while True:
            r = self.session.post(
                f"{BASE_URL}/issues/_search",
                json=payload,
                params={"page": page, "perPage": 100},
            )
            self._raise(r)
            batch = r.json()
            if not batch:
                break
            issues.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return issues
