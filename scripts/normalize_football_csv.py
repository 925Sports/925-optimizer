#!/usr/bin/env python3
"""
Normalize NFL/CFB PrizePicks optimizer CSVs so columns match the multi-sport tool.

Source Google Sheet columns are shifted:
  - "Odds Type" column contains sport name (NFL/CFB)
  - "Headshot URL" column contains standard/demon/goblin
  - "Data ID" column contains the real headshot URL
  - Edge lives in "% Edge" (tool expects "Edge %")
"""
import csv
import sys
from pathlib import Path

def normalize(in_path: Path, out_path: Path) -> int:
    with in_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not reader.fieldnames:
            out_path.write_text("", encoding="utf-8")
            return 0

    normalized = []
    for r in rows:
        odds_raw = (r.get("Headshot URL") or r.get("Odds Type") or "standard").strip().lower()
        odds = odds_raw if odds_raw in ("standard", "demon", "goblin") else "standard"

        headshot = (r.get("Headshot URL") or "").strip()
        if not headshot.startswith("http"):
            headshot = (r.get("Data ID") or "").strip()

        edge = (r.get("Edge %") or r.get("% Edge") or "").strip()

        new_row = {
            "Date": r.get("Date", ""),
            "Start Time": r.get("Start Time", ""),
            "Player Name": r.get("Player Name", ""),
            "Stat Type": r.get("Stat Type", ""),
            "Line Score": r.get("Line Score", ""),
            "Odds Type": odds,
            "Headshot URL": headshot,
            "Data ID": r.get("Data ID", ""),
            "Over %": r.get("Over %", ""),
            "Under %": r.get("Under %", ""),
            "No-Vig Over %": r.get("No-Vig Over %", ""),
            "No-Vig Under %": r.get("No-Vig Under %", ""),
            "True Point": r.get("True Point", ""),
            "Average Line": r.get("Average Line", ""),
            "Average Over %": r.get("Average Over %", ""),
            "Average Under %": r.get("Average Under %", ""),
            "Average No-Vig Over %": r.get("Average No-Vig Over %", ""),
            "Average No-Vig Under %": r.get("Average No-Vig Under %", ""),
            "Percent Difference": r.get("Percent Difference", ""),
            "Max No-Vig %": r.get("Max No-Vig %", ""),
            "Bet Tag": (r.get("Bet Tag") or "").strip(),
            "Projection": r.get("Projection", ""),
            "Projection vs Line": r.get("Projection vs Line", ""),
            "Edge %": edge,
            "Correlates": r.get("Correlates", ""),
            "Team": r.get("Team", "") or r.get("team", ""),
            "Game Short Title": r.get("Game Short Title", "") or r.get("Game", ""),
            "Fav": r.get("Fav", ""),
            "O/U": r.get("O/U", "") or r.get("Over/Under", ""),
            "Callout Bet Tag": r.get("Callout Bet Tag", ""),
            "Position": r.get("Position", ""),
        }
        if new_row["Player Name"] and new_row["Line Score"]:
            normalized.append(new_row)

    fieldnames = list(normalized[0].keys()) if normalized else [
        "Date","Start Time","Player Name","Stat Type","Line Score","Odds Type",
        "Headshot URL","Data ID","Over %","Under %","No-Vig Over %","No-Vig Under %",
        "True Point","Average Line","Average Over %","Average Under %",
        "Average No-Vig Over %","Average No-Vig Under %","Percent Difference",
        "Max No-Vig %","Bet Tag","Projection","Projection vs Line","Edge %",
        "Correlates","Team","Game Short Title","Fav","O/U","Callout Bet Tag","Position",
    ]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(normalized)

    return len(normalized)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: normalize_football_csv.py <input.csv> <output.csv>")
        sys.exit(1)
    n = normalize(Path(sys.argv[1]), Path(sys.argv[2]))
    print(f"Normalized {n} rows → {sys.argv[2]}")
