from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from Routes.config import Config
import urllib.parse

server = Config.SQLSERVER_IP
database = "ritas_po_system"
username = Config.SQLSERVER_USER
password = Config.SQLSERVER_PASS
UPLOAD_FOLDER = "Images"

app = Flask(__name__, template_folder="../templates", static_folder="../static/")
app.config["UPLOAD_FOLDER"]  = UPLOAD_FOLDER
app.secret_key = "Ritas2023"
app.config["SESSION_TYPE"] = "filesystem"


params = urllib.parse.quote_plus(
     "DRIVER={ODBC DRIVER 18 for SQL Server};SERVER="
    + server
    + ";DATABASE="
    + database
    + ";ENCRYPT=no;UID="
    + username
    + ";PWD="
    + password
)

app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc:///?odbc_connect=%s" % params
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from Routes import index, Tracking

