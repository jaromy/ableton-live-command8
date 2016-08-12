# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

from _Framework.MixerComponent import MixerComponent 
from SpecialChannelStripComponent import SpecialChannelStripComponent 
from _Framework.ButtonElement import ButtonElement 
class SpecialMixerComponent(MixerComponent):
    ' Special mixer class that uses return tracks alongside midi and audio tracks. Also uses shift button to obtain different modes'
    __module__ = __name__

    def __init__(self, num_tracks, num_returns=0):
        MixerComponent.__init__(self, num_tracks, num_returns)
        self._shift_button = None
        self._shift_pressed = False



    def tracks_to_use(self):
        return (self.song().visible_tracks + self.song().return_tracks)


    def set_shift_button(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if (self._shift_button != button):
            if (self._shift_button != None):
                self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = button
            if (self._shift_button != None):
                self._shift_button.add_value_listener(self._shift_value)
            self.update()



    def _create_strip(self):
        return SpecialChannelStripComponent()


    def _shift_value(self, value):
        assert (self._shift_button != None)
        assert (value in range(128))
        self._shift_pressed = (value != 0)
        self.update()


    #override base class to only handle event if shift is pressed
    def _next_track_value(self, value):
        if not self._shift_pressed:
            MixerComponent._next_track_value(self, value)
            
    #override base class to only handle event if shift is pressed            
    def _prev_track_value(self, value):
        if not self._shift_pressed:
            MixerComponent._prev_track_value(self, value)

            
# local variables:
# tab-width: 4
