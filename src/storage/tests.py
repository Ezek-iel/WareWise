import unittest
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Engine = create_engine("sqlite:///testingDB.db")
Session = sessionmaker(Engine)
testsession = Session()

models.Base.metadata.create_all(Engine)

#  TODO Variable naming issues, plural where singular is meant to be

class TestModels(unittest.TestCase):

    def test_product_category_relationship(self):
       
        testCategory  = models.Category(name = "Food", description = "A food category")

        testProducts = models.Product(name = "Food SPX1", category = testCategory)

        testCategoryProducts = testCategory.products

        self.assertEqual(type(testCategoryProducts[0]) == type(testProducts), True)

    
    def test_resource_category_relationship(self):
        testCategory = models.Category(name = "Elements", description = "Elements")

        testResources = models.Resource(name = "Element 107", category = testCategory)

        testCategoryResources = testCategory.resources

        self.assertEqual(type(testCategoryResources[0]) == type(testResources), True)
    
    
    def test_resource_product_category_relationship(self):
        result_list = []

        testCategory = models.Category(name = "Liquid", description = "Some Liquids")

        testResources = models.Resource(name = "Water", category = testCategory)

        testProducts = models.Product(name = "Juice", category = testCategory)

        result_list.append(type(testCategory.resources[0]))
        result_list.append(type(testCategory.products[0]))

        self.assertEqual(result_list, [type(testResources), type(testProducts)])
    
    def test_order_product_customer_relationship(self):
        result_list = []
        
        testProducts = models.Product(name = "My Product")

        testCustomer = models.Customer(name = "John Doe", contactInfo = "Some Info")

        testOrder = models.Order(product = testProducts, customer = testCustomer)

        result_list.append(type(testOrder.customer))
        result_list.append(type(testOrder.product))

        self.assertEqual(result_list, [type(testCustomer), type(testProducts)])
    
    def test_transaction_supplier_resource(self):
        result_list = []

        testSupplier = models.Supplier(name = "Mary", contactInfo = "Some Info")

        testResource = models.Resource(name = "Silk", description = "Fabric", category = models.Category(name = "Clothes", description = "Cloth resources"), quantity = 500)

        testTransaction = models.Transaction(supplier = testSupplier, resource = testResource)

        result_list.append(type(testTransaction.supplier))
        result_list.append(type(testTransaction.resource))

        check = result_list == [type(testSupplier), type(testResource)] and testTransaction.resource.category.name == "Clothes"

        self.assertEqual(check, True)
        
            
        

if __name__ == "__main__":
    unittest.main()