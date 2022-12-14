# Create a database
from sqlalchemy import (create_engine, Column, Integer, String, Date, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Brands(Base):
    __tablename__ = 'brands'

    brand_id = Column('brand_id', Integer, primary_key=True)
    brand_name = Column('brand_name', String)

    def __repr__(self):
        return f'''
        \rBrand ID: {self.brand_id}
        \rBrand Name: {self.brand_name} 
        '''


class Product(Base):
    __tablename__ = 'product'

    product_id = Column('product_id', Integer, primary_key=True)
    product_name = Column('product_name', String)
    product_quantity = Column('product_quantity', Integer)
    product_price = Column('product_price', Integer)
    date_updated = Column('date_updated', Date)
    brand_id = Column('brand_id', Integer, ForeignKey("brands.brand_id"))

    def __repr__(self):
        return f'''
        \rProduct ID: {self.product_id}
        \rProduct Name: {self.product_name}
        \rProduct Quantitu: {self.product_quantity}
        \rProduct Price: {self.product_price}
        \rDate Update: {self.date_updated}
        \rBrand ID: {self.brand_id} 
        '''