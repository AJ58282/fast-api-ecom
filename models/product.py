from sqlalchemy import Column,BigInteger,Integer,Text,TIMESTAMP,String,Numeric,Boolean
from sqlalchemy.sql import func
from db.base import Base

class Product(Base):
    __tablename__="products"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    category = Column(String(100))
    sku = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
