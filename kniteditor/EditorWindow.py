"""This module contains the editor window."""
import knittingpattern
import os
from kivy.app import App
from .KnittingPatternWidget import KnittingPatternWidget


class EditorWindow(App):

    """The editor window."""

    def build(self):
        """Build the UI elements."""
        self._patterns = knittingpattern.load_from().example("negative-rendering.json")
        pattern = self._patterns.patterns.at(0)
        self.root = KnittingPatternWidget()
        self.root.show_pattern(pattern)
        self.root.mark_row(pattern.rows.at(0))
        self.root.mark_row(pattern.rows.at(1))


def main():
    """Open the editor window."""
    EditorWindow().run()

__all__ = ["main", "EditorWindow"]
