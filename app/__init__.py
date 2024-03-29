from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '&%^&)7896987697*%^%&*^)*^*RTUYTIUY*^&%&*^%&(^(*'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/db_hotel_management?charset=utf8mb4" % quote('Sang@150203')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6

import cloudinary

cloudinary.config(
    cloud_name="dnzpkdfli",
    api_key="566681559361447",
    api_secret="TFdSHrguiVasCYqgX2MRVKgl-YQ"
)

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
login.login_view = 'login'
