# This Python file uses the following encoding: utf-8
from coreapp import app
from flask import request, render_template, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import desc
import json
from werkzeug import secure_filename
import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = SQLAlchemy(app)

folder = "static/uploaded"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# UPLOAD_FOLDER = os.path.join(BASE_DIR, folder)
UPLOAD_FOLDER =  "/home/vcap/fs/838c48b47588a13"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/aboutus/', methods=['GET', 'POST'])
def about():
    if request.method == "POST":
        img = request.form['image']
        print img
        return render_template("about.html", he = img)
    else:
        return render_template("about.html")

@app.route('/wall/', methods=['GET', 'POST'])
def wall():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['comment']
        now = datetime.now()
        now2 = now + timedelta(hours=8)
        db.session.add(message(name, content, now2))
        db.session.commit()
        messages = db.session.query(message).order_by(desc(message.date)).all()
        flash(u"谢谢您的留言")
        return render_template("wall.html", messagess=messages)
    else:
        messages = db.session.query(message).order_by(desc(message.date)).all()
        flash(u"欢迎来留言")
        return render_template("wall.html", messagess=messages)



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
            return redirect("/")
        else:
            flash(u"账号密码错误")
            return redirect("/")

    else:
        flash(u"账号密码错误")
        return redirect("/")

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash(u"你已成功登出")
    return redirect(url_for('home'))

@app.route('/wall/delete/<number>', methods=['GET','DELETE'])
def delete_message(number=None):
    if request.method == "DELETE":
        delete_message = message.query.get(int(number))
        context = {
            "name": delete_message.name,
            "content": delete_message.content,
            "date": delete_message.date.strftime("%Y-%m-%d %H:%M:%S")
        }
        db.session.delete(delete_message)
        db.session.commit()
        return jsonify(**context)
        # return redirect("/wall/")
    else:
        flash(u"删除发生错误")
        return redirect("/wall/")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file((file.filename).lower()):
            filename = secure_filename(file.filename)
            file.filename = "1.png"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('uploaded_file',
                                    filename=file.filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploaded/', methods=['GET', 'POST'])
def uploaded_file():
    filename = request.args.get("filename","")
    imgpath = " /home/vcap/fs/838c48b47588a13" + filename
    return render_template("about.html", filename=filename, imgpath=imgpath)
