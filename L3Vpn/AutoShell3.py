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
import abc
import paramiko
import time
from multiprocessing.pool import ThreadPool
import re
import datetime
import psutil
import logging
import getpass
import os
import pandas as pd
from io import StringIO


from Database.Queries import RunSqlQuery


class FormalAutoShellInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_l3vpn_data') and
                callable(subclass.load_l3vpn_data) and
                hasattr(subclass, 'load_device_data') and
                callable(subclass.load_device_data) and
                hasattr(subclass, 'term_zero') and
                callable(subclass.term_zero) and
                hasattr(subclass, 'l3vpn_shell') and
                callable(subclass.l3vpn_shell) and
                hasattr(subclass, 'layer2_shell') and
                callable(subclass.layer2_shell) and
                hasattr(subclass, 'cios_build_l3vpn') and
                callable(subclass.ciscoios_build_vpn) and
                hasattr(subclass, 'cios_build_l2') and
                callable(subclass.ciscoios_build_l2) and
                hasattr(subclass, 'find_ipv4') and
                callable(subclass.find_ipv4) and
                hasattr(subclass, 'l3vpn4_changes') and
                callable(subclass.l3vpn4_changes) or

                NotImplemented)


    @abc.abstractmethod
    def load_l3vpn_data(self,query_string: str):
        """Load the vpn data from sql query"""
        raise NotImplementedError

    @abc.abstractmethod
    def load_device_data(self,query_string: str):
        """Load L3vpn device data"""
        raise NotImplementedError


    @abc.abstractmethod
    def term_zero(self, device_id: str):
        """The Command for to make terminal length zero"""
        raise NotImplementedError

    @abc.abstractmethod
    def l3vpn_shell(self, host_ip: str):
        """Make l3vpn4_changes on PE device"""
        raise NotImplementedError

    @abc.abstractmethod
    def layer2_shell(self, host_ip: str):
        """Make l3vpn4_changes on CE switch"""
        raise NotImplementedError


    @abc.abstractmethod
    def cios_build_l3vpn(self):
        """Builds Cisco IOS MPLS VPN"""
        raise NotImplementedError

    @abc.abstractmethod
    def cios_build_l2(self):
        """Builds Cisco IOS MPLS VPN"""
        raise NotImplementedError


    @abc.abstractmethod
    def find_ipv4(self, input_string: str):
        """Search for ipv4"""
        raise NotImplementedError

    @abc.abstractmethod
    def l3vpn4_changes(self, service_name: str):
        """Brings together vpn4 L2/L3 changes and implements sequentially"""
        raise NotImplementedError





