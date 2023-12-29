from sqlalchemy import case, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class  CRUDBase:

    model = None


    @classmethod
    async def get_by_id(cls, session: AsyncSession, model_id: int):
        query = select(cls.model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, **filters: dict):
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()


    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()
        

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        """ORM approach"""
        new_obj = cls.model(**data)
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
        return new_obj 

        """Core approach that doesn't work"""
        # stmt = insert(cls.model).values(**data).returning(cls.model.id)
        # result = await session.execute(stmt)
        # await session.commit()
        # await session.flush()
        # return result.scalar_one_or_none()
        
       
    @classmethod
    async def add_bulk(cls, session: AsyncSession, data: list[dict]):
        objects = [cls.model(**obj) for obj in data]
        session.add_all(objects)
        await session.commit()


    @classmethod
    async def update(cls, session: AsyncSession, filters: dict, **data):
        stmt = (
            update(cls.model).
            filter_by(**filters).
            values(**data)
        )
        await session.execute(stmt)
        await session.commit()


    @classmethod
    async def update_bulk(cls, session: AsyncSession, update_by: str, filters: dict, data: list[dict]):
        pass
        # whens = {getattr(cls.model, update_by):obj for obj in data}
        # print(whens)

        # columns = data[0].keys()

        # whens = [
        #     (cls.model.internal_id == obj['internal_id'], obj) 
        #     for obj in data
        # ]
        # stmt = (
        #     update(cls.model)
        #     .values(
        #         case(
        #             *whens,
        #         )
        #     )
        #     .filter_by(**filters)
        # )
        # await session.execute(stmt)
        # await session.commit()        


    @classmethod
    async def delete(cls, session: AsyncSession, **filters):
        stmt = delete(cls.model).filter_by(**filters)
        result = await session.execute(stmt)
        await session.commit()
        #return result.rowcount





