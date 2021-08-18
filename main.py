
from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import request,redirect,url_for,render_template,send_file
from sqlalchemy import select
import pymysql
from sqlalchemy.orm import Session
pymysql.install_as_MySQLdb()
app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://AbleNetAdmin:$TestAdMin$336@10.1.0.3/ablenet"
app.debug = True

db = SQLAlchemy(app)


class L3Vpn(db.Model):

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    SerViceName = db.Column(db.String(50))  # VPN0001
    CustomerName = db.Column(db.String(50))  # Fifa
    CustomerAddress = db.Column(db.String(600))  # 9543 Culver Blvd, Culver City, Los Angeles, California 90232
    Status = db.Column(db.String(50))  # Active/Inactive
    ProviderEdge = db.Column(db.String(50))  # bas01PE01
    AsNumber = db.Column(db.String(50))  # 65001:1
    BgpPassword = db.Column(db.String(50))  # dfghjlkgh
    Rd = db.Column(db.String(50))  # 65001:1
    Rt = db.Column(db.String(50))  # 65001:1
    ImportVpn = db.Column(db.String(300))  # vpn00005
    Routes = db.Column(db.String(50))  # 10.100.100.0 255.255.255.0
    CustomerNextHop = db.Column(db.String(50))  # 10.100.100.100
    PeInterface = db.Column(db.String(50))  # Gi0/0.3
    WanVlan = db.Column(db.String(50))  # 103
    ManVlan = db.Column(db.String(50))  # 903
    PeWanIPAddress = db.Column(db.String(50))  # 10.100.100.1 255.255.255.252
    CeWanIPAddress = db.Column(db.String(50))  # 10.100.100.2 255.255.255.252
    ManageInterface = db.Column(db.String(50))  # Gi0/0.903
    PeManagementWanIp = db.Column(db.String(50))  # 172.16.0.0/16
    CeManagementWanIp = db.Column(db.String(50))  # 172.16.1.10
    CeLoopback = db.Column(db.String(50))  # 172.16.0.6
    Cir = db.Column(db.String(50))  # 50mbps
    Switch = db.Column(db.String(50))  # zur01ceSW01
    SwitchInterface = db.Column(db.String(50))  # Gi0/0


    def __init__(self,SerViceName,CustomerName,CustomerAddress,Status,
                 ProviderEdge,AsNumber,BgpPassword,Rd,Rt,ImportVpn,
                 Routes,CustomerNextHop,PeInterface,WanVlan,ManVlan,
                 PeWanIPAddress,CeWanIPAddress,ManageInterface,
                 PeManagementWanIp,CeManagementWanIp,CeLoopback,
                 Cir,Switch,SwitchInterface

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
        self.PeWanIPAddress = PeWanIPAddress
        self.CeWanIPAddress = CeWanIPAddress
        self.ManageInterface = ManageInterface
        self.PeManagementWanIp = PeManagementWanIp
        self.CeManagementWanIp = CeManagementWanIp
        self.CeLoopback = CeLoopback
        self.Cir = Cir
        self.Switch = Switch
        self.SwitchInterface = SwitchInterface


    def __repr__(self):

        return '<VPN %r>' % self.SerViceName


incoming_sell_output = []


@app.route("/")
def index():


    links = ['/add_l3vpn4','/verify_l3vpn4']

    return render_template("index.html",links=links)




@app.route('/add_l3vpn4')
def add_l3vpn4():
    
    links = ['/', '/verify_l3vpn4']

    from GeneratePassword import PassWordGen

    bgp_pass = PassWordGen()
    print(bgp_pass)
    return render_template('add_l3vpn4.html',bgp_pass=bgp_pass,links=links)






@app.route('/post_l3vpn4_new', methods=['POST'])
def post_l3vpn4():

    l3vpnv4 = L3Vpn(request.form['SerViceName'],
                    request.form['CustomerName'],
                    request.form['CustomerAddress'],
                    request.form['Status'],
                    request.form['ProviderEdge'],
                    request.form['AsNumber'],
                    request.form['BgpPassword'],
                    request.form['Rd'],
                    request.form['Rt'],
                    request.form['ImportVpn'],
                    request.form['Routes'],
                    request.form['CustomerNextHop'],
                    request.form['PeInterface'],
                    request.form['WanVlan'],
                    request.form['ManVlan'],
                    request.form['PeWanIPAddress'],
                    request.form['CeWanIPAddress'],
                    request.form['ManageInterface'],
                    request.form['PeManagementWanIp'],
                    request.form['CeManagementWanIp'],
                    request.form['CeLoopback'],
                    request.form['Cir'],
                    request.form['Switch'],
                    request.form['SwitchInterface'],

                    )

    db.session.add(l3vpnv4)
    db.session.commit()

    return redirect(url_for('index'))



@app.route('/verify_l3vpn4',methods=['GET','POST'])
def verify_l3vpn4():

    links = ['/', '/verify_l3vpn4']

    find_l3vpn4 = L3Vpn.query.all()

    return render_template('verify_l3vpn4.html',links=links)


@app.route('/provision_l3vpn4',methods=['GET','POST'])
def provision_l3vpn4():

    links = ['/','/verify_l3vpn4','/show_shell_output']

    return render_template('provision_l3vpn4.html',
                           links=links)



@app.route('/deactivate_l3vpn4',methods=['GET','POST'])
def deactivate_l3vpn4():

    links = ['/','/verify_l3vpn4','/show_shell_output']

    return render_template('deactivate_l3vpn4.html',
                           links=links)



@app.route('/post_provision_l3vpn4_new', methods=['POST'])
def post_provision_l3vpn4():


    form = request.form
    search_vlaue = form['search_string']
    user_name = form['user_name']
    password = form['password']
    enable_pass = form['enable_pass']


    if   search_vlaue:
        from L3Vpn.AutoShell3 import Channel

        activate = Channel(servie_name=search_vlaue, user_name=user_name, password=password, enable_pass=enable_pass)
        activate.build_L3vpn()
        l3shell_out = activate.get_remote_sell_out()
        incoming_sell_output.append(l3shell_out)


        return redirect(url_for('provision_l3vpn4'))

    else:
        return redirect(url_for('provision_l3vpn4'))




@app.route('/post_deactivate_l3vpn4', methods=['POST'])
def post_deactivate_l3vpn4():


    form = request.form
    search_vlaue = form['search_string']
    user_name = form['user_name']
    password = form['password']
    enable_pass = form['enable_pass']


    if   search_vlaue:
        from L3Vpn.AutoShell3 import Channel

        de_activate = Channel(servie_name=search_vlaue, user_name=user_name, password=password, enable_pass=enable_pass)
        de_activate.decom_L3vpn()

        l3shell_out = de_activate.get_remote_sell_out()
        incoming_sell_output.append(l3shell_out)


        return redirect(url_for('deactivate_l3vpn4'))

    else:
        return redirect(url_for('deactivate_l3vpn4'))










@app.route('/search',methods=['GET','POST'])
def search():

    links = ['/', '/provision_l3vpn4','/provision_l3vpn4','/deactivate_l3vpn4']


    form = request.form
    search_vlaue =  form['search_string']
    print(search_vlaue)
    search = "%{}%".format(search_vlaue)
    print(search)

    l3vpn4_attr = L3Vpn.query.filter(L3Vpn.SerViceName.like(search)).first()

    if l3vpn4_attr:

        return  render_template('verify_l3vpn4.html',links=links,
                                CustomerName=l3vpn4_attr.CustomerName,
                                CustomerAddress = l3vpn4_attr.CustomerAddress,
                                Status = l3vpn4_attr.Status,
                                ProviderEdge = l3vpn4_attr.ProviderEdge,
                                AsNumber = l3vpn4_attr.AsNumber,
                                BgpPassword = l3vpn4_attr.BgpPassword,
                                Rd = l3vpn4_attr.Rd,
                                Rt = l3vpn4_attr.Rt,
                                ImportVpn = l3vpn4_attr.ImportVpn,
                                Routes = l3vpn4_attr.Routes,
                                CustomerNextHop = l3vpn4_attr.CustomerNextHop,
                                PeInterface = l3vpn4_attr.PeInterface,
                                WanVlan = l3vpn4_attr.WanVlan,
                                ManVlan = l3vpn4_attr.ManVlan,
                                PeWanIPAddress = l3vpn4_attr.PeWanIPAddress,
                                CeWanIPAddress = l3vpn4_attr.CeWanIPAddress,
                                ManageInterface = l3vpn4_attr.ManageInterface,
                                PeManagementWanIp = l3vpn4_attr.PeManagementWanIp,
                                CeManagementWanIp = l3vpn4_attr.CeManagementWanIp,
                                CeLoopback = l3vpn4_attr.CeLoopback,
                                Cir = l3vpn4_attr.Cir,
                                Switch = l3vpn4_attr.Switch,
                                SwitchInterface = l3vpn4_attr.SwitchInterface
                                )
    else:


 
        return  render_template('verify_l3vpn4.html',match_not_found =True,links=links)



@app.route('/show_shell_output')
def show_shell_output():

    if len(incoming_sell_output) > 0:
        L3remote_sell_out = incoming_sell_output
        L3remote_sell_out = L3remote_sell_out[0].split('\r\n')
        conf = L3remote_sell_out.index('PE1#configure terminal')
        L3remote_sell_out = L3remote_sell_out[conf:]
        #L3remote_sell_out = 'hello'


    else:
        L3remote_sell_out = None



    return render_template('/show_shell_output.html',L3remote_sell_out=L3remote_sell_out)




if __name__ == "__main__":
    app.run(debug=True)