from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import request,redirect,url_for,render_template
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


@app.route('/')
def index():

    return render_template('add_l3vpn4.html')




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



@app.route("/about")
def home():
    return render_template("about.html")





if __name__ == "__main__":
    app.run(debug=True)