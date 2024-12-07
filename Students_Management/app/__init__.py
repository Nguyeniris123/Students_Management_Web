from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/studentdb?charset=utf8mb4" % quote('@Minh27092004')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 8
db = SQLAlchemy(app)