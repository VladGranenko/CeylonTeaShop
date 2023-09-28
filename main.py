import os
from flask import Flask, render_template, redirect, url_for, flash, jsonify, request, session, Response
from flask_login import login_user, current_user, login_required, logout_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlite3 import IntegrityError
#
from models_pack import (
                                dBase, ProductsAndServices, CartItem, IncomeInvoices,
                                Customers, ExpenseInvoices
                                )
from Forms import RegisterForm, LoginForm, CartItemForm, ServiceForm
from admin import Admin
from invoices import make_expense_inv
#
from io import BytesIO


# DATABASE_URL = 'postgresql:// rrkwkroydgayuw : d23bf925b7e627af11e1016930dfbc4768be1db602e05a33f400d5ee9e29d7e9 @ ec2-54-208-11-146.compute-1.amazonaws.com : 5432 / d8f5g71 qofgt98'


def create_app(name_database='DATABASE_K2P'):
    #
    app = Flask(__name__)
    app.name_database = name_database
    app.config['SECRET_KEY'] = '3fe0bb6b1b2e70201wxyzf0f6c31f53b0036499d&'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{name_database}.db'
    return app


app = create_app()
dBase.init_app(app)
#
admin_email = "admin@admin.com"
app.register_blueprint(Admin, url_prefix='/admin')
#
login_manager = LoginManager(app)
login_manager.login_view = 'loginUser'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return Customers.query.get(int(id))


@app.route('/sign-up', methods=["GET", 'POST'])
def sign_up():
    form_register = RegisterForm()
    #
    if form_register.validate_on_submit():
        hash = generate_password_hash(form_register.psw.data)
        new_customer = Customers(email=form_register.email.data, password=hash)
        try:
            dBase.session.add(new_customer)
            dBase.session.commit()
            flash('Успішна реєстрація', category='lucky')
            return redirect(url_for('loginUser'))

        except IntegrityError:
            dBase.session.rollback()
            flash('Помилка під час реєстрації. Можливо, такий користувач вже існує.', category='unlucky')
    elif form_register.is_submitted():
        flash('Під час реєстрації сталася помилка. Перевірте введені дані.', category='unlucky')
    #
    return render_template('sign_up.html', form=form_register, title='Sign Up')


@app.route('/login', methods=['GET', 'POST'])
def loginUser():
    form_login = LoginForm()
    def LoginFunction(object, msg_lucky, msg_un, url):
        if object and not object.authenticated:
            object.authenticated = True
            login_user(object)
            if object != admin_email:
                session['name_product'], session['price_product'] = None, None
                session['name_service'], session['price_service'] = None, None
            flash(msg_lucky, category='lucky')
            dBase.session.commit()
            return redirect(url_for(url))
        else:
            if not object:
                flash('Користувача не знайдено.', category='unlucky')
            else:
                flash(msg_un, category='unlucky')
            return redirect(url_for('loginUser'))
    #
    if form_login.validate_on_submit():
        user = Customers.query.filter_by(email=form_login.email.data).first()
        if form_login.email.data == admin_email and form_login.psw.data == "admin":
          admin = Customers.query.filter_by(email=admin_email).first()
          return LoginFunction(
                                 object=admin, msg_lucky='Ви успiшно увiйшли до панелi адмiнiстратора',
                                 msg_un='Адмiн вже знаходиться в системi', url="admin.show_admin_panel"
        )
        elif user and check_password_hash(user.password, form_login.psw.data):
            return LoginFunction(
                                 object=user, msg_lucky='Ви увійшли в систему.',
                                 msg_un='Користувач вже знаходиться в системi', url="ShopView"
        )
        else:
            flash('Користувача не знайдено.', category='unlucky')
            return redirect(url_for('loginUser'))
    #
    if current_user.is_authenticated:
        if current_user.email == admin_email:
            return redirect(url_for('admin.show_admin_panel'))
        else:
            return redirect(url_for('ShopView'))
    #
    return render_template('login.html', form_login=form_login, title='Login')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        CartItem.query.filter_by(user_id=current_user.id, expense_invoice_id=None).delete()
        current_user.authenticated = False
        dBase.session.commit()
        logout_user()
        flash('Ви вийшли з облікового запису.', category='lucky')
    #
    return redirect(url_for('loginUser'))


