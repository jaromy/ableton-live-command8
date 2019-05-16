
import Live
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement
from consts import *
class ShiftableSelectorComponent(ModeSelectorComponent):
    __doc__ = ' SelectorComponent that assigns buttons to functions based on the shift button '
    def __init__(self, device_bank_buttons, device_param_controls, mute_buttons, encoder_modes, session, mixer, device):
        assert len(device_bank_buttons) == 3
        assert len(device_param_controls) == 8        
        ModeSelectorComponent.__init__(self)
        self._toggle_pressed = False
        self._device_bank_buttons = device_bank_buttons
        self._encoder_modes = encoder_modes
        self._device_param_controls = device_param_controls
        self._mute_buttons = mute_buttons
        self._session = session
        self._mixer = mixer
        self._device = device


    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        self._device_bank_buttons = None
        self._encoder_modes = None
        self._session = None
        self._mixer = None
        self._device = None
        return None


    def set_mode_toggle(self, button):
        ModeSelectorComponent.set_mode_toggle(self, button)
        self.set_mode(0)


    def number_of_modes(self):
        return 2


    def update(self):
        if self.is_enabled():
            if (self._mode_index == 0):
                self._device.set_enabled(False)
                self._encoder_modes.set_enabled(True)            
                for index in range(len(self._mute_buttons)):
                    strip = self._mixer.channel_strip(index)
                    strip.set_mute_button(self._mute_buttons[index])
                    strip.set_arm_button(None)
            elif (self._mode_index == 1):
                self._device.set_enabled(True)
                self._encoder_modes.set_enabled(False)
                for index in range(len(self._mute_buttons)):
                    strip = self._mixer.channel_strip(index)
                    strip.set_mute_button(None)
                    strip.set_arm_button(self._mute_buttons[index])
            else :
                assert False
                
        return None
        

    def _toggle_value(self, value):
        assert self._mode_toggle != None
        assert value in range(128)
        self._toggle_pressed = value > 0
        self.set_mode(int(self._toggle_pressed))
        return None



