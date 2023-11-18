import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Student, TeacherStudent, Contact


fake = Faker('uk-UA')


def insert_contacts():
    for _ in range(10):
        contact = Contact(
            first_name=fake.first_name(),
            lust_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
        )
        session.add(contact)


if __name__ == '__main__':
    try:
        insert_contacts()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
