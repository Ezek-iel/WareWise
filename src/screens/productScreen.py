        #* All imports

from storage.database_actions import getallData, addProduct, getSupplierNames
from storage.settings import getProductTypes


from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFillRoundFlatIconButton, MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.lang.builder import Builder

kv = open("kv/productScreen.kv").read()

class NavContent(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.pos_hint = {"center_y" : 1.0}

        self.userOption = OneLineIconListItem(IconLeftWidget(icon = "account"),text = "Suppliers")
        self.resourceOption = OneLineIconListItem(IconLeftWidget(icon = "cart"),text = "Items")
        self.productsOption = OneLineIconListItem(IconLeftWidget(icon = "devices"),text = "Products")
        self.databaseOption = OneLineIconListItem(IconLeftWidget(icon = "backup-restore"),text = "Restore")
        self.settingsOption = OneLineIconListItem(IconLeftWidget(icon = "cog-outline"),text = "Settings")
        
        self.add_widget(self.userOption)
        self.add_widget(self.resourceOption)
        self.add_widget(self.productsOption)
        self.add_widget(self.databaseOption)
        self.add_widget(self.settingsOption)

class RecordProductButton(MDFloatingActionButtonSpeedDial):
    """
    * button used to trigger the add product form, 
    ! child of the root screen class
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "standard"
        self.root_button_anim = True
        self.pos_hint = {"center_x" : 0.9, "center_y" : 0.07}  

class FormTextField(MDTextField):
    """
    * A text field with the ability to validate text upon user input
    ! Targeted for numeric purposes
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_text = self.check
    
    def check(self, instance, text):
        if len(text) == 0 or text.isnumeric():
            self.error = False
            self.helper_text = ""
        else:
            self.error = True
            self.helper_text = "Value must be numeric"

class AddItemForm(MDBoxLayout):
    """
    * The form that adds a product to the database
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.spacing= "16dp"
        self.padding = "8dp"
        self.size_hint_y= None
        self.height= "235dp"
        self.orientation = "vertical"

        # * Data to be retrieved from the form
        self.productData = None
        self.quantityData = None
        self.priceData = None
        
        # * The product type field in the form
        self.productFieldLayout = MDBoxLayout(spacing = "7dp")
        self.productLabel = MDLabel(text = "Choose Product Type", pos_hint = {"center_y" : 0.2})
        self.productField= MDFillRoundFlatIconButton(icon = "devices", text = "Product Type")
        self.productField.bind(on_press = self.productOptions)

        
        # * The quantity field in the form
        #self.quantityField = MDTextField(helper_text = "Item quantity", helper_text_mode = "persistent")
        self.quantityField = FormTextField(hint_text = "Product quantity", helper_text_mode = "persistent")

        # * The supplier field in the form
        self.priceField = FormTextField(hint_text = "Product price", helper_text_mode = "persistent")
        

        self.productFieldLayout.add_widget(self.productField)
        self.productFieldLayout.add_widget(self.productLabel)
        self.add_widget(self.productFieldLayout)    
        
        
        self.add_widget(self.quantityField)
        self.add_widget(self.priceField)

        self.productMenu = None
            
    def setProduct(self,value):
        self.productLabel.text = value
        self.productData = value

    
    def productOptions(self, instance):
        """
        * A menu with a set of product types for the product field
        TODO connect the options to an actual database
        """
        menu_items = [{"text" : f'{i}', "viewclass" : "OneLineListItem", "on_release" : lambda x=f"{i}": self.setProduct(x),
        } for i in getProductTypes()]
        self.productMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
                                          ,width_mult = 4)
        self.productMenu.open()

    def getData(self, instance):
        """
        * Get all the required data from the form
        TODO properly implement this function
        """
        self.quantityData = self.quantityField.text
        self.priceData = self.priceField.text

        addProduct(self.productData, self.priceData, self.quantityData)
        return (self.productData, self.priceData, self.quantityData)

class DataScreen(MDScreen):
    """ 
    * A screen containing all the product data
    ! A left navigation bar is also added
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.mainLayout = MDNavigationLayout()
        self.screenManager = MDScreenManager()
        
        self.tableScreen = MDScreen()
        self.tableScreenLayout = MDBoxLayout(orientation = "vertical", padding = 20)

        self.tableLayout = MDAnchorLayout()
        self.tableLayout.size_hint = (1 , 0.9)

        self.table =  MDDataTable( 
            size_hint=(0.8, 0.9),
            use_pagination = True,
            column_data = [
            ("Product Type", dp(40)),
            ("Date",dp(40)),
            ("Unit Price", dp(40)),
            ("Quantity", dp(40))
            ],
            row_data = getallData("products"),
            elevation = 2,
        )

        self.tableLayout.add_widget(self.table)
        
        self.topbar = MDTopAppBar(title = "WareWise [Products Table]",left_action_items = [["menu", lambda x: self.open_nav(),"More Options"]])
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2
        
        self.navdrawer = MDNavigationDrawer(radius = (0,8,8,0))
        self.navcontent= NavContent()

        self.navdrawer.add_widget(self.navcontent)

        self.tableScreenLayout.add_widget(self.tableLayout)
        self.tableScreen.add_widget(self.tableScreenLayout)
        self.tableScreen.add_widget(self.topbar)
        
        self.screenManager.add_widget(self.tableScreen)
        self.mainLayout.add_widget(self.screenManager)
        self.mainLayout.add_widget(self.navdrawer)
        
        self.add_widget(self.mainLayout)

    def open_nav(self):
        """
        * Open the left navigation bar with the top bar left button
        """
        self.navdrawer.set_state("open")
    
class ProductScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.data = {"New Product" : ["pencil","on_press",self.open_dialog]}  

        self.addProductForm = AddItemForm()
        self.addFormDialog = None

        self.dataScreen = DataScreen()
        self.resourceButton = RecordProductButton(data = self.data, root_button_anim = True, hint_animation = True)

        self.add_widget(self.dataScreen)
        self.add_widget(self.resourceButton)

    def open_dialog(self, *args):
        if not self.addFormDialog:
            self.addFormDialog = MDDialog(
                title ="Record Item",
                size_hint = (1, 1),
                type = "custom",
                content_cls = self.addProductForm,
                buttons = [MDRaisedButton(text = "SUBMIT", on_press = self.addTableRow)]
            )
        self.addFormDialog.open()
    
    def addTableRow(self, *args):
        self.addProductForm.getData(*args)
        self.dataScreen.table.row_data = getallData("products")

class WareWise(MDApp):
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        

        return ProductScreen()

if __name__ == '__main__':
    WareWise().run()