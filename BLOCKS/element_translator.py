# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/BLOCKS/element_translator.py
# Compiled at: 2018-04-23 20:27:04
from __future__ import absolute_import, print_function, unicode_literals

class ElementTranslator(object):

    def __init__(self, elements=None, feedback_channel=None, non_feedback_channel=None, *a, **k):
        super(ElementTranslator, self).__init__(*a, **k)
        assert elements is not None
        self._elements = elements
        self._feedback_channel = feedback_channel
        self._non_feedback_channel = non_feedback_channel
        return

    def set_enabled(self, enable):
        for element in self._elements:
            channel = self._non_feedback_channel
            if enable:
                element.reset_state()
                channel = self._feedback_channel
            element.set_channel(channel)
