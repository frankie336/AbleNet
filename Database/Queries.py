from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pymysql
from sqlalchemy import select
pymysql.install_as_MySQLdb()
import abc



Base = automap_base()
engine = create_engine("mysql://AbleNetAdmin:$TestAdMin$336@10.1.0.3/ablenet",echo = True)
Base.prepare(engine, reflect=True)



class FormalQueryServiceInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'query_l3vpn_data') and
                callable(subclass.load_vpn_data) and
                hasattr(subclass, 'query_device') and
                callable(subclass.query_device) or

                NotImplemented)



    @abc.abstractmethod
    def query_l3vpn_data(self, service_name: str):
        """Query L3vpn data"""
        raise NotImplementedError

    @abc.abstractmethod
    def query_device(self, device_name: str):
        """Query physical device"""
        raise NotImplementedError







class RunSqlQuery(FormalQueryServiceInterface):
    def __init__(self):

        self.session = Session(engine)



    def query_l3vpn_data(self, service_name: str):
        """Query L3vpn data"""

        vpn = Base.classes.l3_vpn
        stmt = select(vpn).where(vpn.SerViceName == service_name)
        result = self.session.execute(stmt)

        for vpn_obj in result.scalars():
            service_provision_dict = {'service_name': vpn_obj.SerViceName, 'customer_name': vpn_obj.CustomerName,
                                     'Status': vpn_obj.Status, 'provider_edge': vpn_obj.ProviderEdge,
                                     'pe_interface': vpn_obj.PeInterface,'wan_vlan':vpn_obj.WanVlan,
                                      'man_vlan':vpn_obj.ManVlan,'pe_wan_ip': vpn_obj.PeWanIPAddress,
                                      'ce_wan_ip': vpn_obj.CeWanIPAddress,'management_interface': vpn_obj.ManageInterface,
                                     'management_ip': vpn_obj.ManagementIp, 'as_number': vpn_obj.AsNumber,
                                     'bgp_password': vpn_obj.BgpPassword, 'route_distinguisher': vpn_obj.Rd,
                                     'route_target': vpn_obj.Rt, 'import_vpn': vpn_obj.ImportVpn,
                                     'customer_routes': vpn_obj.Routes, 'customer_next_hop': vpn_obj.CustomerNextHop,
                                     'ce_switch': vpn_obj.Switch, 'ce_switch_interface': vpn_obj.SwitchInterface,
                                     'Cir': vpn_obj.Cir

                                     }

            return service_provision_dict


    def query_device(self, device_name: str):
        """Query physical device"""

        device = Base.classes.devices
        stmt = select(device).where(device.HostName == device_name)
        result = self.session.execute(stmt)

        for device_obj in result.scalars():
            device_dict = {'host_name': device_obj.HostName, 'management_ip': device_obj.ManagementIpAddress,
                           'model_name': device_obj.ModelName, 'site_name': device_obj.SiteName
                           }

            return device_dict





