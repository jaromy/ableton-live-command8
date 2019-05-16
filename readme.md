# Ableton Live Command|8

Remote MIDI Script for using Command|8 control surface in Ableton Live

## Getting Started


### Prerequisites

* Ableton Live 8 (may work on later versions, but only tested on 8.4.2)
* Digidesign Command|8 control surface (tested using firmware v02.01.02)

### Installing

1. **Copy 'Command8' folder to the Remote Scripts location for Ableton Live:**

	* Windows: \ProgramData\Ableton\Live x.x\Resources\MIDI Remote Scripts\  
	(This folder is hidden by default)
	* Mac: The Remote Script folder is inside the Ableton Live application bundle. Locate the Live application in Finder, right click on it and select "Show Package Content". Then navigate to: /Contents/App-Resources/MIDI Remote Scripts/


	For more info, see instructions on Ableton website: [installing third-party control surfaces](https://help.ableton.com/hc/en-us/articles/209072009-Installing-Third-Party-Control-Surfaces)

2. **Upload SysEx file containing stand-alone preset to Command|8:**
	* File: 'command8-preset-ableton-live.syx' 
	* This can be done via Pro Tools, or using another MIDI application. 
	* For additional help, see Command|8 User Guide:  **"Loading and Saving Presets with SysEx"** in the section
	 **"Using Stand-Alone Mode"**


## Usage

There are three modes:

1. ***Base*** - i.e. normal mode. Faders are mapped to volume for each track. Same for mute & solo buttons. Encoders are mapped to pan L/R for each track.
Select buttons will launch the first clip for each track.

2. ***Bank*** - when 'bank' button is engaged on Command|8, this allows access to the Master volume, Return A, and Return B levels via the upper most 4 faders (far right on console).
Additionally, crossfade is assigned to a fader. Cue Level and tempo are assigned to the two upper-most (far right) encoders.

3. ***Shift*** - when 'EQ' button is engaged on Command|8, this activates an alternate 'bank' of functionality as follows:
	* *Mute Buttons* - these control the record/arm status for each track
	* *Encoders* - these control device parameters for any device on the currently selected track. E.g, if you have an instance of Impulse running on a track, the encoders would allow you to adjust the volume for each drum part (kick, snare, hi-hat, etc).

For more info, there are PDF diagrams of the console in the 'docs' folder that describe what each button does for each of the three modes.


Additionally, the top row of buttons has special functionality that affects the rest of the console:

* **EQ (Shift)** - accesses "Shift" mode
* **Dynamics (Pan)** - assigns encoders to track pan L/R
* **Insert (Send A Select)** - assigns encoders to Send A level
* **Pan/Send/PRE (Send B Select)** - assigns encoders to Send B level
* **< Page (Bank L)** - addresses the next 8 tracks to the left
* **Page > (Bank R)** - addresses the next 8 tracks to the right
* **Master Bypass (Track Select L)** - selects the track to the left of the current selected track
* **Esc (Track Select R)** - selects the track to the right of the current selected track




## Versioning
| Version       | Author| Date   			| Description						|
| ------------- |:-----:| :-------------- | :-------------------------- |
| 1.0      		 | JJR 	| August 12, 2016 | Initial Version					|


## Authors

* **Jaromy Russo** - *Initial work* - [Jaromy on GitHub](https://github.com/jaromy)

## License

This project is licensed under the GPL v3.0 License.

