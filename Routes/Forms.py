from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    DateField,
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    IntegerField,
    FloatField,
    TextAreaField,
    validators,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from Routes import db
from Routes.model import User, Department


class RegistrationForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.department.choices = [i.Name for i in Department.query.all()]

    fname = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    department = SelectField("Department", coerce=str, validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    rls = ["User", "Approver"]
    role = SelectField("Role", choices=rls, validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(Email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField("Login")


class LoginValidation(Form):
    user_name_pid = StringField(
        "",
        validators=[DataRequired()],
        render_kw={"autofocus": True, "placeholder": "Enter User"},
    )

    user_pid_Password = PasswordField(
        "",
        validators=[DataRequired()],
        render_kw={"autofocus": True, "placeholder": "Enter your login Password"},
    )


class UpdateAccountForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department.choices = [i.Name for i in Department.query.all()]

    fname = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    department = SelectField("Department", coerce=str, validators=[DataRequired()])
    rls = ["User", "Approver"]
    role = SelectField("Role", choices=rls, validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate_email(self, email):
        user = User.query.filter_by(Email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class DepartmentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    dept_code = StringField("Dept Code", validators=[DataRequired()])
    submit = SubmitField("Submit")


class POForm(FlaskForm):
    PO_number = IntegerField("PO Number", validators=[DataRequired()])
    dept_code = StringField(
        "Dept Code", render_kw={"readonly": True}, validators=[DataRequired()]
    )
    department = StringField(
        "Department", render_kw={"readonly": True}, validators=[DataRequired()]
    )
    description = TextAreaField("Brief Description", validators=[DataRequired()])
    vendor = StringField("Vendor", validators=[DataRequired()])
    vendor_address = StringField("Vendor Address")
    vendor_city = StringField("Vendor City")
    vendor_state = StringField("Vendor State")
    vendor_zip = StringField("Vendor Zip Code")
    vendor_phone = StringField("Vender Phone Number")
    order_date = DateField("Order Date", validators=[DataRequired()])
    recieved_date = DateField("Recieved Date")
    total = FloatField("Order Total", validators=[DataRequired()])
    requester = StringField(
        "Requester", render_kw={"readonly": True}, validators=[DataRequired()]
    )
    approval = SelectField(
        "Approved?", choices=["Pending", "No", "Yes"], render_kw={"readonly": True}
    )
    approver = StringField("Approver", validators=[DataRequired()])
    submit = SubmitField("Submit")


class POItemForm(FlaskForm):
    id = IntegerField(
        "PO Number", render_kw={"readonly": True}, validators=[DataRequired()]
    )
    product_name = StringField(
        "Product Name",
        render_kw={"placeholder": "Product Name"},
        validators=[DataRequired()],
    )
    quantity = IntegerField(
        "Quantity", render_kw={"placeholder": "Quantity"}, validators=[DataRequired()]
    )
    price = FloatField(
        "Price", render_kw={"placeholder": "Price"}, validators=[DataRequired()]
    )


class ApprovalForm(FlaskForm):
    Notes = TextAreaField("Notes")
