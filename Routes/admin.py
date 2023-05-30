from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (current_user, login_required, login_user, logout_user)
from Routes.model import Department, User
from Routes import app, db, bcrypt
from Routes.Forms import RegistrationForm, LoginForm, DepartmentForm, LoginValidation
from Routes.global_ldap_authentication import *
import os

@app.route('/admin')
def adminIndex():
    users = User.query.all()
    return render_template('Shared/admin.html', Users=users)

@app.route('/adduser')
def addUser():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
                Name = form.name.data,
                Email = form.email.data,
                Department = form.department.data
                )
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('adminIndex'))
