from app.models import Class, Semester, Student, Subject, Grade, User, UserRole
from flask_admin import Admin, BaseView, expose
from app import app, db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect

# Khởi tạo Flask-Admin
admin = Admin(app, name='Quản trị hệ thống', template_mode='bootstrap4')

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



class SemesterView(AdminView):
    column_list = ('year', 'semester_number')
    column_labels = {
        'year': 'Năm học',
        'semester_number': 'Học kỳ'
    }
    column_filters = ['year', 'semester_number']

class ClassView(NhanVienAdminView):
    column_list = ('year', 'semester_number')

class StudentView(NhanVienAdminView):
    column_list = ('year', 'semester_number')

class SubjectView(AdminView):
    column_list = ('year', 'semester_number')

class GradeView(GiaoVienAdminView):
    column_list = (
    'student.name', 'subject.name', 'semester.year', 'semester.semester_number', 'grade_type', 'grade_value', 'attempt')
    column_labels = {
        'student.name': 'Học sinh',
        'subject.name': 'Môn học',
        'semester.year': 'Năm học',
        'semester.semester_number': 'Học kỳ',
        'grade_type': 'Loại điểm',
        'grade_value': 'Giá trị điểm',
        'attempt': 'Lần kiểm tra'
    }
    column_filters = ['grade_type', 'semester.year', 'semester.semester_number']


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


# Thêm các bảng vào Flask-Admin
admin.add_view(SemesterView(Semester, db.session))
admin.add_view(ClassView(Class, db.session))  # Chỉ giáo viên có thể truy cập
admin.add_view(StudentView(Student, db.session))  # Nhân viên có thể truy cập
admin.add_view(SubjectView(Subject, db.session))
admin.add_view(GradeView(Grade, db.session))  # Chỉ giáo viên có thể truy cập
admin.add_view(LogoutView(name='Đăng xuất'))  # Đăng xuất trên trang flask-admin