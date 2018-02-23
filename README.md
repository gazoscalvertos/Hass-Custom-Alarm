# Home Assistant - Custom Alarm Interface!
## Intro :-)
<img align="right" width="376.5" height="525" src="https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/BTC.png">

Welcome my fellow modders, tinkerers, home assistant wizards!!

Follow the thread [here](https://community.home-assistant.io/t/yet-another-take-on-an-alarm-system/32386)

Consider donating to this project to keep it going as anything contributed will be placed back in to enable more hardware integration, new features and bug squashing.

This is very much a community project so if you wish to chip in then please do!! I could really use a CSS, animation, design guru to make this look amazing. Also please feel free to leave comments, suggestions, enhancements and fixes!!

### Features:
- MQTT Integration
- Alarm State Persistence on reboots/power restore (NEW)
- Lockout of HA sidebar when armed (NEW)
- Custom Panel allowing your own html to display whatever you choose (Cameras, Sliding Images etc) (NEW)
- Passcode Attemps/Lockout
- Support for custom device states
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
- delayed and immediate mode 'per' alarm activation (home/away/perimeter?)
- Customisable Themes
  - Time Based themes (Dark at Night - Light during day)
  - Possibly a full black one with a Cylon style bar when activated?
  - Please submit some ideas here
- Guest mode / reduced feature set
- Clean up of code (html/css/python)
- Anything anyone else can think of

## Installation Guide
To get this running add the files (alarm.yaml, panels/alarm.html, custom_components/alarm_control_panel/bwalarm.py, www/lib/countdown360.js, www/lib/jquery-3.2.1.min.js, www/alarm/alarm.css) from this repo into your home assistant configuration directory, then add the following to your configuration.yaml file:

**NOTE:** If you already have a panel_custom.yaml for say floorplan then just copy and paste the code from this repo file into your own panel_custom.yaml to prevent floorplan from being overritten.
**NOTE:** Same goes for Automations.yaml. Append the samples inside of this file into your own automations.yaml

```
alarm_control_panel: !include alarm.yaml
panel_custom: !include panel_custom.yaml
```
## Configuration variables:

**Alarm.yaml configuration settings:**

- platform: bwalarm **#[REQUIRED, String] Name of the custom alarm component. Do not change**
- name: House **#[REQUIRED, String]This can be changed to whatever suits your need, ensure this attribute matches the one in your panel_custom.yaml 'alarmid: alarm_control_panel.house'**

- code: '9876' **#[REQUIRED, digits] should consist of one or more digits ie '6482' ensure your passcode is encapsulated by quotes**
- panic_code: '1234' **#[OPTIONAL, digits] Panic Code should consist of one or more digits ie '1234' ensure your passcode is encapsulated by quotes, it needs to be different to your standard alarm code. This enables a special panic mode. This can be used under duress to deactivate the alarm which would appear to the unseeing eye as deactivated however a special attribute [panic_mode] listed under the alarm_control_panel.[identifier] will change to ACTIVE. This status could be used in your automations to send a notification to someone else police/spouse/sibling/neighbour that you are under duress. To deactive this mode arm then disarm your alarm in the usual manner.**

- pending_time: 25 **#[REQUIRED, Number] Grace time in seconds to allow for exit and entry using Away mode**
- trigger_time: 600 **#[REQUIRED, Number] How long the trigger runs before returning to the previos set alarm state**

- alarm: automation.alarm_triggered **#[REQUIRED, String] The automation to fire when the alarm has been triggered**
- warning: automation.alarm_warning **#[OPTIONAL, String] The automation to fire when the alarm has been tripped**
#### [OPTIONAL SETTINGS] 
- clock: True  **#[OPTIONAL, Boolean] False by default. True enables a clock in the center of the status bar**
- perimeter_mode: True **#[OPTIONAL, Boolean] False by default. True enables perimeter mode, this could be known as 'Day Mode' i.e. only arm the doors whilst there is someone using all floors**
- weather: True **#[OPTIONAL, Boolean] False by Default. Allows a weather summary to be displayed on the status bar. Dark Sky weather component must be enabled with the name sensor.dark_sky_summary**
- persistence: False **#[OPTIONAL, Boolean] False by Default. Allows this custom component to save the state of the alarm to file then reinstate it in the event of power loss.**
- hide_passcode: True **#[OPTIONAL, Boolean] True by default. This is a security feature when enabled hides the passcode while entering disarm code.**
- hide_sidebar: True **#[OPTIONAL, Boolean] False by default. This is a security feature when enabled hides the HA sidebar when the alarm is armed. The sidebar re-appears when the alarm is disarmed.**
- hide_sensor_groups: True **#[OPTIONAL, Boolean] - False by default. Setting this to True hides sensor groups (all sensors, immediate sensors, delayed sensors, inactive sensors) from the display. Open sensors will still appear**
-hide_custom_panel: True **#[OPTIONAL, Boolean] - True by default. Setting this to False enables a custom panel below the sensors groups which allows you to add your own html code. Use this to bring any other features you would like to see for example displaying live camera feeds, a rotating image gallery, custom HA buttons and sensors. To use this enable the custom panel in alarm.yaml (custom_panel: True) then ensure you take a copy of custom-element.html and add it to you www/alarm/ folder. Edit the html code between the template tags. I'm have added a custom sample folder where I will upload examples of 'things' which can be added here. Please contribute!!!**

### [PASSCODE RELATED]
- passcode_attempts: 3 #[OPTIONAL, number] Disabled if commented out. When a value equal or greater than 0 is set, the system will only allow the set amount of password attempts before timing out
- passcode_attempts_timeout: 30 #[OPTIONAL, number] Default 30 seconds. When set with the password attempts option the panel will timeout for the amount of seconds set if the password is entered incorrectly as per the password_attempts option. The system will then reset the allowed password attempts

### [MQTT RELATED]
- mqtt: True #[OPTIONAL, boolean] False by default. Settings this to True will enable MQTT Mode. Uncomment options below to use See the README for guidance.
- override_code: True #[OPTIONAL, boolean] False by default. if true allows MQTT commands to disarm the alarm without a valid code.
- state_topic: 'home/alarm' #[OPTIONAL, string] The MQTT topic HA will publish state updates to.
- command_topic: 'home/alarm/set' #[OPTIONAL, string] The MQTT topic HA will subscribe to, to receive commands from a remote device to change the alarm state.
- qos: 0 #[OPTIONAL, number] The maximum QoS level for subscribing and publishing to MQTT messages. Default is 0.
- payload_disarm: "DISARM" #[OPTIONAL, string] The payload to disarm this Alarm Panel. Default is “DISARM”.
- payload_arm_home: "ARM_HOME" #[OPTIONAL, string] The payload to set armed-home mode on this Alarm Panel. Default is “ARM_HOME”.
- payload_arm_away: "ARM_AWAY" #[OPTIONAL, string] The payload to set armed-away mode on this Alarm Panel. Default is “ARM_AWAY”.
- payload_arm_night: "ARM_NIGHT" #[OPTIONAL, string] The payload to set armed-night mode on this Alarm Panel. Default is “ARM_NIGHT”.

### [COLOURS]  Use any HTML format
- warning_colour: 'orange' #[OPTIONAL, string]
- pending_colour: 'orange' #[OPTIONAL, string]
- disarmed_colour: '#03A9F4' #[OPTIONAL, string]
- armed_home_colour: 'black' #[OPTIONAL, string]
- armed_away_colour: 'black' #[OPTIONAL, string]
- triggered_colour: 'red' #[OPTIONAL, string]

### [SENSOR GROUPS]
- immediate: #[OPTIONAL, list of entities] Sensors in this group tigger the alarm immediately
-- binary_sensor.top_floor_multi_sensor_sensor #EXAMPLE
-- binary_sensor.lounge_multi_sensor_sensor #EXAMPLE
- delayed: #[OPTIONAL, list of entities] Sensors in this group start the clock (pending_time) when tripped before the alarm is activated in 'Away' mode
-- binary_sensor.kitchen_multi_sensor_sensor #EXAMPLE
-- binary_sensor.hall_multi_sensor_sensor #EXAMPLE
- homemodeignore: #[OPTIONAL, list of entities], Same as notathome but hopefully the title is more self explanatory. Can still use notathome for backwards compatibility, Note sensors can exist in more than one group notice top_floor appears in two groups
-- binary_sensor.top_floor_multi_sensor_sensor #EXAMPLE
- override: #[OPTIONAL, list of entities] Use this group to automatically override the warning message on open sensors when setting 'away' mode. (I use this as I have a motion sensor at the front door)
-- binary_sensor.hall_multi_sensor_sensor #EXAMPLE
- perimeter: #[OPTIONAL, list of entities] This group is special and only effects 'perimeter mode'. If perimeter_mode is enabled then any sensor in this group will trigger the alarm immediately if arm perimeter is set. There is no delayed group for this mode (unless requested as a feature of course!)
-- binary_sensor.toilet_window_sensor #EXAMPLE

### [CUSTOM STATUSES]
-custom_supported_statuses_on: #[OPTIONAL, list of strings] CUSTOM SENSOR STATUSES - These settings allow devices which are not natively supported by this panel to be used. This is to be used when the state of the device is not recognised by the panel. Examples are provided below 
-- 'running' #EXAMPLE
-custom_supported_statuses_off:
-- 'not_running' #EXAMPLE

### Testing
- Tested on HA v0.63.2

### Changelog
- (23/02/18) NEW FEATURE - Override the pending time when arming away mode so that the alarm arms instantly. To do this pass a code parameter of '-1' to the service, this could be in the form of an automation such as:
```
  alias: '[Alarm] Instantly Arm Away Mode'
  trigger:
  ... place your trigger here ...
  action:
  - service: alarm_control_panel.alarm_arm_away
    entity_id: alarm_control_panel.house
    data:
      code: '-1'
``` 

- (16/02/18) NEW FEATURE - PERSISTENCE!!!!!!!! Enabling persistence in the alarm.yaml file allows this component to save the alarm state everytime it changes. This means if there is a power outage or server crash/failure then upon restart HA will auto load the previous alarm state. This has not been tested in windows but in theory should work. Ensure HA has permission to write to the config folder as this creates a new file named alarm.json.
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
