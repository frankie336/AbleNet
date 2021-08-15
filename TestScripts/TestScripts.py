"""
Created on Mon Jan 11 20:08:27 2021
#! Python 3.8
@author: Francis Neequaye
         francis.neequaye@gmail.com
"""


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



def test_AutoShell():
    """ """
    from L3Vpn.AutoShell3 import ChannelClass

    activate = ChannelClass()
    activate.l3vpn4_changes(service_name='vpn00005')


def test_GeneratePassword():
    """ """
    from GeneratePassword import PassWordGen
    print(PassWordGen())



if __name__ == "__main__":
    pass
    #test_AutoShell()
    #test_CreateL3vpnTable()
    #test_GeneratePassword()
    test_CreateDeviceTable()