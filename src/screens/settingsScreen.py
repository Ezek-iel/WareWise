from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRaisedButton, MDRoundFlatButton
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.toolbar import MDTopAppBar

from screens.storage.settings import getProductTypes, getResourceTypes, addProductType, addResourceType
from screens.components import NavContent


class OptionCard(MDCard):
    def __init__(self, text = None ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.style = "elevated"
        self.line_color=(0.2, 0.2, 0.2, 0.8)
        self.shadow_offset=(0, -1)

        self.layout = MDBoxLayout(orientation = "horizontal", padding = dp(30), spacing = dp(20))

        self.property = MDLabel(text = self.text)


        self.layout.add_widget(self.property)

        self.add_widget(self.layout)

class SettingsLayout(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.layout = MDBoxLayout(orientation = "vertical")
        self.layout.spacing = dp(30)
        self.layout.padding = dp(40)

        self.productOption = OptionCard(text = "Product Types")
        
        self.addProductLayout = MDBoxLayout(orientation = "vertical", spacing = dp(10))
        self.productTextfield = MDTextField(helper_text = "Add Product Type", helper_text_mode = "persistent")
        self.productSubmitButton = MDRaisedButton(text = "Submit")
        self.productSubmitButton.on_press = self.submitNewProduct
        
        self.viewProductTypes = MDFillRoundFlatIconButton(icon = "menu", text = "View Product Types", on_press = self.allProductTypes)

        self.addProductLayout.add_widget(self.productTextfield)
        self.addProductLayout.add_widget(self.productSubmitButton)


        self.productOption.layout.add_widget(self.addProductLayout)
        self.productOption.layout.add_widget(self.viewProductTypes)



        self.resourceOption = OptionCard(text = "Resource Types")
        self.addResourceLayout = MDBoxLayout(orientation = "vertical", spacing = dp(10))
        self.resourceTextField = MDTextField(helper_text = "Add Resource Type", helper_text_mode = "persistent")
        
        self.resourceSubmitButton = MDRaisedButton(text = "Submit")
        self.resourceSubmitButton.on_press = self.submitNewResource

        self.addResourceLayout.add_widget(self.resourceTextField)
        self.addResourceLayout.add_widget(self.resourceSubmitButton)
        
        self.viewResourceTypes = MDFillRoundFlatIconButton(icon = "menu", text = "View Resource Types", on_press = self.allResourceTypes)
        self.resourceOption.layout.add_widget(self.addResourceLayout)
        self.resourceOption.layout.add_widget(self.viewResourceTypes)

        self.layout.add_widget(self.productOption)
        self.layout.add_widget(self.resourceOption)
        self.add_widget(self.layout)

    def submitNewProduct(self):
        addProductType(self.productTextfield.text)
    
    def submitNewResource(self):
        addResourceType(self.resourceTextField.text)
    
    def allProductTypes(self,instance):
        menu_items = [{"text" : f'{i}', "viewclass" : "OneLineListItem"} for i in getProductTypes()]
        self.productTypeMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
                                          ,width_mult = 4)
        self.productTypeMenu.open()
    
    def allResourceTypes(self,instance):
        menu_items = [{"text" : f'{i}', "viewclass" : "OneLineListItem"} for i in getResourceTypes()]
        self.resourceTypeMenu = MDDropdownMenu(caller = instance, items = menu_items, max_height = dp(50 * 5)
                                          ,width_mult = 4)
        self.resourceTypeMenu.open()

class SettingScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.navLayout = MDNavigationLayout()
        self.navLayoutManager = MDScreenManager()

        self.navLayoutScreen = MDScreen()
        self.navSettingsLayout = SettingsLayout()
        
        self.topbar = MDTopAppBar(title = "Warewise [Settings]", icon = "account")
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2


        
        self.navLayoutManager.add_widget(self.navLayoutScreen)
        self.navLayoutScreen.add_widget(self.navSettingsLayout)
        self.navLayoutScreen.add_widget(self.topbar)
        
        self.navLayout.add_widget(self.navLayoutManager)

        self.add_widget(self.navLayout)

