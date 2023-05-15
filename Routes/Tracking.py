from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (current_user, login_required, login_user, logout_user)
from Routes.model import Department, User, POEntry, POItem
from Routes import app, db, bcrypt
from Routes.Forms import RegistrationForm, LoginForm, DepartmentForm, POForm

@app.route('/TrackingSheet/<dpt>', methods=['GET', 'POST'])
def trackingSheet(dpt):
    form = POForm()
    user_dept = current_user.Department
    user_dept_class = Department.query.filter_by(Name=user_dept).first()
    form.department.data = user_dept_class.Name
    form.dept_code = user_dept_class.Dept_Code
    form.requester = f"{current_user.FirstName} {current_user.LastName}"
    if request.method == 'POST':
        entry = POEntry(
            PO_Number = form.PO_number.data,
            Dept_Code = form.dept_code.data,
            Department = form.department.data,
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
            Approver = form.approver.data
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for(trackingSheet))        
    entries = POEntry.query.filter_by(Department=dpt)
    return render_template("trackingSheet.html", entries=entries, form=form)