from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
import requests
from tempfile import mkdtemp

from helpers import checkInput, checkAngles, findThirdAngle, countList, sinePossible, sineLawAngle, sineLawSide, ambiguousCalculate, ambiguousOrder, sineLawAmb, cosineAngle, cosineSide


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def trig(): 
    if request.method == "POST":
        # Add user values to lists
        tmpAngles = []
        tmpAngles.append(request.form.get("A"))
        tmpAngles.append(request.form.get("B"))
        tmpAngles.append(request.form.get("C"))

        tmpSides = []
        tmpSides.append(request.form.get("a"))
        tmpSides.append(request.form.get("b"))
        tmpSides.append(request.form.get("c"))

        ambOld = []                                     # Stores angles that were given to by the user
                                                        # Cast values to float. If error occurs redirect to error page
        angles = []
        for angle in tmpAngles:
            if angle == "":
                angles.append(None)
            else:
                try:
                    angles.append(float(angle))
                    ambOld.append(float(angle))
                except ValueError:
                    session['error'] = "Invalid input"
                    return redirect("/error")

        sides = []
        for side in tmpSides:
            if side == "":
                sides.append(None)
            else:
                try:
                    sides.append(float(side))
                except ValueError:
                    session['error'] = "Invalid input"
                    return redirect("/error")
        
        # Check for correct input
        correctSides = checkInput(sides)
        correctAngles = checkInput(angles)
        if correctSides == False or correctAngles == False:
            session['error'] = "Invalid input"
            return redirect("/error")

        # If possible get the third angle
        if checkAngles(angles) == True:
            thirdAngle = findThirdAngle(angles)
            for i in range(len(angles)):
                if angles[i] == None:
                    angles[i] = thirdAngle
        if checkAngles(angles) == "Error":
            session['error'] = "Triangles must have a total angle of 180 degrees"
            return redirect("/error")

        knownAngles = countList(angles)
        knownSides = countList(sides)
        if knownSides < 1:
            session['error'] = "You must provide at least 1 side to be able to solve"
            return redirect("/error")

        ambiguousCase = False                           # True if ambiguous case is possible
        ambNew = []                                     # List that stores new angles found during sine law
        # First check if sine law is possible
        sineValue = sinePossible(angles, sides)
        if sineValue != None:
            # Calculate with sine law until all values are found
            while(True):
                for i in range(3):
                    if angles[i] == None:
                        if sides[i] == None:
                            continue
                        else:
                            angles[i] = sineLawAngle(angles[i], sides[i], sineValue)
                            if angles[i] == None:
                                session['error'] = "No solution"
                                return redirect("/error")
                            ambNew.append(angles[i])
                    if sides[i] == None:
                        if angles[i] == None:
                            continue
                        else:
                            sides[i] = sineLawSide(sides[i], angles[i], sineValue)
                if checkAngles(angles) == True:
                    thirdAngle = findThirdAngle(angles)
                    for i in range(len(angles)):
                        if angles[i] == None:
                            angles[i] = thirdAngle
                if None in sides:
                    continue
                else:
                    break
            # If possible solve ambiguous case
            if len(ambOld) == 1 and len(ambNew) == 1:
                ambiguousAngles = ambiguousCalculate(ambOld, ambNew)
                if ambiguousAngles != None:
                    ambiguousCase = True
                    findAmb = ambiguousAngles[2]
                    ambiguousAngles = ambiguousOrder(ambiguousAngles, angles)
                    # Use sine law to find ambiguous side
                    ambiguousSides = sides.copy()
                    ambIndex = 0
                    for i in range(3):
                        if ambiguousAngles[i] == findAmb:
                            ambIndex = i
                    ambiguousSides[ambIndex] = sineLawAmb(ambiguousAngles, ambiguousSides, ambIndex)
                    for i in range(3):
                        ambiguousSides[i] = round(ambiguousSides[i], 2)
        else:
            while(True):                                    # Calculate with cosine law
                if knownSides == 3:                         # If all sides are known, calculate all angles
                    for i in range(3):
                        angles[i] = cosineAngle(sides, i)
                        if angles[i] == None:
                            session['error'] = "No solution"
                            return redirect("/error")
                else:                                       # Else find all sides and repeat loop until all values known
                    for j in range(3):
                        if sides[j] == None:
                            if angles[j] != None:
                                sides[j] = cosineSide(sides, angles[j], j)
                                knownSides = 3
                if None in sides or None in angles:
                    continue
                else:
                    break

        # Round values to 2 decimal places and store in session
        for i in range(3):
            angles[i] = round(angles[i], 2)
        session['angles'] = angles

        for j in range(3):
            sides[j] = round(sides[j], 2)
        session['sides'] = sides

        if ambiguousCase == True:
            session['ambTrue'] = True
            for k in range(3):
                ambiguousAngles[k] = round(ambiguousAngles[k], 2)
            session['ambAngles'] = ambiguousAngles
            session['ambSides'] = ambiguousSides
        else:
            session['ambTrue'] = False
            session['ambAngles'] = None

        session['inputted'] = True
        return redirect('/solution')
    else:
        return render_template("unsolved.html")

@app.route("/solution", methods=["GET", "POST"])
def solution():
    if request.method == "POST":
        # Clear session and return user to main page
        session.clear()
        return redirect("/")
    else:
        # Check if user has inputted an answer
        if session.get('inputted') != True:
            return redirect("/")
        if session['ambTrue'] == True:
            return render_template("solved.html", ambiguousCase=session['ambTrue'], angles=session['angles'], sides=session['sides'], ambAngles=session['ambAngles'], ambSides=session['ambSides'])
        else:
            return render_template("solved.html", angles=session['angles'], sides=session['sides'])

@app.route("/error", methods=["GET", "POST"])
def error():
    if request.method == "POST":
        session.clear()
        return redirect("/")
    else:
        return render_template("error.html", error_message=session['error'])




if __name__ == '__main__':
    app.secret_key = '\xe6\x0c\xa7\x0f\x8b\xf4u\xcbd\xb1\x17\xe1\xc54O!R\n\x01B\xb5S\x11X'
    app.run()
