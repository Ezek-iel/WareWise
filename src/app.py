from kivymd.app import MDApp

from screens.productScreen import ProductScreen
# from screens.homeScreen import HomeScreen
from screens.resourceScreen import ResourceScreen
# from screens.settingsScreen import SettingScreen
from screens.supplierScreen import SupplierScreen
from screens.categoryScreen import CategoryScreen
from screens.employeeScreen import EmployeeScreen
from screens.transactionScreen import TransactionScreen

from storage.models import Base, Engine
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

class Tab(MDFloatLayout, MDTabsBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_style = "uiFont"


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mainlayout = MDBoxLayout(orientation = "vertical")
        self.tabs = MDTabs()


        self.productTab = Tab(icon = "package-variant", title = "Products")
        self.productTab.add_widget(ProductScreen())

        self.resourceTab = Tab(icon = "factory", title = "Resources")
        self.resourceTab.add_widget(ResourceScreen())
        
        self.supplierTab = Tab(icon = "account-multiple-outline", title = "Suppliers")
        self.supplierTab.add_widget(SupplierScreen())    

        self.categoryTab = Tab(icon = "cart", title = "Categories")
        self.categoryTab.add_widget(CategoryScreen())  

        self.employeeTab = Tab(icon = "account", title = "Employees")
        self.employeeTab.add_widget(EmployeeScreen())

        self.transactionTab = Tab(icon = "account", title = "Transaction")
        self.transactionTab.add_widget(TransactionScreen())


        # self.tabs.add_widget(self.homeTab)
        self.tabs.add_widget(self.productTab)
        self.tabs.add_widget(self.resourceTab)
        self.tabs.add_widget(self.supplierTab)
        self.tabs.add_widget(self.categoryTab)
        self.tabs.add_widget(self.employeeTab)
        self.tabs.add_widget(self.transactionTab)
        # self.tabs.add_widget(self.settingsTab)

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