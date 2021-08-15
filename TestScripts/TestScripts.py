"""
Created on Mon Jan 11 20:08:27 2021
#! Python 3.8
@author: Francis Neequaye
         francis.neequaye@gmail.com
"""
from L3Vpn.AutoShell3 import ChannelClass


def TestAutoShell():

    activate = ChannelClass()
    activate.l3vpn4_changes(service_name='vpn00005')


if __name__ == "__main__":
    TestAutoShell()