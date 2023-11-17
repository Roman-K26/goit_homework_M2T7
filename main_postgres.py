from conf.db import session
from conf.models import Teacher, Student, TeacherStudent
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

if __name__ == '__main__':
    get_student_join()
    get_student()