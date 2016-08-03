"""A dialog for the settings to knit."""
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.button import Button
from AYABInterface import get_machines, get_connections
from AYABInterface.machines import KH910
from kivy.logger import Logger
from .localization import _


first_machine = KH910()

class AYABKnitSettings(BoxLayout):
    
    """Class containing the settings to connect to the AYAB shield."""
    
    colors_layout = ObjectProperty(None)
    
    def populate_drop_down(self, drop_down, entries, attribute, location):
        drop_down.clear_widgets()
        for entry in entries:
            Logger.info("populate dropdown for {}: {}"
                        "".format(attribute, entry))
            button = Button(
                text=entry.name, height=44, size_hint_y=None, on_release=
                lambda a, entry=entry: setattr(self, attribute, entry))
            drop_down.add_widget(button)
        drop_down.open(location)   
        
    # the machines
    
    machine = ObjectProperty(first_machine)
    machine_name = StringProperty(first_machine.name)
    ayab_machines_dropdown = ObjectProperty(None)
    machine_button = ObjectProperty(None)

    def populate_machines_drop_down(self):
        self.populate_drop_down(self.ayab_machines_dropdown, get_machines(),
                                "machine", self.machine_button)
    
    def on_machine(self, instance, value):
        Logger.info("machine chosen: {}".format(value))
        self.machine_name = value.name

    # the connections
        
    connection = ObjectProperty(None)
    connection_name = StringProperty(_("Choose a connection!"))
    ayab_connections_dropdown = ObjectProperty(None)
    connection_button = ObjectProperty(None)

    def populate_connections_drop_down(self):
        self.populate_drop_down(self.ayab_connections_dropdown,
                                get_connections(),
                                "connection", self.connection_button)
    
    
    def on_connection(self, instance, value):
        Logger.info("connection chosen: {}".format(value))
        self.connection_name = value.name

Factory.register('AYABKnitSettings', cls=AYABKnitSettings)
__all__ = ["AYABKnitSettings"]
