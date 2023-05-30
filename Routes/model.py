from Routes import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Department(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    Name = db.Column(db.String(60), nullable=False)
    Dept_Code = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"{self.Dept_Code}, {self.Name}"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(60), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Department = db.Column(db.String(60), nullable=False)
    roles = db.Column(db.String(50))
    LastLogin = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.email}')"


User.ReportsToID = db.Column(db.Integer, db.ForeignKey(User.id))
User.ReportsTo = db.relationship("User", backref="subordinates", remote_side=User.id)


class POEntry(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    PO_Number = db.Column(db.Integer)
    Dept_Code = db.Column(db.String(60), nullable=False)
    Department = db.Column(db.String(60), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Vendor = db.Column(db.String(60), nullable=False)
    Vendor_Address = db.Column(db.String(60))
    Vendor_City = db.Column(db.String(60))
    Vendor_State = db.Column(db.String(60))
    Vendor_Zip = db.Column(db.String(60))
    Vendor_Phone = db.Column(db.String(60))
    Order_Date = db.Column(db.Date, nullable=False)
    Recieved_Date = db.Column(db.Date)
    Total = db.Column(db.Float)
    Requester = db.Column(db.String(60), nullable=False)
    Approver = db.Column(db.String(60))
    Approval_Status = db.Column(db.String, nullable=False)
    Hidden = db.Column(db.Boolean)
    PO_Status = db.Column(db.String(60))
    POItem = db.relationship("POItem", backref="POEntry", lazy=True)
    Approval = db.relationship("Approval", backref="POEntry", lazy=True)

    def __repr__(self):
        return f"POEntry('{self.PO_Number}', '{self.Department}', '{self.Approval_Status}', {self.Hidden}, {self.PO_Status})"


class POItem(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    PO_id = db.Column(db.Integer, db.ForeignKey("po_entry.id"), nullable=False)
    Product_Name = db.Column(db.String(60), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Float, nullable=False)


class Approval(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    PO_id = db.Column(db.Integer, db.ForeignKey("po_entry.id"), nullable=False)
    Requester = db.Column(db.String(60), nullable=False)
    Approver = db.Column(db.String(60))
    DateRequested = db.Column(db.DateTime, nullable=False)
    DateApproved = db.Column(db.DateTime)
    Status = db.Column(db.String(60), nullable=False)
    Notes = db.Column(db.Text)
