from app import app
from app.api.utils.parser.checkers import CheckPassword

from app.models import db_session
from app.models.__all_models import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    first_name = StringField("Имя", validators=[DataRequired()])
    last_name = StringField("Фамилия", validators=[DataRequired()])

    email = StringField('Почта', validators=[DataRequired()])

    password = PasswordField("Пароль", validators=[DataRequired()])
    password_repeat = PasswordField("Повторите пароль", validators=[DataRequired()])

    subjects = SelectMultipleField("Предметы", choices=[], validators=[DataRequired()])
    groups = SelectMultipleField("Группы", choices=[], validators=[DataRequired()])

    submit = SubmitField('Создать аккаунт')

    def check_password_equal(self):
        if self.password.data != self.password_repeat.data:
            self.password_repeat.errors = ["Пароли должны совпадать"]
            return False
        return True

    def check_password(self):
        try:
            CheckPassword.check_string(self.password.data)
        except Exception as e:
            self.password.errors = [e]
            return False
        return True

    def check_email(self):
        session = db_session.create_session()
        user = session.query(User).filter(User.email == self.email.data).first()
        if user is not None:
            self.email.errors = ["Пользователь с такой почтой уже существует"]
            return False
        return True

    def check_form(self):
        email_pass = self.check_email()
        password_eq_pass = self.check_password_equal()
        password_pass = self.check_password()
        if email_pass and password_pass and password_eq_pass:
            user = User()
            user.name = self.first_name.data
            user.surname = self.last_name.data
            user.email = self.email.data
            user.set_password(self.password.data)
            return user
        return None
