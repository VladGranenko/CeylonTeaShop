import os
from flask import Blueprint, flash, redirect, render_template, url_for, request, Response
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
#
from Forms import ChangeNodeForm, GenerateReportForm
from models_pack import dBase, ProductsAndServices
from invoices import handler_income_inv, make_invoice, make_report_range, check_nodes_range
#
from io import BytesIO


Admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@Admin.route('/admin-panel', methods=["GET", "POST"])
@login_required
def show_admin_panel():
    gnt_form = GenerateReportForm()
    products = dBase.session.query(ProductsAndServices).order_by(ProductsAndServices.is_product).all()

    return render_template(
              'admin.html',  products=products, title="Admin-Panel", gnt_form=gnt_form
    )


@Admin.route('/generate_report', methods=["GET", "POST"])
@login_required
def generate_report():
    gnt_form = GenerateReportForm()
    start = gnt_form.start_date.data
    finish = gnt_form.finish_date.data
    if start and finish and start < finish:
        if check_nodes_range(start_point=start, finish_point=finish):
            excel_buffer = BytesIO()
            make_report_range(start_date=start, finish_date=finish, buffer=excel_buffer)
            excel_buffer.seek(0)
            return Response(
                             excel_buffer.read(),
                             mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={'Content-Disposition': 'attachment;filename=report.xlsx'}
                            )
        else:
            flash('У вибраному дiапазонi записи вiдсутнi', category="unlucky")
    else:
        flash('Кiнцева дата повинна опереджувати початкову', category="unlucky")
    #
    return redirect(url_for('admin.show_admin_panel'))


@Admin.route('/load-excel', methods=["GET", "POST"])
@login_required
def load_excel():
    excel_file = request.files['excel-file']
    if excel_file.filename.endswith('.xlsx') or excel_file.filename.endswith('.xls'):
        upload_folder = 'excel_invoices'
        file_path = os.path.join(upload_folder, 'excel_file.xlsx')
        excel_file.save(file_path)
        try:
            if make_invoice(excel_file):
                dBase.session.bulk_insert_mappings(ProductsAndServices, handler_income_inv(excel_file))
                dBase.session.commit()
                os.remove(file_path)
                #
                flash("Данi успiшно доданi", category="lucky")
                return redirect(url_for('admin.show_admin_panel'))
            else:
                flash("Файл не вiдповiдае вимогам внесення записiв ", category="unlucky")
        except IntegrityError:
            flash("Необхiдно заповнити усi данi.", category="unlucky")
            return redirect(url_for('admin.show_admin_panel'))
    else:
        flash("Формат файлу мае бути у форматi .xlsx або .xls", category="unlucky")
    return redirect(url_for('admin.show_admin_panel'))


@Admin.route('/admin-panel/delete/<int:product_id>', methods=["GET", "POST"])
@login_required
def delete_nodes(product_id):
    node = ProductsAndServices.query.get(product_id)
    id_object = node.id
    name_object = node.name
    if node and request.method == "POST":
        dBase.session.delete(node)
        dBase.session.commit()
        #
        flash(f"Запис {id_object} успiшно видалено", category="lucky")
        return redirect(url_for('admin.show_admin_panel'))
    #
    return render_template(
                           'delete_nodes.html', title="Delete nodes", id_object=id_object,
                           name_object=name_object
    )


@Admin.route('/admin-panel/change/<int:product_id>', methods=["GET", "POST"])
@Admin.route('/admin-panel/add_node', methods=["GET", "POST"])
@login_required
def action_nodes(product_id=None):
    node = ProductsAndServices.query.get(product_id) if product_id is not None else None
    id_object = node.id if node is not None else None
    if node:
        title, button = f"Редагувати запис з id: {product_id}", "Змiнити"
        form = ChangeNodeForm(obj=node)
    else:
        title, button = "Додати новий товар", "Створити"
        form = ChangeNodeForm()
    #
    if form.validate_on_submit():
        if node is None:
            new_node = ProductsAndServices(
                                            name=form.name.data,
                                            price=form.price.data,
                                            quantity=form.quantity.data,
                                            supplier=form.supplier.data,
                                            is_product=form.is_product.data,
                                            definition=form.definition.data
            )
            dBase.session.add(new_node)
        else:
            form.populate_obj(node)
        #
        dBase.session.commit()
        flash('Запис успiшно оновлено', category='lucky')
        return redirect(url_for('admin.show_admin_panel'))
    #
    if request.method == 'POST' and not form.validate_on_submit():
        flash('Будь ласка, виправте помилки у формі.', category='unlucky')
    #
    return render_template(
                         'action_nodes.html', form=form, id_object=id_object, title=title, button_form=button
    )

