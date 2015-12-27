from coreapp import app
from flask import request, render_template
import datetime


@app.route('/')
def home():
    return render_template("home.html")



if __name__ == "__main__":
    app.debug = True
    app.run()
