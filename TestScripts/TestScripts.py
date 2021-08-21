"""
Created on Mon Jan 11 20:08:27 2021
#! Python 3.8
@author: Francis Neequaye
         francis.neequaye@gmail.com
"""
import time

def test_CreateL3vpnTable():
    """ """
    from Database.CreateTables import CreateL3vpnTable
    print('Running Script to create L3vpnTable')
    CreateL3vpnTable()


def test_CreateDeviceTable():
    """ """
    from Database.CreateTables import CreateDeviceTable
    print('Running Script to create CreateDeviceTable')
    CreateDeviceTable()


def test_vpn3build():
    """ """
    from autoshell.AutoShell3 import Channel

    activate = Channel(service_name='vpn00005', user_name='cisco', password='cisco', enable_pass='cisco')
    activate.build_mpls_three()


def test_vpn3decom():
    """ """
    from autoshell.AutoShell3 import Channel
    activate = Channel(service_name='vpn00005', user_name='cisco', password='cisco', enable_pass='cisco')
    activate.decom_mpls_three()


def test_GeneratePassword():
    """ """
    from GeneratePassword import PassWordGen
    print(PassWordGen())


def test_passing_shell():
    from L3Vpn.AutoShell3 import Channel
    obj1 = ChannelClass(user_name='cisco', password='cisco', enable_pass='cisco')
    print(obj1.get_remote_sell_out())
    obj1.set_remote_sell_out('Hello World')
    print(obj1.get_remote_sell_out())

    obj1.l3vpn4_changes(service_name='vpn00005')


if __name__ == "__main__":
    pass
    test_vpn3build()
    #time.sleep(1)
    #test_vpn3decom()
    # test_CreateL3vpnTable()
    # test_GeneratePassword()
    # test_CreateDeviceTable()
    # test_passing_shell()




