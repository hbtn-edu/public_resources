#!/usr/bin/env python3
"""
Lab: Debugging with print().

Quality check: count how many sensor readings are at or above a minimum
acceptable level (threshold). This starter contains a logic bug (no crash).

There are several spots where temporary print() calls can help inspect
state during the loop.
"""

def reading_is_ok(value, threshold):
    """
    Return True if the reading meets or exceeds the threshold.

    (Per spec: "OK" means value is at or above the threshold.)
    """
    return value < threshold


def count_ok_readings(readings, threshold):
    """Return how many readings count as OK."""
    ok_count = 0
    index = 0
    for value in readings:
        passes = reading_is_ok(value, threshold)
        if passes:
            ok_count += 1
        index += 1
    return ok_count


def main():
    readings = [10, 50, 55, 90, 12]
    threshold = 50
    result = count_ok_readings(readings, threshold)
    print("OK readings:", result)


if __name__ == "__main__":
    main()
