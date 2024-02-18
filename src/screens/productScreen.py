        #* All imports


from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFillRoundFlatIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from screens.components import FormTextField


from storage.models import Product, dbSession, ProductType, Category


kv = open("screens/kv/productScreen.kv").read()

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



class AddItemForm(MDBoxLayout):
    """
    * The form that adds a product to the database
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.spacing= "16dp"
        self.padding = "8dp"
        self.size_hint_y= None
        self.height= "400dp"
        self.orientation = "vertical"

        # * Data to be retrieved from the form
        self.productData = None
        self.quantityData = None
        self.priceData = None
        self.categoryData = None
        self.productTypeData = None
        
        # * The product type field in the form
        self.productFieldLayout = MDBoxLayout(spacing = "7dp")
        self.productLabel = MDLabel(text = "Choose Product Type", pos_hint = {"center_y" : 0.2})
        self.productField= MDFillRoundFlatIconButton(icon = ProductType.icon, text = "Product Type")
        self.productField.bind(on_press = self.productOptions)

         # * The category field in the form
        self.categoryFieldLayout = MDBoxLayout(spacing = "7dp")
        self.categoryLabel = MDLabel(text = "Choose Category", pos_hint = {"center_y" : 0.2})
        self.categoryField= MDFillRoundFlatIconButton(icon = Category.icon, text = "Category")
        self.categoryField.bind(on_press = self.categoryOptions)

        
        # * The quantity field in the form
        self.quantityField = FormTextField(hint_text = "Product Quantity", helper_text_mode = "persistent")

        # * The supplier field in the form
        self.priceField = FormTextField(hint_text = "Product Price", helper_text_mode = "persistent")
        
        #* The Name field in the form
        self.nameField = FormTextField(hint_text = "Product Name", helper_text_mode = 'persistent')

        #* The description field in the form
        self.descriptionField = FormTextField(hint_text = "Product Description", helper_text_mode = 'persistent')

        self.productFieldLayout.add_widget(self.productField)
        self.productFieldLayout.add_widget(self.productLabel)
        self.add_widget(self.productFieldLayout)  
        
        self.categoryFieldLayout.add_widget(self.categoryLabel)
        self.categoryFieldLayout.add_widget(self.categoryField)

        self.add_widget(self.categoryFieldLayout)
        
        self.add_widget(self.quantityField)
        self.add_widget(self.priceField)
        self.add_widget(self.nameField)
        self.add_widget(self.descriptionField)
    

        self.productMenu = None
            
    def setProductType(self,value):
        """
        * Set the text beside the product button and also the product data
        """
        productTypeToRetrieve = dbSession.query(ProductType).filter_by(name = value).first()

        self.productLabel.text = productTypeToRetrieve.name
        self.productTypeData = productTypeToRetrieve

    def setCategory(self, value):
        """
        * Set the text beside the product button and also the product data
        """
        categoryToRetrieve = dbSession.query(Category).filter_by(name = value).first()

        self.categoryLabel.text = categoryToRetrieve.name
        self.categoryData = categoryToRetrieve

    
    def productOptions(self, instance):
        """
        * A menu with a set of product types for the product fields
        """
        menu_items = [{"text" : f'{i.name}', "viewclass" : "OneLineListItem", "on_release" : lambda x=f"{i.name}": self.setProductType(x),
        } for i in dbSession.query(ProductType).all()]
        self.productMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
         ,width_mult = 4)
        self.productMenu.open()
    
    def categoryOptions(self, instance):
        """
        * A menu with a set of categories for category field
        """
        menu_items = [{"text" : f'{i.name}', "viewclass" : "OneLineListItem", "on_release" : lambda x=f"{i.name}": self.setCategory(x),
        } for i in dbSession.query(Category).all()]
        self.categoryMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
         ,width_mult = 4)
        self.categoryMenu.open()

    def getData(self, instance):
        """
        * Get all the required data from the form
        //TODO properly implement this function
        """
        self.quantityData = self.quantityField.text
        self.priceData = self.priceField.text
        self.nameData = self.nameField.text
        self.categoryData
        self.productTypeData
        self.descriptionData = self.descriptionField.text

        productToAdd = Product(name = self.nameData, unitPrice = self.priceData, description = self.descriptionData,quantity = self.quantityData, productType = self.productTypeData, category = self.categoryData)

        dbSession.add(productToAdd)
        dbSession.commit()

        return productToAdd

class DataScreen(MDScreen):
    """ 
    * A screen containing all the product data
    ! A left navigation bar is also added
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.mainLayout = MDNavigationLayout()
        self.screenManager = MDScreenManager()
        

        # * Layout for the table including the top app bar
        # ! The top app bar will soon be replaced with tabs......
        self.tableScreen = MDScreen()
        self.tableScreenLayout = MDBoxLayout(orientation = "vertical", padding = 20)

        self.tableLayout = MDAnchorLayout()
        self.tableLayout.size_hint = (1 , 0.9)

        self.table =  MDDataTable( 
            size_hint=(0.8, 0.9),
            use_pagination = True,
            column_data = [
            ("Product Name", dp(40)),
            ("Product Unit Price",dp(40)),
            ("Product Description", dp(40)),
            ("Quantity", dp(40)),
            ("Category",dp(40))
            ],
            row_data = [(product.name, product.unitPrice, product.description, product.quantity, product.category.name) for product in dbSession.query(Product).all()],
            elevation = 0,
        )

        self.tableLayout.add_widget(self.table)
        
        self.topbar = MDTopAppBar(title = "WareWise [Products Table]", left_action_items = [[Product.icon]])
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2

        self.tableScreenLayout.add_widget(self.tableLayout)
        self.tableScreen.add_widget(self.tableScreenLayout)
        self.tableScreen.add_widget(self.topbar)
        
        self.screenManager.add_widget(self.tableScreen)
        self.mainLayout.add_widget(self.screenManager)
        
        self.add_widget(self.mainLayout)

    
class ProductScreen(MDScreen):
    """
    * The main screen of the window including the table layout
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.data = {"New Product" : [Product.icon,"on_press",self.open_dialog]}  

        self.addProductForm = AddItemForm()
        self.addFormDialog = None

        self.dataScreen = DataScreen()
        self.resourceButton = RecordProductButton(data = self.data, root_button_anim = True, hint_animation = True)

        self.add_widget(self.dataScreen)
        self.add_widget(self.resourceButton)

    def open_dialog(self, *args):
        """
        * Opens the add product form dialog
        """
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
        """
        * Add a table row in realtime
        """

        self.addProductForm.getData(*args)
        self.dataScreen.table.row_data = [(product.name, product.unitPrice, product.description,product.quantity, product.category.name) for product in dbSession.query(Product).all()]
