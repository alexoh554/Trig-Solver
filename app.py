from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
import requests
from tempfile import mkdtemp

from helpers import checkInput, checkAngles, findThirdAngle

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
        tmpSides = []
        tmpSides.append(request.form.get("a"))
        tmpSides.append(request.form.get("b"))
        tmpSides.append(request.form.get("c"))

        tmpAngles = []
        tmpAngles.append(request.form.get("A"))
        tmpAngles.append(request.form.get("B"))
        tmpAngles.append(request.form.get("C"))

        # Cast values to float
        sides = []
        for side in tmpSides:
            try:
                sides.append(float(side))
            except ValueError:
                sides.append(None)
        
        angles = []
        for angle in tmpAngles:
            try:
                angles.append(float(angle))
            except ValueError:
                angles.append(None)

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
        elif checkAngles(angles) == "Error":
            session['error'] = "Triangles must have a total angle of 180 degrees"
            return redirect("/error")

        print(angles)
        print(sides)


        return render_template('solved.html')
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
        if not session["A"]:
            return redirect("/")
        return render_template("solved.html")

@app.route("/error", methods=["GET", "POST"])
def error():
    if request.method == "POST":
        session.clear()
        return redirect("/")
    else:
        return render_template("error.html")




if __name__ == '__main__':
    app.secret_key = '\xe6\x0c\xa7\x0f\x8b\xf4u\xcbd\xb1\x17\xe1\xc54O!R\n\x01B\xb5S\x11X'
    app.run()
