from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, join
from sqlalchemy.orm import sessionmaker, relationship, declarative_base



engine = create_engine("sqlite:///:memory:", echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    fullname = Column('fullname', String)

class Adress(Base):
    __tablename__ = 'addresses'
    id = Column('id', Integer, primary_key=True)
    email_address = Column('email_address', String(50), nullable=False)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    user = relationship('User')


Base.metadata.create_all(engine)

if __name__ == '__main__':
    n_user = User(name='Petya', fullname='Petya Vasechkin')
    session.add(n_user)
    n_adress = Adress(email_address='petyavas@mail', user=n_user)
    session.add(n_adress)
    session.commit()

    users = session.query(User).all()
    for row in users:
        print(row.id, row.name, row.fullname)

    user = session.query(User).filter_by(id=1).first()
    print(user.fullname)

    address = session.query(Adress).first()
    print(address.email_address)

    session.close()