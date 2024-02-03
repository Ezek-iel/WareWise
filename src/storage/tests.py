import unittest
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(Engine)
testsession = Session()


class TestModels(unittest.TestCase):

    def setUp(self):
        models.Base.metadata.create_all(Engine)
    

    def test_product_category_relationship(self):
       
        testCategory  = models.Category(name = "Food", description = "A food category")
        testProducts = models.Product(name = "Food SPX1", category = testCategory, unitPrice = 3000)

        testCategoryProducts = testCategory.products
        self.assertIsInstance(testCategoryProducts[0], type(testProducts))

    
    def test_resource_category_relationship(self):
        
        testCategory = models.Category(name = "Elements", description = "Elements")
        testResources = models.Resource(name = "Element 107", category = testCategory)

        testCategoryResources = testCategory.resources
        self.assertIsInstance(testCategoryResources[0], type(testResources))
    
    
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
        testResource = models.Resource(name = "Silk", description = "Fabric", category = models.Category(name = "Clothes", description = "Cloth resources"), quantity = 500,  unitPrice = 500)

        testTransaction = models.Transaction(supplier = testSupplier, resource = testResource)
        result_list.append(type(testTransaction.supplier))
        result_list.append(type(testTransaction.resource))

        check = result_list == [type(testSupplier), type(testResource)] and testTransaction.resource.category.name == "Clothes"
        self.assertEqual(check, True)

    def test_product_productType_relationship(self):
        testProduct = models.Product(name = "Wool", unitPrice = 3000)
        testProductType = models.ProductType(name = "Sheep Cloth", basePrice = 3000)

        testProduct.productType = testProductType

        self.assertIsInstance(testProduct.productType, type(testProductType))
    
    def test_resource_resourceType_relationship(self):
        testResource = models.Resource(name = "cow", unitPrice = 4000)
        testResourceType = models.ResourceType(name = "Animals", basePrice = 4000)

        testResource.resourceType = testResourceType

        self.assertIsInstance(testResource.resourceType, type(testResourceType))

    def tearDown(self) -> None:
        models.Base.metadata.drop_all(Engine)

if __name__ == "__main__":
    unittest.main()