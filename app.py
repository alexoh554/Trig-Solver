from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
import requests
from tempfile import mkdtemp

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
        return render_template('solved.html')
    else:
        return render_template("unsolved.html")





if __name__ == '__main__':
    app.secret_key = '\xe6\x0c\xa7\x0f\x8b\xf4u\xcbd\xb1\x17\xe1\xc54O!R\n\x01B\xb5S\x11X'
    app.run()
