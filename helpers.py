from decimal import Decimal

def checkInput(values):
    for value in values:
        try:
            if value <= 0:
                return False
        except TypeError:
            continue

def checkAngles(angles):
    knownAngles = 0
    for angle in angles:
        if angle != None:
            knownAngles += 1
    if knownAngles == 2:
        return True
    elif knownAngles == 3:
        totalAngles = 0
        for angle in angles:
            totalAngles += angle
        if totalAngles != 180:
            return "Error"
    else:
        return False

def findThirdAngle(angles):
    thirdAngle = Decimal(180)
    for angle in angles:
        if angle != None:
            thirdAngle = Decimal(thirdAngle) - Decimal(angle)
    return thirdAngle
