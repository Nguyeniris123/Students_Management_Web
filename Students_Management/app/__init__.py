from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
from flask_mail import Mail

app = Flask(__name__)

app.secret_key = 'nhom10@321'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/studentdb?charset=utf8mb4" % quote("Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config['MAIL_USE_TLS'] = True
app.config["MAIL_USERNAME"] = "trannhatminh2709@gmail.com"
app.config["MAIL_PASSWORD"] = 'wocbyokoxhtqxbqy'
mail = Mail(app)

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
# Configuration
cloudinary.config(
    cloud_name = "dnwyvuqej",
    api_key = "559324578186686",
    api_secret = "tjXbrfktUPN8lYMmE9SN-33QXjc", # Click 'View API Keys' above to copy your API secret
    secure=True
)