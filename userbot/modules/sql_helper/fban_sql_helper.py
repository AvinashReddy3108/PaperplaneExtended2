try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError
from sqlalchemy import Column, Integer, distinct, func


class FBan(BASE):
    __tablename__ = "fban"
    chat_id = Column(Integer(), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = int(chat_id)  # ensure int


FBan.__table__.create(checkfirst=True)


def get_fban():
    try:
        return SESSION.query(FBan)
    finally:
        SESSION.close()


def is_fban(chat_id):
    try:
        return SESSION.query(FBan).filter(FBan.chat_id == int(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_chat_fban(chat_id):
    adder = FBan(int(chat_id))
    SESSION.add(adder)
    SESSION.commit()


def remove_chat_fban(chat_id):
    rem = SESSION.query(FBan).get(int(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
