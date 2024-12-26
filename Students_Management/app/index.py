from flask import flash, render_template, request, redirect, jsonify
from app import dao
from app import app, login, mail
from flask_login import login_user, logout_user, current_user
from app.models import UserRole
from flask_mail import Message


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/lookuppoints", methods=['get'])
def lookuppoints():
    ms = ""
    aleart=""
    years = dao.load_year()
    semesters = dao.load_semester(1)
    year = request.args.get('year')
    semester = request.args.get('semester')
    subject_score = {}
    subjects = []
    score_types = []
    average_subject = {}
    if current_user.is_authenticated:
        if (current_user.user_role.__eq__(UserRole.USER)):
            if semester:
                class_grade_id = dao.get_classgrade_id(current_user.id)
                subjects = dao.load_subject(semester_id=int(semester), class_grade_id=class_grade_id)
                score_types = dao.load_score_type()
                if subjects and score_types:
                    ms = "Đã tải dữ liệu hoàn tất"
                    aleart = "success"
                    for subject in subjects:
                        dao_result = dao.get_average_score(subject_id=subject.id, student_id=current_user.id)
                        average_subject[subject.id] = round(dao_result, 1) if dao_result else 0
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
                    aleart = "danger"
        else:
            ms = "Không phải học sinh nên không có dữ liệu" 
            aleart = "warning"     
                
    return render_template('lookinguppoint.html', aleart = aleart, message=ms, years=years, subjects=subjects, subject_score=subject_score, score_types=score_types, semesters=semesters, average_subject=average_subject)


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
    if current_user.is_authenticated:
        if current_user.user_role.__eq__(UserRole.USER):
            if email or phone or address or avatar:
                if dao.change_information(current_user.id, email, phone, address, avatar):
                    msg = "Thông tin đã được cập nhật"
                    alert = "success"
            if currentPassword and confirmPassword and newPassword:
                if dao.check_password(newPassword, confirmPassword):
                    if dao.change_password(current_user.id, currentPassword, newPassword):
                        mesg_title = "Cập nhật mật khẩu"
                        sender = "noreply@app.com"
                        message = Message(mesg_title,sender=sender, recipients=[current_user.email])
                        mesg_body = "Bạn đã đặt lại mật khẩu là"
                        data = {
                            'title': mesg_title,
                            'body': mesg_body,
                            'user_name': current_user.name,
                            'password': newPassword
                        }
                        message.html = render_template("email.html", data=data)
                        try:
                            mail.send(message)
                            msg = "Cập nhật mật khẩu thành công"
                            alert = "success"
                        except Exception as e:
                            print(e)
                            msg = "Lỗi không gửi được email"
                            alert = "danger"
                    else:
                        msg = "Lỗi không cập nhật được mật khẩu"
                        alert = "danger"
                else:
                    msg = "Mật khẩu không khớp"
                    alert = "danger"

    return render_template('changeinfo_student.html', msg=msg, alert=alert)


@app.route("/login", methods=['get', 'post'])
def login_process():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        u = dao.auth_user(username=username, password=password)
        if u:
            login_user(u)
            return redirect('/')  # dieu huong ve trang chu
    return render_template('login.html')


@app.route("/login-admin", methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    if u:
        # Đăng nhập người dùng nếu mật khẩu đúng
        login_user(u)
    else:
        # Nếu thông tin đăng nhập sai, hiển thị thông báo lỗi
        flash("Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin đăng nhập.", "danger")
    return redirect('/admin')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/login')

if __name__ == '__main__':
    from app import admin  # chạy trang admin flask
    app.run(debug=True, port=5001)  # Thay port mặc định (5000) thành 5001
