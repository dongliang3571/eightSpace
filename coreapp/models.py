from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class message(db.Model):
    __tablename__ = "usermessage"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    content = db.Column(db.String(120))
    date = db.Column(db.DateTime)

    def __init__(self, name, content, date):
        self.name = name
        self.content = content
        self.date = date

    def __repr__(self):
        return '<Posted on: %r User:%r Message:%r>' % (self.date, self.name, self.content)

class admin(db.Model):
    __tablename__ = "administrator"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<username: %r password:%r>' % (self.username, self.password)

class theme(db.Model):
    __tablename__="themes"
    id = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(40), nullable=False)
    is_new = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(500), nullable=False)
    short_intro = db.Column(db.String(400), nullable=False)
    time_limit = db.Column(db.String(40), nullable=True)
    number_people = db.Column(db.String(400), nullable=False)
    easiness = db.Column(db.Integer)
    number_room = db.Column(db.String(400), nullable=False)
    date = db.Column(db.DateTime)

    def __init__(self, image_link, title, is_new, description, short_intro, time_limit, number_people, easiness, number_room, date):
        self.image_link = image_link
        self.title = title
        self.is_new = is_new
        self.description = description
        self.short_intro = short_intro
        self.time_limit = time_limit
        self.number_people = number_people
        self.easiness = easiness
        self.number_room = number_room
        self.date = date

    def __repr__(self):
        return '<title: %r date: %r>' % (self.title, self.date)
