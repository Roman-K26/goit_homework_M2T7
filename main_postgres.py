from conf.db import session
from datetime import datetime
from sqlalchemy import and_
from conf.models import Teacher, Student, TeacherStudent, Contact
from sqlalchemy.orm import joinedload, subqueryload

def get_student_join():
    students = session.query(Student).join(Student.teachers).all()
    for s in students:
        columns = ["id", "full_name", "teachers"]
        r = [dict(
            zip(columns, (s.id, s.full_name, [(t.id, t.full_name) for t in s.teachers])))]
        print(r)

# 2 варіант:

def get_student():
    students = session.query(Student).options(joinedload(Student.teachers)).limit(5).offset(3).all() # пагінація
    for s in students:
        columns = ["id", "full_name", "teachers"]
        r = [dict(
            zip(columns, (s.id, s.full_name, [(t.id, t.full_name) for t in s.teachers])))]
        print(r)


def get_teachers():
    teachers = session.query(Teacher).options(joinedload(Teacher.students, innerjoin=True)).all()
    for t in teachers:
        columns = ["id", "full_name", "students"]
        r = [dict(
            zip(columns, (t.id, t.full_name, [(s.id, s.full_name) for s in t.students])))]
        print(r)

def get_teachers_outerjoin():
    teachers = session.query(Teacher).outerjoin(Teacher.students).all()
    for t in teachers:
        columns = ["id", "full_name", "students"]
        r = [dict(
            zip(columns, (t.id, t.full_name, [(s.id, s.full_name) for s in t.students])))]
        print(r)


def get_teachers_by_date():
    teachers = session.query(Teacher).options(joinedload(Teacher.students, innerjoin=True)) \
        .filter(and_(Teacher.start_work >= datetime(year=2020, month=1, day=1),
                     Teacher.start_work <= datetime(year=2021, month=1, day=1))).all()
    for t in teachers:
        columns = ["id", "full_name", "start_work", "students"]
        r = [dict(
            zip(columns, (t.id, t.full_name, t.start_work, [(s.id, s.full_name) for s in t.students])))]
        print(r)


def get_students_with_contacts():
    students = session.query(Student).join(Contact).all()
    for s in students:
        columns = ["id", "fullname", "contacts"]
        r = [dict(
            zip(columns, (s.id, s.full_name, [(c.id, c.full_name) for c in s.contacts])))]
        print(r)


def get_info():
    students = (session.query(Student.id, Student.full_name, Teacher.full_name.label("teacher_fullname"),
                              Contact.full_name.label("contact_fullname")).select_from(Student)
                .join(TeacherStudent).join(Teacher).join(Contact).all())
    for s in students:
        columns = ["id", "fullname", "teachers", "contacts"]
        r = [dict(
            zip(columns, (s.id, s.full_name, s.teacher_fullname, s.contact_fullname)))]
        print(r)


# зробити апдейт

def update_student(s_id, teachers: list[Teacher]):
    student = session.query(Student).filter_by(id=s_id).first()
    student.teachers = teachers
    session.commit()
    return student

# удалить
def remove_student(s_id):
    student = session.query(Student).filter_by(id=s_id).first()
    session.delete(student)
    session.commit()


if __name__ == '__main__':
    #get_student_join()
    #get_student()
    #get_teachers()
    #get_teachers_outerjoin()
    #get_teachers_by_date()
    #get_students_with_contacts()
    #get_info()
    #t = session.query(Teacher).filter(Teacher.id.in_([1, 2, 3])).all()
    #st = update_student(8, t)
    #print(st)
    remove_student(8)