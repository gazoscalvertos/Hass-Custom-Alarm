## Configuration variables:

**bwlarm.yaml configuration settings:**

- platform: bwalarm **#[REQUIRED, String] Name of the custom alarm component. Do not change**
- name: House **#[OPTIONAL, String]Do not change**

- code: '9876' **#[REQUIRED, digits] should consist of one or more digits ie '6482' ensure your passcode is encapsulated by quotes**
- panic_code: '1234' **#[OPTIONAL, digits] Panic Code should consist of one or more digits ie '1234' ensure your passcode is encapsulated by quotes, it needs to be different to your standard alarm code. This enables a special panic mode. This can be used under duress to deactivate the alarm which would appear to the unseeing eye as deactivated however a special attribute [panic_mode] listed under the alarm_control_panel.[identifier] will change to ACTIVE. This status could be used in your automations to send a notification to someone else police/spouse/sibling/neighbour that you are under duress. To deactive this mode arm then disarm your alarm in the usual manner.**

- code_to_arm: False **#[OPTIONAL, Boolean] False by default. If True, to set alarm via panel/MQTT command/service call you need to supply a master/user code**

- alarm: automation.alarm_triggered **#[REQUIRED, String] The automation to fire when the alarm has been triggered**
- warning: automation.alarm_warning **#[OPTIONAL, String] The automation to fire when the alarm has been tripped**
#### [OPTIONAL SETTINGS]
- clock: True  **#[OPTIONAL, Boolean] False by default. True enables a clock in the center of the status bar**
- enable_night_mode: False **#[OPTIONAL, Boolean] False by default. True enables what could be known as 'Perimeter Mode' i.e. only arm the doors whilst there is someone using all floors**
- weather: True **#[OPTIONAL, Boolean] False by Default. Allows a weather summary to be displayed on the status bar. Dark Sky weather component must be enabled with the name sensor.dark_sky_summary**
- persistence: False **#[OPTIONAL, Boolean] False by Default. Allows this custom component to save the state of the alarm to file then reinstate it in the event of power loss.**
- ignore_open_sensors: False **#[OPTIONAL, Boolean] False by Default. If False, set alarm only if there is no active sensors, otherwise always set alarm**
- hide_passcode: True **#[OPTIONAL, Boolean] True by default. This is a security feature when enabled hides the passcode while entering disarm code.**
- hide_sidebar: True **#[OPTIONAL, Boolean] False by default. This is a security feature when enabled hides the HA sidebar when the alarm is armed. The sidebar re-appears when the alarm is disarmed.**
- hide_sensor_groups: True **#[OPTIONAL, Boolean] - False by default. Setting this to True hides sensor groups (all sensors, immediate sensors, delayed sensors, inactive sensors) from the display. Open sensors will still appear**
-hide_custom_panel: True **#[OPTIONAL, Boolean] - True by default. Setting this to False enables a custom panel below the sensors groups which allows you to add your own html code. Use this to bring any other features you would like to see for example displaying live camera feeds, a rotating image gallery, custom HA buttons and sensors. To use this enable the custom panel in alarm.yaml (custom_panel: True) then ensure you take a copy of custom-element.html and add it to you www/alarm/ folder. Edit the html code between the template tags. I'm have added a custom sample folder where I will upload examples of 'things' which can be added here. Please contribute!!!**

## Timings
- **pending_time:** 25 #[OPTIONAL, Number, default 25] Grace time in seconds to allow for exit and entry using Away mode.
- **trigger_time:** 600 #[OPTIONAL, Number, default 600] The time in seconds of the trigger time in which the alarm is firing.  before returning previous set alarm state.

### [STATES]
- **armed_night:** #[OPTIONAL]
    **pending_time:** 10 #[OPTIONAL] State specific setting if not defined inherits from above top level time
    **trigger_time:** 300 #[OPTIONAL] State specific setting if not defined inherits from above top level time
    #[OPTIONAL however either an immediate or delayed group must exist] Sensors in this group tigger the alarm immediately
    immediate:
      - binary_sensor.your_sensors
    #[OPTIONAL] Sensors in this group start the clock (pending_time) when tripped before the alarm is triggered
    delayed:
      - binary_sensor.your_sensors
    #[OPTIONAL] Use this group to automatically override the warning message on open sensors when arming. (I use this as I have a motion sensor at the front door)
    override:
    - binary_sensor.your_sensor

