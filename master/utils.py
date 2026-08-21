from decimal import Decimal, InvalidOperation

def to_decimal(value):
    try:
        return Decimal(value or 0)
    except (InvalidOperation, TypeError, ValueError):
        return Decimal('0.00')
