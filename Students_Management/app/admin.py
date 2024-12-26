from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from sqlalchemy import Date

from app.models import (Class, Student, User, UserRole, Semester, Subject,
                        Score, ScoreType, ClassGrade, Year, RegulationMaxStudent, RegulationAge, Schedule, LoaiDiem,
                        Gender, ClassRoom)
from app.dao import get_students_by_class, get_scores_by_subject, add_score, edit_score, delete_score, \
    get_all_students_average_score, get_students_by_kw, add_student, delete_student, change_student_class, \
    add_student_to_class
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, request, jsonify, make_response
from reportlab.pdfgen import canvas


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name='Quản trị hệ thống', template_mode='bootstrap4', index_view=MyAdminIndexView())


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedAdminView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedTeacherView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and (
                current_user.user_role == UserRole.ADMIN or current_user.user_role == UserRole.GIAOVIEN)


class AuthenticatedStaffView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and (
                current_user.user_role == UserRole.ADMIN or current_user.user_role == UserRole.NHANVIEN)


class AdminView(ModelView):
    def is_accessible(self):
        # Chỉ admin mới có quyền truy cập
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class GiaoVienView(ModelView):
    def is_accessible(self):
        # Chỉ giáo viên mới có quyền truy cập
        return current_user.is_authenticated and current_user.user_role == UserRole.GIAOVIEN


class NhanVienView(ModelView):
    def is_accessible(self):
        # Chỉ nhân viên mới có quyền truy cập
        return current_user.is_authenticated and current_user.user_role == UserRole.NHANVIEN


class NhanVienAdminView(ModelView):
    def is_accessible(self):
        # Cho phép truy cập nếu user là nhân viên hoặc admin
        return current_user.is_authenticated and (
                current_user.user_role == UserRole.ADMIN or current_user.user_role == UserRole.NHANVIEN)


class GiaoVienAdminView(ModelView):
    def is_accessible(self):
        # Cho phép truy cập nếu user là nhân viên hoặc admin
        return current_user.is_authenticated and (
                current_user.user_role == UserRole.ADMIN or current_user.user_role == UserRole.GIAOVIEN)


# class StudentView(NhanVienAdminView):
#     column_list = ['id', 'name', 'username', 'sex', 'birth', 'regulation_age', 'address', 'phone', 'email', 'user_role']
#     form_columns = ['name', 'username', 'sex', 'birth', 'address', 'phone', 'email']
#     column_searchable_list = ['id', 'name']
#     column_editable_list = ['name', 'sex', 'birth', 'address', 'phone', 'email']


class ClassView(NhanVienAdminView):
    column_list = ['id', 'name', 'students', 'regulation_max_student', 'class_grade', 'class_room']
    form_columns = ['name', 'students', 'class_grade', 'class_room']
    column_labels = {
        'students': 'Students - Gender - Birth'
    }
    column_searchable_list = ['id', 'name']

class ClassRoomView(AdminView):
    column_list = ['id', 'name', 'classes']
    column_searchable_list = ['id', 'name']

class ClassGradeView(AdminView):
    column_list = ['id', 'name', 'subjects', 'classes', 'year']
    column_searchable_list = ['id', 'name']


class SemesterView(AdminView):
    column_list = ['id', 'name', 'year', 'subjects']
    form_columns = ['name', 'year', 'subjects']
    column_filters = ['id', 'name']


class YearView(AdminView):
    column_list = ['id', 'name', 'semesters', 'class_grades']
    form_columns = ['name', 'semesters', 'class_grades']
    column_filters = ['id', 'name']


class SubjectView(AdminView):
    column_list = ['id', 'name', 'class_grade', 'semester', 'description']
    form_columns = ['name', 'class_grade', 'semester', 'description']
    column_searchable_list = ['id', 'name']


# class ScoreView1(GiaoVienAdminView):
#     column_list = ['id', 'student', 'so_diem', 'attempt', 'subject', 'score_type']
#     column_filters = ['id']
#     can_export = True


class ScoreTypeView(AdminView):
    column_list = ['id', 'name', 'he_so']
    form_columns = ['name', 'he_so']
    column_filters = ['id', 'name']


