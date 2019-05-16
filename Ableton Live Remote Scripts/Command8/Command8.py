# script for the Avid Command|8 Control Surface

import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.ChannelStripComponent import ChannelStripComponent 
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ChannelTranslationSelector import ChannelTranslationSelector
from _Framework.TransportComponent import TransportComponent
from SpecialMixerComponent import SpecialMixerComponent
from SpecialSessionComponent import SpecialSessionComponent
from SpecialViewControllerComponent import DetailViewControllerComponent
from EncModeSelectorComponent import EncModeSelectorComponent
from RingedEncoderElement import RingedEncoderElement
from ShiftableDeviceComponent import ShiftableDeviceComponent
from ShiftableSelectorComponent import ShiftableSelectorComponent
from ShiftTranslatorComponent import ShiftTranslatorComponent

from consts import *

def make_button(chan, cc_no, name):
    is_momentary = True
    button = ButtonElement(is_momentary, MIDI_CC_TYPE, chan, cc_no)
    button.name = name
    return button
    
    
    
    
class Command8(ControlSurface):
    __doc__ = " Script for Avid Command|8 Control Surface "

    _active_instances = []
    def _combine_active_instances():
        track_offset = 0
        scene_offset = 0
        for instance in Command8._active_instances:
            instance._activate_combination_mode(track_offset, scene_offset)
            track_offset += instance._session.width()
    _combine_active_instances = staticmethod(_combine_active_instances)

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self.set_suppress_rebuild_requests(True)
        self._device_selection_follows_track_selection = True
        self._mute_buttons = []
        self._arm_buttons = []   
        self._bank_nav_buttons = []
        self._track_nav_buttons = []     
        self._shift_button = None
        self._shift_modes = None 
        self._session = None
        self._mixer = None
        self._setup_session_control()
        self._setup_mixer_control()
        self._session.set_mixer(self._mixer)
        self._setup_device_and_transport_control()
        self._setup_custom_components()
        self.set_suppress_rebuild_requests(False)
        self._do_combine()


    def disconnect(self):
        self._do_uncombine()
        self._shift_button = None
        self._shift_modes = None
        self._session = None
        self._mixer = None
        ControlSurface.disconnect(self)


    def _do_combine(self):
        if self not in Command8._active_instances:
            Command8._active_instances.append(self)
            Command8._combine_active_instances()


    def _do_uncombine(self):
        if ((self in Command8._active_instances) and Command8._active_instances.remove(self)):
            self._session.unlink()
            Command8._combine_active_instances()


    def _activate_combination_mode(self, track_offset, scene_offset):
        if TRACK_OFFSET != -1:
            track_offset = TRACK_OFFSET
        if SCENE_OFFSET != -1:
            scene_offset = SCENE_OFFSET
        self._session.link_with_track_offset(track_offset, scene_offset)          


    def _setup_session_control(self):
        is_momentary = True
        self._shift_button = make_button(0, 19, 'Shift_Button')                       
        scene_launch_button = make_button(0, 20, 'Scene_Launch_Button')
        scene_stop_button = make_button(0, 23, 'Scene_Stop_Button')
        scene_up_button = make_button(0, 21, 'Scene_Up_Button')     
        scene_dn_button = make_button(0, 22, 'Scene_Dn_Button')    
        
        self._session = SpecialSessionComponent(NUM_TRACKS, 8)          # num tracks, num scenes
        self._session.name = 'Session_Control'
        self._session.selected_scene().name = 'Selected_Scene'
        self._session.set_select_buttons(scene_dn_button, scene_up_button)
        self._session.selected_scene().set_launch_button(scene_launch_button)
        self._session.set_stop_all_clips_button(scene_stop_button)
        self._bank_nav_buttons.append(make_button(0, 125, 'Bank_Right_Button'))
        self._bank_nav_buttons.append(make_button(0, 124, 'Bank_Left_Button'))
        self._session.set_track_bank_buttons(self._bank_nav_buttons[0], self._bank_nav_buttons[1])
        self._session.set_track_banking_increment(8)
        clip_launch_buttons = []
        clip_stop_buttons = []
        for index in range(NUM_TRACKS):     
            clip_launch_buttons.append(make_button(0 + index, 75, 'Clip_Launch_%d' % index))
            clip_stop_buttons.append(make_button(0 + index, 76, 'Clip_Stop_%d' % index))
            clip_slot = self._session.selected_scene().clip_slot(index)
            clip_slot.set_launch_button(clip_launch_buttons[-1])
            clip_slot.name = 'Selected_Clip_Slot_' + str(index)

        self._session.set_stop_track_clip_buttons(tuple(clip_stop_buttons))
        self._session.set_shift_button(self._shift_button)



    def _setup_mixer_control(self):
        is_momentary = True
        cuelevel = EncoderElement(MIDI_CC_TYPE, 15, 10, Live.MidiMap.MapMode.absolute)
        mastervolume = SliderElement(MIDI_CC_TYPE, 15, 7)
        crossfader = SliderElement(MIDI_CC_TYPE, 14, 7)
        self._mixer = SpecialMixerComponent(NUM_TRACKS, NUM_RETURNS)      
        self._mixer.name = 'Mixer'
        self._mixer.set_shift_button(self._shift_button)
        self._mixer.set_crossfader_control(crossfader)
        self._mixer.set_prehear_volume_control(cuelevel)
        self._mixer.master_strip().set_volume_control(mastervolume)  
        for track in range(NUM_TRACKS):
            strip = self._mixer.channel_strip(track)
            strip.name = 'Channel_Strip_' + str(track)
