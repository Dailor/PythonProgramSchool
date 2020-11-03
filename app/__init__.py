from app import config_app

from app.models import db_session

from app.modules import admin, pupil, teacher

from app.api.task.task_resource import PupilSolutionForTask, PupilSolutionsListForTask
from app.api.solution_checker.solution_checker_resource import SolutionCheckerResource

from flask import Flask

from flask_login.login_manager import LoginManager
from flask_restful import Api
from flask_recaptcha import ReCaptcha
from flask_mail import Mail

app = None
recaptcha = None
login_manager = None
api = None
mail = None


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
    api.add_resource(SolutionCheckerResource, config_app.CheckerConfig.CALLBACK_ADDRESS)



def init_app():
    app.add_template_global(name='STATIC_FILES_VERSION', f=app.config['STATIC_FILES_VERSION'])

    init_db()
    init_additions()
    blueprint_routes_register()
    api_register()


def get_app():
    global app, api, recaptcha, login_manager, mail

    app = Flask(__name__)
    app.config.from_object(config_app.DevelopmentConfig)

    recaptcha = ReCaptcha()
    login_manager = LoginManager()
    api = Api(app)
    mail = Mail(app)

    init_app()

    from app import routes
    from app import login_manager_init

    return app
