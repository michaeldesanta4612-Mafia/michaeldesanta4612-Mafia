import json
from pathlib import Path
from datetime import datetime


INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0"
]

CELL = 13
GAP = 4

LEFT = 60
TOP = 45

WEEKS = 53
DAYS = 7


def main():

    if not INPUT.exists():
        raise FileNotFoundError(
            "data/contributions.json not found."
        )

    data = json.loads(
        INPUT.read_text(
            encoding="utf-8"
        )
    )

    lookup = {
        item["date"]: item["level"]
        for item in data["days"]
    }

    dates = sorted(lookup.keys())

    # Keep the latest 371 days
    dates = dates[-371:]

    # Fill missing positions
    dates = (
        [""] * (371 - len(dates))
        + dates
    )

    svg = []

    svg.append(
        '''<svg
xmlns="http://www.w3.org/2000/svg"
width="860"
height="185"
viewBox="0 0 860 185">

<style>

.terminal {
    font-family: "Courier New", monospace;
}

.cell {
    opacity: 0;
    animation: reveal .35s ease-out forwards;
}

@keyframes reveal {

    from {
        opacity: 0;
        transform: translateY(-8px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}

</style>

<rect
width="860"
height="185"
rx="12"
fill="#090d14"/>

<text
x="20"
y="25"
class="terminal"
font-size="15"
fill="#39d353">

adix4612@github ~ $ ./contributions.sh

</text>
'''
    )

    # Day labels
    labels = {
        1: "Mon",
        3: "Wed",
        5: "Fri"
    }

    for day, label in labels.items():

        y = (
            TOP
            + day * (CELL + GAP)
            + 10
        )

        svg.append(
            f'''
<text
x="8"
y="{y}"
class="terminal"
font-size="10"
fill="#8b949e">

{label}

</text>
'''
        )

    # Contribution cells
    for week in range(WEEKS):

        for day in range(DAYS):

            index = (
                week * DAYS
                + day
            )

            if index >= len(dates):
                continue

            date = dates[index]

            if date:

                level = lookup.get(
                    date,
                    0
                )

            else:

                level = 0

            level = max(
                0,
                min(
                    int(level),
                    5
                )
            )

            x = (
                LEFT
                + week * (CELL + GAP)
            )

            y = (
                TOP
                + day * (CELL + GAP)
            )

            delay = (
                week * 0.02
                + day * 0.01
            )

            svg.append(
                f'''
<g
class="cell"
style="animation-delay:{delay:.3f}s">

<rect
x="{x}"
y="{y}"
width="{CELL}"
height="{CELL}"
rx="3"
fill="{PALETTE[level]}"/>

<title>
{date}: contribution level {level}
</title>

</g>
'''
            )

    total = data["stats"]["total"]

    svg.append(
        f'''
<text
x="20"
y="172"
class="terminal"
font-size="12"
fill="#8b949e">

{total:,} contribution levels

</text>

<text
x="600"
y="172"
class="terminal"
font-size="11"
fill="#8b949e">

Less

</text>
'''
    )

    # Legend
    for i, color in enumerate(PALETTE):

        x = 640 + i * 22

        svg.append(
            f'''
<rect
x="{x}"
y="162"
width="16"
height="11"
rx="3"
fill="{color}"/>
'''
        )

    svg.append(
        '''
<text
x="785"
y="172"
class="terminal"
font-size="11"
fill="#8b949e">

More

</text>

</svg>
'''
    )

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8"
    )

    print(
        f"Created {OUTPUT}"
    )


if __name__ == "__main__":
    main()
