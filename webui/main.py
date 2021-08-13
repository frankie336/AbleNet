from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://AbleNetAdmin:$TestAdMin$336@10.1.0.3/ablenet"




@app.route("/")
def home():
    return render_template("about.html")





if __name__ == "__main__":
    app.run(debug=True)