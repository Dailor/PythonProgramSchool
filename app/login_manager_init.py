from flask import redirect

from app.models import db_session
from app.models.__all_models import User

from app import login_manager


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def load_user(session_id):
    session = db_session.create_session()
    return session.query(User).filter(User.session_id == session_id).first()