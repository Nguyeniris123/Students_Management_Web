from datetime import datetime
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app.models import User, Score, ScoreType, Student, Gender, Regulation, Year, Semester, Subject, RegulationAge, RegulationMaxStudent
from app import app, db
import hashlib
import cloudinary.uploader

def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User.query.filter(User.username.__eq__(username),
                          User.password.__eq__(password))

    # if role:
    #     u = u.filter(User.user_role.__eq__(role))

    return u.first()

def get_user_by_id(id):
    return User.query.get(id)

def get_students_by_kw(keyword=None):
    if keyword:
        return Student.query.filter(Student.name.ilike(f"%{keyword}%")).all()
    return Student.query.order_by(Student.name).all()

def add_student(data):
    try:
        # Lấy thông tin từ form
        name = data.get('name')
        gender = data.get('gender')
        birth = data.get('birth')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')

        # Kiểm tra dữ liệu đầu vào
        if not all([name, gender, birth, email, phone, address]):
            return {'success': False, 'message': 'Dữ liệu không đầy đủ.'}

        # Chuyển đổi ngày sinh từ chuỗi sang kiểu Date
        birth_date = datetime.strptime(birth, '%Y-%m-%d').date() if birth else None

        # Tạo đối tượng học sinh mới
        new_student = Student(
            username=phone,  # Đặt username là số điện thoại
            name=name,
            sex=Gender(int(gender)),  # Chuyển giá trị gender thành Enum
            birth=birth_date,
            email=email,
            phone=phone,
            address=address
        )

        # Thêm học sinh vào cơ sở dữ liệu
        db.session.add(new_student)
        db.session.commit()

        return {'success': True, 'message': 'Thêm học sinh thành công!'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': 'Lỗi: Tuổi học sinh sai quy định, số đt không được giống nhau'}


def delete_student(student_id):
    try:
        # Tìm học sinh theo ID
        student = Student.query.get(student_id)
        if not student:
            return {'success': False, 'message': 'Học sinh không tồn tại.'}

        # Xóa học sinh
        db.session.delete(student)
        db.session.commit()

        return {'success': True, 'message': 'Xóa học sinh thành công!'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': 'Lỗi khi xoá học sinh'}

def change_student_class(student_id, new_class_id):
    try:
        # Tìm học sinh theo ID
        student = Student.query.get(student_id)

        # Cập nhật class_id
        student.class_id = new_class_id
        db.session.commit()
        return {'success': True, 'message': 'Chuyển lớp chưa xác định thành công.'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': 'Không thể chuyển sang lớp chưa xác định'}

def add_student_to_class(student_id, class_id):
    try:
        # Tìm học sinh theo ID
        student = Student.query.get(student_id)
        if not student:
            return {'success': False, 'message': 'Học sinh không tồn tại.'}

        # Cập nhật class_id của học sinh
        student.class_id = class_id
        db.session.commit()
        return {'success': True, 'message': 'Thêm học sinh vào lớp thành công.'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': str(e)}



# Lay ra nhung hoc sinh hoc mon hoc
def get_all_students_average_score(subject_id):
    return db.session.query(Score.student_id,Score.subject_id,(func.sum(Score.so_diem * ScoreType.he_so)/func.sum(ScoreType.he_so)).label('DiemTrungBinh'))\
        .filter(Score.subject_id.__eq__(subject_id)).join(ScoreType,ScoreType.id.__eq__(Score.score_type_id)).group_by(Score.student_id).all()


def get_students_by_class(class_id, keyword=None):
    query = Student.query.filter_by(class_id=class_id)
    if keyword:
        query = query.filter(Student.name.like(f"%{keyword}%"))
    return query.order_by(Student.name).all()


def get_scores_by_subject(subject_id):
    return Score.query.filter_by(subject_id=subject_id).all()


def add_score(student_id, subject_id, score_type_name, score_value):
    try:
        # Lấy loại điểm từ bảng ScoreType
        score_type = ScoreType.query.filter_by(name=score_type_name).first()
        if not score_type:
            return {"success": False, "message": "Không tìm thấy loại điểm."}

        # Tạo điểm mới
        new_score = Score(
            student_id=student_id,
            subject_id=subject_id,
            score_type_id=score_type.id,
            so_diem=score_value
        )

        db.session.add(new_score)
        db.session.commit()
        return {"success": True, "message": "Thêm điểm thành công!"}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"success": False, "message": 'Lỗi: Điểm phải từ 0 - 10, Số cột điểm không được vượt quá quy định'}


def edit_score(score_id, new_value):
    try:
        # Tìm điểm cần sửa
        score = Score.query.get(score_id)
        if not score:
            return {"success": False, "message": "Không tìm thấy điểm."}

        # Cập nhật giá trị mới
        score.so_diem = new_value
        db.session.commit()
        return {"success": True, "message": "Sửa điểm thành công!"}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"success": False, "message": 'Lỗi: Điểm phải từ 0 - 10, Số cột điểm không được vượt quá quy định'}


def delete_score(score_id):
    try:
        # Tìm điểm cần xóa
        score = Score.query.get(score_id)
        if not score:
            return {"success": False, "message": "Không tìm thấy điểm."}

        # Xóa điểm
        db.session.delete(score)
        db.session.commit()
        return {"success": True, "message": "Xóa điểm thành công!"}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"success": False, "message": 'Lỗi'}
    
def get_user_by_id(id):
    return User.query.get(id)

def load_year():
    return Year.query.order_by('id').all()

def load_semester(id=None):
    if id:
        return Semester.query.order_by('id').filter_by(year_id = id).all()
    
def load_subject(semester_id=None, class_grade_id=None):
    if semester_id and class_grade_id:
        return Subject.query.order_by('id').filter_by(semester_id = semester_id, class_grade_id = class_grade_id).all()
    
def load_score_type():
    return ScoreType.query.order_by('id').all()

def load_score(score_type_id=None, student_id=None, subject_id=None):
    query = Score.query
    if score_type_id and student_id and subject_id:
        return query.filter_by(student_id=student_id, subject_id=subject_id, score_type_id=score_type_id).all()
        
def load_regulation(id=None):
    if id:
        return Regulation.query.get(id)
    return Regulation.query.order_by('id').all()
 
def load_detail_regulation(id=None):
    if id:
        if RegulationAge.query.get(id):
            return RegulationAge.query.filter(RegulationAge.id.__eq__(id)).first()
        if RegulationMaxStudent.query.get(id):
            return RegulationMaxStudent.query.filter(RegulationMaxStudent.id.__eq__(id)).first()
        
def change_password(student_id=None, password=None, new_password=None):
    if student_id and password and new_password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        new_password = str(hashlib.md5(new_password.strip().encode('utf-8')).hexdigest())
        user = User.query.filter(User.id.__eq__(student_id), User.password.__eq__(password)).first()
        if user:
            user.password = new_password
            db.session.commit()
            return True
        else:
            return False
        
def change_information(student_id=None, email=None, phone=None, address=None, avatar=None):
    if student_id:
        user = User.query.get(student_id)
        if user:
            if email:
                user.email = email
                db.session.commit()
            if phone:
                user.phone = phone
                db.session.commit()
            if address:
                user.address = address
                db.session.commit()
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                user.avatar = res.get('secure_url')
                db.session.commit()
            if email or phone or address or avatar:
                return True

    return False

def check_password(new_password=None, confirm_password=None):
    if confirm_password and new_password:
        if confirm_password.__eq__(new_password):
            return True
    return False

def get_classgrade_id(student_id:None):
    if student_id:
        student = Student.query.get(student_id)
        if student:
            return student.class_.class_grade.id

def get_average_score(subject_id=None, student_id=None):
    if student_id and subject_id:
        query = db.session.query(
            (func.sum(Score.so_diem * ScoreType.he_so) / func.sum(ScoreType.he_so))
        ).select_from(Score)  # select_from được gọi đầu tiên

        # Thêm join sau khi select_from
        query = query.join(ScoreType, ScoreType.id == Score.score_type_id)

        # Thêm filter sau khi join
        query = query.filter(
            Score.subject_id == subject_id,
            Score.student_id == student_id
        )
        # Thực hiện nhóm dữ liệu và trả về kết quả
        return query.group_by(Score.subject_id).scalar()