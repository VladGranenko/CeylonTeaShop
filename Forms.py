from flask_wtf import FlaskForm

from models_pack import ProductsAndServices
from wtforms import (
                     StringField, SubmitField, IntegerField, FileField, SelectField,
                     BooleanField, PasswordField, FloatField, TextAreaField, DateField
                    )
from wtforms.validators import Email, DataRequired, Length, EqualTo, NumberRange


class RegisterForm(FlaskForm):
    email = StringField('Почта:', validators=[
                        Email(message='Повинен бути формат електронної пошти зі знаком @ та домен')]
    )
    psw = PasswordField(
                        'Пароль #1:', validators=[DataRequired(),
                        Length(min=5, max=20, message='Довжина пароля має бути від 5 до 20 символів.')]
    )
    psw2 = PasswordField(
                        'Пароль #2:', validators=[DataRequired(),
                        EqualTo('psw', message='Паролі не збігаються.'),
                        Length(min=5, max=20, message='Довжина пароля має бути від 5 до 20 символів.')]
    )
    submit = SubmitField('Реєстрацiя')

class LoginForm(FlaskForm):
    email = StringField('Почта:', validators=[
                        Email(message='Повинен мати формат електронної пошти зі знаком @ та домен')]
    )
    psw = PasswordField(
          'Пароль:', validators=[
                     DataRequired(),
                     Length(min=5, max=20, message='Довжина пароля повинна бути від 5 до 20 символів')]
    )
    submit = SubmitField('Вхід')


class LoadExcelForm(FlaskForm):
    file_excel = FileField("Завантажити Excel", validators=[DataRequired()])
    submit = SubmitField("Додати")


class GenerateReportForm(FlaskForm):
    start_date = DateField('Вiд:', format='%Y-%m-%d', validators=[DataRequired()])
    finish_date = DateField('До:', format='%Y-%m-%d', validators=[DataRequired()])
    submit_rpt = SubmitField('Створити')

class ChangeNodeForm(FlaskForm):
    name = StringField('Назва:', validators=[
                        Length(min=4, max=50, message='Довжина назви повинна бути від 4 до 50 символів.')]
    )
    price = FloatField('Вартість:', validators=[
                        NumberRange(min=1, max=2000, message='Вартість повинна бути в діапазоні від 1 до 2000')]
    )
    quantity = IntegerField('Кiлькicть:', validators=[
                        NumberRange(min=1, max=500, message='Кількість повинна бути в діапазоні від 1 до 500')]
    )
    supplier = StringField('Поставщик:', validators=[
                        Length(min=4, max=15, message='Довжина назви поставщика повинна бути від 4 до 15 символів.')]
    )
    definition = TextAreaField('Опис:',
                               validators=[Length(max=1000,
                               message='Довжина опису повинна бути до 1000 символів.')]
    )
    is_product = BooleanField('Продукт:')
    submit = SubmitField()


class CartItemForm(FlaskForm):
    name_product = SelectField('Назва:', validators=[DataRequired(message='Виберіть продукт')]
    )
    price_product = FloatField('Вартість:', validators=[
                    NumberRange(min=1, max=2000, message='Вартість повинна бути в діапазоні від 1 до 2000')]
    )
    quantity_product = IntegerField('Кількість:', validators=[
                        NumberRange(min=1, max=500, message='Кількість повинна бути в діапазоні від 1 до 500')]
    )
    submit_name = SubmitField("В кошик")

    def __init__(self):
        super(CartItemForm, self).__init__()
        unique_names = ProductsAndServices.query.filter_by(is_product=True).with_entities(
                                                                    ProductsAndServices.name).distinct()
        self.name_product.choices = [('-', '- не вибрано ')] + [(name, name) for name, in unique_names]


class ServiceForm(FlaskForm):
    name_service = SelectField('Послуга:', validators=[DataRequired(message='Виберіть послугу')]
    )
    price_service = FloatField('Вартість:', validators=[
                    NumberRange(min=1, max=2000, message='Вартість повинна бути в діапазоні від 1 до 2000')]
    )
    submit_service = SubmitField('Додати')
    def __init__(self):
        super(ServiceForm, self).__init__()
        service_names = ProductsAndServices.query.filter_by(is_product=False).with_entities(
            ProductsAndServices.name).distinct().all()
        self.name_service.choices = [('-', '- не вибрано ')] + [(name, name) for name, in service_names]