import abc
from abc import ABC
import paramiko
import time
import re
import datetime
import logging
#from Database.Queries import RunSqlQuery
#
"""
Created on Mon Jan 11 20:08:27 2021
#! Python 3.8
@author: Francis Neequaye
         francis.neequaye@gmail.com
"""

"""
Script Instructions 
_____
1.Enter the remote IP's addresses of 
Cisco (or other) devices on each search
of the Hosts.dat file
2. Enter input commands on each line of
the Commands.dat file 
"""

#yryyrrtytrg

class FormalAutoShellInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'set_service_dict') and
                callable(subclass.set_service_dict) and

                hasattr(subclass, 'get_service_dict') and
                callable(subclass.get_service_dict) and

                hasattr(subclass, 'cios_pe_build_mpls_three_commands') and
                callable(subclass.cios_pe_build_mpls_three_commands) and

                hasattr(subclass, 'cios_ce_switch_build_commands') and
                callable(subclass.cios_ce_switch_build_commands) and

                hasattr(subclass, 'cios_pe_decom_mpls_three_commands') and
                callable(subclass.cios_pe_decom_mpls_three_commands) and

                hasattr(subclass, 'cios_ce_decom_mpls_switch_commands') and
                callable(subclass.cios_ce_decom_mpls_switch_commands) and

                hasattr(subclass, 'pe_mpls_three_shell_session') and
                callable(subclass.pe_mpls_three_shell_session) and

                hasattr(subclass, 'ce_sw_shell_session') and
                callable(subclass.ce_sw_shell_session) and

                hasattr(subclass, 'find_ipv4_routes') and
                callable(subclass.find_ipv4_routes) and

                hasattr(subclass, 'set_remote_shell_out') and
                callable(subclass.set_remote_shell_out) and

                hasattr(subclass, 'get_remote_shell_out') and
                callable(subclass.get_remote_shell_out) and

                hasattr(subclass, 'build_mpls_three') and
                callable(subclass.build_mpls_three) or

                NotImplemented)

    @abc.abstractmethod
    def set_service_dict(self, query_string: str):
        """Service data dictionary setter"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_service_dict(self):
        """Service data dictionary getter"""
        raise NotImplementedError

    @abc.abstractmethod
    def cios_pe_build_mpls_three_commands(self):
        """Builds Cisco IOS MPLS L3VPN service on  PE"""
        raise NotImplementedError

    @abc.abstractmethod
    def cios_pe_decom_mpls_three_commands(self):
        """Removes L3vpn service from PE"""
        raise NotImplementedError

    @abc.abstractmethod
    def cios_ce_switch_build_commands(self):
        """Builds Cisco IOS Switching for mpls service"""
        raise NotImplementedError

    @abc.abstractmethod
    def cios_ce_decom_mpls_switch_commands(self):
        """Removes L3vpn switch config"""
        raise NotImplementedError

    @abc.abstractmethod
    def pe_mpls_three_shell_session(self, session_type: str):
        """Connects to the cli shell of the PE device to make changes"""
        raise NotImplementedError

    @abc.abstractmethod
    def ce_sw_shell_session(self, session_type: str):
        """Make build_mpls_three4_changes on CE switch"""
        raise NotImplementedError

    @abc.abstractmethod
    def find_ipv4_routes(self, input_string: str):
        """Search for ipv4 routes in strings"""
        raise NotImplementedError

    @abc.abstractmethod
    def set_remote_shell_out(self, val):
        """Sets the remote_shell_out class attribute"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_remote_shell_out(self):
        """gets the remote_shell_out class attribute"""
        raise NotImplementedError

    @abc.abstractmethod
    def build_mpls_three(self):
        """Implements L3vpn changes on PE router and CE switch"""
        raise NotImplementedError


