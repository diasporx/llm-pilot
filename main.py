import argparse
import json
import os
import re
import sys

from src.client import TrackerClient
from src.serializer import serialize_issue


def sprint_number(sprint_name: str) -> str:
    match = re.search(r"\d+", sprint_name)
    return match.group() if match else re.sub(r"\s+", "-", sprint_name).lower()


def fetch_sprint(sprint: str, queue: str):
    client = TrackerClient()
    num = sprint_number(sprint)
    out_dir = f"data/sprint-{num}"
    os.makedirs(out_dir, exist_ok=True)

    print(f"Fetching sprint '{sprint}', queue '{queue}'...")
    raw_issues = client.search_issues(sprint, queue)
    print(f"Found {len(raw_issues)} issues\n")

    for raw in raw_issues:
        key = raw["key"]
        print(f"  {key}  {raw.get('summary', '')}")
        raw_comments = client.get_comments(key)
        issue = serialize_issue(raw, raw_comments)
        path = f"{out_dir}/{key}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(issue, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(raw_issues)} files → {out_dir}/")


def fetch_issue(issue_key: str, sprint: str = None):
    client = TrackerClient()
    print(f"Fetching issue {issue_key}...")
    raw = client.get_issue(issue_key)
    raw_comments = client.get_comments(issue_key)
    issue = serialize_issue(raw, raw_comments)

    if sprint:
        num = sprint_number(sprint)
    elif issue.get("sprint"):
        num = sprint_number(issue["sprint"])
    else:
        print("Спринт не указан и не найден в задаче. Укажи --sprint, например: issue DEV-17525 --sprint 31")
        sys.exit(1)

    out_dir = f"data/sprint-{num}"
    os.makedirs(out_dir, exist_ok=True)
    path = f"{out_dir}/{issue_key}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(issue, f, ensure_ascii=False, indent=2)
    print(f"Saved → {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Yandex Tracker fetcher")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami", help="Check token and show current user + org IDs")

    p_sprint = sub.add_parser("sprint", help="Fetch all issues in a sprint")
    p_sprint.add_argument("--sprint", required=True, help='e.g. "Спринт 31 ПП"')
    p_sprint.add_argument("--queue", required=True, help='e.g. DEV')

    p_issue = sub.add_parser("issue", help="Fetch a single issue")
    p_issue.add_argument("key", help="e.g. DEV-18281")
    p_issue.add_argument("--sprint", help="Sprint number or name, e.g. 31 or \"Спринт 31 ПП\"")

    args = parser.parse_args()

    if args.cmd == "whoami":
        client = TrackerClient()
        status = client.token_status()
        if status == "valid":
            print("Токен валиден.\n")
        else:
            print(f"Токен недействителен (статус: {status})")
            print("Получи новый токен: https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a")
            sys.exit(1)

        orgs = client.get_orgs_360()
        if orgs:
            print("Найдены организации Яндекс 360:\n")
            for org in orgs:
                print(f"  ORG_ID = \"{org.get('id')}\"  —  {org.get('name')}")
            print("\nВставь нужный ORG_ID в config.py и установи ORG_TYPE = \"yandex360\"")
        else:
            print("Не удалось определить ORG_ID автоматически.")
            print("Найди его вручную:\n")
            print("  Открой https://admin.yandex.ru")
            print("  URL будет вида: https://admin.yandex.ru/company/XXXXXXX/...")
            print("  XXXXXXX — это и есть ORG_ID\n")
            print("  Затем вставь в config.py:")
            print('  ORG_ID = "XXXXXXX"')
    elif args.cmd == "sprint":
        fetch_sprint(args.sprint, args.queue)
    elif args.cmd == "issue":
        fetch_issue(args.key, args.sprint)
