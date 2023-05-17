from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (current_user, login_required, login_user, logout_user)
from Routes.model import Department, User, POEntry, POItem
from Routes import app, db, bcrypt
from Routes.Forms import RegistrationForm, LoginForm, DepartmentForm, POForm, POItemForm
from datetime import date


@app.route('/TrackingSheet/<dpt>', methods=['GET', 'POST'])
def trackingSheet(dpt):
    form = POForm()
    ItemForm =  POItemForm()
    user_dept = current_user.Department
    user_dept_class = Department.query.filter_by(Name=user_dept).first()
    form.requester.data = current_user.Name
    form.department.data = user_dept_class.Name
    form.dept_code.data = user_dept_class.Dept_Code
    # form.po_number.data = POEntry.query.order_by(POEntry.PO_Number.desc()).first() + 1
    form.PO_number.data = '1647'
    form.order_date.data = f"{date.today()}"
    if request.method == 'POST':
        po_number = 1655
        entry = POEntry(
            PO_Number = form.PO_number.data,
            Dept_Code = form.dept_code.data,
            Department = form.department.data,
            Description = form.description.data,
            Vendor = form.vendor.data,
            Vendor_Address = form.vendor_address.data,
            Vendor_City = form.vendor_city.data,
            Vendor_State = form.vendor_state.data,
            Vendor_Zip = form.vendor_zip.data,
            Vendor_Phone = form.vendor_phone.data,
            Order_Date = form.order_date.data,
            Recieved_Date = form.recieved_date.data,
            Total = form.total.data,
            Requester = form.requester.data,
            Approver = form.approver.data,
            Status = "Pending"
        )
        db.session.add(entry)
        db.session.commit()
        items = []
        item_count = int(request.form['item_count'])
        for i in range(1, item_count+1):
            item = POItem(
                PO_Number = form.PO_number.data,
                Product_Name = request.form[f'product_name_{i}'],
                Quantity = int(request.form[f'quantity_{i}']),
                Price = float(request.form[f'price_{i}'])
            )
            items.append(item)
            
        db.session.add_all(items)
        db.session.commit()
        return redirect(url_for('Tracking/trackingSheet', dpt=dpt))        
    entries = POEntry.query.filter_by(Department=dpt)
    return render_template("Tracking/trackingSheet.html", entries=entries, form=form, itemform=ItemForm, date=date)