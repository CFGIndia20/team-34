from flask import Flask, render_template, url_for, redirect, request, session, flash
from db import students, db


def upload_user_data(name, email, password, dob, aadhar_no, address, entrance_score, is_enrolled,
                              slot_preference_1, slot_preference_2, slot_preference_3, slot_preference_4, batch_id):
    student = students(name= name, email= email, password= password, dob= dob, aadhar_no= aadhar_no, address= address, entrance_score= entrance_score, is_enrolled= is_enrolled, slot_preference_1= slot_preference_1, slot_preference_2= slot_preference_2, slot_preference_3= slot_preference_3, slot_preference_4= slot_preference_4, batch_id= batch_id)
    db.session.add(student)
    db.session.commit()


def upload_entrance_test_data(total):
    if "email" in session:
        email = session.email
        student = students.query.filter_by(email=email).first()
        student.entrance_score = total
        db.session.commit()
    else:
        return "Please Login First"

def upload_slot_data(slot1, slot2, slot3, slot4):
    if "email" in session:
        email = session.email
        student = students.query.filter_by(email=email).first()
        student.slot_preference_1 = slot1
        student.slot_preference_2 = slot2
        student.slot_preference_3 = slot3
        student.slot_preference_4 = slot4
    else:
        return "Please Login First"

