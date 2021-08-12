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
    PeInterface = Column(String(50))#Gi0/0.3
    ManageInterface=Column(String(50))#Gi0/0.903
    ManagementIp = Column(String(50))#172.16.0.0/16
    Vlan =  Column(String(50))#102
    Cir = Column(String(50))#50mbps
    Switch = Column(String(50))#zur01ceSW01
    SwitchInterface = Column(String(50))#Gi0/0

    #def __repr__(self):
        #return "<PE(SerViceName='%s',CustomerName='%s',CustomerAddress='%s',Status='%s', ProviderEdge='%s',AsNumber='%s',BgpPassword='%s',Rd='%s',Rt='%s',ImportVpn='%s',Routes='%s',PeInterface='s%',ManageInterface='%s',ManagementIp='%s',Vlan='%s',Cir='%s',Switch='%s',SwitchInterface='%s')>" % (
            #self.SerViceName, self.CustomerName,self.CustomerName,self.CustomerAddress,self.Status,self.ProviderEdge,self.AsNumber,self.BgpPassword,self.Rd,self.Rt,self.ImportVpn,self.Routes,self.PeInterface,self.ManageInterface,self.ManagementIp,self.Vlan,self.Vlan,self.Cir,self.Switch,self.SwitchInterface)

Session = sessionmaker(bind=engine)

def CreateL3Vpn(query,commit,SerViceName,CustomerName,
                CustomerAddress,Status,
                ProviderEdge,AsNumber,
                BgpPassword,Rd,Rt,ImportVpn,
                Routes,PeInterface,
                ManageInterface,
                ManagementIp,Vlan,
                Cir,Switch,
                SwitchInterface,

                ):

    Base.metadata.create_all(engine)#Ceates the table

    """
    Create an instance of the mapped class
    """
    vpn = L3Vpn(SerViceName=SerViceName,CustomerName=CustomerName,
                CustomerAddress=CustomerAddress,Status=Status,
                ProviderEdge=ProviderEdge,AsNumber=AsNumber,
                BgpPassword=BgpPassword,Rd=Rd,Rt=Rt,ImportVpn=ImportVpn,
                Routes=Routes,PeInterface=PeInterface,
                ManageInterface=ManageInterface,ManagementIp=ManagementIp,
                Vlan=Vlan,Cir=Cir,Switch=Switch,SwitchInterface=SwitchInterface
                )


    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(vpn)

    """
    Use this block for queries
    """
    if query ==True:
        for instance in session.query(L3Vpn).order_by(L3Vpn.id):
            print(instance.SerViceName, instance.Status)


    #our_vpn = session.query(L3Vpn).filter_by(SerViceName='vpn0001').first()
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
def L3VpnTableInteract(query,commit):

    query = query
    commit = False
    SerViceName='vpn00001'
    CustomerName='Flynn Communications'
    CustomerAddress='9543 Culver Blvd ,Culver City, Los Angeles, California 90232, United States'
    Status='Active'
    ProviderEdge='bas01PE01'
    AsNumber='65001'
    BgpPassword = PassWordGen()
    Rd = '1000'
    Rt='1000'
    ImportVpn=''
    Routes='10.100.200.0 255.255.255.0'
    PeInterface='Gi0/0.3'
    ManageInterface='Gi0/0.903'
    ManagementIp='172.16.0.5'
    Vlan='103'
    Cir='25'
    Switch='bas01ceSW01'
    SwitchInterface='Gi0/2'

    CreateL3Vpn(query,commit,SerViceName,CustomerName,
                    CustomerAddress,Status,
                    ProviderEdge,AsNumber,
                    BgpPassword,Rd,Rt,
                    ImportVpn,
                    Routes,PeInterface,
                    ManageInterface,
                    ManagementIp,Vlan,
                    Cir,Switch,
                    SwitchInterface,
                    )


L3VpnTableInteract(query=True,commit=False)




