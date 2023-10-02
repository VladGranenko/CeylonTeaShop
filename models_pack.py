from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

dBase = SQLAlchemy()


# Модель для таблицы "Клiенти"
class Customers(UserMixin, dBase.Model):
    __tablename__ = 'customers'

    id = dBase.Column(dBase.Integer, primary_key=True)
    email = dBase.Column(dBase.String(255), nullable=False)
    password = dBase.Column(dBase.String(20), nullable=False)
    time = dBase.Column(dBase.DateTime, default=datetime.utcnow())
    authenticated = dBase.Column(dBase.Boolean)

    def __init__(self, email, password):
        super(Customers, self).__init__()
        self.email = email
        self.password = password
        self.authenticated = False

    def get_id(self):
        return str(self.id)


# Модель для таблицi "Товари та Послуги"
class ProductsAndServices(dBase.Model):
    __tablename__ = 'products_and_services'

    id = dBase.Column(dBase.Integer, primary_key=True)
    name = dBase.Column(dBase.String(255), nullable=False)
    price = dBase.Column(dBase.Float, nullable=False)
    quantity = dBase.Column(dBase.Integer, nullable=False)
    supplier = dBase.Column(dBase.String(255), nullable=False)
    is_product = dBase.Column(dBase.Boolean, default=True)
    definition = dBase.Column(dBase.Text(), nullable=True)
    #
    invoice_id = dBase.Column(dBase.Integer, dBase.ForeignKey('income_invoices.id'))
    income_invoice_rel = dBase.relationship('IncomeInvoices', back_populates='products_rel')
    def __repr__(self):
        return f"Назва: {self.name}, price: {self.price}, quantity: {self.quantity}"

# Модель для таблицi "Архівовані Товари"
class HistoricalProducts(dBase.Model):
    __tablename__ = 'historical_products'
    id = dBase.Column(dBase.Integer, primary_key=True)
    name_hist = dBase.Column(dBase.String(255), nullable=False)
    quantity_hist = dBase.Column(dBase.Integer, nullable=False)
    #
    invoice_id = dBase.Column(dBase.Integer, dBase.ForeignKey('income_invoices.id'))
    invoice_rel_hist = dBase.relationship('IncomeInvoices', back_populates='history_rel')

# Модель для таблицы "Прибутковi накладнi"
class IncomeInvoices(dBase.Model):
    __tablename__ = 'income_invoices'

    id = dBase.Column(dBase.Integer, primary_key=True)
    inc_invoice_date = dBase.Column(dBase.DateTime, default=datetime.utcnow())
    total_amount = dBase.Column(dBase.Integer, nullable=False)
    total_price = dBase.Column(dBase.Float, nullable=False)
    #
    supplier_id = dBase.Column(dBase.Integer, dBase.ForeignKey('suppliers.id'), nullable=False)
    supplier = dBase.relationship('Suppliers', backref='income_invoices')
    products_rel = dBase.relationship('ProductsAndServices', back_populates='income_invoice_rel')
    history_rel = dBase.relationship('HistoricalProducts', back_populates='invoice_rel_hist')


# Модель для таблицi "Видатковi накладнi"
class ExpenseInvoices(dBase.Model):
    __tablename__ = 'expense_invoices'

    id = dBase.Column(dBase.Integer, primary_key=True)
    exp_invoice_date = dBase.Column(dBase.DateTime, default=datetime.utcnow())
    #
    customer_id = dBase.Column(dBase.Integer, dBase.ForeignKey('customers.id'), nullable=False)
    customer = dBase.relationship('Customers', backref='expense_invoices')
    expense_items = dBase.relationship('CartItem', back_populates='expense_invoice')


class CartItem(dBase.Model):
    id = dBase.Column(dBase.Integer, primary_key=True)
    user_id = dBase.Column(dBase.Integer)
    name_item = dBase.Column(dBase.String(255), nullable=False)
    price_item = dBase.Column(dBase.Float, nullable=False)
    quantity_item = dBase.Column(dBase.Integer, nullable=False)
    #
    expense_invoice_id = dBase.Column(dBase.Integer, dBase.ForeignKey('expense_invoices.id'))
    expense_invoice = dBase.relationship('ExpenseInvoices', back_populates='expense_items')


# Модель для таблицы "Поставщики"
class Suppliers(dBase.Model):
    __tablename__ = 'suppliers'

    id = dBase.Column(dBase.Integer, primary_key=True)
    name = dBase.Column(dBase.String(255), nullable=False, unique=True)
    contact_email = dBase.Column(dBase.String(255), nullable=True)

