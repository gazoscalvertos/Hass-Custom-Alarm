# Configuration variables (in bwalarm.yaml)

#### platform
<s style="margin-left:1em;"></s> _(string) (Required)_  
<s style="margin-left:1em;"></s> Domain name of this integration. **Please do not change**.  
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> bwalarm  

#### name
<s style="margin-left:1em;"></s> _(string) (Optional)_  
<s style="margin-left:1em;"></s> Name of the integration entity.  
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> House  

#### pending\_time
<s style="margin-left:1em;"></s> _(integer) (Optional)_  
<s style="margin-left:1em;"></s> Grace time _(in seconds)_ to allow for exit/entry.  
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> 25  

#### warning\_time
<s style="margin-left:1em;"></s> _(integer) (Optional)_  
<s style="margin-left:1em;"></s> Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> 25  

#### trigger\_time
<s style="margin-left:1em;"></s> _(integer) (Optional)_  
<s style="margin-left:1em;"></s> Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back to previously set alarm mode.  
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> 600  

#### code
<s style="margin-left:1em;"></s> _(string) (Required)_  
<s style="margin-left:1em;"></s> Master passcode to set/disarm the alarm. It must consist of one or more digits surrounded by quotes.  
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> 600  

#### code\_to\_arm
<s style="margin-left:1em;"></s> _(boolean) (Optional)_  
<s style="margin-left:1em;"></s> If `true`, a master/user passcode is required to set the alarm via panel/MQTT command/service call.  
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> `false`  

#### passcode\_attempts
<s style="margin-left:1em;"></s> _(integer) (Optional)_  
<s style="margin-left:1em;"></s> If greater than 0, the system will only allow the set amount of password attempts before timing out.  
<s style="margin-left:1em;"></s> `-1` allows for unlimited number of attempts.  
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> -1  

#### passcode\_attempts\_timeout
<s style="margin-left:1em;"></s> _(integer) (Optional)_  
<s style="margin-left:1em;"></s> When `passcode_attempts`>0 and the passcode is entered incorrectly `passcode_attempts` times,    
<s style="margin-left:1em;"></s> the panel will timeout for the amount set _(in seconds)_ and then reset the number of passcode attempts.  
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> 30  

#### panic\_code
<s style="margin-left:1em;"></s> _(string) (Optional)_  
<s style="margin-left:1em;"></s> Panic passcode disarms the alarm and set a special panic mode attribute that could be used in your automations  
<s style="margin-left:1em;"></s> to send a notification to the police/spouse/neighbour that you are under duress.  
<s style="margin-left:1em;"></s> To clear this attribute arm and then disarm your alarm in the usual manner.  
<s style="margin-left:1em;"></s> It must consist of one or more digits surrounded by quotes.  

#### custom\_supported\_statuses\_on
<s style="margin-left:1em;"></s> _(list) (Optional)_  
<s style="margin-left:1em;"></s> List of strings to consider as sensor's `on` states in addition to standard ones.  
<s style="margin-left:1em;"></s> Allows to use sensors that do not have standard (`on`, `True`, `detected` etc) `on` states.  

#### custom\_supported\_statuses\_off
<s style="margin-left:1em;"></s> _(list) (Optional)_  
<s style="margin-left:1em;"></s> List of strings to consider as sensor's `off` states in addition to standard ones.  
<s style="margin-left:1em;"></s> Allows to use sensors that do not have standard (`off`, `False`, `closed` etc) `off` states.  

#### warning
<s style="margin-left:1em;"></s> _(string) (Optional)_  
<s style="margin-left:1em;"></s> Entity ID to turn on when the alarm has been tripped.  

#### alarm
<s style="margin-left:1em;"></s> _(string) (Optional)_  
<s style="margin-left:1em;"></s> Entity ID to turn on when the alarm has been triggered.  

#### enable\_log
<s style="margin-left:1em;"></s> _(boolean) (Optional)_  
<s style="margin-left:1em;"></s> If `true`, the alarm saves log of actions to a file. Its content is available in the `Activity Log` tab at the bottom of the panel.   
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> `true`  

