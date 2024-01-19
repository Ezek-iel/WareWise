    # * All imports

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

from screens.components import NavContent

class HomeLayout(MDGridLayout):
    """
    * The main layout of the home screen  
    ! The main layout is a (2 x 3) grid
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spacing = ("20dp","50dp")
        self.padding = "80dp"

class HomeCard(MDCard):
    """
    * A card constructor in the home screen
    """
    def __init__(self, icon = None, text = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = icon
        self.text = text
        self.style = "elevated"
        #self.md_bg_color = "#eff0f2"
        self.innerLayout = MDRelativeLayout()
        self.innerIcon = MDIconButton(icon = self.icon, pos_hint={"center_x": 0.5, "center_y": 0.5}, icon_size = "50dp", size_hint = (1,1))
        self.innerLabel = MDLabel(text = self.text, pos_hint={"center_x": 0.85, "center_y": 0.2},font_style = "H6")
        
        self.innerLayout.add_widget(self.innerLabel)
        self.innerLayout.add_widget(self.innerIcon)
        
        self.add_widget(self.innerLayout)

class HomeScreen(MDScreen):
    """
    * The main screen consisting of the Grid of cards and the left navigation bar
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.homeLayout = MDNavigationLayout()
        self.mainScreenManager = MDScreenManager()
        
        self.cardScreen = MDScreen()
        
        # * Top app bar of the home screen
        self.topbar = MDTopAppBar(title = "WareWise Home Screen")
        self.topbar.pos_hint = {"top" : 1}
        self.topbar.elevation = 2
        
        # * Grid of Cards
        self.cardLayout = HomeLayout(cols= 3) #* Grid itself
        
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


       
        

        self.mainScreenManager.add_widget(self.cardScreen)

        self.homeLayout.add_widget(self.mainScreenManager)
        

        self.add_widget(self.homeLayout)

