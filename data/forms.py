from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import PasswordField, StringField, SubmitField, FloatField, FileField, SelectField
from wtforms.validators import DataRequired, Length


class FormLogin(FlaskForm):
    email = StringField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[Length(8, 16, "Пароль от 8 до 16 символов"), DataRequired()])
    submit = SubmitField("Войти")


class FormUserRegistration(FlaskForm):
    fullname = StringField("Ваше имя", validators=[DataRequired()])
    email = StringField("Почта", validators=[DataRequired()])
    level = SelectField(choices=((1, "Не занимался"),
                                 (2, "Занимаюсь пару месяцев"),
                                 (3, "Занимаюсь год"),
                                 (4, "Занимаюсь больше года")))
    password_1 = PasswordField("Пароль", validators=[Length(8, 16, "Пароль от 8 до 16 символов"), DataRequired()])
    password_2 = PasswordField("Повторите Пароль", validators=[Length(8, 16, "Пароль от 8 до 16 символов"), DataRequired()])
    submit = SubmitField("Зарегистрироваться")


class FormCompanyRegistration(FlaskForm):
    name = StringField("Название компании", validators=[DataRequired()])
    email = StringField("Почта", validators=[DataRequired()])
    rates = FloatField("Множитель цены", validators=[DataRequired()])
    logo = FileField("Логотип компании", validators=[FileAllowed(['jpg', 'png'])])
    password_1 = PasswordField("Пароль", validators=[Length(8, 16, "Пароль от 8 до 16 символов"), DataRequired()])
    password_2 = PasswordField("Повторите Пароль", validators=[Length(8, 16, "Пароль от 8 до 16 символов"), DataRequired()])
