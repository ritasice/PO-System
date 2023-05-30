from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from Routes.model import Approval, Department, User, POEntry, POItem
from Routes import app, db
from Routes.Forms import POForm, POItemForm, ApprovalForm
from datetime import date
from werkzeug.exceptions import BadRequestKeyError


@app.route("/TrackingSheet/<dpt>", methods=["GET", "POST"])
@login_required
def trackingSheet(dpt):
    form = POForm()
    ItemForm = POItemForm()
    # user_dept = current_user.Department
    user_dept_class = Department.query.filter_by(Name=dpt).first()
    # form.requester.data = current_user.Name
    form.department.data = user_dept_class.Name
    form.dept_code.data = user_dept_class.Dept_Code
    POEntry.query.order_by("id").all()[-1]
    # form.order_date.data = f"{date.today()}"
    if request.method == "POST":
        entry = POEntry(
            PO_Number=form.PO_number.data,
            Dept_Code=form.dept_code.data,
            Department=form.department.data,
            Description=form.description.data,
            Vendor=form.vendor.data,
            Vendor_Address=form.vendor_address.data,
            Vendor_City=form.vendor_city.data,
            Vendor_State=form.vendor_state.data,
            Vendor_Zip=form.vendor_zip.data,
            Vendor_Phone=form.vendor_phone.data,
            Order_Date=form.order_date.data,
            Recieved_Date=form.recieved_date.data,
            Total=form.total.data,
            Requester=form.requester.data,
            Approver=form.approver.data,
            Approval_Status="Approved",
        )
        db.session.add(entry)
        db.session.commit()

        curEntry = POEntry.query.filter_by(PO_Number=entry.PO_Number).first()

        items = []
        item_count = int(request.form["item_count"])
        for i in range(1, item_count + 1):
            try:
                item = POItem(
                    PO_id=curEntry.id,
                    Product_Name=request.form[f"product_name_{i}"],
                    Quantity=int(request.form[f"quantity_{i}"]),
                    Price=float(request.form[f"price_{i}"]),
                )
                items.append(item)
            except BadRequestKeyError:
                break
        db.session.add_all(items)
        db.session.commit()

        # send_approval_request(last_PO.id + 1)

        return redirect(url_for("trackingSheet", dpt=dpt))
    entries = POEntry.query.filter_by(Department=dpt)
    return render_template(
        "Tracking/trackingSheet.html",
        entries=entries,
        form=form,
        itemform=ItemForm,
        date=date,
        dpt=dpt,
    )


def send_approval_request(po_id):
    recp = User.query.filter_by(id=current_user.ReportsTo).first()
    appr = Approval(
        PO_id=po_id,
        Requester=current_user.Name,
        Approver=recp,
        DateRequested=date.today(),
        Status="Pending",
    )

    db.session.add(appr)
    db.session.commit()

    # url = "http://10.0.1.32:5000/Approval/IT/po_id"
    # sb = "PO Approval"
    # msg = f"Please approve the following PO, located at {url}"

    # os.system(f'echo "{msg}" | mail -s "{sb}" {current_user.Email}')
    # os.system(f'echo "{msg}" | mail -s "{sb}" {recp})

    print(po_id)


@app.route("/TrackingSheet/<dpt>/Approval/<PO>")
@login_required
def approvalStatus(dpt, PO):
    appr = Approval.query.filter_by(PO_id=PO).first()
    entry = POEntry.query.get_or_404(PO)
    items = POItem.query.filter_by(PO_id=PO).all()
    form = ApprovalForm()
    return render_template(
        "Tracking/approval.html",
        dpt=dpt,
        appr=appr,
        form=form,
        entry=entry,
        items=items,
    )


@app.route("/Approval/<dpt>/<PO>")
def approval(dpt, PO):
    appr = Approval.query.filter_by(PO_id=PO).first()
    return render_template("Approvalform.html", appr=appr)
