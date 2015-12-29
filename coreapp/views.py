from coreapp import app
from flask import request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

from models import message

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

@app.route('/aboutus/')
def about():
    return render_template("about.html")

@app.route('/wall/', methods=['GET', 'POST'])
def wall():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['comment']
        now = datetime.now()
        db.session.add(message(name, content, now))
        db.session.commit()
    messages = db.session.query(message).order_by(desc(message.date)).all()
    return render_template("wall.html", messages=messages)



if __name__ == "__main__":
    app.debug = True
    app.run()
