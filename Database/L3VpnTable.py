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
"""
custom local modules
"""
###
from GeneratePassword import PassWordGen

#engine = create_engine('sqlite:///:memory:', echo=True)#For local ManagementIping
engine = create_engine("mysql://AbleNetAdmin:$TestAdMin$336@10.1.0.3/ablenet",echo = True)


Base = declarative_base()

class L3Vpn(Base):
    __tablename__ = 'l3_vpn'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    SerViceName =  Column(String(50))#VPN0001
    CustomerName = Column(String(50))#Fifa
    CustomerAddress = Column(String(600))#9543 Culver Blvd, Culver City, Los Angeles, California 90232
    Status = Column(String(50))# Active/Inactive
    ProviderEdge = Column(String(50))#bas01PE01
    AsNumber = Column(String(50))#65001:1
    BgpPassword = Column(String(50))#dfghjlkgh
    Rd = Column(String(50))#65001:1
    Rt = Column(String(50))#65001:1
    ImportVpn = Column(String(300))#vpn00005
    Routes = Column(String(50))  #10.100.100.0 255.255.255.0
    CustomerNextHop = Column(String(50))  #10.100.100.100
    PeInterface = Column(String(50))#Gi0/0.3
    PeWanIPAddress = Column(String(50))  # 10.100.100.1 255.255.255.252
    CeWanIPAddress = Column(String(50))  # 10.100.100.2 255.255.255.252
    ManageInterface=Column(String(50))#Gi0/0.903
    ManagementIp = Column(String(50))#172.16.0.0/16
    Vlan =  Column(String(50))#102
    Cir = Column(String(50))#50mbps
    Switch = Column(String(50))#zur01ceSW01
    SwitchInterface = Column(String(50))#Gi0/0

    #def __repr__(self):
        #return "<PE(SerViceName='%s',CustomerName='%s',CustomerAddress='%s',Status='%s', ProviderEdge='%s',AsNumber='%s',BgpPassword='%s',Rd='%s',Rt='%s',ImportVpn='%s',Routes='%s',PeInterface='s%',ManageInterface='%s',ManagementIp='%s',Vlan='%s',Cir='%s',Switch='%s',SwitchInterface='%s')>" % (
            #self.SerViceName, self.CustomerName,self.CustomerName,self.CustomerAddress,self.Status,self.ProviderEdge,self.AsNumber,self.BgpPassword,self.Rd,self.Rt,self.ImportVpn,self.Routes,self.PeInterface,self.ManageInterface,self.ManagementIp,self.Vlan,self.Vlan,self.Cir,self.Switch,self.SwitchInterface)



def CreateL3Vpn(query,query_string,commit,SerViceName,CustomerName,
                CustomerAddress,Status,
                ProviderEdge,AsNumber,
                BgpPassword,Rd,Rt,ImportVpn,
                Routes,CustomerNextHop,
                PeInterface,PeWanIPAddress,
                CeWanIPAddress,
                ManageInterface,ManagementIp,
                Vlan,Cir,Switch,
                SwitchInterface,
                ):

    Base.metadata.create_all(engine)#Ceates the table schema

    """
    Create an instance of the mapped class
    """
    vpn = L3Vpn(SerViceName=SerViceName,CustomerName=CustomerName,
                CustomerAddress=CustomerAddress,Status=Status,
                ProviderEdge=ProviderEdge,AsNumber=AsNumber,
                BgpPassword=BgpPassword,Rd=Rd,Rt=Rt,ImportVpn=ImportVpn,
                Routes=Routes,CustomerNextHop=CustomerNextHop,PeInterface=PeInterface,
                PeWanIPAddress=PeWanIPAddress,CeWanIPAddress=CeWanIPAddress,
                ManageInterface=ManageInterface,
                ManagementIp=ManagementIp,Vlan=Vlan,Cir=Cir,
                Switch=Switch,SwitchInterface=SwitchInterface
                )


    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(vpn)

    """
    use this block to commit new services
    """
    if commit ==True:
        session.commit()








"""
Temp solution.
In the full scale version user input
will come in from a web form
"""
def L3VpnTableInteract(query,commit,query_string=None):

    query = query
    query_string = query_string
    commit = commit
    SerViceName='vpn00005'
    CustomerName='Encom'
    CustomerAddress='9543 Culver Blvd ,Culver City, Los Angeles, California 90232, United States'
    Status='Pending'
    ProviderEdge='zur01PE01'
    AsNumber='65001'
    BgpPassword = PassWordGen()
    Rd = '1001'
    Rt='1001'
    ImportVpn='vpn00006'
    Routes='10.10.10.0 255.255.255.0'
    CustomerNextHop ='10.10.10.254'
    PeInterface='Gi0/0.3'
    PeWanIPAddress = '10.0.1.9'
    CeWanIPAddress = '10.0.1.10'
    ManageInterface='Gi0/0.903'
    ManagementIp='172.16.0.6'
    Vlan='103'
    Cir='25'
    Switch='zur01ceSW01'
    SwitchInterface='Gi0/3'


    srvice_provision_dict=CreateL3Vpn(query,query_string,commit,SerViceName,CustomerName,
                    CustomerAddress,Status,
                    ProviderEdge,AsNumber,
                    BgpPassword,Rd,Rt,
                    ImportVpn,Routes,
                    CustomerNextHop,
                    PeInterface,
                    PeWanIPAddress,
                    CeWanIPAddress,
                    ManageInterface,
                    ManagementIp,Vlan,
                    Cir,Switch,SwitchInterface,

                    )


    return srvice_provision_dict









