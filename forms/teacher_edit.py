from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class TeacherEditForm(FlaskForm):
    name = StringField("Имя")
    surname = StringField("Фамилия")
    email = StringField("Email")

    subjects = SelectField("Предметы", validators=[DataRequired()])
    groups = SelectField("Группы", validators=[DataRequired()])

    submit = SubmitField("Изменить")
