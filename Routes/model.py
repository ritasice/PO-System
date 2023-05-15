from Routes import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Department(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    Name = db.Column(db.String(60), nullable=False)
    Dept_Code = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return(f"{self.Dept_Code}, {self.Name}")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(60), nullable=False)
    LastName = db.Column(db.String(60), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    HashPass = db.Column(db.String(60), nullable=False)
    Department = db.Column(db.String(60), nullable=False)
    roles = db.Column(db.String(50))
    
    def __repr__(self):
        return f"User('{self.email}')"

class POEntry(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    PO_Number = db.Column(db.Integer, unique=True)
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
    Status = db.Column(db.String, nullable=False)
    POItem = db.relationship('POItem', backref='POEntry', lazy=True)
    Approval = db.relationship('Approval', backref='Approval', lazy=True)

    def __repr__(self):
        return f"POEntry('{self.PO_Number}', '{self.Department}', '{self.Total}')"

class POItem(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    PO_Number = db.Column(db.Integer, db.ForeignKey('po_entry.PO_Number'), nullable=False)
    Product_Name = db.Column(db.String(60), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Float, nullable=False)

class Approval(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    PO_Number = db.Column(db.Integer, db.ForeignKey('po_entry.PO_Number'), nullable=False)
    Requester = db.Column(db.String(60), nullable=False)
    Approver = db.Column(db.String(60))
    DateRequested = db.Column(db.DateTime, nullable=False)
    Status = db.Column(db.String(60), nullable=False)
    Notes = db.Column(db.Text)
