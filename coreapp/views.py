# This Python file uses the following encoding: utf-8
from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
from sqlalchemy import desc
import json
from werkzeug import secure_filename
import os
import jinja2


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/vcap/fs/838c48b47588a13/production.db'  #for production
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///production.db' # for local only
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

from models import db

db.init_app(app)
db.create_all(app=app)

from models import message, admin, theme
from db_create import init_db

with app.app_context():
    init_db(db)

folder = "static/uploaded"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# UPLOAD_FOLDER = os.path.join(BASE_DIR, folder)
UPLOAD_FOLDER =  "/home/vcap/fs/838c48b47588a13"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def home():
    session["previous_path"] = request.path
    return render_template("home.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error404.html")

@app.route('/themes/')
@app.route('/themes/<number>')
def themes(number=None):
    session["previous_path"] = request.path
    if number:
        newfile_name = "/themepages/theme" + number + ".html"
    else:
        newfile_name = "/themepages/theme.html"

    themes_db = theme.query.order_by(desc(theme.date)).all()
    try:
        return render_template(newfile_name, themes = themes_db)
    except jinja2.exceptions.TemplateNotFound:
        return redirect("themes/")

@app.route('/themes/add_theme/', methods=['GET', 'POST'])
def add_theme():
    if request.method == "POST":
        now = datetime.now()
        image_link = request.form['image_link']
        title = request.form['title']
        is_new_tmp = request.form['is_new']
        is_new = bool(int(is_new_tmp))
        description = request.form['description']
        short_intro = request.form['short_intro']
        time_limit = request.form['time_limit']
        number_people = request.form['number_people']
        easiness = request.form['easiness']
        number_room = request.form['number_room']

        if not (image_link or title or description or short_intro or number_people or number_room):
            flash(u"添加主题失败，必填项目没填")
            return redirect(url_for("themes"))
        else:
            db.session.add(
                theme(
                    image_link,
                    title,
                    is_new,
                    description,
                    short_intro,
                    time_limit,
                    number_people,
                    easiness,
                    number_room,
                    now
                )
            )
            db.session.commit()

            flash(u"添加主题成功")
            return redirect(url_for("themes"))
    else:
        flash(u"添加主题失败")
        return redirect(url_for("themes"))


@app.route('/themes/delete_theme/<number>', methods=['GET', 'DELETE'])
def delete_theme(number=None):
    if request.method == "DELETE":
        delete_theme = theme.query.get(int(number))
        context = {
            "title": delete_theme.title,
        }
        db.session.delete(delete_theme)
        db.session.commit()
        return jsonify(**context)
    else:
        flash(u"删除失败")
        return redirect("/themes/")


@app.route('/stores/<number>')
def stores(number):
    newfile_name = "/storepages/store" + number + ".html"
    return render_template(newfile_name)

@app.route('/aboutus/', methods=['GET', 'POST'])
def about():
    session["previous_path"] = request.path
    if request.method == "POST":
        img = request.form['image']
        print img
        return render_template("about.html", he = img)
    else:
        return render_template("about.html")

@app.route('/wall/', methods=['GET', 'POST'])
def wall():
    session["previous_path"] = request.path
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
            return redirect(session["previous_path"])
        else:
            flash(u"账号密码错误")
            return redirect(session["previous_path"])

    else:
        flash(u"账号密码错误")
        return redirect(session["previous_path"])

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash(u"你已成功登出")
    return redirect(session["previous_path"])

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
    imgpath = "/home/vcap/fs/838c48b47588a13" + filename
    return render_template("about.html", filename=filename, imgpath=imgpath)



app.debug = True
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5010)
