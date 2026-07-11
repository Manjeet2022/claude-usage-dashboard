#!/usr/bin/env python3
import os
import json
from datetime import datetime, timedelta, timezone

import requests

API_BASE = "https://api.anthropic.com/v1/organizations"
ANTHROPIC_VERSION = "2023-06-01"
DAYS_BACK = 7
REVIEW_THRESHOLD_USD = 500

ORGS = [
    {"name": "Antiersolutions-exchange",     "key": os.getenv("ORG1_ADMIN_KEY", "")},
    {"name": "Antiersolutions-DeFi",          "key": os.getenv("ORG2_ADMIN_KEY", "")},
    {"name": "Antier-QA",                     "key": os.getenv("ORG3_ADMIN_KEY", "")},
    {"name": "Antier.Mobile.Ror",             "key": os.getenv("ORG4_ADMIN_KEY", "")},
    {"name": "3rd floor Antiersolutions",     "key": os.getenv("ORG5_ADMIN_KEY", "")},
    {"name": "Antier - Gaming and Metaverse", "key": os.getenv("ORG6_ADMIN_KEY", "")},
]


def fetch_org(org, starting_at, ending_at):
    name, key = org["name"], org["key"]
    if not key:
        return {"name": name, "tokens": 0, "cost": 0, "status": "no_key"}

    headers = {"anthropic-version": ANTHROPIC_VERSION, "x-api-key": key}

    try:
        usage_res = requests.get(
            f"{API_BASE}/usage_report/messages",
            headers=headers,
            params={"starting_at": starting_at, "ending_at": ending_at, "bucket_width": "1d"},
            timeout=30,
        )
        cost_res = requests.get(
            f"{API_BASE}/cost_report",
            headers=headers,
            params={"starting_at": starting_at, "ending_at": ending_at, "bucket_width": "1d", "limit": 31},
            timeout=30,
        )

        if usage_res.status_code != 200 or cost_res.status_code != 200:
            return {"name": name, "tokens": 0, "cost": 0, "status": "error"}

        tokens = 0
        for bucket in usage_res.json().get("data", []):
            for r in bucket.get("results", []):
                tokens += (r.get("uncached_input_tokens") or 0)
                tokens += (r.get("cache_creation_input_tokens") or 0)
                tokens += (r.get("output_tokens") or 0)

        cost = 0.0
        for bucket in cost_res.json().get("data", []):
            for r in bucket.get("results", []):
                amount = r.get("amount", 0)
                try:
                    amount = float(amount)
                except (ValueError, TypeError):
                    amount = 0.0
                cost += amount

        status = "review" if cost > REVIEW_THRESHOLD_USD else "ok"
        return {"name": name, "tokens": tokens, "cost": round(cost, 2), "status": status}

    except requests.RequestException:
        return {"name": name, "tokens": 0, "cost": 0, "status": "error"}


def main():
    ending_at = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    starting_at = ending_at - timedelta(days=DAYS_BACK)
    starting_str = starting_at.strftime("%Y-%m-%dT%H:%M:%SZ")
    ending_str = ending_at.strftime("%Y-%m-%dT%H:%M:%SZ")

    results = [fetch_org(org, starting_str, ending_str) for org in ORGS]

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "period": {"start": starting_str, "end": ending_str},
        "organizations": results,
        "total_tokens": sum(r["tokens"] for r in results),
        "total_cost": round(sum(r["cost"] for r in results), 2),
    }

    with open("data.json", "w") as f:
        json.dump(output, f, indent=2)

    print("data.json written:", json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
