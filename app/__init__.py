from app import config_app

from app.models import db_session

from app.modules import admin, pupil, teacher

from app.api.task.task_resource import PupilSolutionForTask, PupilSolutionsListForTask

from flask import Flask

from flask_login.login_manager import LoginManager
from flask_restful import Api
from flask_recaptcha import ReCaptcha
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(config_app.BaseConfig)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.__factory.remove()


def init_db():
    db_session.global_init(debug=app.config["DEBUG"])

    from app import default_data_in_database


def init_additions():
    recaptcha.init_app(app)
    login_manager.init_app(app)


def blueprint_routes_register():
    app.register_blueprint(admin.blueprint, url_prefix="/admin")
    app.register_blueprint(teacher.blueprint, url_prefix='/teacher')
    app.register_blueprint(pupil.blueprint, url_prefix='/pupil')


def api_register():
    api.add_resource(PupilSolutionForTask, '/api_solution')
    api.add_resource(PupilSolutionsListForTask, '/api_solutions')


def init_app():
    init_db()
    init_additions()
    blueprint_routes_register()
    api_register()


recaptcha = ReCaptcha()
login_manager = LoginManager()
api = Api(app)
mail = Mail(app)

init_app()

from app import routes
from app import login_manager_init
