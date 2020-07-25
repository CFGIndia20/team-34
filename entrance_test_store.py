from flask import Flask, render_template, url_for, redirect, request, session, flash
from db import students, db


def validate():
    if "email" in session:
        return True
    else:
        return False


def upload_entrance_test_data(name, email, password, dob, aadhar_no, address, entrance_score, is_enrolled,
                              slot_preference_1, slot_preference_2, slot_preference_3, slot_preference_4, batch_id):
    student = students(name= name, email= email, password= password, dob= dob, aadhar_no= aadhar_no, address= address, entrance_score= entrance_score, is_enrolled= is_enrolled, slot_preference_1= slot_preference_1, slot_preference_2= slot_preference_2, slot_preference_3= slot_preference_3, slot_preference_4= slot_preference_4, batch_id= batch_id)
    db.session.add(student)
    db.session.commit()
