from kivymd.app import MDApp

from screens.productScreen import ProductScreen
from screens.resourceScreen import ResourceScreen
from screens.supplierScreen import SupplierScreen
from screens.categoryScreen import CategoryScreen
from screens.employeeScreen import EmployeeScreen
from screens.transactionScreen import TransactionScreen
from screens.customerScreen import CustomerScreen
from screens.resourceTypeScreen import ResourceTypeScreen
from screens.productTypeScreen import ProductTypeScreen
from screens.storageScreen import StorageScreen
from screens.orderScreen import OrderScreen

from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

from storage import models

class Tab(MDFloatLayout, MDTabsBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_style = "uiFont"


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mainlayout = MDBoxLayout(orientation = "vertical")
        self.tabs = MDTabs()


        self.productTab = Tab(icon = models.Product.icon, title = "Products")
        self.productTab.add_widget(ProductScreen())

        self.resourceTab = Tab(icon = models.Resource.icon, title = "Resources")
        self.resourceTab.add_widget(ResourceScreen())
        
        self.supplierTab = Tab(icon = models.Supplier.icon, title = "Suppliers")
        self.supplierTab.add_widget(SupplierScreen())    

        self.categoryTab = Tab(icon = models.Category.icon, title = "Categories")
        self.categoryTab.add_widget(CategoryScreen())  

        self.employeeTab = Tab(icon = models.Employee.icon, title = "Employees")
        self.employeeTab.add_widget(EmployeeScreen())

        self.transactionTab = Tab(icon = models.Transaction.icon, title = "Transaction")
        self.transactionTab.add_widget(TransactionScreen())

        self.customerTab = Tab(icon = models.Customer.icon, title = "Customers")
        self.customerTab.add_widget(CustomerScreen())

        self.resourceTypeTab = Tab(icon = models.ResourceType.icon, title = "Resource Types")
        self.resourceTypeTab.add_widget(ResourceTypeScreen())

        self.productTypeTab = Tab(icon = models.ProductType.icon, title = "Product Types")
        self.productTypeTab.add_widget(ProductTypeScreen())

        self.storageTab = Tab(icon = models.Storage.icon, title = "Storages")
        self.storageTab.add_widget(StorageScreen())

        self.orderTab = Tab(icon = models.Order.icon, title = "Order")
        self.orderTab.add_widget(OrderScreen())

        

        self.tabs.add_widget(self.productTab)
        self.tabs.add_widget(self.resourceTab)
        self.tabs.add_widget(self.supplierTab)
        self.tabs.add_widget(self.categoryTab)
        self.tabs.add_widget(self.employeeTab)
        self.tabs.add_widget(self.transactionTab)
        self.tabs.add_widget(self.customerTab)
        self.tabs.add_widget(self.resourceTypeTab)
        self.tabs.add_widget(self.productTypeTab)
        self.tabs.add_widget(self.storageTab)
        self.tabs.add_widget(self.orderTab)


        self.mainlayout.add_widget(self.tabs)
        self.add_widget(self.mainlayout)

    

class WareWise(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.material_style = "M3"

        return MainScreen()

if __name__ == "__main__":
    WareWise().run()