"""
Utility functions for Sales Analytics Platform
"""
import pandas as pd
from datetime import datetime


def validate_date(date_str, format="%Y-%m-%d"):
    """Validate and standardize date format"""
    try:
        return datetime.strptime(str(date_str), format).date()
    except ValueError:
        for fmt in ["%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d"]:
            try:
                return datetime.strptime(str(date_str), fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Cannot parse date: {date_str}")


def clean_amount(amount):
    """Clean and convert amount to float"""
    if isinstance(amount, str):
        amount = amount.replace('$', '').replace(',', '').strip()
    try:
        return float(amount)
    except (ValueError, TypeError):
        return 0.0


def format_currency(amount):
    """Format amount as currency string"""
    return f"${amount:,.2f}"


def check_email(email):
    """Validate email format"""
    return "@" in email and "." in email
