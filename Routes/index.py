from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (current_user, login_required, login_user, logout_user)
from Routes.model import Department, User
from Routes import app, db, bcrypt
from Routes.Forms import RegistrationForm, LoginForm, DepartmentForm, LoginValidation
from Routes.global_ldap_authentication import *
import os

@app.route("/Index", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    form = DepartmentForm()
    if request.method == 'POST':
        department = Department(
            Name = form.name.data,
            Dept_Code = form.dept_code.data
        )
        db.session.add(department)
        db.session.commit()
        flash('Department has been created', 'green')
        return redirect(url_for("index"))
    departments = Department.query.order_by('Name').all()
    
    return render_template("Shared/index.html", departments=departments, form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        user = User.query.filter_by(Email=email).first()
        login_id = user.Name
        dpt = user.Department
        login_password = form.password.data
        root_dn = f"OU={dpt},OU=Headquarters Users,OU=Headquarters,DC=coolsupport,DC=rita"
        # create a directory to hold the Logs
        login_msg = global_ldap_authentication(login_id, login_password, root_dn)
        # validate the connection
        if login_msg == "Success":
            success_message = f"*** Authentication Success "
            print(success_message)
            login_user(user)
            app.logger.info(f"{email} logged in succesfully")
            return redirect(url_for('index'))

        else:
            error_message = f"*** Authentication Failed - {login_msg}"
            print(error_message)
            return render_template("Shared/login.html", error_message=str(error_message), form=form)

    return render_template('Shared/login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            FirstName=form.fname.data,
            LastName=form.lname.data,
            Email=form.email.data,
            Department = form.department.data,
            HashPass = hashed_password,
            roles = form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login', 'green')
        return redirect(url_for("login"))
    return render_template("Shared/register.html", title = "Register", form=form)
