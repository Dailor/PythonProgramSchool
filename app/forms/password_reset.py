from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.api.utils.parser.checkers import CheckPassword


class PasswordChecker:
    def __call__(self, form, field):
        try:
            CheckPassword.check_string(field.data)
        except Exception as e:
            raise ValidationError(e)


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    submit = SubmitField('Восстановить Пароль')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired(), PasswordChecker()])
    password_repeat = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password', message="Пароли должны быть одинаковыми!")])
    submit = SubmitField('Сменить пароль')
