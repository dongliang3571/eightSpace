from views import db



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
