"""A dialog for the settings to knit."""
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from AYABInterface import get_machines, get_connections
from AYABInterface.interaction import Interaction
from AYABInterface.machines import KH910
from kivy.logger import Logger
from .localization import _
from kivy.uix.dropdown import DropDown


class NullCommunication(object):

    """A null object pattern for communication."""

    def stop(self):
        """Do nothing."""


class NullFile(object):

    """A null object pattern for files."""

    def close(self):
        """Do nothing."""

FIRST_MACHINE = KH910()  #: the machine that is displayed as default


class DebugSerial(object):

    """A :class:`serial.Serial` interface proxy that logs the communication."""

    def __init__(self, serial):
        """Create a new DebugSerial object.

        :param serial.Serial serial: the serial interface
        """
        self._serial = serial
        self.close = serial.close

    def write(self, bytes_):
        """Write bytes to the serial and log them.

        :param bytes bytes_: the bytes to write
        """
        Logger.debug("write:", bytes_)
        self._serial.write(bytes_)

    def read(self, *args):
        """Read bytes from the serial and log them.

        :param tuple args: the arguments to pass on to the read method
        :return: the :class:`bytes` read from the serial
        :rtype: bytes
        """
        bytes_ = self._serial.read(*args)
        Logger.debug("read:", bytes_)
        return bytes_


class AYABKnitSettings(BoxLayout):

    """Class containing the settings to connect to the AYAB shield."""

    #: the different colors chosen
    colors_layout = ObjectProperty(None)

    # common

    def populate_drop_down(self, entries, attribute, location):
        """Populate a drop down menu."""
        drop_down = DropDown()
        for entry in entries:
            Logger.info("populate dropdown for {}: {}"
                        "".format(attribute, entry))
            button = Button(
                text=entry.name, height=44, size_hint_y=None,
                on_release=lambda a, entry=entry:
                    setattr(self, attribute, entry))
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

    #: the :class:`~kivy.uix.popup.Popup` to display messages to the user
    popup = ObjectProperty(None)

    # the machines

    #: the machine to use for knitting
    machine = ObjectProperty(FIRST_MACHINE)
    #: the name of the :attr:`machine`
    machine_name = StringProperty(FIRST_MACHINE.name)
    #: the button to choose the machines.
    machine_button = ObjectProperty(None)

    def populate_machines_drop_down(self):
        """Add elements to the machines choice."""
        self.populate_drop_down(get_machines(), "machine", self.machine_button)

    def on_machine(self, instance, value):
        """The machine changed so we need to adapt the machine text."""
        Logger.info("machine chosen: {}".format(value))
        self.machine_name = value.name

    # the connections

    #: the connection to communicate through
    connection = ObjectProperty(None)
    #: the name of the connection
    connection_name = StringProperty(_("Choose a connection!"))
    #: the button to choose the connection with
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

    #: the :class:`~AYABInterface.interaction.Interaction` object to
    #: interact with while knitting
    interaction = ObjectProperty(None)
    #: the :class:`~AYABInterface.communication.Communication` object to
    #: communicate with
    communication = ObjectProperty(NullCommunication())
    #: the :class:`DebugSerial` or :class:`serial.Serial` to use for
    #: communication
    comunication_connection = ObjectProperty(NullFile())
    #: the list of actions to diaplay to the user
    list_of_actions = ObjectProperty(None)
    #: the :class:`~kniteditor.KnittingPatternWidget.KnittingPatternWidget` to
    #: display the pattern to knit and the progess
    pattern_in_progress = ObjectProperty(None)
    #: the :class:`~kivy.uix.button.Button` to start and restart knitting with
    start_knitting_button = ObjectProperty(None)

Factory.register('AYABKnitSettings', cls=AYABKnitSettings)
__all__ = ["AYABKnitSettings", "DebugSerial", "NullCommunication", "NullFile"]
