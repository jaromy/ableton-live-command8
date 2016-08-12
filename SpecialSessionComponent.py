# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

import Live
from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement
class SpecialSessionComponent(SessionComponent):
    " Special SessionComponent for APC combination mode and button to fire selected clip slot. Also uses shift button to obtain different modes "
    __module__ = __name__

    def __init__(self, num_tracks, num_scenes):
        SessionComponent.__init__(self, num_tracks, num_scenes)
        self._slot_launch_button = None
        self._shift_button = None
        self._shift_pressed = False


    def disconnect(self):
        SessionComponent.disconnect(self)
        if (self._slot_launch_button != None):
            self._slot_launch_button.remove_value_listener(self._slot_launch_value)
            self._slot_launch_button = None


    def set_shift_button(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if (self._shift_button != button):
            if (self._shift_button != None):
                self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = button
            if (self._shift_button != None):
                self._shift_button.add_value_listener(self._shift_value)
            self.update()


    def link_with_track_offset(self, track_offset, scene_offset):
        assert (track_offset >= 0)
        assert (scene_offset >= 0)
        if self._is_linked():
            self._unlink()
        self.set_offsets(track_offset, scene_offset)
        self._link()


    def unlink(self):
        if self._is_linked():
            self._unlink()


    def set_slot_launch_button(self, button):
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._slot_launch_button != button):
            if (self._slot_launch_button != None):
                self._slot_launch_button.remove_value_listener(self._slot_launch_value)
            self._slot_launch_button = button
            if (self._slot_launch_button != None):
                self._slot_launch_button.add_value_listener(self._slot_launch_value)

            self.update()


    def _slot_launch_value(self, value):
        assert (value in range(128))
        assert (self._slot_launch_button != None)
        if self.is_enabled():
            if ((value != 0) or (not self._slot_launch_button.is_momentary())):
                if (self.song().view.highlighted_clip_slot != None):
                    self.song().view.highlighted_clip_slot.fire()


    def _shift_value(self, value):
        assert (self._shift_button != None)
        assert (value in range(128))
        self._shift_pressed = (value != 0)
        self.update()


    #override base class to only handle event if shift is not pressed
    def _bank_left_value(self, value):
        if not self._shift_pressed:
            SessionComponent._bank_left_value(self, value)
 
    #override base class to only handle event if shift is not pressed
    def _bank_right_value(self, value):
        if not self._shift_pressed:
            SessionComponent._bank_right_value(self, value)
   
   
#     #override base class to only handle event if shift is pressed 
#     # (otherwise, button is clip launch button
#     def _stop_track_value(self, value, sender):
#         if self._shift_pressed:
#             SessionComponent._stop_track_value(self, value, sender)
            

            

# local variables:
# tab-width: 4
