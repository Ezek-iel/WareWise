from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.list import OneLineIconListItem,IconLeftWidget

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

class MainLayout(MDGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spacing = ("20dp","50dp")
        self.padding = "80dp"

class HomeCard(MDCard):
    def __init__(self, icon = None, text = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = icon
        self.text = text
        self.style = "filled"
        #self.md_bg_color = "#eff0f2"
        self.innerLayout = MDRelativeLayout()
        self.innerIcon = MDIconButton(icon = self.icon, pos_hint={"center_x": 0.5, "center_y": 0.5}, icon_size = "50dp", size_hint = (1,1))
        self.innerLabel = MDLabel(text = self.text, pos_hint={"center_x": 0.85, "center_y": 0.2},font_style = "H6")
        
        self.innerLayout.add_widget(self.innerLabel)
        self.innerLayout.add_widget(self.innerIcon)
        
        self.add_widget(self.innerLayout)

class HomeScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.homeLayout = MDNavigationLayout()
        self.mainScreenManager = MDScreenManager()
        
        self.cardScreen = MDScreen()
        
        self.topbar = MDTopAppBar(title = "WareWise",  left_action_items=[['menu', lambda x: self.open_nav(),"More Options"]])
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2
        
        self.cardLayout = MainLayout(cols= 3)
        self.userCard = HomeCard(icon = "account", text = " Suppliers")
        self.statsCard = HomeCard(icon = "chart-bell-curve-cumulative", text = "Stats")
        self.databaseCard = HomeCard(icon = "database", text = "Database Sync")
        self.productsCard = HomeCard(icon = "devices", text = "Products Info")
        self.resourcesCard = HomeCard(icon = "rocket-launch-outline", text = "Resources")
        self.itemCard = HomeCard(icon = "cart-plus", text = "Items")

        self.cardLayout.add_widget(self.userCard)
        self.cardLayout.add_widget(self.resourcesCard)
        self.cardLayout.add_widget(self.productsCard)
        self.cardLayout.add_widget(self.statsCard)
        self.cardLayout.add_widget(self.databaseCard)
        self.cardLayout.add_widget(self.itemCard)
        
        self.cardScreen.add_widget(self.cardLayout)
        self.cardScreen.add_widget(self.topbar)


        self.navDrawer = MDNavigationDrawer(radius = (0,8,8,0))
        self.navcontent = NavigationContent()
        self.navDrawer.add_widget(self.navcontent)

        self.mainScreenManager.add_widget(self.cardScreen)

        self.homeLayout.add_widget(self.mainScreenManager)
        self.homeLayout.add_widget(self.navDrawer)

        self.add_widget(self.homeLayout)

    
    def open_nav(self):
        self.navDrawer.set_state("open")




class WareWise(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        return HomeScreen()


if __name__ == "__main__":
    WareWise().run()
