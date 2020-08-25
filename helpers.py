from decimal import Decimal

def checkInput(values):
    for value in values:
        try:
            if value <= 0:
                return False
        except TypeError:
            continue

