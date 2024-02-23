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
kv = open("screens/kv/resourcesScreen.kv").read()

from storage.models import dbSession, Resource, ResourceType, Category

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
        self.categoryData = None
        self.descriptionData = None
        self.priceData = None
        


        # * The resource type field in the form
        self.resourceFieldLayout = MDBoxLayout(spacing = "7dp")
        self.resourceLabel = MDLabel(text = "Choose Resource Type", pos_hint = {"center_y" : 0.2})
        self.resourceField= MDFillRoundFlatIconButton(icon = ResourceType.icon, text = "Resource Types")
        self.resourceField.bind(on_press = self.resourceOptions)

        #* The name field in the form
        self.nameField = FormTextField(hint_text = "Resource Name", helper_text_mode = "persistent")

        
        # * The quantity field in the form
        #self.quantityField = MDTextField(helper_text = "Item quantity", helper_text_mode = "persistent")
        self.quantityField = FormTextField(hint_text = "Resource quantity", helper_text_mode = "persistent")

        #* The description field in the form
        self.descriptionField = FormTextField(hint_text = "Resource Description", helper_text_mode = "persistent")

        # * The category field in the form
        self.categoryFieldLayout = MDBoxLayout(spacing = "7dp")
        self.categoryLabel = MDLabel(text = "Choose Category", pos_hint = {"center_y" : 0.2})
        self.supplierField = MDFillRoundFlatIconButton(icon = Category.icon,text = "Supplier")
        self.supplierField.bind(on_press = self.categoryOptions)

        self.priceField = FormTextField(hint_text = "Resource price", helper_text_mode = "persistent")
        

        self.resourceFieldLayout.add_widget(self.resourceField)
        self.resourceFieldLayout.add_widget(self.resourceLabel)
        self.add_widget(self.resourceFieldLayout)    
        
        
        self.add_widget(self.quantityField)
        self.add_widget(self.priceField)
        self.add_widget(self.nameField)

        self.resourceMenu = None
        self.categoryMenu = None
    
    def setResourceType(self,value):
        resourceTypeToRetrieve = dbSession.query(ResourceType).filter_by(name = value).first()
        self.resourceTypeData = resourceTypeToRetrieve
        self.resourceLabel.text = resourceTypeToRetrieve.name
    
    def setCategory(self,value):
        categoryToRetrieve = dbSession.query(Category).filter_by(name = value).first()

        self.categoryData = categoryToRetrieve
        self.categoryLabel.text = categoryToRetrieve.name

    
    def categoryOptions(self, instance):
        menu_items = [{"text" : f'{i.name}', "viewclass" : "OneLineListItem", "on_release" : lambda x=f"{i.name}": self.setCategory(x),
        } for i in dbSession.query(Category).all()]
        self.categoryMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5) ,width_mult = 4)
        self.categoryMenu.open()


    def resourceOptions(self, instance):
        """
        * A menu with a set of resource types for the resource field
        """
        menu_items = [{"text" : f'{i.name}', "viewclass" : "OneLineListItem", "on_release" : lambda x=f"{i.name}": self.setResourceType(x),
        } for i in dbSession.query(ResourceType).all()]
        self.resourceMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5) ,width_mult = 4)
        self.resourceMenu.open()
    

    def getData(self, instance):
        """
        * Get all the required data from the form
        TODO properly implement this function
        """
        self.quantityData = self.quantityField.text
        self.priceData = self.priceField.text
        self.categoryData
        self.resourceTypeData
        self.nameData = self.nameField.text
        self.descriptionData = self.descriptionField.text

        resourceToAdd = Resource(name = self.nameData, unitPrice = self.priceData, description = self.descriptionData, quantity = self.quantityData, category = self.categoryData, resourceType = self.resourceTypeData)

        dbSession.add(resourceToAdd)
        dbSession.commit()

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

        self.dataTableLayout = MDAnchorLayout()
        self.dataTableLayout.size_hint = (1 , 0.9)

        self.table =  MDDataTable( 
            size_hint=(0.8, 0.9),
            use_pagination = True,
            column_data = [
            ("Resource Name", dp(40)),
            ("Resource Unit Price", dp(40)),
            ("Description",dp(40)),
            ("Quantity", dp(40)),
            ("Category", dp(40)),
            ("Resource Type", dp(40))
            ],
            row_data = [(resource.name, resource.unitPrice, resource.description, resource.quantity, resource.category, resource.resourceType) for resource in dbSession.query(Resource).all()],
            elevation = 0,
        )

        self.dataTableLayout.add_widget(self.table)
        
        self.topbar = MDTopAppBar(title = "WareWise [Resources Table]", left_action_items = [[Resource.icon]])
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2
        
        self.tableScreenLayout.add_widget(self.dataTableLayout)
        self.tableScreen.add_widget(self.tableScreenLayout)
        self.tableScreen.add_widget(self.topbar)
        
        self.screenManager.add_widget(self.tableScreen)
        self.mainLayout.add_widget(self.screenManager)
        
        self.add_widget(self.mainLayout)

class ResourceScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.data = {"New Resource" : [Resource.icon,"on_press",self.open_dialog]}  

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
        self.dataScreen.table.row_data =  [(resource.name, resource.unitPrice, resource.description, resource.quantity, resource.category, resource.resourceType) for resource in dbSession.query(Resource).all()]