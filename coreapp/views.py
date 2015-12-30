# This Python file uses the following encoding: utf-8
from coreapp import app
from flask import request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = SQLAlchemy(app)

from models import message
from models import admin


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
    he = "yes"
    return render_template("about.html", he = he)

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

@app.route('/authentication/', methods=['GET', 'POST'])
def authentication():
    if request.method == 'POST':
        admin_object = admin.query.filter_by(id="1")[0]
        db_username = admin_object.username
        db_password = admin_object.password

        attempted_username = request.form['username']
        attempted_password = request.form['password']

        if db_username == attempted_username and db_password == attempted_password:
            session['logged_in'] = True
            flash(u"你已成功登陆")
            return redirect("/wall/")
        else:
            flash(u"账号密码错误")
            return redirect("/home/")

    else:
        flash(u"账号密码错误")
        return redirect("/home/")

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash(u"你已成功登出")
    return redirect(url_for('home'))
