import uuid

from sqlalchemy import UUID, select

from database import database as db
from database.models import ProductOrm
from schemas.product.product import ProductSchema, ProductAddSchema, ProductResponseSchema


class ProductRepository:
    @classmethod
    async def add_one(cls, data: ProductAddSchema) -> ProductResponseSchema:
        async with db.new_session() as session:
            # Генерация нового UUID
            while True:
                random_id = uuid.uuid4()  # Генерация уникального UUID
                # Проверяем, что ID уникален
                query = select(ProductOrm).filter(ProductOrm.id == random_id)
                result = await session.execute(query)
                existing_product = result.scalars().first()
                if not existing_product:
                    break  # Если такого ID нет в базе, выходим из цикла
            
            # Получаем словарь данных для создания продукта
            products_dict = data.model_dump()
            # Добавляем сгенерированный UUID в данные
            products_dict['id'] = random_id
            
            # Создаём объект ORM из словаря
            products = ProductOrm(**products_dict)
            session.add(products)
            await session.flush()
            await session.commit()
           
            # Возвращаем SProductResponse с нужными данными
            return ProductResponseSchema(
                id=str(products.id),  
                name=products.name,
                price=products.price,
                amount=products.amount
            )

    @classmethod
    async def find_all(cls, skip: int = 0, limit: int = 0):
        async with db.new_session() as session:
            query = select(ProductOrm).offset(skip).limit(limit)
            result = await session.execute(query)
            products_models = result.scalars().all()
            
            # Преобразуем ORM объекты в словари перед валидацией
            products_schemas = [ProductSchema.model_validate(orm_to_dict(product_model)) for product_model in products_models]
           
            return products_schemas
        
    @classmethod
    async def find_by_id(cls, product_id: UUID) -> ProductSchema | None:
        async with db.new_session() as session:
            query = select(ProductOrm).filter(ProductOrm.id == product_id)
            result = await session.execute(query)
            product_model = result.scalars().first()

            product_by_id = [ProductSchema.model_validate(orm_to_dict(product_model))]
            
            return product_by_id

    @classmethod
    async def delete_by_id(cls, product_id: UUID) -> bool:
        async with db.new_session() as session:
            query = select(ProductOrm).filter(ProductOrm.id == product_id)
            result = await session.execute(query)
            product_model = result.scalars().first()

            if product_model:
                await session.delete(product_model)
                await session.commit()
                return True
            return False

    @classmethod
    async def update_by_id(cls, product_id: UUID, data: ProductAddSchema) -> ProductSchema | None:
        async with db.new_session() as session:
            query = select(ProductOrm).filter(ProductOrm.id == product_id)
            result = await session.execute(query)
            product_model = result.scalars().first()

            if product_model:
                # Обновляем только переданные данные
                for key, value in data.model_dump().items():
                    setattr(product_model, key, value)
                await session.commit()
                return ProductSchema.model_validate(orm_to_dict(product_model))
            return None
    
# Функция для преобразования объекта ORM в словарь
def orm_to_dict(orm_object):
    return {column: getattr(orm_object, column) for column in orm_object.__table__.columns.keys()}
