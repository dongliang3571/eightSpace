# This Python file uses the following encoding: utf-8
from coreapp.views import db
from coreapp.models import message, admin
from datetime import datetime

db.create_all()

now = datetime.now()
db.session.add(message(u"峰峰",u"布景很用心",now))
# db.session.add(message("yangrong","have a good day",now))
db.session.add(admin("minjie","123"))

db.session.commit()