#### log\_size
<s style="margin-left:1em;"></s> _(integer) (Optional)_  
<s style="margin-left:1em;"></s> Maximum number of the last events to display in the log file.  
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> 10  

#### states
<s style="margin-left:1em;"></s> _(map) (Optional)_  
<s style="margin-left:1em;"></s> Configurations for supported alarm modes.  
  <s></s>  
  <h4 style="margin-left:1em;"> armed_away </h4>

  <s style="margin-left:3em;"></s> _(map) (Required)_  
  <s style="margin-left:3em;"></s> Configuration variables for the `Away` mode.  
  <s></s>  
  <h4 style="margin-left:2em;"> immediate </h4>

  <s style="margin-left:4em;"></s> _(list) (Optional)_  
  <s style="margin-left:4em;"></s> Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
  <s></s>  
  <h4 style="margin-left:2em;"> delayed </h4>

  <s style="margin-left:4em;"></s> _(list) (Optional)_  
  <s style="margin-left:4em;"></s> Tripping sensors from this list starts warning countdown and changes the alarm's mode to `Warning` before triggering.  
  <s></s>  
  <h4 style="margin-left:2em;"> override </h4>

  <s style="margin-left:4em;"></s> _(list) (Optional)_  
  <s style="margin-left:4em;"></s> By default upon setting the alarm it checks if any the of sensors from `immediate` and `delayed` lists are `on` and does not proceed without user confirmation if any of them are `on`.  
  <s style="margin-left:4em;"></s> To exclude some sensors from that check (motion sensor at the front door, for example) add those sensors to this list.  
  <s></s>  
  <h4 style="margin-left:2em;"> pending_time </h4>

  <s style="margin-left:4em;"></s> _(integer) (Optional)_  
  <s style="margin-left:4em;"></s> Grace time _(in seconds)_ to allow for exit/entry.  
  <s></s>  
  <s style="margin-left:4em;"></s> _Default value:_  
  <s style="margin-left:4em;"></s> [appropriate top-level value](#pending_time)  
  <s></s>  
  <h4 style="margin-left:2em;"> warning_time </h4>

  <s style="margin-left:4em;"></s> _(integer) (Optional)_  
  <s style="margin-left:4em;"></s> Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
  <s></s>  
  <s style="margin-left:4em;"></s> _Default value:_  
  <s style="margin-left:4em;"></s> [appropriate top-level value](#warning_time)  
  <s></s>  
  <h4 style="margin-left:2em;"> trigger_time </h4>

  <s style="margin-left:4em;"></s> _(integer) (Optional)_  
  <s style="margin-left:4em;"></s> Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back to previously set alarm mode.  
  <s></s>  
  <s style="margin-left:4em;"></s> _Default value:_  
  <s style="margin-left:4em;"></s> [appropriate top-level value](#trigger_time)  
  <s></s>  
  <h4 style="margin-left:1em;"> armed_home </h4>

  <s style="margin-left:3em;"></s> _(map) (Required)_  
  <s style="margin-left:3em;"></s> Configuration variables for the `Home` mode.  
  <s></s>  
  <h4 style="margin-left:2em;"> immediate </h4>

  <s style="margin-left:4em;"></s> _(list) (Optional)_  
  <s style="margin-left:4em;"></s> Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
  <s></s>  
  <h4 style="margin-left:2em;"> delayed </h4>

  <s style="margin-left:4em;"></s> _(list) (Optional)_  
  <s style="margin-left:4em;"></s> Tripping sensors from this list starts warning countdown and changes the alarm's mode to `Warning` before triggering.  
  <s></s>  
  <h4 style="margin-left:2em;"> override </h4>

  <s style="margin-left:4em;"></s> _(list) (Optional)_  
  <s style="margin-left:4em;"></s> By default upon setting the alarm the integration checks if any of sensors from `immediate` and `delayed` lists are `off` and prevents from proceeding if any of them are `on`.  
  <s style="margin-left:4em;"></s> To exclude some sensors from that check (motion sensor at the front door, for example) add those sensors to this list.  
  <s></s>  
  <h4 style="margin-left:2em;"> pending_time </h4>

  <s style="margin-left:4em;"></s> _(integer) (Optional)_  
  <s style="margin-left:4em;"></s> Grace time _(in seconds)_ to allow for exit/entry.  
  <s></s>  
  <s style="margin-left:4em;"></s> _Default value:_  
  <s style="margin-left:4em;"></s> [appropriate top-level value](#pending_time)  
  <s></s>  
  <h4 style="margin-left:2em;"> warning_time </h4>

  <s style="margin-left:4em;"></s> _(integer) (Optional)_  
  <s style="margin-left:4em;"></s> Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
  <s></s>  
  <s style="margin-left:4em;"></s> _Default value:_  
  <s style="margin-left:4em;"></s> [appropriate top-level value](#warning_time)  
  <s></s>  
  <h4 style="margin-left:2em;"> trigger_time </h4>

  <s style="margin-left:4em;"></s> _(integer) (Optional)_  
  <s style="margin-left:4em;"></s> Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back to previously set alarm mode.  
  <s></s>  
  <s style="margin-left:4em;"></s> _Default value:_  
  <s style="margin-left:4em;"></s> [appropriate top-level value](#trigger_time)  
  <s></s>  
  <h4 style="margin-left:1em;"> armed_night </h4>

  <s style="margin-left:3em;"></s> _(map) (Optional)_  
  <s style="margin-left:3em;"></s> Configuration variables for the `Night` mode. Check [`enable_night_mode`]("#enable_night_mode") variable for details.  
  <s></s>  
  <h4 style="margin-left:2em;"> immediate </h4>

  <s style="margin-left:4em;"></s> _(list) (Optional)_  
  <s style="margin-left:4em;"></s> Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
  <s></s>  
  <h4 style="margin-left:2em;"> delayed </h4>

  <s style="margin-left:4em;"></s> _(list) (Optional)_  
  <s style="margin-left:4em;"></s> Tripping sensors from this list starts warning countdown and changes the alarm's mode to `Warning` before triggering.  
  <s></s>  
  <h4 style="margin-left:2em;"> override </h4>

  <s style="margin-left:4em;"></s> _(list) (Optional)_  
  <s style="margin-left:4em;"></s> By default upon setting the alarm the integration checks if any of sensors from `immediate` and `delayed` lists are `off` and prevents from proceeding if any of them are `on`.  
  <s style="margin-left:4em;"></s> To exclude some sensors from that check (motion sensor at the front door, for example) add those sensors to this list.  
  <s></s>  
  <h4 style="margin-left:2em;"> pending_time </h4>

  <s style="margin-left:4em;"></s> _(integer) (Optional)_  
  <s style="margin-left:4em;"></s> Grace time _(in seconds)_ to allow for exit/entry.  
  <s></s>  
  <s style="margin-left:4em;"></s> _Default value:_  
  <s style="margin-left:4em;"></s> [appropriate top-level value](#pending_time)  
  <s></s>  
  <h4 style="margin-left:2em;"> warning_time </h4>

  <s style="margin-left:4em;"></s> _(integer) (Optional)_  
  <s style="margin-left:4em;"></s> Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
  <s></s>  
  <s style="margin-left:4em;"></s> _Default value:_  
  <s style="margin-left:4em;"></s> [appropriate top-level value](#warning_time)  
  <s></s>  
  <h4 style="margin-left:2em;"> trigger_time </h4>

  <s style="margin-left:4em;"></s> _(integer) (Optional)_  
  <s style="margin-left:4em;"></s> Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back to previously set alarm mode.  
  <s></s>  
  <s style="margin-left:4em;"></s> _Default value:_  
  <s style="margin-left:4em;"></s> [appropriate top-level value](#trigger_time)  

#### enable\_night\_mode  
<s style="margin-left:1em;"></s>_(boolean) (Optional)_  
<s style="margin-left:1em;"></s>If `true`, adds `NIGHT` button to the panel and allows setting the alarm to Night mode via MQTT/service call.  
<s></s>  
<s style="margin-left:1em;"></s>_Default value:_  
<s style="margin-left:1em;"></s>`false`  

#### enable\_persistence
<s style="margin-left:1em;"></s>_(boolean) (Optional)_  
<s style="margin-left:1em;"></s>If `true`, allows the alarm to save its state to file and then reinstate it in the event of power loss.  
<s></s>  
<s style="margin-left:1em;"></s>_Default value:_  
<s style="margin-left:1em;"></s>`false`

#### ignore\_open\_sensors  
<s style="margin-left:1em;"></s>_(boolean) (Optional)_  
<s style="margin-left:1em;"></s>If `false`, set the alarm only if there is no active sensors. Otherwise set alarm without checking sensors' states.  
<s></s>  
<s style="margin-left:1em;"></s>_Default value:_  
<s style="margin-left:1em;"></s>`false`

#### users
<s style="margin-left:1em;"></s>_(list) (Optional)_  
<s style="margin-left:1em;"></s>List of users' configuration variables grouped by their IDs.  
<s></s>  
  <h4 style="margin-left:1em;"> id </h4>

  <s style="margin-left:2em;"></s> _(map) (Required)_  
  <s style="margin-left:2em;"></s>  Unique user ID.  
  <s style="margin-left:2em;"></s>  The integration gathers all necessary information automatically if the panel uses admin credentials when accessing Home Assistant.  
  <s></s>  
  <h4 style="margin-left:2em;"> name </h4>

  <s style="margin-left:4em;"></s> _(string) (Required)_  
  <s style="margin-left:4em;"></s> Human-friendly user name.  
  <s></s>  
  <h4 style="margin-left:2em;"> picture </h4>

  <s style="margin-left:4em;"></s> _(string) (Optional)_  
  <s style="margin-left:4em;"></s> Badge _(filename)_ to be used in the `Activity Log` next to this user's name.  
  <s></s>  
  <h4 style="margin-left:2em;"> code </h4>

  <s style="margin-left:4em;"></s> _(string) (Required)_  
  <s style="margin-left:4em;"></s> **Unique** individual passcode to set/disarm the alarm that fulfills the [passcode requirements](#passcode_requirements).  
  <s></s>  
  <h4 style="margin-left:2em;"> enabled </h4>

  <s style="margin-left:4em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:4em;"></s> If `true`, this user can control the alarm.  
  <s></s>  
  <s style="margin-left:4em;"></s> _Default value:_  
  <s style="margin-left:4em;"></s> `true`  

#### mqtt
<s style="margin-left:1em;"></s>_(map) (Optional)_  
<s style="margin-left:1em;"></s>MQTT configuration variables. See more details about MQTT interface [below](#mqtt_interface).  
  <s></s>  
  <h4 style="margin-left:1em;"> enable_mqtt </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Required)_  
  <s style="margin-left:3em;"></s> Enables/disables MQTT interface of the alarm, i.e ability to control it with MQTT messages and get its status by subscribing to its state topic.  
  <s></s>  
  <h4 style="margin-left:1em;"> qos </h4>

  <s style="margin-left:3em;"></s> _(integer) (Optional)_  
  <s style="margin-left:3em;"></s> The maximum QoS level for MQTT messages.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> 0  
  <s></s>  
  <h4 style="margin-left:1em;"> state_topic </h4>

  <s style="margin-left:3em;"></s> _(string) (Optional)_  
  <s style="margin-left:3em;"></s> The MQTT topic the alarm will publish its state updates to.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> home/alarm  
  <s></s>  
  <h4 style="margin-left:1em;"> command_topic </h4>

  <s style="margin-left:3em;"></s> _(string) (Optional)_  
  <s style="margin-left:3em;"></s> The MQTT topic the alarm will subscribe to, to receive commands.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> home/alarm/set  
  <s></s>  
  <h4 style="margin-left:1em;"> payload_arm_away </h4>

  <s style="margin-left:3em;"></s> _(string) (Optional)_  
  <s style="margin-left:3em;"></s> The MQTT payload to set the alarm to `Away` mode.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> ARM\_AWAY  
  <s></s>  
  <h4 style="margin-left:1em;"> payload_arm_home </h4>

  <s style="margin-left:3em;"></s> _(string) (Optional)_  
  <s style="margin-left:3em;"></s> The MQTT payload to set the alarm to `Home` mode.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> ARM\_HOME  
  <s></s>  
  <h4 style="margin-left:1em;"> payload_arm_night </h4>

  <s style="margin-left:3em;"></s> _(string) (Optional)_  
  <s style="margin-left:3em;"></s> The MQTT payload to set the alarm to `Night` mode.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> ARM\_NIGHT  
  <s></s>  
  <h4 style="margin-left:1em;"> payload_disarm </h4>

  <s style="margin-left:3em;"></s> _(string) (Optional)_  
  <s style="margin-left:3em;"></s> The MQTT payload to disarm the alarm.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> DISARM  
  <s></s>  
  <h4 style="margin-left:1em;"> override_code </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, allows MQTT commands to disarm the alarm without a code.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `false`  
  <s></s>  
  <h4 style="margin-left:1em;"> pending_on_warning </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, publishes `pending` state when the alarm is tripped instead of `warning`.  
  <s style="margin-left:3em;"></s> This is to allow integration with other MQTT panels which react to this state.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `false`  

#### panel
<s style="margin-left:1em;"></s>_(map) (Optional)_  
<s style="margin-left:1em;"></s> Panel (GUI) configuration variables.  
  <s></s>  
  <h4 style="margin-left:1em;"> panel_title </h4>

  <s style="margin-left:3em;"></s> _(string) (Optional)_  
  <s style="margin-left:3em;"></s>The text that shows on the header bar.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> Home Alarm  
  <s></s>  
  <h4 style="margin-left:1em;"> enable_clock </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, displays current time in the status bar.  
  <s style="margin-left:3em;"></s> Note that `sensor.time` must exist within your Home Assistant configuration for this option to work.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `true`  
  <s></s>  
  <h4 style="margin-left:1em;"> enable_clock_12hr </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, displays clock in 12hour mode.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `false`  
  <s></s>  
  <h4 style="margin-left:1em;"> enable_weather </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, displays the weather summary in the status bar.  
  <s style="margin-left:3em;"></s> Note that `sensor.weather_summary` or `sensor.dark_sky_summary` must exist within your Home Assistant configuration for this option to work.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `false`  
  <s></s>  
  <h4 style="margin-left:1em;"> enable_sensors_panel </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, adds `Alarm Sensors` tab to the bottom of the panel.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `true`  
  <s></s>  
  <h4 style="margin-left:1em;"> enable_fahrenheit </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, displays the temperature in Fahrenheit.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `false`  
  <s></s>  
  <h4 style="margin-left:1em;"> hide_passcode </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, masks the passcode within the panel input box when typing.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `false`  
  <s></s>  
  <h4 style="margin-left:1em;"> hide_sidebar </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, this security feature hides the Home Assistant sidebar to prevent access to Home Assistant settings when the alarm is set. The sidebar re-appears when the alarm is disarmed.  
  <s style="margin-left:3em;"></s> Note: if your Home Assistant is v96.3 or newer, go to your `Profile settings` in Home Assistant and select `Always hide the sidebar` for this option to work correctly.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `true`  
  <s></s>  
  <h4 style="margin-left:1em;"> hide_sensors </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, this security feature hides the `Alarm Sensors` tab while the alarm is set.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `true`  
  <s></s>  
  <h4 style="margin-left:1em;"> round_buttons </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> Choose whether the alarm buttons should be round or rectangular.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `false`  
  <s></s>  
  <h4 style="margin-left:1em;"> shadow_effect </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, adds shadow effect to text.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `false`  
  <s></s>  
  <h4 style="margin-left:1em;"> enable_serif_font </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, `Lobster` serif font will be used to display the title, time and weather.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `false`  
  <s></s>  
  <h4 style="margin-left:1em;"> enable_camera_panel </h4>

  <s style="margin-left:3em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:3em;"></s> If `true`, cameras listed below to be displayed as a panel.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> `false`  
  <s></s>  
  <h4 style="margin-left:1em;"> cameras </h4>

  <s style="margin-left:3em;"></s> _(list) (Optional)_  
  <s style="margin-left:3em;"></s> List of cameras' entity IDs to display their feeds.  
  <s></s>  
  <h4 style="margin-left:1em;"> camera_update_interval </h4>

  <s style="margin-left:3em;"></s> _(string) (Optional)_  
  <s style="margin-left:3em;"></s> Time _(in seconds)_ the camera(s)' image updates.  
  <s></s>  
  <s style="margin-left:3em;"></s> _Default value:_  
  <s style="margin-left:3em;"></s> 5  

  <h4 style="margin-left:1em;"> themes </h4>

  <s style="margin-left:3em;"></s> _(map) (Optional)_  
  <s style="margin-left:3em;"></s> Themes allow you to override the default Home Assistant colors. See more details about defining colors [below](#themes_colors).  
  <s></s>  
  <h4 style="margin-left:2em;"> name </h4>

  <s style="margin-left:4em;"></s> _(string) (Required)_  
  <s style="margin-left:4em;"></s> Unique name of the theme.  
  <s></s>  
  <h4 style="margin-left:3em;"> active </h4>

  <s style="margin-left:5em;"></s> _(boolean) (Optional)_  
  <s style="margin-left:5em;"></s> Only active theme overrides default Home Assistant colors.  
  <s></s>  
  <s style="margin-left:5em;"></s> _Default value:_  
  <s style="margin-left:5em;"></s> `false`  
  <s></s>  
  <h4 style="margin-left:3em;"> disarmed_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> When the alarm is disarmed the panel will display this color in both the top header background and the centre panel background.  
  <s></s>  
  <h4 style="margin-left:3em;"> pending_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> When the alarm is arming the panel will display this color in both the top header background and the centre panel background.  
  <s></s>  
  <h4 style="margin-left:3em;"> armed_away_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> When the alarm is in `Away` mode the panel will display this color in both the top header background and the centre panel background.  
  <s></s>  
  <h4 style="margin-left:3em;"> armed_home_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> When the alarm is in `Home` mode the panel will display this color in both the top header background and the centre panel background.  
  <s></s>  
  <h4 style="margin-left:3em;"> armed_night_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> When the alarm is in `Night` mode the panel will display this color in both the top header background and the centre panel background.  
  <s></s>  
  <h4 style="margin-left:3em;"> warning_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> If a sensor is tripped when the alarm is set the panel will display this color in both the top header background and the centre panel background.  
  <s></s>  
  <h4 style="margin-left:3em;"> triggered_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> When the alarm has been triggered the panel will display this color in both the top header background and the centre panel background.  
  <s></s>  
  <h4 style="margin-left:3em;"> panel_background_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The background color of the main content section.  
  <s></s>  
  <h4 style="margin-left:4em;"> panel_outer_background_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The background color of both the status bar and the menu bar.  
  <s></s>  
  <h4 style="margin-left:3em;"> panel_text_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The color of the general text within the panel.  
  <s></s>  
  <h4 style="margin-left:3em;"> header_background_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The background color of very top header bar.  
  <s></s>  
  <h4 style="margin-left:3em;"> header_text_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The text color on very top header bar.  
  <s></s>  
  <h4 style="margin-left:3em;"> alarmstatus_text_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The text color to display the alarm status.  
  <s></s>  
  <h4 style="margin-left:3em;"> time_text_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The text color to display time.  
  <s></s>  
  <h4 style="margin-left:3em;"> weather_text_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The text color to display weather summary.  
  <s></s>  
  <h4 style="margin-left:3em;"> weather_image_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The color of weather image.  
  <s></s>  
  <h4 style="margin-left:3em;"> info_header_text_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The color of the heading within a particular section.  
  <s></s>  
  <h4 style="margin-left:3em;"> info_detail_text_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The color of the descriptive text within a particular section.  
  <s></s>  
  <h4 style="margin-left:3em;"> title_text_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The color of the title text within a particular section.  
  <s></s>  
  <h4 style="margin-left:3em;"> subtitle_text_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The color of the subtitle text within a particular section.  
  <s></s>  
  <h4 style="margin-left:3em;"> opensensors_title_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The color of the `Open Sensors` dialog.  
  <s></s>  
  <h4 style="margin-left:3em;"> button_background_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The background color of the alarm buttons.  
  <s></s>  
  <h4 style="margin-left:3em;"> cancel_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The background color of the `Cancel` button.  
  <s></s>  
  <h4 style="margin-left:3em;"> override_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The background color of the `Override` button.  
  <s></s>  
  <h4 style="margin-left:3em;"> info_panel_buttons_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The color of the menu buttons.  
  <s></s>  
  <h4 style="margin-left:3em;"> arm_button_border_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The border color of the alarm buttons.  
  <s></s>  
  <h4 style="margin-left:3em;"> arm_button_text_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The color of the text within the alarm buttons.  
  <s></s>  
  <h4 style="margin-left:3em;"> paper_listbox_background_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The background color of the listboxes.  
  <s></s>  
  <h4 style="margin-left:3em;"> paper_listbox_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The text color within the listboxes.  
  <s></s>  
  <h4 style="margin-left:3em;"> paper_item_selected___color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The text color of the item selected within a selection box.  
  <s></s>  
  <h4 style="margin-left:3em;"> action_button_border_color </h4>

  <s style="margin-left:5em;"></s> _(string) (Optional)_  
  <s style="margin-left:5em;"></s> The color of the border surrounding the action buttons.  

#### admin\_password
<s style="margin-left:1em;"></s> _(string) (Optional)_  
<s style="margin-left:1em;"></s> Password to access the `Settings` tab.  
<s></s>  
<s style="margin-left:1em;"></s> _Default value:_  
<s style="margin-left:1em;"></s> HG28!!&dn  


### BOOLEAN VALUES CONVENTION
Boolean values `true` and `false` are **case-sensitive**.  
Boolean `true` can be substituted by its **case-insensitive** string equivalent "1", "true", "yes", "on" or "enable", or any non-zero integer.  
Boolean `false` can be substituted by any string apart from string equivalents of `true`, or number `0`.  

### SERVICE CALLS
All service calls use domain `alarm_control_panel` and accept the `entity_id` parameter:  
#### entity\_id
<s></s> _(string) (Optional)_  
<s></s> Full name _(domain.object\_id)_ of the alarm integration entity to control. If no such variable used, the service call will applicable to all entities of this integration.  

#### ARM PASSCODE REQUIREMENTS
Service calls `alarm_arm_home`, `alarm_arm_away` and `alarm_arm_night` accept optional `code` parameter that has extended specification compared to [passcode requirements](#code) by allowing a special code "override".  
This special code tells the alarm to set immediately, while with a normal code the alarm will change its state to `pending` first for the corresponding `pending_time` and then change to a corresponding Armed state.  
These service calls also take into account value of [`ignore_open_sensors`](#ignore_open_sensors) configuration variable. If it is `false` (default value, i.e safe arming), the alarm will be set only if there is no active sensors detected.  

There is `set_ignore_open_sensors` service call that allows to change value of `ignore_open_sensors` configuration variable.  
Please refer to the [services' description](../../services.yaml) and the [Examples](examples.md#service-calls) page for more details.  

### MQTT INTERFACE
When MQTT interface is [enabled](#enable_mqtt), the alarm publishes its status to the [state topic](#state_topic) and listens to commands on the [command topic](#command_topic).  
There are three arm commands (for [`Away`](#payload_arm_away), [`Home`](#payload_arm_home) and [`Night`](#payload_arm_night)) and one [disarm](#payload_disarm) command and they behave exactly as corresponding [service calls](#service-calls) do.
All commands are case-insensitive and accept parameters in a form of a [JSON object](http://www.json.org).  
Please refer to the [Examples](examples.md#mqtt-interface) page for more details.

### SETTING ALARM FROM THE PANEL
Note that if you set the alarm from the panel, it always checks for active sensors and let you choose between `Arm anyway` and `Cancel arming` if any detected.

### THEMES COLORS
Color string should contain a [standard HTML color name, hex color code or RGB value](https://htmlcolorcodes.com).  
All optional themes' colors are `black` by default.  
