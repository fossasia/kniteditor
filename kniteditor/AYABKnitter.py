"""This is a prototypical interface of a Knitter

class KnittingTechnique(object):

    "A way to knit."

    def get_settings_dialog(self, pattern):

    def get_settings(self):

    def get_name(self):

    def get_knit_job(self, pattern):


class KnitJob(object):

    def decide_what_can_be_knit(self, pattern):

    def give_instructions(self):

    def current_instruction(self):

    @property
    def technique(self):
"""
