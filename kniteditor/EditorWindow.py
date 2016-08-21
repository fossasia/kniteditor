"""This module contains the editor window."""
import knittingpattern
import os
from kivy.app import App
from kivy.uix.pagelayout import PageLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from .dialogs import LoadDialog, SaveDialog
from .localization import _, list_languages, change_language_to, \
    current_language, language_code_to_translation
import json
from .settings import Settings

LANGUAGE_CODE = "current"  #: the language code name
LANGUAGE_SECTION = "language"  #: the language section name


class Root(PageLayout):

    """This is the root of the application."""

    knitting_pattern = ObjectProperty(None)
    knit_settings = ObjectProperty(None)

    def show_open_file_dialog(self):
        """Open the file dialog for loading."""
        content = LoadDialog(load=self.load_path, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save_file_dialog(self):
        """Open the file dialog for saving."""
        content = SaveDialog(save=self.save_path, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load_path(self, path, filenames):
        """Load knitting patterns from several files."""
        file_path = filenames[0]
        extension = os.path.splitext(file_path.lower())[1]
        if extension == ".json":
            patterns = knittingpattern.load_from_path(file_path)
        else:
            converter = knittingpattern.convert_from_image()
            patterns = converter.path(file_path).knitting_pattern()
        pattern = patterns.patterns.at(0)
        self.knitting_pattern.show_pattern(pattern)
        self.dismiss_popup()

    def save_path(self, path, filename):
        """Save a knitting pattern to a path."""
        print("save")

        self.dismiss_popup()

    def dismiss_popup(self):
        """Close the popup window."""
        self._popup.dismiss()


class EditorWindow(App):

    """The editor window."""

    def get_application_config(self):
        """Return the application's configuration directory.

        :return: the path to the configuration file
        :rtype: str

        .. seealso:: :meth:`kivy.app.App.get_application_config`
        """
        return super().get_application_config('~/.%(appname)s.ini')

    def build_config(self, config):
        """Build the configuration.

        :param kivy.config.ConfigParser config: the configuration parser

        .. seealso:: `Application Configuration
         <https://kivy.org/docs/api-kivy.app.html#application-configuration>`__
        """
        config.setdefaults(LANGUAGE_SECTION, {
            LANGUAGE_CODE: current_language()
        })

    def build_settings(self, settings):
        """Create the applications settings dialog.

        :param  kivy.uix.settings.Settings settings: the settings for this app

        .. seealso:: `Create a settings panel
          <https://kivy.org/docs/api-kivy.app.html#create-a-settings-panel>`__,
          :meth:`kivy.uix.settings.Settings.add_json_panel`,
          :mod:`kivy.uix.settings`
        """
        settings.add_json_panel(_('KnitEditor'), self.config,
                                data=self.settings_specification)

    def update_language_from_config(self):
        """Set the current language of the application from the configuration.
        """
        config_language = self.config.get(LANGUAGE_SECTION, LANGUAGE_CODE)
        change_language_to(config_language)

    @property
    def settings_specification(self):
        """The settings specification as JSON string.

        :rtype: str
        :return: a JSON string


        """
        settings = [
            {"type": "optionmapping",
             "title": _("Language"),
             "desc": _("Choose your language"),
             "section": LANGUAGE_SECTION,
             "key": LANGUAGE_CODE,
             "options": {code: language_code_to_translation(code)
                         for code in list_languages()}}
        ]
        return json.dumps(settings)

    def on_config_change(self, config, section, key, value):
        """The configuration was changed.

        :param kivy.config.ConfigParser config: the configuration that was
          changed
        :param str section: the section that was changed
        :param str key: the key in the section that was changed
        :param value: the value this key was changed to

        When this method is called, it issued calls to change methods if they
        exist in this order:

        - ``config_change_in_section_{section}_key_{key}(value)``
        - ``config_change_in_section_{section}(key, value)``
        """
        section_call = "config_change_in_section_{}".format(section)
        key_call = "{}_key_{}".format(section_call, key)
        if hasattr(self, key_call):
            getattr(self, key_call)(value)
        elif hasattr(self, section_call):
            getattr(self, section_call)(key, value)

    def config_change_in_section_language_key_current(self, new_language):
        """Set the new language of the application.

        Same as :func:`kniteditor.localization.change_language_to`
        """
        change_language_to(new_language)

    def build(self):
        """Build the application."""
        self.settings_cls = Settings
        self.update_language_from_config()

    def on_start(self):
        """The application is started.

        .. seealso:: :meth:`kivy.app.App.on_start`
        """
        self.show_example()

    def on_stop(self):
        """The application terminates.

        .. seealso:: :meth:`kivy.app.App.on_stop`
        """
        self.root.knit_settings.stop()

    def show_example(self):
        """Show an example knitting pattern."""
        patterns = knittingpattern.load_from().example("block4x4.json")
        pattern = patterns.patterns.at(0)
        self.root.knitting_pattern.show_pattern(pattern)

__all__ = ["EditorWindow", "Root", "LANGUAGE_CODE", "LANGUAGE_SECTION"]
