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
            zip(columns, (s.id, s.fullname, [(c.id, c.fullname) for c in s.contacts])))]
        print(r)

if __name__ == '__main__':
    #get_student_join()
    #get_student()
    #get_teachers()
    #get_teachers_outerjoin()
    #get_teachers_by_date()
    get_students_with_contacts()