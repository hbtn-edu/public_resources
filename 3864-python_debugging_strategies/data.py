#!/usr/bin/env python3
"""
Lab: Following the data.

Goal: compute total order amount after discount.
The script runs but produces wrong totals due to bad data propagation
across multiple functions.
"""


def parse_discount_rate(percent_text):
    """Convert percentage text to decimal rate (e.g. '10' -> 0.10)."""
    value = float(percent_text)
    return value


def compute_subtotal(items):
    """Return subtotal from (name, price, qty) rows."""
    subtotal = 0.0
    for _, unit_price, qty in items:
        subtotal += unit_price * qty
    return subtotal


def apply_discount(subtotal, discount_rate):
    """Apply percentage discount to subtotal."""
    return subtotal * (1 - discount_rate)


def compute_final_total(items, discount_text):
    """Compute final total from cart rows and textual discount."""
    subtotal = compute_subtotal(items)
    rate = parse_discount_rate(discount_text)
    discounted_amount = apply_discount(subtotal, rate)
    return round(discounted_amount, 2)


def main():
    cart = [
        ("notebook", 12.50, 2),
        ("pen", 1.20, 5),
        ("eraser", 0.80, 1),
    ]
    discount_text = "10"
    final_total = compute_final_total(cart, discount_text)
    print("Final total:", final_total)


if __name__ == "__main__":
    main()
