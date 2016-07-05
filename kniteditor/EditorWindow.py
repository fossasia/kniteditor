"""This module contains the editor window."""
from kivy.app import App
from kivy.uix.button import Button


class EditorWindow(App):

    """The editor window."""

    def build(self):
        """Build the UI elements."""
        return Button(text="Hello World")


def main():
    """Open the editor window."""
    EditorWindow().run()

__all__ = ["main", "EditorWindow"]
