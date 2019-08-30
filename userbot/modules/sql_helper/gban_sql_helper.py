try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError
from sqlalchemy import Column, Integer, distinct, func


class GBan(BASE):
    __tablename__ = "gban"
    chat_id = Column(Integer(), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = int(chat_id)  # ensure int


GBan.__table__.create(checkfirst=True)


def get_gban():
    try:
        return SESSION.query(GBan)
    finally:
        SESSION.close()


def is_gban(chat_id):
    try:
        return SESSION.query(GBan).filter(GBan.chat_id == int(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_chat_gban(chat_id):
    adder = GBan(int(chat_id))
    SESSION.add(adder)
    SESSION.commit()


def remove_chat_gban(chat_id):
    rem = SESSION.query(GBan).get(int(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
