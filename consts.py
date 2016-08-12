# Combination Mode offsets
# ------------------------
TRACK_OFFSET = -1 #offset from the left of linked session origin; set to -1 for auto-joining of multiple instances
SCENE_OFFSET = 0 #offset from the top of linked session origin (no auto-join)


#For Command|8 we'll only use banks of 8 faders, even though there is a 'Bank' button on the Command|8 that will allow us to send 16.
# Ableton Live is set up to use banks of 8, and we want to be able to use the encoders as dual-use for device parameters and sends, pans, etc.
NUM_TRACKS = 8     # physical track count on h/w device (i.e number of faders) for audio/midi
NUM_RETURNS = 2     # physical return track count on h/w device (send/returns only)