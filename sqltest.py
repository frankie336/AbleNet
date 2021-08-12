#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 09:10:57 2021

@author: thanosprime
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()

print(sqlalchemy.__version__)

"""
engine = create_engine("mysql://AbleNetAdmin:$TestAdMin$336@10.100.100.101/",echo = True).connect()
"""
engine = create_engine('sqlite:///:memory:', echo=True)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


Base.metadata.create_all(engine)


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)


ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')

print(ed_user.fullname)
str(ed_user.id)


Session = sessionmaker(bind=engine)



ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')

