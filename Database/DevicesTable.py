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
def CreateDevice(query,query_string,commit,HostName,ManagementIpAddress,ServiceType,
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
    Use this block for queries
    """
    if query == True:

        from sqlalchemy import select

        stmt = select(Device).where(Device.HostName == query_string)
        result = session.execute(stmt)

        for device_obj in result.scalars():

            device_dict = {'host_name':device_obj.HostName,'management_ip':device_obj.ManagementIpAddress,
                           'model_name':device_obj.ModelName,'site_name':device_obj.SiteName
                           }

            return device_dict
    else:
        pass

    """
    use this block to commit new services
    """
    if commit == True:
        session.commit()


def DeviceTableInteract(query,commit,query_string=None):

    query = query
    query_string = query_string
    commit = commit
    HostName='bas01PE01'
    ManagementIpAddress ='172.16.0.7'
    ServiceType = 'PE'
    ModelName = 'IOSv-L3'
    SiteName = 'bas01'

    device_dict=CreateDevice(query,query_string,commit,HostName,
                 ManagementIpAddress,
                 ServiceType,ModelName,SiteName)


    return device_dict



