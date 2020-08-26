from decimal import Decimal
import math

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
        totalAngles = Decimal(0)
        for angle in angles:
            totalAngles += Decimal(angle)
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

def countList(items):
    count = 0
    for item in items:
        if item == None:
            continue
        count += 1
    return count

def sinePossible(angles, sides):
    for i in range(3):
        if angles[i] != None:
            if sides[i] != None:
                sine = math.sin(math.radians(angles[i])) / sides[i]
                return sine
    return None

def sineLawAngle(angle, side, sineValue):
    sineValue = sineValue * side
    angle = math.asin(math.radians(sineValue))
    return angle

def sineLawSide(side, angle, sineValue):
    tmp = math.sin(math.radians(angle))
    side = tmp / sineValue
    return side
