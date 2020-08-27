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
    try:
        angle = math.degrees(math.asin(sineValue))
        return angle
    except ValueError:
        return None

def sineLawSide(side, angle, sineValue):
    tmp = math.sin(math.radians(angle))
    side = tmp / sineValue
    return side

def ambiguousCalculate(old, new):
    new2 = Decimal(180) - Decimal(new[0])
    ambAngle = Decimal(180) - Decimal(new2) - Decimal(old[0])
    if ambAngle < 0:
        return None
    else:
        newAngles = []
        newAngles.append(old)
        newAngles.append(new2)
        newAngles.append(ambAngle)
        return newAngles

def cosineAngle(sides, key):
    # Reorder sides by key
    newSides = []
    newSides.append(sides[key])
    for side in sides:
        if side != sides[key]:
            newSides.append(side)
    # Run formula
    numerator = newSides[1]**2 + newSides[2]**2 - newSides[0]**2
    denominator = 2 * newSides[1] * newSides[2]
    angle = numerator / denominator
    try:
        angle = math.degrees(math.acos(angle))
        return angle
    except ValueError:
        return None
def cosineSide(sides, angle, key):
    # Find angles that are not key
    otherSides = []
    for side in sides:
        if side != sides[key]:
            otherSides.append(side)
    equation1 = otherSides[0]**2 + otherSides[1]**2
    equation2 = 2 * otherSides[0] * otherSides[1] * math.cos(math.radians(angle))
    newSide = equation1 - equation2
    return math.sqrt(newSide)