class QueryService(FormalAutoShellInterface, ABC):
    def __init__(self, service_name):
        self.service_name = service_name
        self.service_dict = {}
        self.customer_name = None
        self.cir = None
        self.vrf = None
        self.rd = None
        self.rt = None
        self.pe_interface = None
        self.type1_rd = None  # A Type1 route distinguisher
        self.provider_edge = None
        self.ce_switch = None
        self.pe_ip = None
        self.pe_device_dict = {}
        self.ce_device_dict = {}
        self.ce_ip = None
        self.ipv4next_hop = None
        self.customer_routes = None
        self.ce_cust_switch_int = None
        self.extracted_routes = None
        self.wan_vlan = None
        self.man_vlan = None
        self.pe_wan_ip = None
        self.service_policy = None
        self.home_as = None
        self.remote_as = None
        self.bgpnei = None
        self.bgp_pass = None
        self.manage_int = None
        self.ce_man_ip = None
        self.pe_man_ip = None
        self.ce_manwan_ip = None
        self.wan_description = None

    def find_ipv4_routes(self, input_string: str):
        """Search for ipv4 routes in string"""
        pat = r"(\d\d?\d?\.\d\d?\d?\.\d\d?\d?\.\d\d?\d? \d\d?\d?\.\d\d?\d?\.\d\d?\d?\.\d\d?\d?)"
        ipv4_address = re.findall(pat, input_string)
        return ipv4_address

    def set_service_dict(self, query_string: str):
        """Load the vpn data set from sql query"""
        query = RunSqlQuery()
        self.service_dict = query.query_l3vpn_data(service_name=self.service_name)
        self.customer_name = self.service_dict['customer_name']
        self.cir = self.service_dict['Cir']
        self.vrf = self.service_dict['service_name']
        self.rd = self.service_dict['as_number']
        # self.rt =
        self.pe_interface = self.service_dict['pe_interface']
        self.type1_rd = self.service_dict['as_number'] + ':' + \
                        self.service_dict['route_distinguisher']

        self.provider_edge = self.service_dict['provider_edge']
        self.ce_switch = self.service_dict['ce_switch']

        self.pe_interface = self.service_dict['pe_interface']
        self.wan_description = self.service_dict['service_name']
        self.pe_wan_ip = self.service_dict['pe_wan_ip']
        self.home_as = '65000'
        self.remote_as = self.service_dict['as_number']
        self.bgpnei = self.service_dict['ce_wan_ip']
        self.bgp_pass = self.service_dict['bgp_password']
        self.manage_int = self.service_dict['management_interface']
        self.ce_man_ip = self.service_dict['ce_man_ip']
        self.pe_man_ip = self.service_dict['management_ip']
        self.ce_manwan_ip = self.service_dict['ce_manwan_ip']

        """
        Matches the management IP's of PE and CE devices
        """
        self.pe_device_dict = query.query_device(device_name=self.provider_edge)
        self.pe_ip = self.pe_device_dict['management_ip']
        self.ce_device_dict = query.query_device(device_name=self.ce_switch)
        self.ce_ip = self.ce_device_dict['management_ip']
        """
        Customer routes
        """
        self.customer_routes = self.service_dict['customer_routes']
        self.extracted_routes = self.find_ipv4_routes(input_string=self.customer_routes)
        self.ipv4next_hop = self.service_dict['customer_next_hop']
        """
        L2 CE Switching 
        """
        self.ce_cust_switch_int = self.service_dict['ce_switch_interface']
        self.wan_vlan = self.service_dict['wan_vlan']
        self.man_vlan = self.service_dict['man_vlan']

    def get_service_dict(self):
        """Service data dictionary getter"""
        return self.service_dict


class BuildService(QueryService, ABC):
    def __init__(self, service_name, user_name, password, enable_pass):
        super().__init__(service_name)

        self.__user_name = user_name
        self.__password = password
        self.__enable_pass = enable_pass

    def cios_pe_build_mpls_three_commands(self):
        """Builds Cisco IOS MPLS L3VPN service"""

        """
        Set the Service up by calling an instance of the service data setter which contains the variables needed
        """
        self.set_service_dict(query_string=self.service_name)  # 1
        print(self.get_service_dict())  # 2

        """
        CIR POLICING
        Cir policing templates are already present on the
        PE. Thus, we need to point this script to the correct
        template by matching the Cir entered on the database
        """
        if self.service_dict['Cir'] == '16':
            self.service_policy = 'police_16mbps'

        if self.service_dict['Cir'] == '59':
            self.service_policy = 'police_59mbps'

        if self.service_dict['Cir'] == '118':
            self.service_policy = 'police_118mbps'

        if self.service_dict['Cir'] == '236':
            self.service_policy = 'police_236mbps'

        if self.service_dict['Cir'] == '472':
            self.service_policy = 'police_472mbps'

        """
        CUSTOMER ROUTES
        """
        customer_routes = self.service_dict['customer_routes']  # special case for finding multiple routes

        # found_routes = self.find_ipv4(input_string=customer_routes)

        commands = ['terminal length 0',
                    'enable',
                    self.__enable_pass,
                    'show clock',
                    'configure terminal',
                    'ip vrf ' + self.service_name,
                    'rd ' + self.type1_rd,
                    'route-target export ' + self.type1_rd,
                    'route-target import ' + self.type1_rd,
                    'description ' + self.customer_name,
                    'exit',

                    'interface ' + self.pe_interface,
                    'description ' + self.wan_description,
                    'ip vrf forwarding ' + self.vrf,
                    'encapsulation dot1Q ' + self.wan_vlan,
                    'ip address ' + self.pe_wan_ip + ' 255.255.255.252',
                    'service-policy output ' + self.service_policy,
                    'exit',

                    'router bgp ' + self.home_as,
                    'address-family ipv4 vrf ' + self.vrf,
                    'redistribute static',
                    'neighbor ' + self.bgpnei + ' remote-as ' + self.remote_as,
                    'neighbor ' + self.bgpnei + ' as-override',
                    'neighbor ' + self.bgpnei + ' description ' + self.vrf,
                    'neighbor ' + self.bgpnei + ' password ' + self.bgp_pass,
                    'exit-address-family',
                    'exit',

                    'interface ' + self.manage_int,
                    'description ' + self.vrf,
                    'encapsulation dot1Q ' + self.man_vlan,
                    'ip vrf forwarding vpn00001',
                    'ip address ' + self.pe_man_ip + ' 255.255.255.252',
                    'exit',
                    'ip route vrf vpn00001 ' + self.ce_man_ip + ' 255.255.255.255 ' + self.ce_manwan_ip + ' name ' + self.vrf
                    # 'end',
                    # 'write memory'

                    ]

        return commands

    def cios_ce_switch_build_commands(self):
        """Builds Cisco IOS Switching for mpls service"""

        commands = ['terminal length 0',
                    'enable',
                    self.__enable_pass,
                    'configure terminal',
                    'vlan ' + self.wan_vlan,
                    'name ' + self.vrf,
                    'exit',
                    'interface ' + self.ce_cust_switch_int,
                    'description ' + self.vrf,
                    'switchport trunk encapsulation dot1q',
                    'switchport trunk allowed vlan ' + self.wan_vlan,
                    'switchport trunk allowed vlan add ' + self.man_vlan,
                    'no shutdown',
                    'end',
                    'write memory'

                    ]

        return commands

    def cios_pe_decom_mpls_three_commands(self):
        """Removes L3vpn service from PE"""

        commands = ['terminal length 0',
                    'enable',
                    self.__enable_pass,
                    'show clock',
                    'configure terminal',
                    'no ip vrf ' + self.vrf,
                    'no interface ' + self.pe_interface,

                    'end', 'write memory']

        return commands

    def cios_ce_decom_mpls_switch_commands(self):
        """Removes L3vpn switch config"""

        commands = ['enable',
                    self.__enable_pass,
                    'configure terminal',
                    'interface ' + self.ce_cust_switch_int,
                    'no switchport access vlan ' + self.wan_vlan,
                    'no vlan ' + self.wan_vlan
                    # 'default interface ' + self.ce_cust_switch_int
                    ]
        return commands


