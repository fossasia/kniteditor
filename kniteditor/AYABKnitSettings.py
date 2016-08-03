"""A dialog for the settings to knit."""
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.button import Button
from AYABInterface import get_machines
from AYABInterface.machines import KH910
from kivy.logger import Logger


first_machine = KH910()

class AYABKnitSettings(BoxLayout):
    
    """Class containing the settings to connect to the AYAB shield."""
    
    machine = ObjectProperty(first_machine)
    machine_name = StringProperty(first_machine.name)
    colors_layout = ObjectProperty(None)
    ayab_machines_dropdown = ObjectProperty(None)
    machine_type_button = ObjectProperty(None)
    ayab_connection_dropdown = ObjectProperty(None)
    communication_selection = StringProperty("USB - COM01")
    
    def populate_machines_drop_down(self):
        """Build the settings menu."""
        machines = get_machines()
        self.ayab_machines_dropdown.clear_widgets()
        for machine in machines:
            Logger.info("populate machines dropdown: {}".format(machine))
            button = Button(
                text=machine.name, height=44, size_hint_y=None, on_release=
                lambda a, machine=machine: setattr(self, "machine", machine))
            self.ayab_machines_dropdown.add_widget(button)
        self.ayab_machines_dropdown.open(self.machine_type_button)
    
    def on_machine(self, instance, value):
        Logger.info("machine chosen: {}".format(value))
        self.machine_name = value.name

    def populate_connection_drop_down(self):
        """Build the settings menu."""
        machines = get_machines()
        self.ayab_machines_dropdown.clear_widgets()
        for machine in machines:
            Logger.info("populate machines dropdown: {}".format(machine))
            button = Button(
                text=machine.name, height=44, size_hint_y=None, on_release=
                lambda a, machine=machine: setattr(self, "machine", machine))
            self.ayab_machines_dropdown.add_widget(button)
        self.ayab_machines_dropdown.open(self.machine_type_button)
    
    def on_machine(self, instance, value):
        Logger.info("machine chosen: {}".format(value))
        self.machine_name = value.name

Factory.register('AYABKnitSettings', cls=AYABKnitSettings)
__all__ = ["AYABKnitSettings"]
