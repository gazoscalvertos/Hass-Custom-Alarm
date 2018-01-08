# Home Assistant - Custom Alarm Interface!
## Intro :-)
<img align="right" width="300" height="300" src="https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/BTC.png">

Welcome my fellow modders, tinkerers, home assistant wizards!!

Follow the new thread [here](https://community.home-assistant.io/t/yet-another-take-on-an-alarm-system/32386)

This repo is a custom take on the [default alarm provided in this link](https://home-assistant.io/components/alarm_control_panel.manual/)

First of all a big thanks to @drytoastman [for getting this off the ground](https://community.home-assistant.io/t/a-different-take-on-an-alarm-system/7809)

This is very much a community project so if you wish to chip in then please do!! I could really use a CSS, animation, design guru to make this look amazing. Also please feel free to leave comments, suggestions, enhancements and fixes!!

### Testing
- Tested on HA v0.60.1

### Changelog
- (08/01/17) NEW FEATURE - MQTT Integration. Enable this by setting mqtt to True in the yaml. See alarm.yaml for optional settings. This is based on the [manual mqtt code](https://home-assistant.io/components/alarm_control_panel.manual_mqtt/). [MQTT Needs to be enabled in your HA setup and configured appropriately](https://home-assistant.io/docs/mqtt/broker/#embedded-broker) then you should be able to use [custom panels such as this](https://play.google.com/store/apps/details?id=com.thanksmister.iot.mqtt.alarmpanel&hl=en)
- (28/12/17) Added a new feature 'Panic Mode' this allows you to set a panic code in the alarm.yaml. When using this code to deactivate the alarm, the alarm is deactivated however a special attribute panic_mode is set to ACTIVE. Use this backed with your automations to trigger custom messages to those who can assist.
- (28/12/17) Added support for override sensors. When sensors are placed in this group any which are open when activing the alarm are ignored. 
- (27/12/17) Added support for devices with open/closed, true/false, locked/unlocked, detected/undetected statuses. There are some heavy changes on the code in readiness for a settings page and an optional screensaver.
- (19/11/17) Added optional perimeter mode (activates a 'perimeter' group only) which could also ne known as 'Home Day' mode. Added weather sensor into status bar (You must have dark sky weather component enabled specifically sensor.dark_sky_summary), added 0 to code panel.
- (13/11/17) Added sample automation.yaml. Fixed GUI issues with groups. Outlined base code for 'Perimeter mode'
- (12/11/17) You can now use either homemodeignore or notathome group title for sensors that need to be ignored during home mode
- (12/11/17) Added a check (displays open sensors in highlighted group) for open sensors when setting alarm (changes button text to override alarm). **NOTE** override in alarm.yaml isn't quite ready yet and you will still need to manually override via the button in the interface for now.

## Installation Guide
To get this running add the files (alarm.yaml, panels/alarm.html, custom_components/alarm_control_panel/bwalarm.py) from this repo into your home assistant configuration directory, then add the following to your configuration.yaml file:

**NOTE:** If you already have a panel_custom.yaml for say floorplan then just copy and paste the code from this repo file into your own panel_custom.yaml to prevent floorplan from being overritten.
**NOTE:** Same goes for Automations.yaml. Append the samples inside of this file into your own automations.yaml

```
alarm_control_panel: !include alarm.yaml
panel_custom: !include panel_custom.yaml
```
### Features:
- MQTT Integration
- Code panel 0-9 on disarm only
- Weather Status (Optional) - **NOTE:** You must have dark sky weather component enabled specifically sensor.dark_sky_summary.
- Peimeter Mode (Optional) - Allows you to part activate the alarm in Home Day mode. I use this to only arm a particular set of sensors (doors) whilst im using all floors.
- clock display (Optional)
- Digit code entry on disarm
- Themed colours depending on alarm state
- Countdown timer on 'Pending' state
- Panic Mode
- Notification of Open Sensors with the option to override

### To be implemented:
- Settings page to adjust non-critical features (colours/information)
- MQTT Support
- Debug Mode available in settings
- Screensaver
- Lockout of HA sidebar when armed
- delayed and immediate mode 'per' alarm activation (home/away/perimeter?)
- Customisable Themes
  - Time Based themes (Dark at Night - Light during day)
  - Possibly a full black one with a Cylon style bar when activated?
  - Please submit some ideas here
- Guest mode / reduced feature set
- Clean up of code (html/css/python)
- Anything anyone else can think of

## Note!
Beware, here be dragons! There may be bugs, issues whilst I get this off the ground and there will definately be design problems when used with different size browsers etc. Hopefully we can conquer these in due course!..

## Thanks!
Thanks to the community for all the input into this.

All of this modding, coding, tinkering is very thirsty work. Consider buying me a beer :beer: :+1:

BTC Address: 1NFeyzpKKiKbBYSmCLQZQLxBqJbhSbqmwd

## Credits
[A great countdown JS that I have slightly modded](https://github.com/johnschult/jquery.countdown360)
