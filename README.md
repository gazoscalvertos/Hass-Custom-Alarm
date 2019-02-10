# Home Assistant - Custom Alarm Interface!
## Intro :-)

Welcome my fellow modders, tinkerers, home assistant wizards!!

Follow the thread [here](https://community.home-assistant.io/t/yet-another-take-on-an-alarm-system/32386)

Consider donating to this project to keep it going as anything contributed will be placed back in to enable more hardware integration, new features and bug squashing.

This is very much a community project so if you wish to chip in then please do!! I could really use a CSS, animation, design guru to make this look amazing. Also please feel free to leave comments, suggestions, enhancements and fixes!!

**NOTE!!! MAJOR CHANGE** It's time to publish the New UI and settings into the master release.

## Installation

You will need to copy the following files into your home assistant configuration directory

alarm.yaml	*This files stores your alarm configuration. An options page will be created for this file*
custom_components/alarm_control_panel/bwalarm.py *The brains of the operation. This is the logic of the custom alarm system*
panels/alarm.html *This is the interface for the custom alarm component. It's actually optional as the alarm will function without it but recommended for ease of setup*
www/alarm/[ALL FILES] *These files control how the interface looks and feels*
www/lib/[ALL FILES] *These files add additional functionality to the interface in order to work*
www/images/ha.png *An image file used for the interface log*

To get things working with Home Assistant (HA) you will need to adjust your configuration.yaml to instruct HA to use your new custom alarm component, add the following to this file:
```
alarm_control_panel: !include alarm.yaml
```
You will also need to tell HA where your new panel interface file is. Also add the following to your configuration.yaml:
```
panel_custom: !include panel_custom.yaml
```
You may need to restart HA if the component doesn't load first time as HA will need to install a dependency (ruamel.yaml).

It's advisable to start with a new alarm.yaml file with the minimum configuration set:
```
platform: bwalarm
name: House
```
Your new interface can be used to modify your alarm.yaml directly.

The default password to access the settings page is: **HG28!!&dn**

Please test and provide feedback/suggestions.

### Features:
- State specific groups and times (NEW)
- User specific codes
- Panic Mode
- MQTT Integration
- Floorplan Integration
- Alarm State Persistence on reboots/power restore
- Lockout of HA sidebar when armed
- Custom Panel allowing your own html to display whatever you choose (Cameras, Sliding Images etc)
- Passcode Attemps/Lockout
- Support for custom device states
- Code panel 0-9 on disarm only
- Weather Status (Optional) - **NOTE:** Weather sensor nows supports generic sensors (sensor.weather_summary & sensor.weather_temperature) if these are not found then it will default to the dark sky sensors (sensor.dark_sky_summary & sensor.dark_sky_temperature)
- Perimeter Mode (Optional) - I use this to only arm a particular set of sensors (doors) whilst I'm using all floors.
- Masks passcode on entry
- clock display (Optional)
- Digit code entry on disarm
- Themed colours depending on alarm state
- Countdown timer on 'Pending' state
- Notification of Open Sensors with the option to override
- Information/Debug panel

### Testing
- Tested on HA v0.87 and below.

### Change Log:
- 10/02/19:
- [FIX] Panel lockout display
- [FIX] HA 0.87 compatibility
- [REQUEST] Included switches into the sensor lists as requested
- [ENHANCEMENT] Modified the layouts due to polymer changes

- 27/11/18:
- [FEATURE] Adding some basic error handling which will be enhanced at a later date
- [FIX BUG] Fixed margin issue in firefox (settings)
- [REQUEST] Sorted sensors alphabetically
- [FIX BUG] Fixed clock, serif, weather, passcode display issues

- 22/11/18:
- Quite a few bugs and issues have been resolved on this release. There has also been a number of changes to the config file layout so you are likely required to start from scratch as the users, themes and panel settings have changed.

- Updated alarm.html to 1.3.3
- Updated bwalarm.py to 1.1.3

- fixed duplicate sensors in settings panel
- fixed passcode attempts setting
- fixed code to arm display issues
- fixed persistant mode
- fixed sesnor groups
- fixed code to arm panel display and alignment
- reformated logs
- fixed log (displaying name and image)
- removed windows line feed
- integrated HASS users into alarm automatically however these initially are disabled
- fixed switch breaks on service call
- fixed themes

## Note!
Beware, here be dragons! There may be bugs, issues whilst I get this off the ground and there will definately be design problems when used with different size browsers etc. Hopefully we can conquer these in due course!..

## Thanks!
Thanks to the community for all the input into this.

Consider supporting this project and donate! All funds will go towards bringing new features, hardware support and bug squashing!!

- BTC Address: 1NFeyzpKKiKbBYSmCLQZQLxBqJbhSbqmwd
- LTC Address: LTUViN3QUESkQk3mG2hvTzhLRQPVAd269f
- XRP Address: rwuMp76ht6dmGvipxwKr5ZE6VpF7ZKC7qs
- ETH Address: 0xCbeD2D2cf0434370c1ca126707009b876b736609
- Paypal: ha.custom.alarm@gmail.com

## Credits
[A great countdown JS that I have slightly modded](https://github.com/johnschult/jquery.countdown360)
