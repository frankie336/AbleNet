
from Database.L3VpnTable import L3VpnTableInteract
from Database.DevicesTable import DeviceTableInteract

def main():
    pass
    #DeviceTableInteract(commit=True)

    srvice_provision_dict=L3VpnTableInteract(query=False, commit=True)



if __name__ == '__main__':
    main()

