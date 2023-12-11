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
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.dialog import MDDialog

class RecordInventoryButton(MDFloatingActionButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = "pencil"
        self.type = "standard"
        self.pos_hint = {"center_x" : 0.9, "center_y" : 0.07}


class DataScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainLayout = MDNavigationLayout()
        self.screenManager = MDScreenManager()
        
        self.tableScreen = MDScreen()
        
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
        padding = "40dp"
        )
        
        self.topbar = MDTopAppBar(title = "WareWise",left_action_items = [["menu", lambda x: self.open_nav(),"More Options"]])
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2
        
        self.navdrawer = MDNavigationDrawer(radius = (0,8,8,0))
        
        self.tableScreen.add_widget(self.dataTable)
        self.tableScreen.add_widget(self.topbar)
        self.tableScreen.add_widget(RecordInventoryButton())
        
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
        return DataScreen()
    
if __name__ == '__main__':
    WareWise().run()