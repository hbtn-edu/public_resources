#!/usr/bin/env python3
"""
Lab: First steps with pdb.

Compute an adjusted average from raw scores. The script runs, but the result
is wrong due to a logic bug that is easier to isolate with pdb than with
ad-hoc prints.
"""


def normalize_score(raw, bonus):
    """Apply bonus and cap score at 100."""
    adjusted = raw + bonus
    if adjusted > 100:
        adjusted = 100
    return adjusted


def compute_adjusted_average(scores, bonus):
    """Return rounded average after normalization."""
    raw_sum = 0
    count = 0

    for raw in scores:
        adjusted = normalize_score(raw, bonus)
        raw_sum += raw
        count += 1

    if count == 0:
        return 0.0

    return round(raw_sum / count, 2)


def main():
    scores = [40, 60, 80]
    bonus = 10
    final_avg = compute_adjusted_average(scores, bonus)
    print("Adjusted average:", final_avg)


if __name__ == "__main__":
    main()
