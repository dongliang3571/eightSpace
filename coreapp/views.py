from coreapp import app
from flask import request, render_template
import datetime


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/themes/')
@app.route('/themes/<number>')
def themes(number=None):
    if number:
        newfile_name = "/themepages/theme" + number + ".html"
    else:
        newfile_name = "/themepages/theme.html"

    return render_template(newfile_name)


@app.route('/stores/<number>')
def stores(number):
    newfile_name = "/storepages/store" + number + ".html"
    return render_template(newfile_name)


if __name__ == "__main__":
    app.debug = True
    app.run()
