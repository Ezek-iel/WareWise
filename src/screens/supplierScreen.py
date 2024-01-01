from storage.database_actions import getallData, addSupplier
from storage.settings import getResourceTypes

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDRoundFlatIconButton, MDFillRoundFlatIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField

from kivy.lang import Builder

kv = open("kv\\supplierScreen.kv").read()

class RecordSupplierButton(MDFloatingActionButtonSpeedDial):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "standard"
        self.root_button_anim = True
        self.pos_hint = {"center_x" : 0.9, "center_y" : 0.07}

class NavigationContent(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orientation = "vertical"
        self.pos_hint = {"center_y" : 1.0}
    
        self.userOption = OneLineIconListItem(IconLeftWidget(icon = "account"),text = "Suppliers")
        self.resourcesOption = OneLineIconListItem(IconLeftWidget(icon = "cart"),text = "Items")
        self.productsOption = OneLineIconListItem(IconLeftWidget(icon = "devices"),text = "Products")
        self.databaseOption = OneLineIconListItem(IconLeftWidget(icon = "backup-restore"),text = "Restore")
        self.settingsOption = OneLineIconListItem(IconLeftWidget(icon = "cog-outline"),text = "Settings")
        
        self.add_widget(self.userOption)
        self.add_widget(self.resourcesOption)
        self.add_widget(self.productsOption)
        self.add_widget(self.databaseOption)
        self.add_widget(self.settingsOption)

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

        self.navDrawer = MDNavigationDrawer()
        self.navContent = NavigationContent()

        self.topbar = MDTopAppBar(title = "WareWise [Supplier Table]",left_action_items = [["menu", lambda x: self.open_nav(),"More Options"]])
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2

        self.data_table = MDAnchorLayout(size_hint = (1, 0.9))
        self.table = MDDataTable(
            size_hint = (0.8,0.9),
            use_pagination = True,
            column_data = [
                ("Name", dp(40)),
                ("Address",dp(40)),
                ("Resource Type",dp(40)),
            ],
            row_data = [tuple(row) for row in getallData("suppliers")],
            elevation = 2
        )

        self.data_table.add_widget(self.table)
        
        self.innerScreen.add_widget(self.data_table)
        self.innerScreen.add_widget(self.topbar)

        self.screenManager.add_widget(self.innerScreen)
        self.mainLayout.add_widget(self.screenManager)

        self.navDrawer.add_widget(self.navContent)
        self.mainLayout.add_widget(self.navDrawer)

        self.add_widget(self.mainLayout)

    def open_nav(self):
        self.navDrawer.set_state("open")

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
        self.addressData = None
        self.resourceData = None
        
        # * The supplier name field in the form
        self.nameField = FormField(hint_text = "Supplier Name", helper_text_mode = "persistent")
        
        # * The resource type field in the form
        self.resourceFieldLayout = MDBoxLayout(spacing = "7dp")
        self.resourceLabel = MDLabel(text = "Choose Resource Type", pos_hint = {"center_y" : 0.2})
        self.resourceField= MDFillRoundFlatIconButton(icon = "devices", text = "Resource Type")
        self.resourceField.bind(on_press = self.resourceOptions)
        
        # * The address name field in the form
        self.addressField = FormField(hint_text = "Supplier Address", helper_text_mode = "persistent")
        

        self.resourceFieldLayout.add_widget(self.resourceField)
        self.resourceFieldLayout.add_widget(self.resourceLabel)
        self.add_widget(self.resourceFieldLayout)    
        
        
        self.add_widget(self.nameField)
        self.add_widget(self.addressField)

        self.resourceMenu = None
        self.supplierMenu = None
               
    def setResource(self,value):
        self.resourceLabel.text = value
        self.resourceData = value

    
    def resourceOptions(self, instance):
        """
        * A menu with a set of product types for the product field
        TODO connect the options to an actual database
        """
        menu_items = [{"text" : f'{i}', "viewclass" : "OneLineListItem", "on_release" : lambda x=f"{i}": self.setResource(x),
        } for i in getResourceTypes()]
        self.resourceMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
                                          ,width_mult = 4)
        self.resourceMenu.open()
    

    def getData(self, instance):
        """
        * Get all the required data from the form
        TODO properly implement this function
        """
        self.nameData = self.nameField.text
        self.addressData = self.addressField.text
        
        addSupplier(name = self.nameData, resource = self.resourceData, address = self.addressData)

class SupplierScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.data = {"New Product" : ["pencil","on_press",self.open_dialog]}  

        self.addSupplierForm = AddItemForm()
        self.addFormDialog = None

        self.dataScreen = DataScreen()
        self.resourceButton = RecordSupplierButton(data = self.data, root_button_anim = True, hint_animation = True)

        self.add_widget(self.dataScreen)
        self.add_widget(self.resourceButton)

    def open_dialog(self, *args):
        if not self.addFormDialog:
            self.addFormDialog = MDDialog(
                title ="Record Item",
                size_hint = (1, 1),
                type = "custom",
                content_cls = self.addSupplierForm,
                buttons = [MDRaisedButton(text = "SUBMIT", on_press = self.addTableRow)]
            )
        self.addFormDialog.open()
    
    def addTableRow(self, *args):
        self.addSupplierForm.getData(*args)
        self.dataScreen.table.row_data = getallData("suppliers")

class WareWise(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"    
        self.theme_cls.material_style = "M3"
        return SupplierScreen()

if __name__ == "__main__":
    WareWise().run()