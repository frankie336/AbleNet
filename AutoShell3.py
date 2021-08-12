''"""
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

from L3VpnTable import L3VpnTableInteract
from DevicesTable import DeviceTableInteract


class FormalAutoShellInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_vpn_data') and
                callable(subclass.load_vpn_data) and
                hasattr(subclass, 'term_zero') and
                callable(subclass.term_zero) and
                hasattr(subclass, 'uni_shell') and
                callable(subclass.uni_shell) and
                hasattr(subclass, 'cios_build_vpn') and
                callable(subclass.ciscoios_build_vpn) or
                NotImplemented)


    @abc.abstractmethod
    def load_vpn_data(self):
        """Load the vpn data from sql query"""
        raise NotImplementedError

    @abc.abstractmethod
    def term_zero(self, device_id: str):
        """The Command for to make terminal length zero"""
        raise NotImplementedError

    @abc.abstractmethod
    def uni_shell(self, host_ip: str):
        """Univeral SSH conection"""
        raise NotImplementedError


    @abc.abstractmethod
    def cios_build_vpn(self):
        """Builds Cisco IOS MPLS VPN"""
        raise NotImplementedError




class LoadDataToList(FormalAutoShellInterface):

    def load_vpn_data(self):
        """Load the vpn data from sql query"""
        service_provision_dict = L3VpnTableInteract(query=True, commit=False)
        return service_provision_dict


    def term_zero(self, device_id: str):
        """The Command for to make terminal length zero"""

        term_zero_list = ['terminal length 0\n']

        if device_id == 'cisco':
            terminal_length = term_zero_list[0]

            return terminal_length


    def cios_build_vpn(self):
        """Builds Cisco IOS MPLS VPN"""

        service_provision_dict = L3VpnTableInteract(query=True, commit=False,query_string='vpn00005')

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

        customer_routes = service_provision_dict['customer_routes']


        """
        Configure wan Interface
        """
        wan_int = 'interface '+service_provision_dict['pe_interface']
        des_wan_int = 'description '+service_provision_dict['service_name']
        assg_vrf = 'vrf forwarding '+service_provision_dict['service_name']
        encap = 'encapsulation dot1Q '+service_provision_dict['vlan']
        wan_ip_addr = 'ip address '+service_provision_dict['pe_wan_ip']+' 255.255.255.252'
        """
        Configure bgp
        """
        v4neighbor = service_provision_dict['ce_wan_ip']#One time neighbour deginition
        rtrbgp = 'router bgp 65000'
        vpn4 = 'address-family ipv4 vrf '+service_provision_dict['service_name']
        redistcon = 'redistribute connected'
        rediststat ='redistribute static'
        v4neigh = 'neighbor '+v4neighbor+' remote-as '+service_provision_dict['as_number']
        desv4eigh = 'neighbor '+v4neighbor+' description '+service_provision_dict['service_name']
        v4pass = 'neighbor '+v4neighbor+' password '+service_provision_dict['bgp_password']
        as_verride = 'neighbor '+v4neighbor+' as-override'
        exitvpn4 = 'exit-address-family'


        commands = ['configure terminal',vrf,rd,rt_ex,rt_imp,des_vrf,'exit',
                    wan_int,des_wan_int,encap,wan_ip_addr,'exit',
                    rtrbgp,vpn4,redistcon,rediststat,v4neigh,as_verride,
                    desv4eigh,v4pass,exitvpn4,'exit',

                    'do wr']




        print(customer_routes)


        return commands

        for x in x :





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

    def __init__(self):
        self.date_time = datetime.datetime.now().strftime("%Y-%m-%d")
        self.username = username
        self.password = password




    def uni_shell(self, host_ip: str):
        """Univeral SSH conection"""


        terminal_length = self.term_zero(device_id='cisco')

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host_ip, port=22, username=self.username, password=password, look_for_keys=False, timeout=None)
            channel = ssh.get_transport().open_session()
            channel.invoke_shell()
        except Exception as e:
            print(host_ip, e.args)
            return

        channel.sendall(terminal_length)  # Send terminal length zero command

        channel.sendall('enable\n')
        time.sleep(.2)
        channel.sendall('cisco\n')#Need a dynamic solution  for password here
        time.sleep(.2)


        command_set = self.cios_build_vpn()

        for x in command_set:
            time.sleep(.2)
            channel.sendall(x + "\n")



        time.sleep(.2)
        shell_output = channel.recv(9999).decode(encoding='utf-8')  # Receive buffer output

        ssh.close()
        print(shell_output)


        #print('Succesfull connection to ' + host_name + ' at IP address:' + host_ip)



    def main(self):

        pe_device = DeviceTableInteract(query=True, commit=False, query_string='zur01PE01')
        pe_ip = pe_device['management_ip']
        host_name = pe_device['host_name']

        self.uni_shell(host_ip=pe_ip)






if __name__ == "__main__":
    username = 'cisco'#Enter network device username temp solution
    password = 'cisco' #temp solution
    a = ChannelClass()
    #a. HyperShell()
    a.main()
