import json
from autoshell.AutoShell3 import Channel
from GeneratePassword import password_gen
from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import request,redirect,url_for,render_template,send_file,jsonify
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
    PeWanIPAddress = db.Column(db.String(50))  #10.100.100.1 255.255.255.252
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




@app.route('/test_page')
def testpage():

    return render_template("test_page.html")



@app.route("/")
def index():


    links = ['/add_l3vpn4','/verify_l3vpn4','/update_l3vpn4/']

    return render_template("index.html",links=links)


@app.route('/add_l3vpn4')
def add_l3vpn4():
    
    links = ['/', '/verify_l3vpn4']
    bgp_pass = password_gen()

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





@app.route('/update_l3vpn4/',methods=['GET','POST'])
def update():
    links = ['/', '/provision_l3vpn4', '/provision_l3vpn4',
             '/deactivate_l3vpn4', '/update_l3vpn4']
    return render_template('update_l3vpn4.html',
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

        activate = Channel(service_name=search_vlaue, user_name=user_name, password=password, enable_pass=enable_pass)
        activate.build_mpls_three()

        l3shell_out = activate.get_remote_shell_out()

        incoming_sell_output.clear()
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

    de_activate = Channel(service_name=search_vlaue, user_name=user_name, password=password, enable_pass=enable_pass)

    de_activate.decom_mpls_three()

    test = de_activate.get_remote_shell_out()

    incoming_sell_output.clear()
    incoming_sell_output.append(test)

    print(de_activate.get_remote_shell_out())

    return redirect(url_for('deactivate_l3vpn4'))








@app.route('/edited',methods=['GET','POST'])
def edited():

    links = ['/', '/provision_l3vpn4','/provision_l3vpn4',
             '/deactivate_l3vpn4','/update_l3vpn4']

    if request.method == "POST":
        SerViceName = request.form.get("SerViceName")
        CustomerName = request.form.get("CustomerName")
        CustomerAddress = request.form.get("CustomerAddress ")
        Status = request.form.get("Status")
        ProviderEdge = request.form.get("ProviderEdge")
        AsNumber = request.form.get("AsNumber")
        BgpPassword = request.form.get("BgpPassword")
        Rd = request.form.get("Rd")
        Rt = request.form.get("Rt")
        ImportVpn = request.form.get("ImportVpn")
        Routes = request.form.get("Routes")
        CustomerNextHop = request.form.get("CustomerNextHop")
        PeInterface = request.form.get("PeInterface")
        WanVlan = request.form.get("WanVlan")
        ManVlan = request.form.get("ManVlan")
        CeWanIPAddress = request.form.get("CeWanIPAddress")
        ManageInterface = request.form.get("ManageInterface")
        PeManagementWanIp = request.form.get("PeManagementWanIp")
        CeManagementWanIp = request.form.get("CeManagementWanIp")
        CeLoopback = request.form.get("CeLoopback")
        Cir = request.form.get("Cir")
        Switch = request.form.get("Switch")
        SwitchInterface = request.form.get("SwitchInterface")


        result = L3Vpn.query.filter_by(SerViceName=SerViceName).first()

    if CustomerAddress is not None:
        print("Making Edit to CustomerAddress on SQL Table")
        result.CustomerAddress = CustomerAddress
        db.session.commit()

    if Status is not None:
        print("Making Edit to Status on SQL Table")
        result.Status = Status
        db.session.commit()

    if ProviderEdge is not None:
        print("Making Edit to ProviderEdge on SQL Table")
        result.ProviderEdge = ProviderEdge
        db.session.commit()

    if AsNumber is not None:
        print("Making Edit to AsNumber on SQL Table")
        result.AsNumber = AsNumber
        db.session.commit()

    if BgpPassword is not None:
        print("Making Edit to BgpPassword on SQL Table")
        result.BgpPassword = BgpPassword
        db.session.commit()

    if Rd is not None:
        print("Making Edit to Rd on SQL Table")
        result.Rd = Rd
        db.session.commit()

    if Rt is not None:
        print("Making Edit to Rt on SQL Table")
        result.Rt = Rt
        db.session.commit()

    if ImportVpn is not None:
        print("Making Edit to ImportVpn on SQL Table")
        result.ImportVpn = ImportVpn
        db.session.commit()

    if Routes is not None:
        print("Making Edit to Routes on SQL Table")
        result.Routes = Routes
        db.session.commit()

    if CustomerNextHop is not None:
        print("Making Edit to CustomerNextHop on SQL Table")
        result.CustomerNextHop = CustomerNextHop
        db.session.commit()

    if PeInterface is not None:
        print("Making Edit to PeInterface on SQL Table")
        result.PeInterface = PeInterface
        db.session.commit()

    if WanVlan is not None:
        print("Making Edit to WanVlan on SQL Table")
        result.WanVlan = WanVlan
        db.session.commit()

    if ManVlan is not None:
        print("Making Edit to ManVlan on SQL Table")
        result.ManVlan = ManVlan
        db.session.commit()

    if CeWanIPAddress is not None:
        print("Making Edit to CeWanIPAddress on SQL Table")
        result.CeWanIPAddress = CeWanIPAddress
        db.session.commit()

    if ManageInterface is not None:
        print("Making Edit to ManageInterface on SQL Table")
        result.ManageInterface = ManageInterface
        db.session.commit()

    if PeManagementWanIp is not None:
        print("Making Edit to PeManagementWanIp on SQL Table")
        result.PeManagementWanIp = PeManagementWanIp
        db.session.commit()

    if CeManagementWanIp is not None:
        print("Making Edit to CeManagementWanIp on SQL Table")
        result.CeManagementWanIp = CeManagementWanIp
        db.session.commit()


    if CeLoopback is not None:
        print("Making Edit to CeLoopback on SQL Table")
        result.CeLoopback = CeLoopback
        db.session.commit()

    if Cir is not None:
        print("Making Edit to Cir on SQL Table")
        result.Cir = Cir
        db.session.commit()

    if Cir is not None:
        print("Making Edit to Cir on SQL Table")
        result.Cir = Cir
        db.session.commit()

    if Switch is not None:
        print("Making Edit to Switch on SQL Table")
        result.Switch = Switch
        db.session.commit()

    if SwitchInterface is not None:
        print("Making Edit to SwitchInterface on SQL Table")
        result.SwitchInterface = SwitchInterface
        db.session.commit()

    return redirect(url_for('index'))





@app.route('/change',methods=['GET','POST'])
def change():

    links = ['/', '/provision_l3vpn4','/provision_l3vpn4',
             '/deactivate_l3vpn4','/update_l3vpn4']


    form = request.form
    search_string =  form['search_string']
    print(search_string)
    #l3vpn4_attr = L3Vpn.query.filter(L3Vpn.SerViceName.like(search)).first()
    result = L3Vpn.query.filter_by(SerViceName=search_string).first()
    db.session.commit()

    if result:
        return  render_template('update_l3vpn4.html',
                                links=links,search_string=search_string,
                                CustomerName=result.CustomerName,
                                CustomerAddress = result.CustomerAddress,
                                Status = result.Status,
                                ProviderEdge = result.ProviderEdge,
                                AsNumber = result.AsNumber,
                                BgpPassword = result.BgpPassword,
                                Rd = result.Rd,
                                Rt = result.Rt,
                                ImportVpn = result.ImportVpn,
                                Routes = result.Routes,
                                CustomerNextHop = result.CustomerNextHop,
                                PeInterface = result.PeInterface,
                                WanVlan = result.WanVlan,
                                ManVlan = result.ManVlan,
                                PeWanIPAddress = result.PeWanIPAddress,
                                CeWanIPAddress = result.CeWanIPAddress,
                                ManageInterface = result.ManageInterface,
                                PeManagementWanIp = result.PeManagementWanIp,
                                CeManagementWanIp = result.CeManagementWanIp,
                                CeLoopback = result.CeLoopback,
                                Cir = result.Cir,
                                Switch = result.Switch,
                                SwitchInterface = result.SwitchInterface
                                )
    else:

        return  render_template('update_l3vpn4.html',match_not_found =True,links=links)





@app.route('/search',methods=['GET','POST'])
def search():

    links = ['/', '/provision_l3vpn4','/provision_l3vpn4',
             '/deactivate_l3vpn4','/update_l3vpn4']



    form = request.form
    search_string =  form['search_string']
    print(search_string)
    #l3vpn4_attr = L3Vpn.query.filter(L3Vpn.SerViceName.like(search)).first()
    result = L3Vpn.query.filter_by(SerViceName=search_string).first()


    db.session.commit()

    if result:
        return  render_template('verify_l3vpn4.html',links=links,
                                CustomerName=result.CustomerName,
                                CustomerAddress = result.CustomerAddress,
                                Status = result.Status,
                                ProviderEdge = result.ProviderEdge,
                                AsNumber = result.AsNumber,
                                BgpPassword = result.BgpPassword,
                                Rd = result.Rd,
                                Rt = result.Rt,
                                ImportVpn = result.ImportVpn,
                                Routes = result.Routes,
                                CustomerNextHop = result.CustomerNextHop,
                                PeInterface = result.PeInterface,
                                WanVlan = result.WanVlan,
                                ManVlan = result.ManVlan,
                                PeWanIPAddress = result.PeWanIPAddress,
                                CeWanIPAddress = result.CeWanIPAddress,
                                ManageInterface = result.ManageInterface,
                                PeManagementWanIp = result.PeManagementWanIp,
                                CeManagementWanIp = result.CeManagementWanIp,
                                CeLoopback = result.CeLoopback,
                                Cir = result.Cir,
                                Switch = result.Switch,
                                SwitchInterface = result.SwitchInterface
                                )
    else:

        return  render_template('verify_l3vpn4.html',match_not_found =True,links=links)



@app.route('/show_shell_output')
def show_shell_output():

    #incoming_sell_output.clear()

    if len(incoming_sell_output) > 0:
        L3remote_sell_out = incoming_sell_output
        L3remote_sell_out = L3remote_sell_out[0].split('\r\n')
        conf = L3remote_sell_out.index('PE1#show clock')
        L3remote_sell_out = L3remote_sell_out[conf:]

        print(L3remote_sell_out)

    else:
        L3remote_sell_out = None

@app.route('/all', methods=['GET'])
def api_all():

    args1 = request.args['args1']
    l3vpn4_attr = L3Vpn.query.filter(L3Vpn.SerViceName.like(args1)).first()

    vpn_api = [

         {'CustomerName':l3vpn4_attr.CustomerName,
          'CustomerAddress': l3vpn4_attr.CustomerAddress,
           'Status' : l3vpn4_attr.Status,
           'AsNumber': l3vpn4_attr.AsNumber,
           'Rd' : l3vpn4_attr.Rd,
           'Rt' : l3vpn4_attr.Rt,
           'ProviderEdge': l3vpn4_attr.ProviderEdge,
           'BgpPassword' : l3vpn4_attr.BgpPassword,
           'ImportVpn' : l3vpn4_attr.ImportVpn,
           'Routes': l3vpn4_attr.Routes,
           'CustomerNextHop': l3vpn4_attr.CustomerNextHop,
           'PeInterface': l3vpn4_attr.PeInterface,
           'WanVlan': l3vpn4_attr.WanVlan,
           'ManVlan':l3vpn4_attr.ManVlan,
           'PeWanIPAddress': l3vpn4_attr.PeWanIPAddress,
           'CeWanIPAddress': l3vpn4_attr.CeWanIPAddress,
           'ManageInterface':  l3vpn4_attr.ManageInterface,
           'PeManagementWanI':l3vpn4_attr.PeManagementWanIp,
           'CeManagementWanIp': l3vpn4_attr.CeManagementWanIp,
           'CeLoopback': l3vpn4_attr.CeLoopback,
           'Cir':l3vpn4_attr.Cir,
           'Switch': l3vpn4_attr.Switch,
           'SwitchInterface': l3vpn4_attr.SwitchInterface



          }

     ]

    return jsonify(vpn_api)

    #return render_template('/show_shell_output.html',L3remote_sell_out=L3remote_sell_out)
if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=3000,debug=True)

