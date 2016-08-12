
from _Framework.ModeSelectorComponent import ModeSelectorComponent 
from _Framework.ButtonElement import ButtonElement 
from _Framework.MixerComponent import MixerComponent 
class EncModeSelectorComponent(ModeSelectorComponent):
    ' Class that reassigns encoders to different mixer functions. Makes use of shift for the mode selectors. '

    def __init__(self, mixer):
        assert isinstance(mixer, MixerComponent)
        ModeSelectorComponent.__init__(self)
        self._controls = None
        self._mixer = mixer
        self._shift_button = None
        self._shift_pressed = False

    def disconnect(self):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._controls = None
        self._mixer = None
        ModeSelectorComponent.disconnect(self)


    def set_shift_button(self, button):
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if (self._shift_button != button):
            if (self._shift_button != None):
                self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = button
            if (self._shift_button != None):
                self._shift_button.add_value_listener(self._shift_value)
            self.update()


    def set_modes_buttons(self, buttons):
        assert ((buttons == None) or (isinstance(buttons, tuple) or (len(buttons) == self.number_of_modes())))
        identify_sender = True
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if (buttons != None):
            for button in buttons:
                assert isinstance(button, ButtonElement)
                self._modes_buttons.append(button)
                button.add_value_listener(self._mode_value, identify_sender)

        self.set_mode(0)
        self.update()


    def set_controls(self, controls):
        assert ((controls == None) or (isinstance(controls, tuple)))  #jjr - remaining part is leftover from Axiom code -#  and (len(controls) == 8)))
        self._controls = controls
        self.set_mode(0)
        self.update()


    def number_of_modes(self):
        return 3



    def on_enabled_changed(self):
        if (not self._shift_pressed):
            self.set_mode(self._mode_index)
        self.update()


    def update(self):
        assert (self._modes_buttons != None)
        if self.is_enabled() and not self._shift_pressed:
            if (self._modes_buttons != None):
                for index in range(len(self._modes_buttons)):
                    if (index == self._mode_index):
                        self._modes_buttons[index].turn_on()
                    else:
                        self._modes_buttons[index].turn_off()

            if (self._controls != None):            
                for index in range(len(self._controls)):
                    if (self._mode_index == 0):
                        self._mixer.channel_strip(index).set_pan_control(self._controls[index])
                        self._mixer.channel_strip(index).set_send_controls((None, None))
                    elif (self._mode_index == 1):
                        self._mixer.channel_strip(index).set_pan_control(None)
                        self._mixer.channel_strip(index).set_send_controls((self._controls[index], None))
                    elif (self._mode_index == 2):
                        self._mixer.channel_strip(index).set_pan_control(None)
                        self._mixer.channel_strip(index).set_send_controls((None, self._controls[index]))
                    else:
                        print 'Invalid mode index'
                        assert False
            #self._rebuild_callback()


    def _shift_value(self, value):
        assert (self._shift_button != None)
        assert (value in range(128))
        self._shift_pressed = (value != 0)
        self.update()
