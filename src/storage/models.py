from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from datetime import datetime
from typing import Any

Base : Any = declarative_base()

Engine =  create_engine("sqlite:///database.db")

Session = sessionmaker(Engine)
dbSession = Session()

# Creating all models
    
class Category(Base):
    __tablename__ = "categories"
    icon = "vector-arrange-below"
    categoryId = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    products = relationship('Product', back_populates='category')
    resources = relationship("Resource", back_populates="category")

    def __repr__(self):
        return f"Category {self.name}"

class Product(Base):
    __tablename__ = "products"
    icon = "cart"
    productId = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    unitPrice = Column(Integer, nullable=False)
    description = Column(String, nullable = True)
    quantity = Column(Integer, default = int(1))
    categoryId = Column(Integer, ForeignKey("categories.categoryId"))
    productTypeId = Column(Integer, ForeignKey("product_types.typeId"))

    category = relationship('Category', back_populates='products')
    orders = relationship("Order", back_populates="product")
    productType = relationship("ProductType", back_populates="products")


    def __repr__(self):
        return f"Product <{self.name}>"

class Resource(Base):
    icon = "diamond-stone"
    __tablename__ = "resources"
    resourceId = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    unitPrice = Column(Integer, nullable = False)
    description = Column(String, nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    categoryId = Column(Integer, ForeignKey("categories.categoryId"))
    resourceTypeId = Column(Integer, ForeignKey("resource_types.typeId"))

    category = relationship("Category",back_populates='resources')
    transactions = relationship("Transaction", back_populates="resource")
    resourceType = relationship("ResourceType", back_populates="resources")

    def __repr__(self):
        return f'Resource <{self.name}>'

class Customer(Base):
    icon = "account"
    __tablename__ = "customers"
    customerId = Column(Integer, primary_key = True)
    name = Column(String, nullable=False)
    contactInfo = Column(String, nullable=False)

    orders = relationship("Order", back_populates='customer')

    def __repr__(self):
        return f"Customer <{self.name}>"

class Supplier(Base):
    icon = "account"
    __tablename__ = "suppliers"
    supplierId = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contactInfo = Column(String, nullable=False)

    transactions = relationship("Transaction", back_populates="supplier")

    def __repr__(self):
        return f"Supplier <{self.name}>"

class Storage(Base):
    icon = "warehouse"
    __tablename__ = "storages"
    storageId = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    def __repr__(self):
        return f"Storage <{self.name}>"

class Employee(Base):
    icon = "account"
    __tablename__ = "employees"
    employeeId = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    role = Column(String, nullable=False)

    def __repr__(self):
        return f"Employee <{self.name}>"

class Order(Base):
    icon = "package-variant"
    __tablename__ = "orders"
    orderId = Column(Integer, primary_key=True)
    date = Column(DateTime, default = datetime.utcnow())
    
    customerId = Column(Integer, ForeignKey("customers.customerId"))
    productId = Column(Integer, ForeignKey("products.productId"))

    quantity = Column(Integer, default=1)

    customer = relationship('Customer', back_populates="orders")
    product = relationship("Product", back_populates="orders")

    def __repr__(self):
        return f"Order <{self.orderId}, {self.date}>"

class Transaction(Base):
    icon = "card-account-details"
    __tablename__ = "transactions"
    
    transactionId = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow())
    quantity = Column(Integer, default = 1)
    supplierId = Column(Integer, ForeignKey("suppliers.supplierId"))
    resourceId = Column(Integer, ForeignKey("resources.resourceId"))

    supplier = relationship("Supplier", back_populates="transactions")

    resource = relationship("Resource", back_populates="transactions")

class ProductType(Base):
    icon = "cart-variant"
    __tablename__ = "product_types"

    typeId = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    basePrice = Column(Integer, nullable=False)

    products = relationship("Product", back_populates='productType')

    def __repr__(self):
        return f'Product Type {self.name}'

class ResourceType(Base):
    icon = "diamond-stone"
    __tablename__ = "resource_types"

    typeId = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    basePrice = Column(Integer, nullable=False)

    resources = relationship("Resource", back_populates='resourceType')

    def __repr__(self):
        return f'Resource Type {self.name}'
    