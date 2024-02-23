from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField

from storage.models import  Storage, dbSession


kv = open("screens\\kv\\supplierScreen.kv").read()

class RecordStorageButton(MDFloatingActionButtonSpeedDial):
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

        self.topbar = MDTopAppBar(title = "WareWise [Storage Table]",left_action_items = [[Storage.icon]])
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2

        self.dataTable = MDAnchorLayout(size_hint = (1, 0.9))
        self.table = MDDataTable(
            size_hint = (0.8,0.9),
            use_pagination = True,
            column_data = [
                ("Name", dp(40)),
                ("Address",dp(40)),
            ],
            row_data = [(storage.name, storage.address) for storage in dbSession.query(Storage).all()],
            elevation = 0,
            rows_num = 10
        )

        self.dataTable.add_widget(self.table)
        
        self.innerScreen.add_widget(self.dataTable)
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
        self.height= "150dp"
        self.orientation = "vertical"

        # * Data to be retrieved from the form
        self.nameData = None
        self.addressData = None
        
        # * The supplier name field in the form
        self.nameField = FormField(hint_text = "Storage Name", helper_text_mode = "persistent")
        
        # * The resource type field in the form
        
        # * The address name field in the form
        self.addressField = FormField(hint_text = "Storage Address", helper_text_mode = "persistent")
               
        
        self.add_widget(self.nameField)
        self.add_widget(self.addressField)
    

    def getData(self, instance):
        """
        * Get all the required data from the form
        TODO properly implement this function
        """
        self.nameData = self.nameField.text
        self.addressData = self.addressField.text

        storageToAdd = Storage(name = self.nameData, address = self.addressData)
        dbSession.add(storageToAdd)
        dbSession.commit()

class StorageScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.data = {"New Storage" : [Storage.icon,"on_press",self.open_dialog]}  

        self.addStorageForm = AddItemForm()
        self.addFormDialog = None

        self.dataScreen = DataScreen()
        self.resourceButton = RecordStorageButton(data = self.data, root_button_anim = True, hint_animation = True)

        self.add_widget(self.dataScreen)
        self.add_widget(self.resourceButton)

    def open_dialog(self, *args):
        if not self.addFormDialog:
            self.addFormDialog = MDDialog(
                title ="Record Item",
                size_hint = (1, 1),
                type = "custom",
                content_cls = self.addStorageForm,
                buttons = [MDRaisedButton(text = "SUBMIT", on_press = self.addTableRow)]
            )
        self.addFormDialog.open()
    
    def addTableRow(self, *args):
        self.addStorageForm.getData(*args)
        self.dataScreen.table.row_data = [(storage.name, storage.address) for storage in dbSession.query(Storage).all()]