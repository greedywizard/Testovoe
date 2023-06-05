import logging
import sqlite3
from typing import Type

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class PipelineOptions(Base):
    __tablename__ = 'PipelineOptions'

    seed_phrase = Column(String, nullable=False, primary_key=True)
    discord_login = Column(String)
    discord_pass = Column(String)
    twitter_login = Column(String)
    twitter_pass = Column(String)
    restore_point = Column(String)
    restore_data = Column(String)
    is_complete = Column(Boolean, nullable=False)
    is_restore = Column(Boolean, nullable=False)


def CreateTable():
    logging.warning('Таблица с параметрами для аккаунтов не найдена. Пожалуйста заполните таблицу в data.db')
    conn = sqlite3.connect('data.db')

    engine = create_engine('sqlite:///data.db')
    Base.metadata.create_all(engine)

    conn.close()


def GetAll() -> list[Type[PipelineOptions]]:
    engine = create_engine('sqlite:///data.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    res = session.query(PipelineOptions).filter_by(is_complete=False).all()

    session.close()
    return res


def UpdateRecord(opt: Type[PipelineOptions]):
    engine = create_engine('sqlite:///data.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    obj = session.query(PipelineOptions).filter_by(id=opt.id).first()
    obj.is_restore = opt.is_restore
    obj.is_complete = opt.is_complete
    obj.restore_point = opt.restore_point
    obj.restore_data = opt.restore_data

    session.commit()
    session.close()
