"""A dialog for the settings to knit."""
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty


class AYABKnitSettings(BoxLayout):
    
    """Class containing the settings to connect to the AYAB shield."""
    
    machine_type = StringProperty("KH910")
    communication_selection = StringProperty("USB - COM01")
    colors_layout = ObjectProperty(None)

Factory.register('AYABKnitSettings', cls=AYABKnitSettings)
__all__ = ["AYABKnitSettings"]
