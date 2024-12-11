from email.policy import default
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from sqlalchemy.event import listens_for
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin
from datetime import date, datetime
import hashlib

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2
    GIAOVIEN = 3
    NHANVIEN = 4


class Gender(RoleEnum):
    MALE = 1
    FEMALE = 2


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False, default=str(hashlib.md5('1'.encode('utf-8')).hexdigest()))
    user_role = db.Column(db.Enum(UserRole), default=UserRole.USER)
    sex = db.Column(db.Enum(Gender), default=Gender.MALE)  # Giới tính (Enum)
    birth = db.Column(db.Date, nullable=True, default=date(2004, 7, 4))
    address = db.Column(db.String(100), nullable=False, default='123 HCM')  # Địa chỉ
    phone = db.Column(db.String(10), nullable=False, default='0123456789')
    email = db.Column(db.String(100), nullable=False, default='user@example.com')
    avatar = db.Column(db.String(100),
                       default='https://res.cloudinary.com/dnwyvuqej/image/upload/v1733499646/default_avatar_uv0h7z.jpg')

    # Định nghĩa cho cơ chế kế thừa
    # type = db.Column(db.String(50), nullable=False)  # Trường phân biệt kiểu
    #
    # __mapper_args__ = {
    #     'polymorphic_identity': 'user',  # Định danh cho User
    #     'polymorphic_on': type           # Dựa vào trường `type` để phân biệt
    # }


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Tham chiếu đến User
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False, default=1)


    # __mapper_args__ = {
    #     'polymorphic_identity': 'student',  # Định danh cho Student
    # }


# Bảng lớp học
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, nullable=False)  # Khối lớp (10, 11, 12)
    max_students = db.Column(db.Integer, nullable=False, default=40)
    students = relationship('Student', backref='class', lazy=True)


# Lớp Teacher
class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Khóa chính tham chiếu từ User
    department = db.Column(db.String(100), nullable=True)  # Khoa/Bộ môn của giáo viên

    # __mapper_args__ = {
    #     'polymorphic_identity': 'teacher',
    # }


# Lớp Staff
class Staff(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Khóa chính tham chiếu từ User
    position = db.Column(db.String(100), nullable=True)  # Vị trí làm việc

    # __mapper_args__ = {
    #     'polymorphic_identity': 'staff',
    # }


# Bảng năm học và học kỳ
class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(9), nullable=False)  # Ví dụ: "2023-2024"
    semester_number = db.Column(db.Integer, nullable=False)  # Học kỳ 1 hoặc 2

    __table_args__ = (
        db.UniqueConstraint('year', 'semester_number', name='unique_year_semester'),
    )


# Bảng môn học
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


# Bảng điểm
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    score_type = db.Column(db.String(50), nullable=False)  # '15_minutes', '45_minutes', 'final'
    score_value = db.Column(db.Float, nullable=False)
    attempt = db.Column(db.Integer, nullable=True)  # Số lần kiểm tra (1, 2, ...)

    # student = db.relationship('Student', backref='score')
    # subject = db.relationship('Subject', backref='score')
    semester = db.relationship('Semester', backref='score')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        u1 = User(name='admin',
                  username='admin',
                  password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
                  user_role=UserRole.ADMIN)
        db.session.add(u1)

        teacher1 = Teacher(
            name="Nguyen Thi B",
            username="teacher1",
            password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
            user_role=UserRole.GIAOVIEN,
            sex=Gender.FEMALE,
            birth=date(1998, 6, 20),
            address="12 Nguyen Trai, HCMC",
            phone="0908123456",
            email="lan@example.com",
            avatar="https://example.com/avatar.jpg",
            # type="teacher"
        )
        db.session.add(teacher1)

        class1 = Class(name='10A1', grade=10, max_students=40)
        db.session.add(class1)
        # Giả sử bạn đã có một đối tượng `class_` trong cơ sở dữ liệu, ta sẽ tạo một học sinh thuộc lớp đó.
        class_instance = Class.query.first()  # Lấy lớp đầu tiên từ bảng `class`

        # Tạo một đối tượng Student
        student1 = Student(
            name="Nguyen Thi Lan",
            username="studentA",
            password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
            user_role=UserRole.ADMIN,
            sex=Gender.FEMALE,
            birth=date(2005, 6, 20),
            address="12 Nguyen Trai, HCMC",
            phone="0908123456",
            email="lan@example.com",
            avatar="https://example.com/avatar.jpg",
            class_id=class_instance.id,  # Tham chiếu đến lớp
            # type="student"
        )
        db.session.add(student1)
        db.session.commit()
