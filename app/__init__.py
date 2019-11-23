from flask import Flask,render_template,redirect,flash,Blueprint
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
from flask_migrate import Migrate
from config import Config
from flask_mail import Mail


app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)
blueprint = Blueprint('errors',__name__)
from app import routes,models,errors

# 这行必须放在最后





if __name__ == '__main__':
    app.run(debug = True)
