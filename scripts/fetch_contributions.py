import json
from pathlib import Path
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup


USERNAME = "adix4612"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")


def main():

    print(f"Fetching contributions for {USERNAME}...")

    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    days = []

    for cell in soup.select(
        "td.ContributionCalendar-day"
    ):

        date = cell.get("data-date")

        level = cell.get(
            "data-level",
            "0"
        )

        if date:

            try:

                days.append({
                    "date": date,
                    "level": int(level)
                })

            except ValueError:
                pass

    if not days:
        raise RuntimeError(
            "No contribution cells found."
        )

    total = sum(
        item["level"]
        for item in days
    )

    current_streak = 0

    for item in reversed(days):

        if item["level"] > 0:
            current_streak += 1

        else:
            break

    longest_streak = 0
    running = 0

    for item in days:

        if item["level"] > 0:

            running += 1

            longest_streak = max(
                longest_streak,
                running
            )

        else:

            running = 0

    best_day = max(
        days,
        key=lambda x: x["level"],
        default=None
    )

    monthly = {}

    for item in days:

        month = item["date"][:7]

        monthly[month] = (
            monthly.get(month, 0)
            + item["level"]
        )

    data = {
        "username": USERNAME,

        "updated": datetime.now(
            timezone.utc
        ).isoformat(),

        "days": days,

        "stats": {
            "total": total,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "best_day": best_day,
            "monthly": monthly
        }
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT.write_text(
        json.dumps(
            data,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        f"Saved {OUTPUT}"
    )


if __name__ == "__main__":
    main()
