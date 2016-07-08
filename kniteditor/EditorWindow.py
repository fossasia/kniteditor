"""This module contains the editor window."""
import knittingpattern
import os
from kivy.app import App
from .KnittingPatternWidget import KnittingPatternWidget


class EditorWindow(App):

    """The editor window."""

    def build(self):
        """Build the UI elements."""
        patterns = knittingpattern.load_from().example("Cafe.json")
        self._patterns = patterns
        self.root = KnittingPatternWidget(self._patterns)
        self.root.build()


def main():
    """Open the editor window."""
    EditorWindow().run()

__all__ = ["main", "EditorWindow"]