class LoadDataToList(FormalAutoShellInterface):

    def load_l3vpn_data(self,query_string: str):
        """Load the vpn data from sql query"""

        query = RunSqlQuery()
        service_provision_dict = query.query_l3vpn_data(service_name=query_string)

        return service_provision_dict


    def load_device_data(self,query_string: str):
        """Load L3vpn device data"""
        query = RunSqlQuery()
        device_dict = query.query_device(device_name=query_string)

        return device_dict




    def term_zero(self, device_id: str):
        """The Command for to make terminal length zero"""

        term_zero_list = ['terminal length 0\n']

        if device_id == 'cisco':
            terminal_length = term_zero_list[0]

            return terminal_length

    def find_ipv4(self, input_string: str):
        """Search for ipv4"""

        pat = r"(\d\d?\d?\.\d\d?\d?\.\d\d?\d?\.\d\d?\d? \d\d?\d?\.\d\d?\d?\.\d\d?\d?\.\d\d?\d?)"
        ipv4_address = re.findall(pat, input_string)
        return ipv4_address


    def cios_build_l3vpn(self):
        """Builds Cisco IOS MPLS VPN"""

        service_provision_dict = self.load_l3vpn_data(query_string='vpn00005')
        print(service_provision_dict)

        type1_rd = service_provision_dict['as_number']+':'+service_provision_dict['route_distinguisher']#One time definition of rd/rt

        """
        make vrf
        """
        vrf = 'ip vrf '+service_provision_dict['service_name']
        rd = 'rd '+type1_rd
        rt_ex = 'route-target export '+type1_rd
        rt_imp = 'route-target import '+type1_rd
        des_vrf = 'description '+service_provision_dict['customer_name']




        """
        Configure wan Interface
        """
        wan_int = 'interface '+service_provision_dict['pe_interface']
        des_wan_int = 'description '+service_provision_dict['service_name']
        assg_vrf = 'vrf forwarding '+service_provision_dict['service_name']
        encap = 'encapsulation dot1Q '+service_provision_dict['wan_vlan']
        wan_ip_addr = 'ip address '+service_provision_dict['pe_wan_ip']+' 255.255.255.252'
        """
        Configure managment interface
        """
        man_int = 'interface '+service_provision_dict['management_interface']
        l3dotq = 'encapsulation dot1Q '+service_provision_dict['man_vlan']
        man_ip_addr = 'ip address ' + service_provision_dict['management_ip'] + ' 255.255.255.252'
        man_int_vrf = 'ip vrf forwarding vpn00001'
        """
        Configure bgp
        """
        v4neighbor = service_provision_dict['ce_wan_ip']#One time neighbour definition
        rtrbgp = 'router bgp 65000'
        vpn4 = 'address-family ipv4 vrf '+service_provision_dict['service_name']
        redistcon = 'redistribute connected'
        rediststat ='redistribute static'
        v4neigh = 'neighbor '+v4neighbor+' remote-as '+service_provision_dict['as_number']
        desv4eigh = 'neighbor '+v4neighbor+' description '+service_provision_dict['service_name']
        v4pass = 'neighbor '+v4neighbor+' password '+service_provision_dict['bgp_password']
        as_verride = 'neighbor '+v4neighbor+' as-override'
        exitvpn4 = 'exit-address-family'
        """
        Management domain routing
        """
        man_route = 'ip route vrf vpn00001 '+service_provision_dict['ce_man_ip']+' 255.255.255.255 '\
                    +service_provision_dict['ce_manwan_ip']+' name '+service_provision_dict['service_name']
        """
        Customer routes
        """
        customer_routes = service_provision_dict['customer_routes']  # special case for finding multiple routes
        customer_routes ='10.100.100.0 255.255.255.0,10.200.200.0 255.255.255.0'
        found_routes = self.find_ipv4(input_string=customer_routes)



        #custv4troutes='ip route vrf '+service_provision_dict['service_name']+' '+route+' '+service_provision_dict['customer_next_hop']

        commands = ['configure terminal',vrf,rd,rt_ex,rt_imp,des_vrf,'exit',

                    wan_int,des_wan_int,encap,wan_ip_addr,'exit',
                    rtrbgp,vpn4,redistcon,rediststat,v4neigh,as_verride,
                    desv4eigh,v4pass,exitvpn4,'exit',

                    man_int,des_wan_int,
                    l3dotq,man_int_vrf,man_ip_addr,'exit',
                    man_route

                    ]



        return commands


    def cios_build_l2(self):
        """Builds Cisco IOS Layer2"""
        service_provision_dict = self.load_l3vpn_data(query_string='vpn00005')

        cust_int = service_provision_dict['ce_switch_interface']#One time definition of customer interface


        select_l2_int ='interface '+cust_int
        des_l2_int = 'description '+service_provision_dict['service_name']
        trunk = 'switchport trunk encapsulation dot1q'
        ce_vlan = 'switchport trunk allowed vlan '+service_provision_dict['wan_vlan']
        man_vlan = 'switchport trunk allowed vlan add '+ service_provision_dict['man_vlan']




        commands = ['configure terminal',select_l2_int,des_l2_int ,trunk,
                    ce_vlan,man_vlan,


                    ]

        return commands






    def find_host_name(self, device_id: str, search: str) -> str:
        """Search for device hostname string and strip the prompt"""

        """
        For live Cisco devices
        __________________
        1. Search for the hostname string 
        2.Strip the user mode prompt (>,#)
        from the hostname string 
        3. Save  
        """

        if device_id == 'Cisco_IOS':
            prompts = ['>', '#']
            look_behind_prompt = ['(.+)' + prompts[0], '(.+)' + prompts[1]]
            hostname_pat = re.compile('|'.join(look_behind_prompt))
            to_strip = re.compile('|'.join(prompts))

            stripped = (re.search(to_strip, str(search))).group(0)

            hostname = (re.search(hostname_pat, str(search))).group(0).strip(stripped)

            return hostname


