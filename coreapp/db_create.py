# This Python file uses the following encoding: utf-8
from models import message, admin, theme
from datetime import datetime


def init_db(db):


    now = datetime.now()
    db.session.add(message(u"峰峰",u"布景很用心",now))
    # db.session.add(message("yangrong","have a good day",now))
    db.session.add(admin("minjie","123"))
    db.session.add(
        theme(
            "https://coding.net/api/project/229171/files/515369/imagePreview?width=1440&type=2&1451688312000",
            u"变形金刚",
            True,
            u"非常好玩,非常好玩,非常好玩,非常好玩",
            u"非常好玩",
            u"2小时",
            "4-6",
            4,
            "3-5",
            now
        )
    )

    db.session.add(
        theme(
            "https://coding.net/api/project/229171/files/515370/imagePreview?width=1440&type=2&1451688314000",
            u"魔幻城堡",
            False,
            u"非常好玩,非常好玩,非常好玩,非常好玩",
            u"非常好玩",
            u"2小时",
            "4-6",
            3,
            "3-5",
            now
        )
    )

    db.session.commit()
