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
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown


class NullCommunication(object):

    def stop(self):
        """Do nothing."""


class NullFile(object):

    def close(self):
        """Do nothing."""

first_machine = KH910()


class DebugSerial(object):

    def __init__(self, serial):
        self._serial = serial
        self.close = serial.close

    def write(self, bytes_):
        print("write:", bytes_)
        self._serial.write(bytes_)

    def read(self, *args):
        bytes_ = self._serial.read(*args)
        print("read:", bytes_)
        return bytes_


class AYABKnitSettings(BoxLayout):

    """Class containing the settings to connect to the AYAB shield."""

    colors_layout = ObjectProperty(None)

    # common

    def populate_drop_down(self, entries, attribute, location):
        """Populate a drop down menu."""
        drop_down = DropDown()
        for entry in entries:
            Logger.info("populate dropdown for {}: {}"
                        "".format(attribute, entry))
            button = Button(
                text=entry.name, height=44, size_hint_y=None, on_release=lambda a, entry=entry: setattr(self, attribute, entry))
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
    machine_button = ObjectProperty(None)

    def populate_machines_drop_down(self):
        """Add elements to the machines choice."""
        self.populate_drop_down(get_machines(), "machine", self.machine_button)

    def on_machine(self, instance, value):
        """The machine changed so we need to adapt the machine text."""
        Logger.info("machine chosen: {}".format(value))
        self.machine_name = value.name

    # the connections

    connection = ObjectProperty(None)
    connection_name = StringProperty(_("Choose a connection!"))
    connection_button = ObjectProperty(None)

    def populate_connections_drop_down(self):
        """Add elements to the connection choice."""
        self.populate_drop_down(get_connections(),
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

        self.stop()

        self.interaction = Interaction(pattern, self.machine)
        self.comunication_connection = DebugSerial(self.connection.connect())
        self.communication = self.interaction.communicate_through(
            self.comunication_connection)
        self.communication.on_message(print)
        self.communication.parallelize(2)

        self.populate_actions(self.interaction.actions)

    def stop(self):
        """Stop the connections."""
        self.comunication_connection.close()
        self.communication.stop()

    def build(self):
        """Build the UI for the first time."""
        self.ayab_connections_dropdown.dismiss()
        self.ayab_machines_dropdown.dismiss()

    def populate_actions(self, actions):
        """Show the actions associted with the pattern."""
        self.list_of_actions.clear_widgets()
        for action in actions:
            button = Button(text=str(action))
            self.list_of_actions.add_widget(button)

    interaction = ObjectProperty(None)
    communication = ObjectProperty(NullCommunication())
    comunication_connection = ObjectProperty(NullFile())
    list_of_actions = ObjectProperty(None)
    pattern_in_progress = ObjectProperty(None)
    start_knitting_button = ObjectProperty(None)

Factory.register('AYABKnitSettings', cls=AYABKnitSettings)
__all__ = ["AYABKnitSettings"]
