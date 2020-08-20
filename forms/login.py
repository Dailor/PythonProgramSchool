from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField("Электронная почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class LoginAnswers:
    WRONG_EMAIL = "WRONG_EMAIL", "Пользователя с такой почтой не существует"
    WRONG_PASSWORD = "WRONG_PASSWORD", "Введенный пароль неправильный"
