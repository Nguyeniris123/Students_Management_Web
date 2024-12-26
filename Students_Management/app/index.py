import math
from flask import render_template, request
import dao
<<<<<<< Updated upstream
from __init__ import app
=======
from app import app, login, db
from flask_login import login_user, logout_user, current_user
from app.dao import get_user_by_id
from app.models import UserRole

>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
@app.route("/login")
=======
# @app.route("/send_email/<email>", methods=['get'])
# def send_email(email):
#     password = request.json.get('password')
#     if current_user.is_authenticated:
#         msg_title = "Cập nhật mật khẩu"
#         sender = "noreply@app.com"
#         msg = Message(msg_title, sender=sender, recipients=[email])
#         msg_body = "Bạn đã đặt lại mật khẩu là"
#         data = {
#             'title': msg_title,
#             'body': msg_body,
#             'user_name': current_user.username,
#             'password': password
#         }
#         msg.html = render_template("email.html", data=data)
#
#         try:
#             mail.send(msg)
#             return jsonify({
#                 "title": "Email sent...."
#             })
#         except Exception as e:
#             print(e)
#             return jsonify({
#                 "title": "The Email was not sent"
#             })


@app.route("/lookuppoints", methods=['get'])
def lookuppoints():
    ms = ""
    aleart = ""
    years = dao.load_year()
    semesters = dao.load_semester(1)
    year = request.args.get('year')
    semester = request.args.get('semester')
    subject_score = {}
    subjects = []
    score_types = []
    average_subject = {}
    if current_user.is_authenticated:
        if year is None and semester is None:
            ms = "Chưa chọn dữ liệu"
            aleart = "warning"
        elif (current_user.user_role.__eq__(UserRole.USER)):
            class_grade_id = dao.get_classgrade_id(current_user.id)
            subjects = dao.load_subject(semester_id=int(semester), class_grade_id=class_grade_id)
            for sub in subjects:
                print(sub.name)
            score_types = dao.load_score_type()
            if subjects and score_types:
                ms = "Đã tải dữ liệu hoàn tất"
                aleart = "success"
                for subject in subjects:
                    dao_result = dao.get_average_score(subject_id=subject.id, student_id=current_user.id)
                    average_subject[subject.id] = round(dao_result, 1)
                    if subject.id not in subject_score:
                        # Nếu chưa có subject.id thì tạo một mục mới cho môn học này
                        subject_score[subject.id] = {}
                    for score in score_types:
                        subject_score[subject.id][score.id] = []

                        score_datas = dao.load_score(
                            student_id=current_user.id,
                            score_type_id=score.id,
                            subject_id=subject.id
                        )

                        # score_values=[]

                        # for score_data in score_datas:
                        #     score_values.append(score_data.so_diem)

                        # Kiểm tra nếu có dữ liệu trả về từ dao.load_score
                        if score_datas:
                            subject_score[subject.id][score.id] = score_datas
                        else:
                            print(f"No score data for Subject ID: {subject.id}, Score ID: {score.name}")
                        # for s in subject_score[subject.id][score.id]:
                        #     print(s.so_diem)
                    # print(subject_score[subject.id])
            else:
                ms = "Không có dữ liệu"
                aleart = "delete"

    return render_template('lookinguppoint.html', aleart=aleart, message=ms, years=years, subjects=subjects,
                           subject_score=subject_score, score_types=score_types, semesters=semesters,
                           average_subject=average_subject)


@app.route('/lookuppoints/year/<int:year_id>', methods=['get'])
def year_process(year_id):
    semesters = dao.load_semester(year_id)
    return jsonify({
        "semesters_id": [semester.id for semester in semesters],
        "semesters_name": [f"{semester.name}" for semester in semesters]
    })


@app.route("/regulationtostudent", methods=['get'])
def regulation():
    regulations = dao.load_regulation()
    return render_template('regulation_student.html', regulations=regulations)


@app.route('/regulationtostudent/<int:regulation_id>', methods=['get'])
def regulation_process(regulation_id):
    regulation = dao.load_regulation(regulation_id)
    regulation_detail = dao.load_detail_regulation(regulation_id)
    return jsonify({
        "name": regulation.name,
        "id": regulation.id,
        "max_students": getattr(regulation_detail, 'max_students', None),
        "min_age": getattr(regulation_detail, 'min_age', None),
        "max_age": getattr(regulation_detail, 'max_age', None),
    })


@app.route("/changeinfo", methods=['get', 'post'])
def changeinfo():
    msg = ""
    alert = ""
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    currentPassword = request.form.get('currentPassword')
    newPassword = request.form.get('newPassword')
    confirmPassword = request.form.get('confirmPassword')
    avatar = request.files.get('avatar')
    print(avatar)
    if current_user.is_authenticated:
        if current_user.user_role.__eq__(UserRole.USER):
            if email or phone or address or avatar:
                if dao.change_information(current_user.id, email, phone, address, avatar):
                    msg = "Thông tin đã được cập nhật"
                    alert = "success"
            else:
                msg = "Không có thông tin để cập nhật"
                alert = "warning"
            if currentPassword and confirmPassword and newPassword:
                if dao.check_password(newPassword, confirmPassword):
                    if dao.change_password(current_user.id, currentPassword, newPassword):
                        msg = "Cập nhật mật khẩu thành công"
                        alert = "success"
                        # mesg_title = "Cập nhật mật khẩu"
                        # sender = "noreply@app.com"
                        # message = Message(mesg_title, sender=sender, recipients=[current_user.email])
                        # mesg_body = "Bạn đã đặt lại mật khẩu là"
                        # data = {
                        #     'title': mesg_title,
                        #     'body': mesg_body,
                        #     'user_name': current_user.name,
                        #     'password': newPassword
                        # }
                        # message.html = render_template("email.html", data=data)
                        # try:
                        #     mail.send(message)
                        #     msg = "Cập nhật mật khẩu thành công"
                        #     alert = "success"
                        # except Exception as e:
                        #     print(e)
                        #     msg = "Lỗi không gửi được email"
                        #     alert = "delete"
                    else:
                        msg = "Lỗi không cập nhật được mật khẩu"
                        alert = "delete"
                else:
                    msg = "Mật khẩu không khớp"
                    alert = "delete"
    return render_template('changeinfo_student.html', msg=msg, alert=alert)

@app.route("/login", methods=['get', 'post'])
>>>>>>> Stashed changes
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
