from email.policy import default
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, validates
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin
from datetime import date, datetime
import hashlib


ma_hs_khoi10 = str(datetime.now().year)[-2:] + "10000"
ma_hs_khoi11 = str(datetime.now().year)[-2:] + "11000"
ma_hs_khoi12 = str(datetime.now().year)[-2:] + "12000"

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2
    GIAOVIEN = 3
    NHANVIEN = 4


class Gender(RoleEnum):
    MALE = 1
    FEMALE = 2

class HocKy(RoleEnum):
    HK1 = 1
    HK2 = 2

class KhoiLop(RoleEnum):
    Khoi10 = 1
    Khoi11 = 2
    Khoi12 = 3


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

class Admin(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Tham chiếu đến User

class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Tham chiếu đến User
    # num_instances = 0
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False, default=1)

    def __str__(self):
        return self.name

# def create_student(name, password): #dua vao khoi_lop
#     Student.num_instances += 1 # co the bi trung
#     username = str(int(ma_hs_khoi10) + Student.num_instances)
#     password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
#     return Student(name=name,username=username,password=password)

# Lớp Teacher
class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Khóa chính tham chiếu từ User
    department = db.Column(db.String(100), nullable=True)  # Khoa/Bộ môn của giáo viên


# Lớp Staff
class Staff(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Khóa chính tham chiếu từ User
    position = db.Column(db.String(100), nullable=True)  # Vị trí làm việc

# Bảng lớp học
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    max_students = db.Column(db.Integer, nullable=False, default=40)
    students = relationship('Student', backref='class', lazy=True)
    class_grade_id = db.Column(db.Integer, db.ForeignKey('class_grade.id'), nullable=False)
    # class_grade = db.relationship('ClassGrade', backref=db.backref('classes', lazy=True))  # Quan hệ ngược

    def __str__(self):
        return self.name

# Bang khoi lop
class ClassGrade(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Enum(KhoiLop), default=KhoiLop.Khoi10)
    classes = relationship('Class', backref='class_grade', lazy=True)
    subjects = relationship('Subject', backref='class_grade', lazy=True)

    def __str__(self):
        return self.name

# Bảng năm
class Year(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(9), nullable=False, default='2023-2024') # Ví dụ: "2023-2024"
    semesters = relationship('Semester', backref='year', lazy=True)
    scores = relationship('Score', backref='year', lazy=True)

    def __str__(self):
        return self.name

# Bảng học kỳ
class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Enum(HocKy), default=HocKy.HK1)  # Học kỳ 1 hoặc 2, hoặc cả 2
    year_id = Column(db.Integer, db.ForeignKey('year.id'), nullable=False)
    subjects = relationship('Subject', backref='semester')
    __table_args__ = (
        db.UniqueConstraint('year_id', 'name', name='unique_year_semester'),
    )

# Bảng môn học
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    class_grade_id = Column(db.Integer, db.ForeignKey('class_grade.id'), nullable=False)
    semester_id = Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    # class_grade = relationship('ClassGrade', backref='subjects')
    score_types_association = relationship('SubjectScoreType', backref='subject')
    score_types = association_proxy('score_types_association','score_type')
    __table_args__ = (
        db.UniqueConstraint('semester_id', 'name', name='unique_subject_semester'),
    )
    def __str__(self):
        return self.name

# Bảng loại điểm
class ScoreType(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    he_so = db.Column(db.Integer,default=1)
    subjects_association = relationship('SubjectScoreType',backref='score_type')
    subjects = association_proxy('subjects_association', 'subject')




# Bảng trung gian giữa điểm và loại điểm
class SubjectScoreType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column('subject_id',Integer,ForeignKey('subject.id'),nullable=False)
    score_type_id = db.Column('score_type_id',Integer,ForeignKey('score_type.id'),nullable=False)
    so_cot_diem = db.Column(db.Integer,default=1)




# Bảng điểm
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    so_diem = db.Column(db.Float, nullable=False)
    attempt = db.Column(db.Integer, default=1, nullable=False)
    year_id = Column(db.Integer, db.ForeignKey('year.id'), nullable=False)
    student_id = db.Column(db.Integer, ForeignKey('student.id'), nullable=False)
    subject_score_type_id = db.Column(db.Integer, ForeignKey('subject_score_type.id'), nullable=False)
    # relationship voi bang Student va bang MonHoc-LoaiDiem
    student = relationship('Student', backref='score')
    subject_score_type = relationship('SubjectScoreType', backref='score')
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject_score_type_id', 'attempt', 'year_id',
                            name='unique_point_of_a_subject_in_a_semester'),
    )


# class Regulations(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#
# class Schedule(db.Model):
#     id = db.Column(db.Integer, primary_key=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        admin1 = Admin(name='admin',
                  username='admin',
                  password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
                  user_role=UserRole.ADMIN)
        db.session.add(admin1)

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
        )
        db.session.add(teacher1)

        classgrade1= ClassGrade(name=KhoiLop.Khoi10)
        classgrade2 = ClassGrade(name=KhoiLop.Khoi11)
        classgrade3 = ClassGrade(name=KhoiLop.Khoi12)
        db.session.add(classgrade1)
        db.session.add(classgrade2)
        db.session.add(classgrade3)

        class1 = Class(name='10A1', max_students=40, class_grade=classgrade1)
        db.session.add(class1)

        class_instance = Class.query.first()  # Lấy lớp đầu tiên từ bảng `class`

        # Tạo một đối tượng Student
        student1 = Student(
            name="Nguyen Thi Lan",
            username="studentA",
            password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
            user_role=UserRole.USER,
            sex=Gender.FEMALE,
            birth=date(2005, 6, 20),
            address="12 Nguyen Trai, HCMC",
            phone="0908123456",
            email="lan@example.com",
            avatar="https://example.com/avatar.jpg",
            class_id=class_instance.id,  # Tham chiếu đến lớp
        )
        db.session.add(student1)

        nam1 = Year()
        db.session.add(nam1)

        hocky1 = Semester(year=nam1) # mặc định là học kì 1
        hocky2 = Semester(name=HocKy.HK2, year=nam1)
        db.session.add(hocky2)


        # Tao mon hoc cua 1 khoi lop va cac cot diem trong mon hoc do
        so_cot_15p = 3
        so_cot_1tiet = 2
        so_cot_ck = 1

        diem_15p = ScoreType(name='Diem 15 phut', he_so=1)
        diem_1tiet = ScoreType(name='Diem 1 tiet', he_so=2)
        diem_thi_cuoi_ki = ScoreType(name='Diem thi gk', he_so=3)

        toan10 = Subject(name="Toan10", semester=hocky1, class_grade=classgrade1)
        van10 = Subject(name='Van10', semester=hocky1, class_grade=classgrade1)
        anh10 = Subject(name='Anh10', semester=hocky1, class_grade=classgrade1)

        so_cot_diem15p_mon_toan = SubjectScoreType(subject=toan10, score_type=diem_15p, so_cot_diem=so_cot_15p)
        so_cot_diem1tiet_mon_toan = SubjectScoreType(subject=toan10, score_type=diem_1tiet, so_cot_diem=so_cot_1tiet)

        diem_toan_15p_hs1_hk1 = Score(student=student1, subject_score_type=so_cot_diem15p_mon_toan, so_diem=10,
                                     year=nam1)
        diem_toan_1tiet_hs1_hk1 = Score(student=student1, subject_score_type=so_cot_diem1tiet_mon_toan, so_diem=5,
                                       year=nam1)
        db.session.add(diem_toan_15p_hs1_hk1)
        db.session.add(diem_toan_1tiet_hs1_hk1)
        db.session.commit()
