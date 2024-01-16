        #* All imports

from storage.database_actions import getallData, addResource, getSupplierNames
from storage.settings import getResourceTypes


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

from components import NavContent, FormTextField
kv = open("kv/resourcesScreen.kv").read()

class RecordResourceButton(MDFloatingActionButtonSpeedDial):
    """
    * button used to trigger the add resource form, 
    ! child of the root screen class
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

class AddItemForm(MDBoxLayout):
    """
    * The form that adds a resource to the database
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.spacing= "16dp"
        self.padding = "8dp"
        self.size_hint_y= None
        self.height= "315dp"
        self.orientation = "vertical"

        # * Data to be retrieved from the form
        self.resourceData = None
        self.quantityData = None
        self.supplierData = None
        self.priceData = None
        
        # * The resource type field in the form
        self.resourceFieldLayout = MDBoxLayout(spacing = "7dp")
        self.resourceLabel = MDLabel(text = "Choose Resource Type", pos_hint = {"center_y" : 0.2})
        self.resourceField= MDFillRoundFlatIconButton(icon = "devices", text = "Resource Types")
        self.resourceField.bind(on_press = self.resourceOptions)

        
        # * The quantity field in the form
        #self.quantityField = MDTextField(helper_text = "Item quantity", helper_text_mode = "persistent")
        self.quantityField = FormField(hint_text = "Resource quantity", helper_text_mode = "persistent")

        # * The supplier field in the form
        self.supplierFieldLayout = MDBoxLayout(spacing = "7dp")
        self.supplierLabel = MDLabel(text = "Choose Supplier", pos_hint = {"center_y" : 0.2})
        self.supplierField = MDFillRoundFlatIconButton(icon = "account",text = "Supplier")
        self.supplierField.bind(on_press = self.supplierOptions)

        self.priceField = FormField(hint_text = "Resource price", helper_text_mode = "persistent")
        

        self.resourceFieldLayout.add_widget(self.resourceField)
        self.resourceFieldLayout.add_widget(self.resourceLabel)
        self.add_widget(self.resourceFieldLayout)    
        
        
        self.add_widget(self.quantityField)
        self.add_widget(self.priceField)

        self.supplierFieldLayout.add_widget(self.supplierField)
        self.supplierFieldLayout.add_widget(self.supplierLabel)
        self.add_widget(self.supplierFieldLayout)

        self.resourceMenu = None
        self.supplierMenu = None
    
    def setSupplier(self,value):
        self.supplierLabel.text = value
        self.supplierData = value
            
    def setResource(self,value):
        self.resourceLabel.text = value
        self.resourceData = value

    
    def resourceOptions(self, instance):
        """
        * A menu with a set of resource types for the resource field
        TODO connect the options to an actual database
        """
        menu_items = [{"text" : f'{i}', "viewclass" : "OneLineListItem", "on_release" : lambda x=f"{i}": self.setResource(x),
        } for i in getResourceTypes()]
        self.resourceMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
                                          ,width_mult = 4)
        self.resourceMenu.open()
    
    def supplierOptions(self, instance):
        """
        * A menu with a set of supplier information for the supplier field
        TODO connect the options to an actual database
        """
        menu_items = [{"text" : f'Supplier {i}', "viewclass" : "OneLineListItem", "on_release" : lambda x = i : self.setSupplier(x)} for i in getSupplierNames()]
        self.supplierMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
                                          ,width_mult = 4)
        self.supplierMenu.open()

    def getData(self, instance):
        """
        * Get all the required data from the form
        TODO properly implement this function
        """
        self.quantityData = self.quantityField.text
        self.priceData = self.priceField.text

        addResource(self.supplierData, self.resourceData, self.priceData, self.quantityData)
        return (self.supplierData, self.resourceData, self.priceData, self.quantityData)

class DataScreen(MDScreen):
    """ 
    * A screen containing all the resource data
    ! A left navigation bar is also added
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.mainLayout = MDNavigationLayout()
        self.screenManager = MDScreenManager()
        
        self.tableScreen = MDScreen()
        self.tableScreenLayout = MDBoxLayout(orientation = "vertical", padding = 20)

        self.dataTable = MDAnchorLayout()
        self.dataTable.size_hint = (1 , 0.9)

        self.table =  MDDataTable( 
            size_hint=(0.8, 0.9),
            use_pagination = True,
            column_data = [
            ("Supplier", dp(40)),
            ("Resource Type", dp(40)),
            ("Date",dp(40)),
            ("Unit Price", dp(40)),
            ("Quantity", dp(40))
            ],
            row_data = getallData("resources"),
            elevation = 2,
        )

        self.dataTable.add_widget(self.table)
        
        self.topbar = MDTopAppBar(title = "WareWise [Resources Table]",left_action_items = [["menu", lambda x: self.open_nav(),"More Options"]])
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2
        
        self.navdrawer = MDNavigationDrawer(radius = (0,8,8,0))
        self.navcontent= NavContent()

        self.navdrawer.add_widget(self.navcontent)

        self.tableScreenLayout.add_widget(self.dataTable)
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

class ResourceScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.data = {"New Product" : ["pencil","on_press",self.open_dialog]}  

        self.addResourceForm = AddItemForm()
        self.addFormDialog = None

        self.dataScreen = DataScreen()
        self.resourceButton = RecordResourceButton(data = self.data, root_button_anim = True, hint_animation = True)

        self.add_widget(self.dataScreen)
        self.add_widget(self.resourceButton)

    def open_dialog(self, *args):
        if not self.addFormDialog:
            self.addFormDialog = MDDialog(
                title ="Record Item",
                size_hint = (1, 1),
                type = "custom",
                content_cls = self.addResourceForm,
                buttons = [MDRaisedButton(text = "SUBMIT", on_press = self.addTableRow)]
            )
        self.addFormDialog.open()
    
    def addTableRow(self, *args):
        self.addResourceForm.getData(*args)
        self.dataScreen.table.row_data = getallData("resources")
    

class WareWise(MDApp):
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        return ResourceScreen()

if __name__ == '__main__':
    WareWise().run()