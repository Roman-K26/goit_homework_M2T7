from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property #створення віртуальної гібридної властивості (поля)


Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column('id', Integer, primary_key=True)
    first_name = Column(String(120))
    lust_name = Column(String(120))
    email = Column(String(100))
    phone = Column('cell_phone', String(100))
    address = Column(String(150))
    start_work = Column(Date, nullable=False)
    students = relationship("Student", secondary='teachers_to_students', back_populates="teachers") #звязуємо таблиці

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.lust_name

class Student(Base):
    __tablename__ = 'students'
    id = Column('id', Integer, primary_key=True)
    first_name = Column(String(120))
    lust_name = Column(String(120))
    email = Column(String(100))
    phone = Column('cell_phone', String(100))
    address = Column(String(150))
    start_study = Column(Date, nullable=False)
    teachers = relationship("Teacher", secondary='teachers_to_students', back_populates="students") #звязуємо таблиці

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.lust_name


# звязок "багато до багатьох". Створюється спеціальний клас:

class TeacherStudent(Base):
    __tablename__ = 'teachers_to_students'
    id = Column('id', Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE', onupdate='CASCADE'))
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE', onupdate='CASCADE'))




