import sys
from Routes import app, db
sys.path.append("/home/dpatel/PO-System/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
