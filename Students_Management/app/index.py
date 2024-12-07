import math
from flask import render_template, request
import dao
from __init__ import app

@app.route("/")
def index():
    dao.classify_class()
    # cates = dao.load_categories()
    # cate_id = request.args.get('category_id')
    # kw = request.args.get('kw')
    page = request.args.get('page', 1)
    page_size = app.config.get('PAGE_SIZE', 8)
    # return render_template('index.html', categories=cates, pages=page_size)
    return render_template('index.html', pages=page_size)

@app.route("/login")
def login_process():
    return render_template('login.html')

@app.route("/register")
def register_process():
    return render_template('register.html')

@app.route("/tiepnhanhocsinh", methods=['GET', 'POST'])
def tiepnhanhocsinh_process():
    send_message = ''
    alert = ''
    if request.method.__eq__('POST'):
       student = None
       phone = request.form.get('phone')
       email = request.form.get('email')
       firstname = request.form.get('firstname')
       lastname = request.form.get('lastname')
       dayofbirth = request.form.get('dayofbirth')
       gender = request.form.get('gender')
       address = request.form.get('address')
       if dao.check_student(phone, email).__eq__(True):
           dao.update_user(lastname=lastname, firstname=firstname, phone=phone, email=email, gender=gender, dayofbirth=dayofbirth, address=address)
           send_message = "Update Successfull"
           alert = "primary"
       else:
           if dao.check_student_phone(phone) | dao.check_student_email(email):
               send_message = "User Exist"
               alert = "warning"
           else:
                dao.add_student(phone=phone, email=email, firstname=firstname, lastname=lastname, 
                                dayofbirth=dayofbirth, gender=gender, address=address)
                send_message = "Add Successfull"
                alert = "success"

       students = dao.load_user_student() if dao.load_user_student() else None
    else:
        kw = request.args.get('kw')
        student_id_by_table = request.args.get('student_id')
        student = dao.find_user_by_id(student_id_by_table)
        student_id_del = request.args.get('delete_student')
        if dao.del_student(student_id_del).__eq__(True):
            send_message = "Delete successfull"
            alert = "success"
        students = dao.load_user_student(kw = kw) if dao.load_user_student(kw = kw) else None
        
    return render_template('tiepnhanhocsinh.html', send_message=send_message, student_list=students, student=student, alert=alert)

@app.route("/dieuchinhlop")
def dieuchinhlop_process():
    return render_template('dieuchinhlop.html')

@app.route("/tracuuhocsinh")
def tracuuhocsinh_process():
    return render_template('tracuuhocsinh.html')

@app.route("/quanlymonhoc")
def qlmonhoc_process():
    return render_template('quanlymonhoc.html')

@app.route("/quanlydiem")
def qldiem_process():
    return render_template('quanlydiem.html')

@app.route("/quydinh")
def quydinh_process():
    return render_template('quydinh.html')

@app.route("/tongket")
def tongket_process():
    return render_template('tongket.html')

if __name__ == '__main__':
    app.run(debug=True)
