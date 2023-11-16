from sqlalchemy import Integer, String, ForeignKey, create_engine, select, and_, or_, not_, desc, func, join
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Mapped, mapped_column



engine = create_engine("sqlite:///:memory:", echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    fullname: Mapped[str] = mapped_column(String(150))

class Adress(Base):
    __tablename__ = 'addresses'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email_address: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User')


Base.metadata.create_all(engine)

if __name__ == '__main__':
    n_user = User(name='Petya', fullname='Petya Vasechkin')
    session.add(n_user)
    n_adress = Adress(email_address='petyavas@mail', user=n_user)
    session.add(n_adress)
    n_adress = Adress(email_address='petyavas_new@mail', user=n_user)
    session.add(n_adress)
    session.commit()

    n_user = User(name='Kolia', fullname='Kolia Kolko')
    session.add(n_user)
    n_adress = Adress(email_address='kolia@mail', user=n_user)
    session.add(n_adress)
    session.commit()


    n_user = User(name='Kolia', fullname='Kolia Mycolay')
    session.add(n_user)
    n_adress = Adress(email_address='mykolay@mail', user=n_user)
    session.add(n_adress)
    n_adress = Adress(email_address='mykolay_new@mail', user=n_user)
    session.add(n_adress)
    n_adress = Adress(email_address='mykolay_next@mail', user=n_user)
    session.add(n_adress)
    session.commit()

    n_user = User(name='Adam', fullname='Adam Smith')
    session.add(n_user)
    n_adress = Adress(email_address='smith@mail', user=n_user)
    session.add(n_adress)
    session.commit()

# приклад вибірки даних:
statement = select(User.id, User.name, User.fullname)
for row in session.execute(statement):
    print(row)

statement = select(Adress.id, Adress.email_address, User.fullname).join(Adress.user)
for row in session.execute(statement):
    print(row)

# ще один приклад вибірки:
statement = select(User)
columns = ["id", "name", "fullname"]
result = [dict(zip(columns, (row.id, row.name, row.fullname))) for row in session.execute(statement).scalars()]
print(result)


# приклад вибірки 3:
statement = select(User)
columns = ["id", "name", "fullname"]
result = [dict(zip(columns, (row.User.id, row.User.name, row.User.fullname))) for row in session.execute(statement)]
print(result)

# приклад вибірки 4:
statement = select(User).where(User.fullname == 'Kolia  Kolko')
r = session.execute(statement).scalar_one_or_none()
if r:
    print(r.fullname)

# приклад вибірки 5 (пошук на "містить щось спільне (like)"
statement = select(User).where(User.fullname.like('Kolia%'))
r = session.execute(statement).scalars()
for row in r:
    print(row.fullname)

# приклад вибірки 5 (пошук на "містить щось спільне (like) + ще одна умова)"
statement = select(User).where(User.fullname.like('Kolia%')).where(User.id == 3)
r = session.execute(statement).scalars()
for row in r:
    print(row.fullname)

# приклад вибірки 6 (або або)" - теж саме що і №5

statement = select(User).where(and_(User.fullname.like('Kolia%'), User.id == 3))
r = session.execute(statement).scalars()
for row in r:
    print(row.fullname)

# 7 сортування
statement = select(User).order_by(User.fullname)
columns = ["id", "name", "fullname"]
result = [dict(zip(columns, (row.User.id, row.User.name, row.User.fullname))) for row in session.execute(statement)]
print(result)

# 8 сортування навпаки
statement = select(User).order_by(desc(User.fullname))
columns = ["id", "name", "fullname"]
result = [dict(zip(columns, (row.User.id, row.User.name, row.User.fullname))) for row in session.execute(statement)]
print(result)

# 9 "OR" або
statement = select(User).where(or_(User.fullname.like('Kolia%'), User.id == 3))
r = session.execute(statement).scalars()
for row in r:
    print(row.fullname)

# 10 порахувати кількість адрес для кожного юзера
statement = (
    select(User.fullname, func.count(Adress.id))
    .join(Adress)
    .group_by(User.fullname)
    )
result = session.execute(statement).all()
for fullname, count in result: # розпарсимо результат (для гарнішого вигляду)
    print(f"{fullname}: {count}")  # розпарсимо результат (для гарнішого вигляду)

# 11 порахувати кількість адрес для кожного юзера (те ж саме але через mapping)
statement = (
    select(User.fullname, func.count(Adress.id))
    .join(Adress)
    .group_by(User.fullname)
    )
result = session.execute(statement).mappings()
for row in result:
    print(row)

session.close()