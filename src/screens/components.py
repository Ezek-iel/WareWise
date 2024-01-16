    # * This file contains components that are global across all screens

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.textfield import MDTextField

class NavContent(MDBoxLayout):
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

class FormTextField(MDTextField):
    """
    * A text field with the ability to validate text upon user input
    ! Targeted for numeric purposes
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_text = self.check
    
    def check(self, instance, text):
        """
        * To check the text entered upon any key stroke.
        """
        if len(text) == 0 or text.isnumeric():
            self.error = False
            self.helper_text = ""
        else:
            self.error = True
            self.helper_text = "Value must be numeric"
