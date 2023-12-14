from readCsv import readcsv
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
from kivy.lang.builder import Builder

kv = open("itemScreen.kv").read()


class RecordInventoryButton(MDFloatingActionButtonSpeedDial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "standard"
        self.root_button_anim = True
        self.pos_hint = {"center_x" : 0.9, "center_y" : 0.07}  

class FormField(MDTextField):
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spacing= "16dp"
        self.padding = "8dp"
        self.size_hint_y= None
        self.height= "315dp"
        self.orientation = "vertical"


        self.productData = None
        self.quantityData = None
        self.supplierData = None
        self.priceData = None
        
        self.productButton = MDFillRoundFlatIconButton(icon = "devices", text = "Product Type")
        self.productButton.bind(on_press = self.productOptions)

        

        #self.quantityField = MDTextField(helper_text = "Item quantity", helper_text_mode = "persistent")
        self.quantityField = FormField(hint_text = "Item quantity", helper_text_mode = "persistent")

        self.supplierField = MDFillRoundFlatIconButton(icon = "account",text = "Supplier")
        self.supplierField.bind(on_press = self.supplierOptions)

        self.priceField = FormField(hint_text = "Item price", helper_text_mode = "persistent")

        self.add_widget(self.productButton)    
        self.add_widget(self.quantityField)
        self.add_widget(self.priceField)
        self.add_widget(self.supplierField)

        self.productMenu = None
       
    def menucall(self, text_item):
        print(text_item)
    
    def productOptions(self, instance):
        menu_items = [{"text" : f'Product {i}', "viewclass" : "OneLineListItem"} for i in range(5)]
        self.productMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
                                          ,width_mult = 4)
        self.productMenu.open()
    
    def supplierOptions(self, instance):
        menu_items = [{"text" : f'Supplier {i}', "viewclass" : "OneLineListItem"} for i in range(5)]
        self.productMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
                                          ,width_mult = 4)
        self.productMenu.open()

    
        

class DataScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainLayout = MDNavigationLayout()
        self.screenManager = MDScreenManager()
        
        self.tableScreen = MDScreen()
        self.tableScreenLayout = MDBoxLayout(orientation = "vertical", padding = 20)

        self.titleLabel = MDLabel(text = "Item Table",  font_size = 40, size_hint = (1, 0.2),
                                   halign = "center", valign = "center", font_style = "H4")
        self.dataTable = MDAnchorLayout(MDDataTable(
            use_pagination = True,
            size_hint=(0.8, 0.9),
            column_data = [
                ("Product",dp(30)),
                ("Quantity",dp(30)),
                ("Supplier",dp(30)),
                ("Status",dp(30)),
                ("Price per Unit",dp(30))
            ],
            row_data = [tuple(row) for row in readcsv()],
            elevation = 2,
        ),
    
        size_hint = (1,0.9)

        )
        
        self.topbar = MDTopAppBar(title = "WareWise",left_action_items = [["menu", lambda x: self.open_nav(),"More Options"]])
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2
        
        self.navdrawer = MDNavigationDrawer(radius = (0,8,8,0))

        
        self.tableScreenLayout.add_widget(self.titleLabel)
        self.tableScreenLayout.add_widget(self.dataTable)
        self.tableScreen.add_widget(self.tableScreenLayout)
        self.tableScreen.add_widget(self.topbar)
        
        self.screenManager.add_widget(self.tableScreen)
        self.mainLayout.add_widget(self.screenManager)
        self.mainLayout.add_widget(self.navdrawer)
        
        self.add_widget(self.mainLayout)

    def open_nav(self):
        self.navdrawer.set_state("open")
    

class WareWise(MDApp):
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        self.data = {"New Order" : ["pencil","on_press",self.open_dialog]}    
        return Builder.load_string(kv)

    def open_dialog(self, *args):
        addFormDialog = MDDialog(
            title = "Record Item",
            size_hint = (1,1),
            type = "custom",
            content_cls = AddItemForm(),
        buttons = [MDRaisedButton(text = "SUBMIT")]
        )
        addFormDialog.open()

if __name__ == '__main__':
    WareWise().run()