@app.route('/')
def StartView():
    # list_url = []
    # for rule in app.url_map.iter_rules():
    #     list_url.append(rule.rule)
    return render_template('start.html')


@app.route('/ceylon-tea-shop', methods=['GET', 'POST'])
@login_required
def ShopView():
    product_form = CartItemForm()
    service_form = ServiceForm()
    basket_items = dBase.session.query(CartItem).filter(CartItem.expense_invoice_id == None).all()
    if basket_items == []:
        session['update_value_qnt'] = {}
    #
    total_price = sum([item.price_item * item.quantity_item for item in basket_items])
    total_price = round(total_price, 2)
    total_quantity = sum([item.quantity_item for item in basket_items])
    #
    return render_template(
                'Shop.html', product_form=product_form, backet_pack=basket_items, total_price=total_price,
                total_quantity=total_quantity, service_form=service_form, user=current_user.email
                )


@app.route('/process_product_form', methods=['POST'])
@login_required
def process_product_form():
    product_form = CartItemForm()
    product_form.price_product.data = session['price_product']
    if 'update_value_qnt' not in session:
        session['update_value_qnt'] = {}
    #
    full_qnt, update_value_qnt = 0, session['update_value_qnt']
    #
    if product_form.validate_on_submit():
        products = dBase.session.query(ProductsAndServices).all()
        for product in products:
            if product.name == product_form.name_product.data:
                full_qnt += product.quantity
        #
        cart_item = CartItem.query.filter_by(
                                             user_id=current_user.id,
                                             name_item=product_form.name_product.data,
                                             expense_invoice_id=None).first()
        if full_qnt >= product_form.quantity_product.data and cart_item is None:
            cart_item = CartItem(
                             user_id=current_user.id, name_item=request.form['name_product'],
                             price_item=product_form.price_product.data,
                             quantity_item=request.form['quantity_product'],
                             expense_invoice_id=None
                             )
            full_qnt -= product_form.quantity_product.data
            session['name_product'] = product_form.name_product.data
            update_value_qnt[session['name_product']] = full_qnt
            dBase.session.add(cart_item)
            flash('Продукт успішно додано в кошик.', category='lucky')
        #
        elif cart_item is not None and \
                    update_value_qnt[product_form.name_product.data] >= product_form.quantity_product.data:
            cart_item.quantity_item += product_form.quantity_product.data
            update_value_qnt[product_form.name_product.data] -= product_form.quantity_product.data
            flash('Продукт успішно додано в кошик.', category='lucky')
        #
        else:
            diff = update_value_qnt[product_form.name_product.data] if cart_item is not None else full_qnt
            flash(f'Продукту немаe на складi. Не вистачае: '
                  f'{product_form.quantity_product.data - diff}', category='unlucky')
        dBase.session.commit()
        session['price_product'], session['name_product'] = None, None
    else:
        if request.form['name_product'] == '-':
            flash('Будь ласка, оберіть товар із списку.', category='unlucky')
        else:
            flash('Будь ласка, оберіть кількість товару.', category='unlucky')
        dBase.session.rollback()
    #
    return redirect(url_for('ShopView'))


@app.route('/process_service_form', methods=['POST'])
@login_required
def process_service_form():
    service_form = ServiceForm()
    service_form.price_service.data = session['price_service']
    #
    basket_items = dBase.session.query(CartItem).filter(CartItem.expense_invoice_id == None).all()
    basket_list = [item.name_item for item in basket_items]
    #
    if service_form.validate_on_submit():
        if request.form['name_service'] not in basket_list:
            service_item = CartItem(
                    user_id=current_user.id,
                    name_item=request.form['name_service'] if request.form['name_service'] != '-' else None,
                    price_item=service_form.price_service.data, quantity_item=1
            )
            #
            dBase.session.add(service_item)
            dBase.session.commit()
            #
            flash('Послуга успішно додано в кошик.', category='lucky')
            session['name_service'], session['price_service'] = None, None
        else:
            flash('Послугу вже додано', category='unlucky')
    #
    elif request.form['name_service'] == '-':
        flash('Будь ласка, оберіть послугу із списку.', category='unlucky')
        dBase.session.rollback()
    return redirect(url_for('ShopView'))


