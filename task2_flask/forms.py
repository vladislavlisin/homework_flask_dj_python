from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Email

# формы для добавления

class UniversityForm(FlaskForm):

    # id = IntegerField("ID", validators=[DataRequired()])
    full_title = StringField("Full title", validators=[DataRequired()])
    short_title = StringField("Short title", validators=[DataRequired()])
    foundation_date = DateField("Foundation date", validators=[DataRequired()])
    submit = SubmitField("Apply")

# Cтудент
# ФИО
# Дата рождения
# Университет(только из списка университетов, содержащихся в базе)
# Год поступления


class StudentForm(FlaskForm):

    # id = IntegerField("ID", validators=[DataRequired()])
    FIO = StringField("FIO", validators=[DataRequired()])
    born_date = DateField("Born date", validators=[DataRequired()])
    get_in_date = DateField("Get in university date", validators=[DataRequired()])
    university = IntegerField("University ID", validators=[DataRequired()])
    submit = SubmitField("Apply")


class RegisterForm(FlaskForm):

    # id = IntegerField("ID", validators=[DataRequired()])
    login = StringField("Login", validators=[DataRequired()])
    name = StringField("User name", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    repeat_password = StringField("Repeat password", validators=[DataRequired()])
    submit = SubmitField("Apply")

class LoginForm(FlaskForm):

    # id = IntegerField("ID", validators=[DataRequired()])
    login = StringField("Login", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Apply")