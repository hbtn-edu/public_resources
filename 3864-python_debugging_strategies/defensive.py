#!/usr/bin/env python3
"""
Lab: Defensive debugging and validation.

Goal: compute average score from user-provided text.
Starter assumes ideal input and fails with non-numeric tokens.
"""


def parse_scores_csv(scores_text):
    """Parse comma-separated scores into a list of ints."""
    parts = scores_text.split(",")
    return [int(part) for part in parts]


def average_score(scores):
    """Return arithmetic mean of a non-empty score list."""
    return sum(scores) / len(scores)


def score_band(avg):
    """Classify average score into a textual band."""
    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"


def evaluate_scores(scores_text):
    """Return (average, band) from comma-separated score text."""
    scores = parse_scores_csv(scores_text)
    avg = round(average_score(scores), 2)
    return avg, score_band(avg)


def main():
    scores_text = "90,85,invalid,100"
    avg, band = evaluate_scores(scores_text)
    print("Average:", avg)
    print("Band:", band)


if __name__ == "__main__":
    main()
