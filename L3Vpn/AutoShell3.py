import abc
from abc import ABC

import paramiko
import time
import re
import datetime
import logging
from Database.Queries import RunSqlQuery

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


class FormalAutoShellInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'set_service_dict') and
                callable(subclass.set_service_dict) and
                hasattr(subclass, 'get_service_dict') and
                callable(subclass.get_service_dict) and
                hasattr(subclass, 'cios_pe_build_layer_three_mpls_commands') and
                callable(subclass.cios_pe_build_layer_three_mpls_commands) and
                hasattr(subclass, 'cios_ce_switch_build_commands') and
                callable(subclass.cios_ce_switch_build_commands) and
                hasattr(subclass, 'cios_pe_decom_layer_three_mpls_commands') and
                callable(subclass.cios_pe_decom_layer_three_mpls_commands) and

                hasattr(subclass, 'cios_ce_decom_switch_commands') and
                callable(subclass.cios_pe_decom_layer_three_mpls_commands) and


                hasattr(subclass, 'l3vpn_pe_shell_session') and
                callable(subclass.l3vpn_pe_shell_session) and
                hasattr(subclass, 'layer2_ce_shell_session') and
                callable(subclass.layer2_ce_shell_session) and
                hasattr(subclass, 'l3vpn_pe_decom_shell_session') and
                callable(subclass.layer2_ce_decom_shell_session) and
                hasattr(subclass, 'find_ipv4_routes') and
                callable(subclass.find_ipv4_routes) and
                hasattr(subclass, 'set_remote_sell_out') and
                callable(subclass.set_remote_sell_out) and
                hasattr(subclass, 'get_remote_sell_out') and
                callable(subclass.get_remote_sell_out) and
                hasattr(subclass, 'build_layer_three_mpls') and
                callable(subclass.build_layer_three_mpls) or
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
    def cios_pe_build_layer_three_mpls_commands(self):
        """Builds Cisco IOS MPLS L3VPN service on  PE"""
        raise NotImplementedError

    @abc.abstractmethod
    def cios_pe_decom_layer_three_mpls_commands(self):
        """Removes L3vpn service from PE"""
        raise NotImplementedError


    @abc.abstractmethod
    def cios_ce_switch_build_commands(self):
        """Builds Cisco IOS Switching for mpls service"""
        raise NotImplementedError

    @abc.abstractmethod
    def cios_ce_decom_switch_commands(self):
        """Removes L3vpn switch config"""
        raise NotImplementedError

    @abc.abstractmethod
    def l3vpn_pe_shell_session(self):
        """Connects to the cli shell of the PE device to make changes"""
        raise NotImplementedError

    @abc.abstractmethod
    def l3vpn_pe_decom_shell_session(self):
        """Connects to the cli of PE to decomission l3vpn service"""
        raise NotImplementedError

    @abc.abstractmethod
    def layer2_ce_shell_session(self):
        """Make build_layer_three_mpls4_changes on CE switch"""
        raise NotImplementedError

    @abc.abstractmethod
    def find_ipv4_routes(self, input_string: str):
        """Search for ipv4 routes in strings"""
        raise NotImplementedError

    @abc.abstractmethod
    def set_remote_sell_out(self, val):
        """Sets the remote_shell_out class attribute"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_remote_sell_out(self):
        """gets the remote_shell_out class attribute"""
        raise NotImplementedError

    @abc.abstractmethod
    def build_layer_three_mpls(self):
        """Implements L3vpn changes on PE router and CE switch"""
        raise NotImplementedError


class QueryService(FormalAutoShellInterface, ABC):

    def __init__(self, service_name):
        self.service_name = service_name
        self.service_dict = {}
        self.custmer_name = None
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
        self.cust_int = None
        self.extracted_routes = None
        self.wan_vlan = None
        self.man_vlan = None

    def find_ipv4_routes(self, input_string: str):
        """Search for ipv4 routes in string"""
        pat = r"(\d\d?\d?\.\d\d?\d?\.\d\d?\d?\.\d\d?\d? \d\d?\d?\.\d\d?\d?\.\d\d?\d?\.\d\d?\d?)"
        ipv4_address = re.findall(pat, input_string)
        return ipv4_address

    def set_service_dict(self, query_string: str):
        """Load the vpn data set from sql query"""
        query = RunSqlQuery()
        self.service_dict = query.query_l3vpn_data(service_name=self.service_name)
        self.custmer_name = self.service_dict['customer_name']
        self.cir = self.service_dict['Cir']
        self.vrf = self.service_dict['service_name']
        self.rd = self.service_dict['as_number']
        # self.rt =
        self.pe_interface = self.service_dict['pe_interface']
        self.type1_rd = self.service_dict['as_number'] + ':' + \
                        self.service_dict['route_distinguisher']

        self.provider_edge = self.service_dict['provider_edge']
        self.ce_switch = self.service_dict['ce_switch']

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
        self.cust_int = self.service_dict['ce_switch_interface']
        self.wan_vlan = self.service_dict['wan_vlan']
        self.man_vlan = self.service_dict['man_vlan']

    def get_service_dict(self):
        """Service data dictionary getter"""
        return self.service_dict


class BuildService(QueryService, ABC):
    def __init__(self, service_name):
        super().__init__(service_name)

        pass

    def cios_pe_build_layer_three_mpls_commands(self):
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
            service_policy = 'police_16mbps'

        if self.service_dict['Cir'] == '59':
            service_policy = 'police_59mbps'

        if self.service_dict['Cir'] == '118':
            service_policy = 'police_118mbps'

        if self.service_dict['Cir'] == '236':
            service_policy = 'police_236mbps'

        if self.service_dict['Cir'] == '472':
            service_policy = 'police_472mbps'

        wan_policer = 'service-policy output ' + service_policy

        """
        MAKE CISCO VRF
        """
        vrf = 'ip vrf ' + self.service_name
        route_disting = 'rd ' + self.type1_rd
        route_ex = 'route-target export ' + self.type1_rd
        route_imp = 'route-target import ' + self.type1_rd
        des_vrf = 'description ' + self.custmer_name

        """
        MAKE CISCO WAN INTERFACE   
        """
        wan_int = 'interface ' + self.service_dict['pe_interface']
        des_wan_int = 'description ' + self.service_dict['service_name']
        assg_vrf = 'ip vrf forwarding ' + self.service_dict['service_name']
        encap = 'encapsulation dot1Q ' + self.service_dict['wan_vlan']
        wan_ip_addr = 'ip address ' + self.service_dict['pe_wan_ip'] + ' 255.255.255.252'

        """
        MANAGEMENT INTERFACE
        """
        man_int = 'interface ' + self.service_dict['management_interface']
        l3dotq = 'encapsulation dot1Q ' + self.service_dict['man_vlan']
        man_ip_addr = 'ip address ' + self.service_dict['management_ip'] + ' 255.255.255.252'
        man_int_vrf = 'ip vrf forwarding vpn00001'

        """
        BGP
        """
        v4neighbor = self.service_dict['ce_wan_ip']  # One time neighbour definition
        rtrbgp = 'router bgp 65000'
        vpn4 = 'address-family ipv4 vrf ' + self.service_dict['service_name']
        redistcon = 'redistribute connected'
        rediststat = 'redistribute static'
        v4neigh = 'neighbor ' + v4neighbor + ' remote-as ' + self.service_dict['as_number']
        desv4eigh = 'neighbor ' + v4neighbor + ' description ' + self.service_dict['service_name']
        v4pass = 'neighbor ' + v4neighbor + ' password ' + self.service_dict['bgp_password']
        as_verride = 'neighbor ' + v4neighbor + ' as-override'
        exitvpn4 = 'exit-address-family'

        """
        MANAGEMENT ROUTING 
        """
        man_route = 'ip route vrf vpn00001 ' + self.service_dict['ce_man_ip'] + ' 255.255.255.255 ' \
                    + self.service_dict['ce_manwan_ip'] + ' name ' + self.service_dict['service_name']
        """
        CUSTOMER ROUTES
        """
        customer_routes = self.service_dict['customer_routes']  # special case for finding multiple routes

        # found_routes = self.find_ipv4(input_string=customer_routes)

        commands = ['configure terminal', vrf, route_disting, route_ex, route_imp, des_vrf, 'exit',

                    wan_int, des_wan_int, assg_vrf, encap, wan_ip_addr, wan_policer, 'exit',
                    rtrbgp, vpn4, redistcon, rediststat, v4neigh, as_verride,
                    desv4eigh, v4pass, exitvpn4, 'exit',

                    man_int, des_wan_int,
                    l3dotq, man_int_vrf, man_ip_addr, 'exit',
                    man_route

                    ]

        return commands

    def cios_ce_switch_build_commands(self):
        """Builds Cisco IOS Switching for mpls service"""

        select_l2_int = 'interface ' + self.cust_int
        des_l2_int = 'description ' + self.vrf
        trunk = 'switchport trunk encapsulation dot1q'
        ce_vlan = 'switchport trunk allowed vlan ' + self.wan_vlan
        man_vlan = 'switchport trunk allowed vlan add ' + self.man_vlan

        commands = ['configure terminal', select_l2_int, des_l2_int, trunk,
                    ce_vlan, man_vlan
                    ]

        return commands

    def cios_pe_decom_layer_three_mpls_commands(self):
        """Removes L3vpn service from PE"""
        rem_vrf = 'no ip vrf ' + self.service_name
        rem_pe_int = 'no interface ' + self.pe_interface

        commands = ['configure terminal', rem_vrf, rem_pe_int,

                    'end', 'write memory']

        return commands

    def cios_ce_decom_switch_commands(self):
        """Removes L3vpn switch config"""
        select_l2_int = 'interface ' + self.cust_int
        rem_vlan = 'no switchport access vlan '+self.wan_vlan
        default_interface = 'default interface '+self.cust_int

        commands = ['configure terminal', select_l2_int,rem_vlan,
                    default_interface

                    ]
        return commands





class Channel(BuildService):
    def __init__(self, servie_name, user_name, password, enable_pass):
        super().__init__(servie_name)

        self.date_time = datetime.datetime.now().strftime("%Y-%m-%d")
        self.__user_name = user_name
        self.__password = password
        self.__enable_pass = enable_pass
        self.__remote_shell_out = None

    def set_remote_sell_out(self, val):
        """Sets the remote_shell_out class attribute"""
        self.__remote_shell_out = val

    def get_remote_sell_out(self):

        return self.__remote_shell_out

    def l3vpn_pe_shell_session(self):
        """Connects to the cli shell of the PE device to make changes"""

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

        channel.sendall(b'terminal length 0 \n')
        time.sleep(.1)
        channel.sendall(b'enable\n')
        channel.sendall(self.__enable_pass + '\n')

        command_set = self.cios_pe_build_layer_three_mpls_commands()
        """
        Execute the commands from the command set list
        """
        for x in command_set:
            time.sleep(.1)
            channel.sendall(x + "\n")

        """
        Special case for finding and entering customer routes from the database
        """
        for x in self.extracted_routes:
            time.sleep(.1)
            channel.sendall('ip route vrf ' + self.vrf + ' ' + x + ' ' + self.ipv4next_hop + "\n")

        time.sleep(.2)
        shell_output = channel.recv(9999).decode(encoding='utf-8')  # Receive buffer output

        ssh.close()
        self.set_remote_sell_out(shell_output)
        print(shell_output)

    def l3vpn_pe_decom_shell_session(self):
        """Connects to the cli of PE to decomission l3vpn service"""
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

        channel.sendall(b'terminal length 0 \n')
        time.sleep(.1)
        channel.sendall(b'enable\n')
        channel.sendall(self.__enable_pass + '\n')

        command_set = self.cios_pe_decom_layer_three_mpls_commands()

        """
        Execute the commands from the command set list
        """
        for x in command_set:
            time.sleep(.1)
            channel.sendall(x + "\n")

        time.sleep(.2)
        shell_output = channel.recv(9999).decode(encoding='utf-8')  # Receive buffer output
        ssh.close()
        self.set_remote_sell_out(shell_output)
        print(shell_output)

    def layer2_ce_shell_session(self):
        """Make build_layer_three_mpls4_changes on CE switch"""

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

        channel.sendall(b'terminal length 0 \n')

        channel.sendall(b'enable\n')
        time.sleep(.2)
        channel.sendall(self.__enable_pass + '\n')  # Need a dynamic solution  for password here
        time.sleep(.2)

        command_set = self.cios_ce_switch_build_commands()

        for x in command_set:
            time.sleep(.2)
            channel.sendall(x + "\n")

        channel.sendall(b'end \n')
        channel.sendall(b'write memory\n')

        time.sleep(.2)
        shell_output = channel.recv(9999).decode(encoding='utf-8')  # Receive buffer output
        ssh.close()
        print(shell_output)

    def build_layer_three_mpls(self):
        """Implements L3vpn changes on PE router and CE switch"""

        self.set_service_dict(self.service_name)  # 1
        #self.l3vpn_pe_shell_session()
        self.layer2_ce_shell_session()



    def layer2_ce_decom_shell_session(self):
        """Make build_layer_three_mpls4_changes on CE switch"""

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

        channel.sendall(b'terminal length 0 \n')

        channel.sendall(b'enable\n')
        time.sleep(.2)
        channel.sendall(self.__enable_pass + '\n')  # Need a dynamic solution  for password here
        time.sleep(.2)

        command_set =  self.cios_ce_decom_switch_commands()

        for x in command_set:
            time.sleep(.2)
            channel.sendall(x + "\n")

        channel.sendall(b'end \n')
        channel.sendall(b'write memory\n')

        time.sleep(.2)
        shell_output = channel.recv(9999).decode(encoding='utf-8')  # Receive buffer output
        ssh.close()
        print(shell_output)





    def build_layer_three_mpls(self):
        """Implements L3vpn changes on PE router and CE switch"""

        self.set_service_dict(self.service_name)  # 1
        self.l3vpn_pe_shell_session()
        self.layer2_ce_shell_session()


    def decom_layer_three_mpls(self):
        """decomission L3vpn """

        self.set_service_dict(self.service_name)
        self.l3vpn_pe_decom_shell_session()
        self.layer2_ce_decom_shell_session()


