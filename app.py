from . import config_app
from models import db_session
from models.user import User
from flask import Flask
from flask_login.login_manager import LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


if __name__ == '__main__':
    db_session.global_init()
    config_app.set_config(app)
    app.run(host=config_app.host, port=config_app.port)
