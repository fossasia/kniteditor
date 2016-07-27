"""This module contains the editor window."""
import knittingpattern
import os
import sys
from kivy.app import App
from .KnittingPatternWidget import KnittingPatternWidget
from kivy.uix.pagelayout import PageLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from .dialogs import LoadDialog, SaveDialog


class Root(PageLayout):

    knitting_pattern = ObjectProperty(None)
        
    def show_open_file_dialog(self):
        content = LoadDialog(load=self.load_path, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save_file_dialog(self):
        content = SaveDialog(save=self.save_path, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load_path(self, path, filenames):
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
        print("save")

        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()


class EditorWindow(App):

    """The editor window."""

#    def build(self):
#        """Build the UI elements."""
#        file = "negative-rendering.json"
#
#        self.pattern = KnittingPatternWidget()
#        self.pattern.show_pattern(pattern)
#        self.pattern.mark_row(pattern.rows.at(0))
#        self.root = PageLayout()
#        self.root.add_widget(self.pattern)
#        self.root.add_widget(Button(text='Hello world'))
        

def main(argv=sys.argv):
    """Open the editor window."""
    if "/test" in argv:
        import pytest
        errcode = pytest.main(["--pyargs", "knittingpattern", "kniteditor"])
        sys.exit(errcode)
    EditorWindow().run()

__all__ = ["main", "EditorWindow", "Root"]
