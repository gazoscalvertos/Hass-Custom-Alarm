# Home Assistant - Custom Alarm Interface!
## Intro :-)
<img align="right" width="300" height="300" src="https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/BTC.png">

Welcome my fellow modders, tinkerers, home assistant wizards!!

Follow the thread [here](https://community.home-assistant.io/t/yet-another-take-on-an-alarm-system/32386)

Consider donating to this project to keep it going as anything contributed will be placed back in to enable more hardware integration, new features and bug squashing.

This is very much a community project so if you wish to chip in then please do!! I could really use a CSS, animation, design guru to make this look amazing. Also please feel free to leave comments, suggestions, enhancements and fixes!!

### Testing
- Tested on HA v0.61.1

### Changelog

- (16/02/18) NEW FEATURE - Custom Panel allowing custom html/polymer code!!!!!! Use this to bring any other features you would like to see for example displaying live camera feeds, a rotating image gallery, custom HA buttons and sensors. To use this enable the custom panel in alarm.yaml (custom_panel: True) then ensure you take a copy of custom-element.html and add it to you www/alarm/ folder. Edit the html code between the template tags. I'm have added a custom sample folder where I will upload examples of 'things' which can be added here. Please contribute!!!
- (16/02/18) NEW FEATURE - Added the ability to hide the sensor groups (all sensors, immediate sensors, delayed sensors, inactive sensors) from the display. Open sensors will still appear on the display. (hide_sensor_groups:True) see alarm.yaml for details.
- (16/02/18) NEW FEATURE - Added the ability to mask the passcode during diasarm. The feature will be enabled by deault. See the alarm.yaml for extra information. Credit @mikefero

- (16/02/18) BUG FIX - Added further code to force the sidebar to hide when the alarm is armed. This prevents a simple refresh showing the sidebar.
- (16/02/18) BUG FIX - Given the time label has caused folk issues I have decided to drop the javascript implementation and use the time derived from HA. Ensure you have a time sensor setup in your sensors.yaml:
```
  - platform: time_date
    display_options:
      - 'time'
```
- (15/02/18) BUG FIX - Fixed the code disarm issue.

- (19/01/18) NEW FEATURE - MQTT now allows you to disarm your alarm using the your code. MQTT panels will need to support the format of the payload which is 'DISARM CODE' for example 'DISARM 0000'. To override this so that MQTT can disarm the alarm without passing across the code then set override_code: True in the alarm.yaml. Status feedback to MQTT coming soon...
- (19/01/18) NEW FEATURE - The panel now allows you to hide the sidebar when the alarm is activated preventing in intruder to simply go to configuration and shut down HA. A suitable locked down browser will also be required to prevent the intruder simply changing the URL. You could check out kiosk on android. To activate this feature simply enable hide_sidebar: True in the alarm.yaml NOTE!! Ensure you copy alarm_scripts.js into the appropriate folder 'www/alarm'. This was a tricky feature to implement and future HA updates may break this. If anyone has a better idea on how to code this then be my guest.

- (19/01/18) ADDITIONAL STATE - Added 'motion_detected' as a supported state

- (15/01/18) NOTE!!!!!!! - There are a lot of changes, update all files to ensure everything works. (alarm.yaml, panels/alarm.html, custom_components/alarm_control_panel/bwalarm.py, www/lib/countdown360.js, www/lib/jquery-3.2.1.min.js, www/alarm/alarm.css) Also don't forget to clear your browser cache. Raise any issues you come across

- (15/01/18) NEW FEATURE - Set a maximum number of Passcode attempts with a lockout period. See the alarm.yaml for setup.
- (15/01/18) NEW FEATURE - There is now support for custom and unknown device states. Add your new on/off states into the alarm.yaml file and this component will track them!

- (15/01/18) NEW GUI - The code panel slides in or out depending on the mode. Let me know what you think.

- (15/01/18) BUG FIX - Weather alignment on different modes and devices.
- (15/01/18) BUG FIX - Timer mode now appears in warning mode so you know how long before the alarm triggers.
- (15/01/18) BUG FIX - MQTT now allows custom state/command topics via the alarm.yaml.
- (15/01/18) BUG FIX - Re-aligned buttons for smaller devices.

- (15/01/18) OTHER - Work progressing to clean up the python code.
- (15/01/18) OTHER - CSS is now split from the main http file for readability, still requires a cleanse.

- (15/01/18) COMING SOON - MQTT Support to valid passcodes.
- (15/01/18) COMING SOON - MQTT Support to provide extended feedback to other alarm interfaces i.e. open sensor arrays, lockout feedback.
- (15/01/18) COMING SOON - Persistance support for rebooted systems.
- (15/01/18) COMING SOON - Disabling of the sidebar when armed. Trickier than I thought due to the use of polymer and its sandboxing.
- (15/01/18) COMING SOON - User Guide/Help pages
- (15/01/18) COMING SOON - Customizable settings such as gui colours, collapsable sensor groups
- (15/01/18) COMING SOON - Screensaver mode
- (15/01/18) COMING SOON - Granular times on home/arm mode
- (15/01/18) COMING SOON - Screenshots + Videos

- (08/01/17) NEW FEATURE - MQTT Integration. Enable this by setting mqtt to True in the yaml. See alarm.yaml for optional settings. This is based on the [manual mqtt code](https://home-assistant.io/components/alarm_control_panel.manual_mqtt/). [MQTT Needs to be enabled in your HA setup and configured appropriately](https://home-assistant.io/docs/mqtt/broker/#embedded-broker) then you should be able to use [custom panels such as this](https://play.google.com/store/apps/details?id=com.thanksmister.iot.mqtt.alarmpanel&hl=en)

- (28/12/17) Added a new feature 'Panic Mode' this allows you to set a panic code in the alarm.yaml. When using this code to deactivate the alarm, the alarm is deactivated however a special attribute panic_mode is set to ACTIVE. Use this backed with your automations to trigger custom messages to those who can assist.
- (28/12/17) Added support for override sensors. When sensors are placed in this group any which are open when activing the alarm are ignored. 

- (27/12/17) Added support for devices with open/closed, true/false, locked/unlocked, detected/undetected statuses. There are some heavy changes on the code in readiness for a settings page and an optional screensaver.

- (19/11/17) Added optional perimeter mode (activates a 'perimeter' group only) which could also ne known as 'Home Day' mode. Added weather sensor into status bar (You must have dark sky weather component enabled specifically sensor.dark_sky_summary), added 0 to code panel.

- (13/11/17) Added sample automation.yaml. Fixed GUI issues with groups. Outlined base code for 'Perimeter mode'

- (12/11/17) You can now use either homemodeignore or notathome group title for sensors that need to be ignored during home mode
- (12/11/17) Added a check (displays open sensors in highlighted group) for open sensors when setting alarm (changes button text to override alarm). **NOTE** override in alarm.yaml isn't quite ready yet and you will still need to manually override via the button in the interface for now.

## Installation Guide
To get this running add the files (alarm.yaml, panels/alarm.html, custom_components/alarm_control_panel/bwalarm.py, www/lib/countdown360.js, www/lib/jquery-3.2.1.min.js, www/alarm/alarm.css) from this repo into your home assistant configuration directory, then add the following to your configuration.yaml file:

**NOTE:** If you already have a panel_custom.yaml for say floorplan then just copy and paste the code from this repo file into your own panel_custom.yaml to prevent floorplan from being overritten.
**NOTE:** Same goes for Automations.yaml. Append the samples inside of this file into your own automations.yaml

```
alarm_control_panel: !include alarm.yaml
panel_custom: !include panel_custom.yaml
```
### Features:
- MQTT Integration (NEW)
- Passcode Attemps/Lockout (NEW)
- Support for custom device states (NEW)
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

Consider supporting this project and donate! All funds will go towards bringing new features, hardware support and bug squashing!!

- BTC Address: 1NFeyzpKKiKbBYSmCLQZQLxBqJbhSbqmwd
- LTC Address: LTUViN3QUESkQk3mG2hvTzhLRQPVAd269f
- XRP Address: rwuMp76ht6dmGvipxwKr5ZE6VpF7ZKC7qs
- ETH Address: 0xCbeD2D2cf0434370c1ca126707009b876b736609

## Credits
[A great countdown JS that I have slightly modded](https://github.com/johnschult/jquery.countdown360)
