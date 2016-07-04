"""The main program of the editor.

This file starts the editor window.
"""
from kivy.app import App
from kivy.uix.button import Button


class EditorWindow(App):
    
    """The editor window."""
    
    def build(self):
        """Build the UI elements."""
        return Button(text="Hello World")

EditorWindow().run()