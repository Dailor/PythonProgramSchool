from app import config_app, jinja_global

from app.models import db_session

from app.modules import admin, pupil, teacher

from app.api.task.task_resource import PupilSolutionForTask, PupilSolutionsListForTask
from app.api.solution_checker.solution_checker_resource import SolutionCheckerResource

from flask import Flask

from flask_login.login_manager import LoginManager
from flask_restful import Api
from flask_recaptcha import ReCaptcha
from flask_mail import Mail
from flask_moment import Moment

app = None
recaptcha = None
login_manager = None
api = None
mail = None
moment = None


def init_db():
    db_session.global_init(debug=app.config["DEBUG"])


def init_additions():
    global api, recaptcha, login_manager, mail, moment

    recaptcha = ReCaptcha()
    login_manager = LoginManager()
    api = Api(app)
    mail = Mail(app)
    moment = Moment(app)

    recaptcha.init_app(app)
    login_manager.init_app(app)


def blueprint_routes_register():
    app.register_blueprint(admin.blueprint, url_prefix="/admin")
    app.register_blueprint(teacher.blueprint, url_prefix='/teacher')
    app.register_blueprint(pupil.blueprint, url_prefix='/pupil')


def api_register():
    api.add_resource(PupilSolutionForTask, '/api/solution')
    api.add_resource(PupilSolutionsListForTask, '/api/solutions')
    api.add_resource(SolutionCheckerResource, config_app.CheckerConfig.CALLBACK_ADDRESS)


def load_app():
    init_db()
    from app import default_data_in_database

    jinja_global.set_global_jinja_variables(app)
    init_additions()
    blueprint_routes_register()
    api_register()


def init_app():
    global app

    if app is not None:
        return app

    app = Flask(__name__)
    app.config.from_object(config_app.DevelopmentConfig)

    load_app()

    from app import routes
    from app import login_manager_init

    return app
