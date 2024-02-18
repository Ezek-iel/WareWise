from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFillRoundFlatIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField

from storage.models import Transaction, dbSession, Supplier, Resource


kv = open("screens\\kv\\supplierScreen.kv").read()

class RecordTransactionButton(MDFloatingActionButtonSpeedDial):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "standard"
        self.root_button_anim = True
        self.pos_hint = {"center_x" : 0.9, "center_y" : 0.07}

class FormField(MDTextField):
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

class DataScreen(MDScreen):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mainLayout = MDNavigationLayout()

        self.screenManager = MDScreenManager()
        self.innerScreen = MDScreen()

        self.topbar = MDTopAppBar(title = "WareWise [Transaction Table]", left_action_items = [["card-account-details"]])
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2

        self.data_table = MDAnchorLayout(size_hint = (1, 0.9))
        self.table = MDDataTable(
            size_hint = (0.8,0.9),
            use_pagination = True,
            column_data = [
                ("Date", dp(40)),
                ("Quantity", dp(40)),
                ("Supplier", dp(40)),
                ("Resource", dp(40)),
            ],
            row_data = [(transaction.date, transaction.quantity, transaction.supplier.name, transaction.resource.name) for transaction in dbSession.query(Transaction).all()],
            elevation = 0,
            rows_num = 10
        )

        self.data_table.add_widget(self.table)
        
        self.innerScreen.add_widget(self.data_table)
        self.innerScreen.add_widget(self.topbar)

        self.screenManager.add_widget(self.innerScreen)
        self.mainLayout.add_widget(self.screenManager)

        self.add_widget(self.mainLayout)


class AddItemForm(MDBoxLayout):
    """
    * The form that adds a resource to the database
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.spacing= "16dp"
        self.padding = "8dp"
        self.size_hint_y= None
        self.height= "225dp"
        self.orientation = "vertical"

        # * Data to be retrieved from the form
        self.nameData = None
        self.quantityData = None
        self.supplierData = None
        self.resourceData = None
        
        # * The supplier field in the form
        self.supplierFieldLayout = MDBoxLayout(spacing = "7dp")
        self.supplierLabel = MDLabel(text = "Choose Supplier", pos_hint = {"center_y" : 0.2})
        self.supplierField= MDFillRoundFlatIconButton(icon = Supplier.icon, text = "Supplier")
        self.supplierField.bind(on_press = self.supplierOptions)

        self.supplierFieldLayout.add_widget(self.supplierField)
        self.supplierFieldLayout.add_widget(self.supplierLabel)

         # * The resource field in the form
        self.resourceFieldLayout = MDBoxLayout(spacing = "7dp")
        self.resourceLabel = MDLabel(text = "Choose Resource", pos_hint = {"center_y" : 0.2})
        self.resourceField= MDFillRoundFlatIconButton(icon = Resource.icon, text = "Category")
        self.resourceField.bind(on_press = self.resourceOptions)

        self.resourceFieldLayout.add_widget(self.resourceField)
        self.resourceFieldLayout.add_widget(self.resourceLabel)
            
        # * The address name field in the form
        self.quantityField = FormField(hint_text = "Resource Quantity", helper_text_mode = "persistent")
       
        
        self.add_widget(self.supplierFieldLayout)
        self.add_widget(self.resourceFieldLayout)
        self.add_widget(self.quantityField)
    
    def setSupplier(self, value):
        """
        * Set the text beside the supplier button and also the product data
        """
        supplierToRetrieve = dbSession.query(Supplier).filter_by(name = value).first()

        self.supplierLabel.text = supplierToRetrieve.name
        self.supplierData = supplierToRetrieve
        pass

    def setResource(self, value):
        resourceToRetrieve = dbSession.query(Resource).filter_by(name = value).first()

        self.resourceLabel.text = resourceToRetrieve.name
        self.resourceData = resourceToRetrieve
    
    def supplierOptions(self,instance):
        """
        * A menu with a set of categories for category field
        """
        menu_items = [{"text" : f'{i.name}', "viewclass" : "OneLineListItem", "on_release" : lambda x=f"{i.name}": self.setSupplier(x),
        } for i in dbSession.query(Supplier).all()]
        
        self.supplierMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
         ,width_mult = 4)
        self.supplierMenu.open()
    
    def resourceOptions(self, instance):
        """
        * A menu with a set of categories for category field
        """
        menu_items = [{"text" : f'{i.name}', "viewclass" : "OneLineListItem", "on_release" : lambda x=f"{i.name}": self.setResource(x),
        } for i in dbSession.query(Resource).all()]
        
        self.resourceMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
         ,width_mult = 4)
        self.resourceMenu.open()
    
    def getData(self, instance):
        """
        * Get all the required data from the form
        TODO properly implement this function
        """
        self.quantityData = self.quantityField.text
       
        transactionToAdd = Transaction(quantity = self.quantityData, supplier = self.supplierData, resource = self.resourceData)

        dbSession.add(transactionToAdd)
        dbSession.commit()

class TransactionScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.data = {"New Tranaction" : [Transaction.icon,"on_press",self.open_dialog]}  

        self.addTransactionForm = AddItemForm()
        self.addFormDialog = None

        self.dataScreen = DataScreen()
        self.resourceButton = RecordTransactionButton(data = self.data, root_button_anim = True, hint_animation = True)

        self.add_widget(self.dataScreen)
        self.add_widget(self.resourceButton)

    def open_dialog(self, *args):
        if not self.addFormDialog:
            self.addFormDialog = MDDialog(
                title ="Record Item",
                size_hint = (1, 1),
                type = "custom",
                content_cls = self.addTransactionForm,
                buttons = [MDRaisedButton(text = "SUBMIT", on_press = self.addTableRow)]
            )
        self.addFormDialog.open()
    
    def addTableRow(self, *args):
        self.addTransactionForm.getData(*args)
        self.dataScreen.table.row_data = [(transaction.date, transaction.quantity, transaction.supplier.name, transaction.resource.name) for transaction in dbSession.query(Transaction).all()]