class ChannelClass(LoadDataToList):
    count_cores = psutil.cpu_count(logical=True)  # Count number of cores/threads in CPU

    def __init__(self,user_name,password,enable_pass):
        self.date_time = datetime.datetime.now().strftime("%Y-%m-%d")
        self._user_name = user_name
        self._password = password
        self._enable_pass = enable_pass




    def l3vpn_shell(self, host_ip: str):
        """Make l3vpn4_changes on PE device"""
        terminal_length = self.term_zero(device_id='cisco')

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host_ip, port=22, username=self._user_name, password=self.password, look_for_keys=False, timeout=None)
            channel = ssh.get_transport().open_session()
            channel.invoke_shell()
        except Exception as e:
            print(host_ip, e.args)
            return

        channel.sendall(terminal_length)  # Send terminal length zero command

        channel.sendall('enable\n')
        time.sleep(.2)
        channel.sendall(self._enable_pass+'\n')#Need a dynamic solution  for password here
        time.sleep(.2)


        command_set = self.cios_build_l3vpn()

        for x in command_set:
            time.sleep(.2)
            channel.sendall(x + "\n")

        """
        special case for adding multiple customer routes
        """
        service_provision_dict = self.load_l3vpn_data(query_string='vpn00005')

        customer_routes = service_provision_dict['customer_routes']
        customer_routes ='10.10.10.0 255.255.255.0,10.20.20.20.0 255.255.255.0'
        found_routes = self.find_ipv4(input_string=customer_routes)
        ipv4vrf = service_provision_dict['service_name']
        ipv4next_hop = service_provision_dict['customer_next_hop']

        for x in found_routes:
            time.sleep(.1)
            channel.sendall('ip route vrf '+ipv4vrf+' '+x+' '+ipv4next_hop+"\n")

        channel.sendall('end \n')
        channel.sendall('write memory\n')





        time.sleep(.2)
        shell_output = channel.recv(9999).decode(encoding='utf-8')  # Receive buffer output

        ssh.close()
        print(shell_output)
        #print('Succesfull connection to ' + host_name + ' at IP address:' + host_ip)


    def layer2_shell(self, host_ip: str):
        """Make l3vpn4_changes on CE switch"""
        terminal_length = self.term_zero(device_id='cisco')

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host_ip, port=22, username=self._user_name, password=self._password, look_for_keys=False, timeout=None)
            channel = ssh.get_transport().open_session()
            channel.invoke_shell()
        except Exception as e:
            print(host_ip, e.args)
            return

        channel.sendall(terminal_length)  # Send terminal length zero command

        channel.sendall('enable\n')
        time.sleep(.2)
        channel.sendall(self._enable_pass+'\n')  # Need a dynamic solution  for password here
        time.sleep(.2)

        command_set = self.cios_build_l2()


        for x in command_set:
            time.sleep(.2)
            channel.sendall(x + "\n")


        channel.sendall('end \n')
        channel.sendall('write memory\n')



        time.sleep(.2)
        shell_output = channel.recv(9999).decode(encoding='utf-8')  # Receive buffer output

        ssh.close()
        print(shell_output)



    def l3vpn4_changes(self,service_name: str):
        """Brings together vpn4 L2/L3 changes and implements sequentially"""

        service_provision_dict = self.load_l3vpn_data(query_string=service_name)
        provider_edge = service_provision_dict['provider_edge']
        ce_switch = service_provision_dict['ce_switch']

        """
        L3
        """
        pe_device_dict = self.load_device_data(query_string=provider_edge)
        print(pe_device_dict)
        pe_ip = pe_device_dict['management_ip']
        host_name = pe_device_dict['host_name']
        self.l3vpn_shell(host_ip=pe_ip)
        """
        L2
        """
        ce_switch_dict = self.load_device_data(query_string=ce_switch)
        print(ce_switch_dict)
        ce_switch_ip = ce_switch_dict['management_ip']
        self.layer2_shell(host_ip=ce_switch_ip)





