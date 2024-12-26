<<<<<<< Updated upstream
# from app.models import Category
=======
from datetime import datetime
import cloudinary
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app.models import User, Score, ScoreType, Student, Gender, Year, Semester, Subject, Regulation, RegulationAge, \
    RegulationMaxStudent
from app import app, db
>>>>>>> Stashed changes
import hashlib
from __init__ import db
from models import Student, User, UserRole, SexType, Class
# def load_categories():
#     return Category.query.order_by('id').all()
def load_classes():
    return Class.query.order_by('id').all()

def load_students():
    return Student.query.order_by('id').all()

def add_user(lastname, username, password, avartar, user_role, firstname, phone, email, gender, dayofbirth, address):
    if email and '@' in email:
        username = username if username else email.split('@')[0]
    if password:        
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    avartar = avartar if avartar else 'https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg'
    user_role = user_role if user_role else UserRole.USER
    if gender.__eq__("male"):
        gender = SexType.Male
    else:
        gender = SexType.Female
    address = address if address else None
    u = User(name=lastname, username = username if username else None, password = password if password else str(hashlib.md5('1'.encode("utf-8")).hexdigest()), 
             avatar=avartar, user_role=user_role, phone = phone if phone else None, familyname = firstname if firstname else None,
             email = email if email else None, sex = gender, dayofbirth = dayofbirth if dayofbirth else None, address = address)
    db.session.add(u)
    db.session.commit()

def find_user_by_email_phone(phone, email):
    return User.query.order_by('id').filter_by(phone=phone, email=email).first()
    
def add_student(lastname=None, username=None, password=None, avartar=None, user_role=None, firstname=None, phone=None, email=None, gender=None, dayofbirth=None, address=None, class_id=None):
    add_user(lastname, username, password, avartar, user_role, firstname, phone, email, gender, dayofbirth, address)
    class_id = class_id if class_id else 1
    id = find_user_by_email_phone(phone, email).id
    student = Student(id=id, class_id=class_id)
    db.session.add(student)
    db.session.commit()
    load_user_student()

def classify_class():
    if load_students():
        start = 0
        for class_item in load_classes():
            end = start + class_item.quantity
            students = load_students()[start:end]
            for student in students:
                student.class_id = class_item.id
                db.session.commit()
            start = end

def check_student(phone, email):
    user = User.query.filter_by(phone=phone,email=email).first()
    if user:
        return True
    else:
        return False

def check_student_phone(phone):
    user = User.query.filter_by(phone=phone).first()
    if user:
        return True
    else:
        return False

def check_student_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return True
    else:
        return False

def find_student_by_id(id):
    student = Student.query.filter_by(id=id).first()
    return student

def find_user_by_id(id=None):
    if id:
        user = User.query.filter_by(id=int(id)).first()
    else:
        user = None
    return user


def del_student(id=None):
    if id:
        user = find_user_by_id(int(id))
        student = find_student_by_id(int(id))
        if student:
            db.session.delete(user)
            db.session.delete(student)
            db.session.commit()
            return True
        else:
            return False
    else:
        return False    

def load_users():
    return User.query.order_by('id').all()

def load_user_student(kw=None):
    if kw:
        users = User.query.order_by('id').filter_by(user_role=UserRole.USER).filter(User.name.contains(kw))
    else:
        users = User.query.order_by('id').filter_by(user_role=UserRole.USER)
    return users.all()

<<<<<<< Updated upstream
def update_user(lastname, firstname, phone, email, gender, dayofbirth, address):
    user = find_user_by_email_phone(phone, email)
    if gender.__eq__("male"):
        gender = SexType.Male
    else:
        gender = SexType.Female
    user.name = lastname
    user.familyname = firstname
    user.sex = gender
    user.dayofbirth = dayofbirth
    user.address = address
    db.session.commit()
    load_user_student()
=======
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


def load_year():
    return Year.query.order_by('id').all()


def load_semester(id=None):
    if id:
        return Semester.query.order_by('id').filter_by(year_id=id).all()


def load_subject(semester_id=None, class_grade_id=None):
    if semester_id and class_grade_id:
        return Subject.query.order_by('id').filter_by(semester_id=semester_id, class_grade_id=class_grade_id).all()


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


def get_classgrade_id(student_id: None):
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
>>>>>>> Stashed changes
