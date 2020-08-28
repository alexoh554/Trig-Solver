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
    thirdAngle = 180.0
    for angle in angles:
        if angle != None:
            thirdAngle = thirdAngle - angle
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
                return math.sin(math.radians(angles[i])) / sides[i]
    return None

def sineLawAngle(angle, side, sineValue):
    sineValue = sineValue * side
    try:
        return math.degrees(math.asin(sineValue))
    except ValueError:
        return None

def sineLawSide(side, angle, sineValue):
    tmp = math.sin(math.radians(angle))
    return tmp / sineValue

def ambiguousCalculate(old, new):
    new2 = 180.0 - new[0]
    ambAngle = 180.0 - new2 - old[0]
    if ambAngle < 0:
        return None
    else:
        newAngles = []
        newAngles.append(old[0])
        newAngles.append(new2)
        newAngles.append(ambAngle)
        return newAngles

def ambiguousOrder(ambAngles, angles):
    key = 0
    newOrder = []
    for i in range(3):
        for j in range(3):
            if ambAngles[i] == angles[j]:
                key = i - j
    for k in range(3):
        index = k + key
        if index == 3:
            index = 0
        if index == -1:
            index = 2
        newOrder.append(ambAngles[index])
            

    return newOrder
            

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
        return math.degrees(math.acos(angle))
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