class RegulationMaxStudentView(AdminView):
    column_list = ['id', 'name', 'max_students', 'classes']
    form_columns = ['name', 'max_students', 'classes']


class RegulationAgeView(AdminView):
    column_list = ['id', 'name', 'min_age', 'max_age', 'students']
    form_columns = ['name', 'min_age', 'max_age', 'students']


class ScheduleView(AdminView):
    column_list = []
    form_columns = []


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class StatsView(AuthenticatedAdminView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class StudentView(AuthenticatedStaffView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):

        # Lấy từ khóa tìm kiếm
        keyword = request.args.get('kw', '').strip()

        # Lấy danh sách học sinh từ kw
        students = get_students_by_kw(keyword)


        # Truyền danh sách học sinh và enum Gender vào template
        return self.render(
            'admin/student.html',
            students=students,
            Gender=Gender,  # Truyền enum vào template
            keyword=keyword
        )

    @expose('/add_student', methods=['POST'])
    def add_student(self):
        data = request.get_json()  # Nhận dữ liệu JSON từ client (AJAX)

        # Gọi hàm từ DAO
        result = add_student(data)

        # Trả về kết quả
        return jsonify(result)

    @expose('/delete_student/<int:student_id>', methods=['POST'])
    def delete_student(self, student_id):
        # Gọi hàm từ DAO
        result = delete_student(student_id)

        # Trả về kết quả
        return jsonify(result)

    @expose('/update_student_class', methods=['POST'])
    def update_student_class(self):
        data = request.get_json()
        student_id = data.get('student_id')
        new_class_id = data.get('new_class_id')

        if not student_id or not new_class_id:
            return jsonify({'success': False, 'message': 'Thiếu thông tin học sinh hoặc lớp mới.'})

        result = change_student_class(student_id, new_class_id)
        return jsonify(result)

    @expose('/add_student_to_class', methods=['POST'])
    def add_student_to_class(self):
        data = request.get_json()
        student_id = data.get('student_id')
        class_id = data.get('class_id')

        if not student_id or not class_id:
            return jsonify({'success': False, 'message': 'Thiếu thông tin học sinh hoặc lớp.'})

        result = add_student_to_class(student_id, class_id)
        return jsonify(result)

class StudentClassView(AuthenticatedStaffView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        # Lấy danh sách lớp
        classes = Class.query.order_by(Class.name).all()
        hocsinh = Student.query.order_by(Student.name).all()

        # Lấy từ khóa tìm kiếm
        keyword = request.args.get('kw', '').strip()

        # Khởi tạo dữ liệu rỗng
        students = []

        # Lấy lớp và môn học được chọn
        class_id = request.args.get('class')

        if class_id:
            # Lấy danh sách học sinh
            students = get_students_by_class(class_id, keyword)

        # Truyền danh sách học sinh và enum Gender vào template
        return self.render(
            'admin/studentClass.html',
            students=students,
            classes=classes,
            hocsinh=hocsinh,
            keyword=keyword
        )




class ScoreView(AuthenticatedTeacherView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        # Lấy danh sách lớp và môn học
        classes = Class.query.order_by(Class.name).all()
        subjects = Subject.query.order_by(Subject.name).all()

        # Lấy từ khóa tìm kiếm
        keyword = request.args.get('kw', '').strip()

        # Khởi tạo dữ liệu rỗng
        students = []
        student_scores = {}
        average_scores = []

        # Lấy lớp và môn học được chọn
        class_id = request.args.get('class')
        subject_id = request.args.get('subject')

        if class_id and subject_id:
            # Lấy danh sách học sinh và điểm trung bình
            students = get_students_by_class(class_id, keyword)
            average_scores = get_all_students_average_score(subject_id)

            # Lấy điểm của học sinh cho môn học được chọn
            scores = get_scores_by_subject(subject_id)

            # Phân loại điểm cho từng học sinh
            for student in students:
                student_scores[student.id] = {"15phut": [], "1tiet": [], "cuoiky": []}
                for score in scores:
                    if score.student_id == student.id:
                        score_type_name = score.score_type.name.name
                        if score_type_name == "diem15p":
                            student_scores[student.id]["15phut"].append({"id": score.id, "value": score.so_diem})
                        elif score_type_name == "diem1tiet":
                            student_scores[student.id]["1tiet"].append({"id": score.id, "value": score.so_diem})
                        elif score_type_name == "diemck":
                            student_scores[student.id]["cuoiky"].append({"id": score.id, "value": score.so_diem})

        # Truyền dữ liệu vào template
        return self.render(
            'admin/score.html',
            classes=classes,
            subjects=subjects,
            students=students,
            student_scores=student_scores,
            average_scores=average_scores,
            keyword=keyword
        )

    @expose('/add_score', methods=['POST'])
    def add_score(self):
        data = request.json
        result = add_score(data.get('student_id'), data.get('subject_id'), data.get('score_type'),
                           data.get('score_value'))
        return jsonify(result)

    @expose('/edit_score', methods=['POST'])
    def edit_score(self):
        data = request.json
        result = edit_score(data.get('score_id'), data.get('new_value'))
        return jsonify(result)

    @expose('/delete_score', methods=['POST'])
    def delete_score(self):
        data = request.json
        result = delete_score(data.get('score_id'))
        return jsonify(result)

    @expose('/export_pdf', methods=['POST'])
    def export_pdf(self):
        class_id = request.form.get('class')
        subject_id = request.form.get('subject')

        # Lấy danh sách học sinh
        students = Student.query.filter_by(class_id=class_id).order_by(Student.name).all()

        # Lấy điểm trung bình của từng học sinh
        average_scores = get_all_students_average_score(subject_id)

        # Tạo buffer để lưu file PDF
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Tiêu đề
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 750, "TABLE AVERAGE SCORE")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 730, f"Class: {Class.query.get(class_id).name}")
        pdf.drawString(300, 730, f"Subject: {Subject.query.get(subject_id)}")

        # Bảng điểm
        pdf.drawString(50, 700, "STT")
        pdf.drawString(100, 700, "Student")
        pdf.drawString(400, 700, "Average score")

        y = 680  # Vị trí dòng đầu tiên
        for index, student in enumerate(students):
            avg_score = next((avg.DiemTrungBinh for avg in average_scores if avg.student_id == student.id), None)
            avg_score = f"{avg_score:.2f}" if avg_score else "N/A"

            pdf.drawString(50, y, str(index + 1))  # STT
            pdf.drawString(100, y, student.name)  # Tên học sinh
            pdf.drawString(400, y, avg_score)  # Điểm trung bình

            y -= 20  # Dòng tiếp theo
            if y < 50:  # Tạo trang mới nếu hết trang
                pdf.showPage()
                y = 750

        # Kết thúc file PDF
        pdf.save()
        buffer.seek(0)

        # Trả về file PDF để tải xuống
        response = make_response(buffer.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=bang_diem.pdf'
        response.headers['Content-Type'] = 'application/pdf'
        return response


# Thêm các bảng vào Flask-Admin
# admin.add_view(StudentView(Student, db.session))
# admin.add_view(ScoreView1(Score, db.session))
admin.add_view(StudentView(name='Student'))
admin.add_view(StudentClassView(name='Student in class'))
admin.add_view(ClassView(Class, db.session))
admin.add_view(ScoreView(name='Score'))
admin.add_view(SubjectView(Subject, db.session))
admin.add_view(ScheduleView(Schedule, db.session))
admin.add_view(ClassRoomView(ClassRoom, db.session))
admin.add_view(YearView(Year, db.session))
admin.add_view(ClassGradeView(ClassGrade, db.session))
admin.add_view(SemesterView(Semester, db.session))
admin.add_view(ScoreTypeView(ScoreType, db.session))
admin.add_view(RegulationMaxStudentView(RegulationMaxStudent, db.session))
admin.add_view(RegulationAgeView(RegulationAge, db.session))
admin.add_view(StatsView(name='Stat'))
admin.add_view(LogoutView(name='Logout'))