@app.route('/handler_fifo', methods=['GET', 'POST'])
@login_required
def HandlerFIFO():
    answer = request.args.get('name', '')
    basket_items = dBase.session.query(CartItem).filter(CartItem.expense_invoice_id == None).all()
    # Запит для вилучення товарiв, вiдсортованих по датi надкадноi
    products = (dBase.session.query(ProductsAndServices).join(
               IncomeInvoices, ProductsAndServices.invoice_id == IncomeInvoices.id).filter(
               ProductsAndServices.invoice_id != 0).order_by(IncomeInvoices.inc_invoice_date
               ).all())
    basket_list = dict.fromkeys(
                                [item.name_item for item in basket_items],
                                {'availability': 0, 'exclude': False}
    )
    if basket_items:
        for key in basket_list.keys():
            for product in products:
                if key == product.name:
                    basket_list[key]['availability'] += product.quantity  # increase value item
        # Expense Invoices
        exp_invoice = ExpenseInvoices(customer_id=current_user.id)
        dBase.session.add(exp_invoice)
        dBase.session.commit()
        #
        for product in products:
            for item in basket_items:
                item.expense_invoice_id = exp_invoice.id
                if item.name_item == product.name and item.quantity_item != 0 \
                                                  and not basket_list[item.name_item]['exclude']:
                    if item.quantity_item <= product.quantity:
                        product.quantity -= item.quantity_item
                        basket_list[item.name_item]['exclude'] = True
                    #
                    elif item.quantity_item >= product.quantity:
                        item.quantity_item -= product.quantity
                        dBase.session.delete(product)
        #
        dBase.session.commit()
        #
        if answer == 'load':
            buffer = BytesIO()
            make_expense_inv(buffer, exp_invoice.id)
            buffer.seek(0)
            return Response(
                            buffer.read(), mimetype='application/pdf',
                            headers={'Content-Disposition': 'attachment;filename=report.pdf'}
            )
        else:
            return redirect(url_for('ShopView'))
    #
    return redirect(url_for('ShopView'))


@app.route('/get_price')
def GetPriceService():
    product_name = request.args.get('product_name')
    product_request = ProductsAndServices.query.filter_by(name=product_name).first()
    #
    service_name = request.args.get('service_name')
    service_request = ProductsAndServices.query.filter_by(name=service_name).first()
    try:
        if product_request is not None:
            definition_product = str(product_request.definition)
            session['name_product'] = str(product_name)
            session['price_product'] = float(product_request.price)
            return jsonify({
                'price': session['price_product'], 'definition': definition_product})
        #
        if service_request is not None:
            definition_service = str(service_request.definition)
            session['name_service'] = str(service_name)
            session['price_service'] = float(service_request.price)
            return jsonify({'price': session['price_service'], 'definition': definition_service})
        #
        else:
            return jsonify({'error': 'Товар чи послуга не знайденi'})
    #
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/ceylon-tea-shop/delete/<int:product_id>', methods=["POST"])
@login_required
def DelProductService(product_id):
    node = CartItem.query.get(product_id)
    if node and request.method == "POST":
        try:
            update_value_qnt = session.get('update_value_qnt')
            if node.name_item in update_value_qnt:
                del update_value_qnt[node.name_item]
            #
            dBase.session.delete(node)
            dBase.session.commit()
            return jsonify({"message": "Товар успiшно видалено."})
        #
        except Exception as e:
            return jsonify({"error": str(e)})
    return jsonify({"error": "Товар не знайдено або виникла помилка методу запиту."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

