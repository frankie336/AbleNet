#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 09:10:57 2021

@author: thanosprime
"""
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
#print(sqlalchemy.__version__ )

#engine = create_engine('sqlite:///:memory:', echo=True)#For local testing

engine = create_engine("mysql://AbleNetAdmin:$TestAdMin$336@10.100.100.101/ablenet",echo = True)


Base = declarative_base()

class ProviderEdge(Base):
    __tablename__ = 'pe_routers'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    HostName =  Column(String(50))
    IpAddress = Column(String(50))
    ModelName = Column(String(50))
    SiteName =  Column(String(50))

    def __repr__(self):
        return "<PE(HostName='%s', IpAddress='%s', ModelName='%s',SiteName='%s')>" % (
            self.HostName, self.IpAddress, self.ModelName,self.SiteName)



Base.metadata.create_all(engine)

bas01PE01 = ProviderEdge(HostName='bas01PE01', IpAddress='172.16.0.7', ModelName='IOSv',SiteName='bas01')

Session = sessionmaker(bind=engine)
session = Session()
session.add(bas01PE01)

our_user = session.query(ProviderEdge).filter_by(HostName='basPE01').first()

print(our_user,'*********')


for row in session.query(ProviderEdge, ProviderEdge.HostName).all():
    print(row.ProviderEdge, row.HostName)


session.commit()
