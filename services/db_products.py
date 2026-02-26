from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.product import Product


async def get_all_products_db(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_product_by_id_db(product_id: int, db: AsyncSession):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    return result.scalar_one_or_none()


async def add_product_db(product_data: dict, db: AsyncSession):
    product = Product(**product_data)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def update_product_db(product_id: int, update_data: dict, db: AsyncSession):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise ValueError("Product not found")

    for key, value in update_data.items():
        if value is None:
            continue
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)
    return product


async def delete_product_db(product_id: int, db: AsyncSession):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise ValueError("Product not found")

    await db.delete(product)
    await db.commit()
    return {"message": "product deleted", "data": product}