#             strip.set_arm_button(ButtonElement(not is_momentary, MIDI_CC_TYPE, 0 + track, 16))      #mute and arm will toggle
            strip.set_solo_button(ButtonElement(not is_momentary, MIDI_CC_TYPE, 0 + track, 15))
#             strip.set_mute_button(ButtonElement(not is_momentary, MIDI_CC_TYPE, 0 + track, 14))
            strip.set_volume_control(SliderElement(MIDI_CC_TYPE, 0 + track, 7))
            #strip.set_pan_control(self._ctrl_map[TRACKPAN[track]])
            #strip.set_send_controls((self._ctrl_map[TRACKSENDA[track]], self._ctrl_map[TRACKSENDB[track]], self._ctrl_map[TRACKSENDC[track]]))
            #strip.set_invert_mute_feedback(True)
            strip.set_shift_button(self._shift_button)
        
        for index in range(NUM_RETURNS):
            return_strip = self._mixer.return_strip(index)
            return_strip.name = 'Return_Strip_' + str(index)
            return_strip.set_solo_button(ButtonElement(not is_momentary, MIDI_CC_TYPE, 12 + index, 15))
            return_strip.set_mute_button(ButtonElement(not is_momentary, MIDI_CC_TYPE, 12 + index, 14))
            return_strip.set_volume_control(SliderElement(MIDI_CC_TYPE, 12 + index, 7))
            
            ring_button = ButtonElement(not is_momentary, MIDI_CC_TYPE, 0, 48 + index)  #dummy mapping; no button
            ringed_encoder = RingedEncoderElement(MIDI_CC_TYPE, 12 + index, 10, Live.MidiMap.MapMode.absolute)
            ringed_encoder.name = 'Pan_Control_Return' + str(index)
            ring_button.name = ringed_encoder.name + '_Ring_Mode_Button'
            ringed_encoder.set_ring_mode_button(ring_button)
            return_strip.set_pan_control(ringed_encoder)
            
            
        track_left = ButtonElement(not is_momentary, MIDI_CC_TYPE, 0, 126)      
        track_right = ButtonElement(not is_momentary, MIDI_CC_TYPE, 0, 127)
        self._mixer.set_select_buttons(track_right, track_left)
        self._track_nav_buttons.append(track_left)     #save for later / dual use with device select
        self._track_nav_buttons.append(track_right)    #
        
        
   


    def _setup_device_and_transport_control(self):
        is_momentary = True
        device_bank_buttons = []
        device_param_controls = []
        for index in range(NUM_TRACKS):
            ring_button = ButtonElement(not is_momentary, MIDI_CC_TYPE, 0, 48 + index)  #dummy mapping; no button
            ringed_encoder = RingedEncoderElement(MIDI_CC_TYPE, 0 + index, 10, Live.MidiMap.MapMode.absolute)
            ringed_encoder.name = 'Device_Control_' + str(index)
            ring_button.name = ringed_encoder.name + '_Ring_Mode_Button'
            ringed_encoder.set_ring_mode_button(ring_button)
            device_param_controls.append(ringed_encoder)
        device_bank_labels = ('Bank_1', 'Bank_2', 'Bank_3')
        for index in range(3):
            device_bank_buttons.append(ButtonElement(not is_momentary, MIDI_CC_TYPE, 0, 85 + index))
            device_bank_buttons[-1].name = device_bank_labels[index]
            
        self._device = ShiftableDeviceComponent()
        self._device.name = 'Device_Component'            
        
        self._device.set_bank_nav_buttons(self._bank_nav_buttons[1], self._bank_nav_buttons[0])
        if None not in device_bank_buttons:
            self._device.set_bank_buttons(tuple(device_bank_buttons))
        if None not in device_param_controls:
            self._device.set_parameter_controls(tuple(device_param_controls))
        self._device.set_shift_button(self._shift_button)
        
        self.set_device_component(self._device)     


        detail_view_toggler = DetailViewControllerComponent()
        detail_view_toggler.name = 'Detail_View_Control'
        detail_view_toggler.set_shift_button(self._shift_button)
        detail_view_toggler.set_device_nav_buttons(self._track_nav_buttons[0], self._track_nav_buttons[1])      #dual-use buttons w/shift modifier

        transport = TransportComponent()
        tempo_ring_button = ButtonElement(not is_momentary, MIDI_CC_TYPE, 0, 55)    #dummy mapping; no button    
        tempo_encoder = RingedEncoderElement(MIDI_CC_TYPE, 14, 102, Live.MidiMap.MapMode.absolute)
        tempo_encoder.name = 'Tempo_Control_' + str(index)
        tempo_ring_button.name = tempo_encoder.name + '_Ring_Mode_Button'
        tempo_encoder.set_ring_mode_button(tempo_ring_button)
        transport.set_tempo_control(tempo_encoder)





    def _setup_custom_components(self):
        is_momentary = True             
        mute_buttons = []            #mute and arm will toggle; only need to define one, since one physical button    
        for track in range(NUM_TRACKS):
            mute_buttons.append(ButtonElement(not is_momentary, MIDI_CC_TYPE, 0 + track, 14))
            mute_buttons[-1].name = str(track) + '_Mute_Button'            
            
        encoder_modes = EncModeSelectorComponent(self._mixer)
        encoder_modes.name = 'Track_Control_Modes'
        encoder_modes.set_modes_buttons(self._device._bank_buttons)
        encoder_modes.set_controls(tuple(self._device._parameter_controls))
        encoder_modes.set_shift_button(self._shift_button)
        global_translation_selector = ChannelTranslationSelector()
        global_translation_selector.name = 'Global_Translations'
        global_translation_selector.set_controls_to_translate(tuple(self._device._parameter_controls))
        global_translation_selector.set_mode_buttons(tuple(self._device._bank_buttons))

        bank_button_translator = ShiftTranslatorComponent()
        bank_button_translator.set_controls_to_translate(tuple(self._device._bank_buttons))
        bank_button_translator.set_shift_button(self._shift_button)

        self._shift_modes = ShiftableSelectorComponent(tuple(self._device._bank_buttons), tuple(self._device._parameter_controls), tuple(mute_buttons), encoder_modes, self._session, self._mixer, self._device)
        self._shift_modes.name = 'Shift_Modes'
        self._shift_modes.set_mode_toggle(self._shift_button)








