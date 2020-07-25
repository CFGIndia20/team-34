from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class students(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    dob = db.Column(db.String(10))
    aadhar_no = db.Column(db.Integer)
    address = db.Column(db.String(100))
    entrance_score = db.Column(db.Integer)
    is_enrolled = db.Column(db.Integer)
    slot_preference_1 = db.Column(db.Integer)
    slot_preference_2 = db.Column(db.Integer)
    slot_preference_3 = db.Column(db.Integer)
    slot_preference_4 = db.Column(db.Integer)
    batch_id = db.Column(db.String(20))


    def __init__(self, name, email, password, dob, aadhar_no, address, entrance_score, is_enrolled, slot_preference_1, slot_preference_2, slot_preference_3, slot_preference_4, batch_id):
        self.name = name
        self.email = email
        self.password = password
        self.dob = dob
        self.aadhar_no = aadhar_no
        self.entrance_score = entrance_score
        self.address = address
        self.is_enrolled = is_enrolled
        self.slot_preference_1 = slot_preference_1
        self.slot_preference_2 = slot_preference_2
        self.slot_preference_3 = slot_preference_3
        self.slot_preference_4 = slot_preference_4
        self.batch_id = batch_id

