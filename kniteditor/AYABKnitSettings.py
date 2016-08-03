"""A dialog for the settings to knit."""
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from AYABInterface import get_machines, get_connections
from AYABInterface.interaction import Interaction
from AYABInterface.machines import KH910
from kivy.logger import Logger
from .localization import _


first_machine = KH910()

class AYABKnitSettings(BoxLayout):
    
    """Class containing the settings to connect to the AYAB shield."""
    
    colors_layout = ObjectProperty(None)
    
    # common
    
    def populate_drop_down(self, drop_down, entries, attribute, location):
        """Populate a drop down menu."""
        drop_down.clear_widgets()
        for entry in entries:
            Logger.info("populate dropdown for {}: {}"
                        "".format(attribute, entry))
            button = Button(
                text=entry.name, height=44, size_hint_y=None, on_release=
                lambda a, entry=entry: setattr(self, attribute, entry))
            drop_down.add_widget(button)
        drop_down.open(location)
        
    def display_message(self, title, message):
        """Create a pop up error message.
        
        .. seealso:: :mod:`kivu.uix.popup`
        """
        if self.popup:
            self.popup.dismiss()
        content = Button(text=message, on_press=lambda i: popup.dismiss())
        popup = Popup(title=title, content=content,
                      size_hint=(0.5, 0.5))
        self.popup = popup
        popup.open()
        
    popup = ObjectProperty(None)
    
    # the machines
    
    machine = ObjectProperty(first_machine)
    machine_name = StringProperty(first_machine.name)
    ayab_machines_dropdown = ObjectProperty(None)
    machine_button = ObjectProperty(None)

    def populate_machines_drop_down(self):
        """Add elements to the machines choice."""
        self.populate_drop_down(self.ayab_machines_dropdown, get_machines(),
                                "machine", self.machine_button)
    
    def on_machine(self, instance, value):
        """The machine changed so we need to adapt the machine text."""
        Logger.info("machine chosen: {}".format(value))
        self.machine_name = value.name

    # the connections
        
    connection = ObjectProperty(None)
    connection_name = StringProperty(_("Choose a connection!"))
    ayab_connections_dropdown = ObjectProperty(None)
    connection_button = ObjectProperty(None)

    def populate_connections_drop_down(self):
        """Add elements to the connection choice."""
        self.populate_drop_down(self.ayab_connections_dropdown,
                                get_connections(),
                                "connection", self.connection_button)
    
    
    def on_connection(self, instance, value):
        """The connection changed so we need to adapt the machine text."""
        Logger.info("connection chosen: {}".format(value))
        self.connection_name = value.name
        
        
        
    # knitting
    
    def start_knitting(self, pattern):
        """Start the knitting process with one pattern."""
        if self.connection is None:
            self.display_message(
                _("Please Configure!"),
                _("Please choose a connection before knitting."))
            return
        self.pattern_in_progress.show_pattern(pattern)
        self.start_knitting_button.text = _("Restart knitting!")
        self.interaction = Interaction(pattern, self.machine)
        self.populate_actions(self.interaction.actions)
        
    def populate_actions(self, actions):
        """Show the actions associted with the pattern."""
        self.list_of_actions.clear_widgets()
        for action in actions:
            button = Button(text=str(action))
            self.list_of_actions.add_widget(button)

    interaction = ObjectProperty(None)
    list_of_actions = ObjectProperty(None)
    pattern_in_progress = ObjectProperty(None)
    start_knitting_button = ObjectProperty(None)

Factory.register('AYABKnitSettings', cls=AYABKnitSettings)
__all__ = ["AYABKnitSettings"]
