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

## Timings
- **pending_time:** 25 #[REQUIRED, Number] Grace time in seconds to allow for exit and entry using Away mode. Default 25
- **trigger_time:** 600 #[REQUIRED, Number] The time in seconds of the trigger time in which the alarm is firing.  before returning previous set alarm state. Default 600 (10 minutes)
- **armed_home:** #This can either be armed_home/armed_away/armed_perimeter
-- **pending_time:** 10 #State specific setting
-- **trigger_time:** 300 #State specific setting

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