class Channel(BuildService):
    def __init__(self, service_name, user_name, password, enable_pass):
        super().__init__(service_name, user_name, password, enable_pass)

        self.date_time = datetime.datetime.now().strftime("%Y-%m-%d")
        self.__user_name = user_name
        self.__password = password
        self.__enable_pass = enable_pass
        self.__remote_shell_out = None

    def set_remote_shell_out(self, val):
        """Sets the remote_shell_out class attribute"""
        self.__remote_shell_out = val

    def get_remote_shell_out(self):

        return self.__remote_shell_out

    def pe_mpls_three_shell_session(self, session_type: str):
        """Connects to the cli shell of the PE device to make changes"""

        self.set_remote_shell_out('')

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.pe_ip, port=22, username=self.__user_name, password=self.__password, look_for_keys=False,
                        timeout=None)
            channel = ssh.get_transport().open_session()
            channel.invoke_shell()
        except Exception as e:
            print(self.pe_ip, e.args)
            return

        """
        -If the session_type Arg is set to 'provision set the command set to l3vpn4 build'
        """
        if session_type == 'provision':
            command_set = self.cios_pe_build_mpls_three_commands()

        if session_type == 'decommission':
            command_set = self.cios_pe_decom_mpls_three_commands()

        """
        Execute the commands from the command set list
        """
        for x in command_set:
            time.sleep(.1)
            channel.sendall(x + '\n')
        """
        Special case for finding and entering multiple customer routes from the database
        """
        for x in self.extracted_routes:
            time.sleep(.1)
            channel.sendall('ip route vrf ' + self.vrf + ' ' + x + ' ' + self.ipv4next_hop + "\n")
            channel.sendall(b'end \n')
            channel.sendall(b'write memory \n')

        shell_output = channel.recv(9999).decode(encoding='utf-8')  # Receive buffer output
        time.sleep(1)
        self.set_remote_shell_out(shell_output)
        ssh.close()

        # print(shell_output)

    def ce_sw_shell_session(self, session_type):
        """Make build_mpls_three4_changes on CE switch"""

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ce_ip, port=22, username=self.__user_name, password=self.__password, look_for_keys=False,
                        timeout=None)
            channel = ssh.get_transport().open_session()
            channel.invoke_shell()
        except Exception as e:
            print(self.pe_ip, e.args)
            return

        """
        -If the session_type Arg is set to 'provision set the command set to l3vpn4 build'
        """
        if session_type == 'provision':
            command_set = self.cios_ce_switch_build_commands()
        if session_type == 'decommission':
            command_set = self.cios_ce_decom_mpls_switch_commands()

        for x in command_set:
            time.sleep(.2)
            channel.sendall(x + "\n")

        time.sleep(.2)
        shell_output = channel.recv(9999).decode(encoding='utf-8')  # Receive buffer output
        ssh.close()
        print(shell_output)

    def build_mpls_three(self):
        """Implements L3vpn changes on PE router and CE switch"""

        self.set_service_dict(self.service_name)  # Sets the correct didctionary context per service name

        self.pe_mpls_three_shell_session(session_type='provision')  # Implements changes on PE device
        self.ce_sw_shell_session(session_type='provision')  # 2Implements changes on CE switch

    def decom_mpls_three(self):
        """decomission L3vpn """
        self.set_service_dict(self.service_name)

        self.pe_mpls_three_shell_session(session_type='decommission')
        self.ce_sw_shell_session(session_type='decommission')
