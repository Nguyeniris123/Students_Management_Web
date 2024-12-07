# from app.models import Category
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
