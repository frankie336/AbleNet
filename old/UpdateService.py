class UpdateService:
    def __init__(self,SerViceName,CustomerName,
                 CustomerAddress,Status,
                 ProviderEdge,AsNumber,
                 BgpPassword,Rd,Rt,
                 ImportVpn,Routes,
                 CustomerNextHop,PeInterface,
                 WanVlan,ManVlan,
                 CeWanIPAddress,ManageInterface,
                 PeManagementWanIp,CeManagementWanIp,
                 CeLoopback,Cir,Switch,SwitchInterface

                 ):
        self.SerViceName = SerViceName
        self.CustomerName = CustomerName
        self.CustomerAddress = CustomerAddress
        self.Status = Status
        self.ProviderEdge = ProviderEdge
        self.AsNumber = AsNumber
        self.BgpPassword = BgpPassword
        self.Rd = Rd
        self.Rt = Rt
        self.ImportVpn = ImportVpn
        self.Routes = Routes
        self.CustomerNextHop = CustomerNextHop
        self.PeInterface = PeInterface
        self.WanVlan = WanVlan
        self.ManVlan = ManVlan
        self.CeWanIPAddress = CeWanIPAddress
        self.ManageInterface = ManageInterface
        self.PeManagementWanIp = PeManagementWanIp
        self.CeManagementWanIp = CeManagementWanIp
        self.CeLoopback = CeLoopback
        self.Cir = Cir
        self.Switch = Switch
        self.SwitchInterface = SwitchInterface

    def change_column(self):

        print('Hello UpdateService')

        columns = [self.SerViceName,
                   self.CustomerName,
                   self.CustomerAddress,
                   self.Status,
                   self.ProviderEdge,
                   self.AsNumber,
                   self.BgpPassword,
                   self.Rd,
                   self.Rt,
                   self.ImportVpn,
                   self.Routes,
                   self.CustomerNextHop,
                   self.PeInterface,
                   self.WanVlan,
                   self.ManVlan,
                   self.CeWanIPAddress,
                   self.ManageInterface,
                   self.PeManagementWanIp,
                   self.CeManagementWanIp,
                   self.CeLoopback,
                   self.Cir,
                   self.Switch,
                   self.SwitchInterface
                   ]
        result = L3Vpn.query.filter_by(SerViceName=self.serViceName).first()
        print(result,'>>>><<<<<<>>><<<<>>>')

        #for column in columns:
            #print(column)
        #if something is not None:
            #something.something = something