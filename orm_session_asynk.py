import asyncio
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, join
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import select


engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
DBSession = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

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


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await init()
    async with DBSession() as session:
        n_user = User(name='Petya', fullname='Petya Vasechkin')
        session.add(n_user)
        n_adress = Adress(email_address='petyavas@mail', user=n_user)
        session.add(n_adress)
        await session.commit()

        n_user = User(name='Vasia', fullname='Vasia Pupkin')
        session.add(n_user)
        n_adress = Adress(email_address='pupkins@mail', user=n_user)
        session.add(n_adress)
        await session.commit()

        users = await session.execute(select(User))
        columns = ["id", "name", "fullname"]
        result = [dict(zip(columns, (row.id, row.name, row.fullname))) for row in users.scalars()]
        print(result)

        addresses = await session.execute(select(Adress).join(User))
        for el in addresses.scalars():
            print(el.id, el.email_address, el.user_id, el.user.name, el.user.fullname)




if __name__ == '__main__':
    asyncio.run(main())