#!/usr/bin/env python3
"""Compare recent runs side by side."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wiki_apply_run import collect_runs, print_runs


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare recent wiki runs")
    parser.add_argument("--last", type=int, default=5, help="Anzahl Runs anzeigen")
    args = parser.parse_args()

    runs = collect_runs()[: args.last]
    if not runs:
        print("Keine Runs gefunden in .runs/")
        sys.exit(0)

    print(f"Letzte {len(runs)} Run(s):")
    print_runs(runs)


if __name__ == "__main__":
    main()
