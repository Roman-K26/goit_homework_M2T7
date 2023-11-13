from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, create_engine, join
from sqlalchemy.sql import  select
metadata = MetaData()

engine = create_engine("sqlite:///:memory:", echo=True)

users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
)

addresses = Table('addresses', metadata,
    Column('id', Integer, primary_key=True),
    Column('email_address', String, nullable=False),
    Column('user_id', Integer, ForeignKey('users.id')),
)

metadata.create_all(engine)

if __name__ == '__main__':
    with engine.connect() as conn:
        ins_user = users.insert().values(name='jack', fullname='Jack Jones')
        result = conn.execute(ins_user)
        jones_id = result.lastrowid
        print(jones_id)
        ins_user = users.insert().values(name='Vasia', fullname='Vasia Vasyl')
        result = conn.execute(ins_user)
        vasyl_id = result.lastrowid
        print(vasyl_id)

        result = conn.execute(select(users))
        for row in result:
            print(row)

        ins_address = addresses.insert().values(email_address='jackjons@email.com', user_id=jones_id)
        conn.execute(ins_address)

        ins_address = addresses.insert().values(email_address='vasiavasyl@email.com', user_id=vasyl_id)
        conn.execute(ins_address)

        result = conn.execute(select(addresses))
        for row in result:
            print(row)

        sql_select = select(users.c.id, addresses.c.email_address, users.c.fullname).join(users)
        result = conn.execute(sql_select)
        for row in result:
            print(row)
