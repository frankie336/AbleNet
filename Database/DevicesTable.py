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



#engine = create_engine('sqlite:///:memory:', echo=True)#For local testing
engine = create_engine("mysql://AbleNetAdmin:$TestAdMin$336@10.1.0.3/ablenet",echo = True)

Base = declarative_base()

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    HostName =  Column(String(50))
    ManagementIpAddress = Column(String(50))
    ModelName = Column(String(50))
    SiteName =  Column(String(50))

    def __repr__(self):
        return "<PE(HostName='%s', ManagementIpAddress='%s', ModelName='%s',SiteName='%s')>" % (
            self.HostName, self.ManagementIpAddress, self.ModelName,self.SiteName)


Session = sessionmaker(bind=engine)
def CreateDevice(commit,HostName,ManagementIpAddress,ServiceType,
             ModelName,SiteName):
    
    Base.metadata.create_all(engine)  # Ceates the table schema

    """
    Create an instance of the mapped class
    """
    new_device = Device(HostName=HostName,ManagementIpAddress=ManagementIpAddress,ModelName=ModelName, SiteName=SiteName)

    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(new_device)

    """
    use this block to commit new services
    """
    if commit == True:
        session.commit()


def DeviceTableInteract(commit):
    commit = commit
    HostName='bas01ceSW01'
    ManagementIpAddress ='172.16.0.9'
    ServiceType = 'CEsw'
    ModelName = 'IOSv-L2'
    SiteName = 'bas01'

    CreateDevice(commit, HostName,
                 ManagementIpAddress,
                 ServiceType,
                 ModelName, SiteName)