- **armed_home:** #[REQUIRED]
    **pending_time:** 10 #[OPTIONAL] State specific setting if not defined inherits from above top level time
    **trigger_time:** 300 #[OPTIONAL] State specific setting if not defined inherits from above top level time
    #[OPTIONAL however either an immediate or delayed group must exist] Sensors in this group tigger the alarm immediately
    immediate:
      - binary_sensor.your_sensors
    #[OPTIONAL] Sensors in this group start the clock (pending_time) when tripped before the alarm is triggered
    delayed:
      - binary_sensor.your_sensors
    #[OPTIONAL] Use this group to automatically override the warning message on open sensors when arming. (I use this as I have a motion sensor at the front door)
    override:
    - binary_sensor.your_sensor

- **armed_away:** #[REQUIRED]
    **pending_time:** 25 #[OPTIONAL] State specific setting if not defined inherits from above top level time
    **trigger_time:** 600 #[OPTIONAL] State specific setting if not defined inherits from above top level time
    #[OPTIONAL however either an immediate or delayed group must exist] Sensors in this group tigger the alarm immediately
    immediate:
      - binary_sensor.your_sensors
    #[OPTIONAL] Sensors in this group start the clock (pending_time) when tripped before the alarm is triggered
    delayed:
      - binary_sensor.your_sensors
    #[OPTIONAL] Use this group to automatically override the warning message on open sensors when arming. (I use this as I have a motion sensor at the front door)
    override:
    - binary_sensor.your_sensor

### [PASSCODE RELATED]
- passcode_attempts: 3 #[OPTIONAL, number] Disabled if commented out. When a value equal or greater than 0 is set, the system will only allow the set amount of password attempts before timing out
- passcode_attempts_timeout: 30 #[OPTIONAL, number] Default 30 seconds. When set with the password attempts option the panel will timeout for the amount of seconds set if the password is entered incorrectly as per the password_attempts option. The system will then reset the allowed password attempts

### [MQTT RELATED]
- enable_mqtt: True #[OPTIONAL, boolean] False by default. Settings this to True will enable MQTT Mode. Uncomment options below to use See the README for guidance.
- override_code: True #[OPTIONAL, boolean] False by default. if true allows MQTT commands to disarm the alarm without a valid code.
- state_topic: 'home/alarm' #[OPTIONAL, string] The MQTT topic HA will publish state updates to.
- command_topic: 'home/alarm/set' #[OPTIONAL, string] The MQTT topic HA will subscribe to, to receive commands from a remote device to change the alarm state.
- qos: 0 #[OPTIONAL, number] The maximum QoS level for subscribing and publishing to MQTT messages. Default is 0.
- payload_disarm: "DISARM" #[OPTIONAL, string] The payload to disarm this Alarm Panel. Default is “DISARM”.
- payload_arm_home: "ARM_HOME" #[OPTIONAL, string] The payload to set Arm Home mode on this Alarm Panel. Default is “ARM_HOME”.
- payload_arm_away: "ARM_AWAY" #[OPTIONAL, string] The payload to set Arm Away mode on this Alarm Panel. Default is “ARM_AWAY”.
- payload_arm_night: "ARM_NIGHT" #[OPTIONAL, string] The payload to set Arm Night mode on this Alarm Panel. Default is “ARM_NIGHT”.

### [COLOURS]  Use any HTML format
- warning_colour: 'orange' #[OPTIONAL, string]
- pending_colour: 'orange' #[OPTIONAL, string]
- disarmed_colour: '#03A9F4' #[OPTIONAL, string]
- armed_home_colour: 'black' #[OPTIONAL, string]
- armed_away_colour: 'black' #[OPTIONAL, string]
- triggered_colour: 'red' #[OPTIONAL, string]

### [CUSTOM STATUSES]
-custom_supported_statuses_on: #[OPTIONAL, list of strings] CUSTOM SENSOR STATUSES - These settings allow devices which are not natively supported by this panel to be used. This is to be used when the state of the device is not recognised by the panel. Examples are provided below
  - 'running' #EXAMPLE
-custom_supported_statuses_off:
  - 'not_running' #EXAMPLE
