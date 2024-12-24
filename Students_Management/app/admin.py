from app.models import (Class, Student, User, UserRole, Semester, Subject,
                        Score, ScoreType, ClassGrade, Year, RegulationMaxStudent, RegulationAge, Schedule, LoaiDiem)
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, request, jsonify


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


class StudentView(NhanVienAdminView):
    column_list = ['id', 'name', 'username', 'sex', 'birth', 'regulation_age', 'address', 'phone', 'email', 'user_role']
    form_columns = ['name', 'username', 'sex', 'birth', 'address', 'phone', 'email']
    column_searchable_list = ['id', 'name']
    column_editable_list = ['name', 'sex', 'birth', 'address', 'phone', 'email']


class ClassView(NhanVienAdminView):
    column_list = ['id', 'name', 'students', 'regulation_max_student', 'class_grade', 'class_room']
    form_columns = ['name', 'students', 'class_grade', 'class_room']
    column_labels = {
        'students': 'Students - Gender - Birth'
    }
    column_searchable_list = ['id', 'name']


class ClassGradeView(NhanVienAdminView):
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


class ScoreTypeView(GiaoVienAdminView):
    column_list = ['id', 'name', 'he_so']
    form_columns = ['name', 'he_so']
    column_filters = ['id', 'name']


class RegulationMaxStudentView(AdminView):
    column_list = ['id', 'name', 'max_students', 'classes']
    form_columns = ['name', 'max_students', 'classes']


class RegulationAgeView(AdminView):
    column_list = ['id', 'name', 'min_age', 'max_age']
    form_columns = ['name', 'min_age', 'max_age']


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

        # Lấy lớp và môn học được chọn
        class_id = request.args.get('class')
        subject_id = request.args.get('subject')

        if class_id and subject_id:
            # Lấy danh sách học sinh trong lớp
            query = Student.query.filter_by(class_id=class_id)
            if keyword:
                query = query.filter(Student.name.like(f'%{keyword}%'))
            students = query.order_by(Student.name).all()

            # Lấy điểm của học sinh cho môn học được chọn
            scores = Score.query.filter_by(subject_id=subject_id).all()

            # Phân loại điểm cho từng học sinh
            for student in students:
                student_scores[student.id] = {
                    "15 phút": [],
                    "1 tiết": [],
                    "cuối kỳ": [],
                }
                for score in scores:
                    if score.student_id == student.id:
                        score_type_name = score.score_type.name.name
                        if score_type_name == "diem15p":
                            student_scores[student.id]["15 phút"].append({"id": score.id, "value": score.so_diem})
                        elif score_type_name == "diem1tiet":
                            student_scores[student.id]["1 tiết"].append({"id": score.id, "value": score.so_diem})
                        elif score_type_name == "diemck":
                            student_scores[student.id]["cuối kỳ"].append({"id": score.id, "value": score.so_diem})

        # Truyền dữ liệu vào template
        return self.render(
            'admin/score.html',
            classes=classes,
            subjects=subjects,
            students=students,
            student_scores=student_scores,
            keyword=keyword
        )

    @expose('/add_score', methods=['POST'])
    def add_score(self):
        try:
            data = request.json
            student_id = data.get('student_id')
            subject_id = data.get('subject_id')
            score_type_name = data.get('score_type')  # 'diem15p', 'diem1tiet', 'diemck'
            score_value = data.get('score_value')

            # Kiểm tra dữ liệu đầu vào
            if not all([student_id, subject_id, score_type_name, score_value]):
                return jsonify({'success': False, 'message': 'Dữ liệu không đầy đủ.'})

            # Chuyển đổi loại điểm từ chuỗi sang enum
            if score_type_name == 'diem15p':
                score_type_enum = LoaiDiem.diem15p
            elif score_type_name == 'diem1tiet':
                score_type_enum = LoaiDiem.diem1tiet
            elif score_type_name == 'diemck':  # Điều kiện đúng cho 'diemck'
                score_type_enum = LoaiDiem.diemck
            else:
                raise ValueError(f"Loại điểm không hợp lệ: {score_type_name}")

            # Lấy loại điểm từ bảng ScoreType
            score_type = ScoreType.query.filter_by(name=score_type_enum).first()
            if not score_type:
                return jsonify({'success': False, 'message': 'Không tìm thấy loại điểm tương ứng.'})

            # Tạo điểm mới
            new_score = Score(
                student_id=student_id,
                subject_id=subject_id,
                score_type_id=score_type.id,
                so_diem=score_value
            )

            db.session.add(new_score)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Thêm điểm thành công!'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Lỗi: {str(e)}'})

    @expose('/edit_score', methods=['POST'])
    def edit_score(self):
        try:
            data = request.json
            score_id = data.get('score_id')
            new_value = data.get('new_value')
            if not all([score_id, new_value is not None]):
                return jsonify({'success': False, 'message': 'Dữ liệu không đầy đủ.'})

            # Tìm điểm cần sửa
            score = Score.query.get(score_id)
            if not score:
                return jsonify({'success': False, 'message': 'Không tìm thấy điểm.'})

            # Cập nhật giá trị mới
            score.so_diem = new_value
            db.session.commit()

            return jsonify({'success': True, 'message': 'Sửa điểm thành công!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Lỗi: {str(e)}'})

    @expose('/delete_score', methods=['POST'])
    def delete_score(self):
        try:
            data = request.json
            score_id = data.get('score_id')
            # Kiểm tra dữ liệu đầu vào
            if not score_id:
                return jsonify({'success': False, 'message': 'Dữ liệu không đầy đủ.'})

            # Tìm điểm cần xóa
            score = Score.query.get(score_id)
            if not score:
                return jsonify({'success': False, 'message': 'Không tìm thấy điểm.'})

            # Xóa điểm
            db.session.delete(score)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Xóa điểm thành công!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Lỗi: {str(e)}'})


# Thêm các bảng vào Flask-Admin
admin.add_view(StudentView(Student, db.session))
admin.add_view(ClassView(Class, db.session))
admin.add_view(ClassGradeView(ClassGrade, db.session))
admin.add_view(YearView(Year, db.session))
admin.add_view(SemesterView(Semester, db.session))
admin.add_view(SubjectView(Subject, db.session))
# admin.add_view(ScoreView1(Score, db.session))
admin.add_view(ScoreTypeView(ScoreType, db.session))
admin.add_view(RegulationMaxStudentView(RegulationMaxStudent, db.session))
admin.add_view(RegulationAgeView(RegulationAge, db.session))
admin.add_view(ScheduleView(Schedule, db.session))
admin.add_view(ScoreView(name='Score'))
admin.add_view(StatsView(name='Stat'))
admin.add_view(LogoutView(name='Logout'))
