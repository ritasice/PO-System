from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (current_user, login_required, login_user, logout_user)
from Routes.model import Department, User
from Routes import app, db, bcrypt
from Routes.Forms import RegistrationForm, LoginForm, DepartmentForm

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
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.HashPass, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Login Unsuccessful. Please check email and password", "red")
    return render_template("Shared/login.html", title="Login", form=form)

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
