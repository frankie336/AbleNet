#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 09:10:57 2021

@author: thanosprime
"""
import abc
import inspect

import pymysql
pymysql.install_as_MySQLdb()
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

#engine = create_engine('sqlite:///:memory:', echo=True)#For local PeManagementWanIp ing
engine = create_engine("mysql://AbleNetAdmin:$TestAdMin$336@10.1.0.3/ablenet",echo = True)

Base = declarative_base()

class L3Vpn(Base):
    __tablename__ = 'l3_vpn'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    SerViceName = Column(String(50))  # VPN0001
    CustomerName = Column(String(50))  # Fifa
    CustomerAddress = Column(String(600))  # 9543 Culver Blvd, Culver City, Los Angeles, California 90232
    Status = Column(String(50))  # Active/Inactive
    ProviderEdge = Column(String(50))  # bas01PE01
    AsNumber = Column(String(50))  # 65001:1
    BgpPassword = Column(String(50))  # dfghjlkgh
    Rd = Column(String(50))  # 65001:1
    Rt = Column(String(50))  # 65001:1
    ImportVpn = Column(String(300))  # vpn00005
    Routes = Column(String(50))  # 10.100.100.0 255.255.255.0
    CustomerNextHop = Column(String(50))  # 10.100.100.100
    PeInterface = Column(String(50))  # Gi0/0.3
    WanVlan = Column(String(50))  # 103
    ManVlan = Column(String(50))  # 903
    PeWanIPAddress = Column(String(50))  # 10.100.100.1 255.255.255.252
    CeWanIPAddress = Column(String(50))  # 10.100.100.2 255.255.255.252
    ManageInterface = Column(String(50))  # Gi0/0.903
    PeManagementWanIp = Column(String(50))  # 172.16.0.0/16
    CeManagementWanIp = Column(String(50))  # 172.16.1.10
    CeLoopback = Column(String(50))  # 172.16.0.6
    Cir = Column(String(50))  # 50mbps
    Switch = Column(String(50))  # zur01ceSW01
    SwitchInterface = Column(String(50))  # Gi0/0

    #def __repr__(self):
       #return "<User(name='%s', fullname='%s', nickname='%s')>" % (
        #                    self.name, self.fullname, self.nickname)

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





def CreateL3vpnTable():

    from sqlalchemy.inspection import inspect
    insp = inspect(L3Vpn)
    print(list(insp.columns))
    Base.metadata.create_all(engine)


def CreateDeviceTable():

    from sqlalchemy.inspection import inspect
    insp = inspect(Device)
    print(list(insp.columns))
    Base.metadata.create_all(engine)






