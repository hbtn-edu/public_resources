#!/usr/bin/env python3
"""
Lab: Reading the bug.

Batch summary for a stub sensor: sum numeric readings.
This script is intentionally broken for debugging practice.
"""

def accumulate_readings(values):
    """Sum all readings into a single running sum."""
    running_sum = 0
    for value in values:
        running_sum += value
    return running_sum


def load_today_batch():
    """Return today's readings from the (stub) pipeline."""
    # In production this might come from a file or API; here it is hard-coded.
    return ["12", "5", "7"]


def main():
    batch = load_today_batch()
    result = accumulate_readings(batch)
    print("Total readings:", result)


if __name__ == "__main__":
    main()
