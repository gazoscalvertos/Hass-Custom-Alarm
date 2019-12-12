# Configuration variables (in bwalarm.yaml)

<a id="platform"></a>
**platform**  
&nbsp;&nbsp;&nbsp; _(string) (Required)_  
&nbsp;&nbsp;&nbsp; Domain name of this integration. **Please do not change**.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; bwalarm  

<a id="name"></a>
**name**  
&nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; Name of the integration entity.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; House  

<a id="pending_time"></a>
**pending_time**  
&nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; Grace time _(in seconds)_ to allow for exit/entry.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; 25  

<a id="warning_time"></a>
**warning_time**  
&nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; 25  

<a id="trigger_time"></a>
**trigger_time**  
&nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back to previously set alarm mode.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; 600  

<a id="code"></a>
**code**  
&nbsp;&nbsp;&nbsp; _(string) (Required)_  
<a id="passcode_requirements"></a>
&nbsp;&nbsp;&nbsp; Master passcode to set/disarm the alarm. It must consist of one or more digits surrounded by quotes.  

<a id="code_to_arm"></a>
**code_to_arm**  
&nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; If `true`, a master/user passcode is required to set the alarm via panel/MQTT command/service call.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; `false`  

<a id="passcode_attempts"></a>
**passcode_attempts**  
&nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; If greater than 0, the system will only allow the set amount of password attempts before timing out.  
&nbsp;&nbsp;&nbsp; `-1` allows for unlimited number of attempts.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; -1  

<a id="passcode_attempts_timeout"></a>
**passcode_attempts_timeout**  
&nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; When `passcode_attempts`>0 and the passcode is entered incorrectly `passcode_attempts` times,    
&nbsp;&nbsp;&nbsp; the panel will timeout for the amount set _(in seconds)_ and then reset the number of passcode attempts.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; 30  

<a id="panic_code"></a>
**panic_code**  
&nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; Panic passcode disarms the alarm and set a special panic mode attribute that could be used in  
&nbsp;&nbsp;&nbsp; your automations to send a notification to the police/spouse/neighbour that you are under duress.  
&nbsp;&nbsp;&nbsp; To clear this attribute arm and then disarm your alarm in the usual manner.  
&nbsp;&nbsp;&nbsp; It must consist of one or more digits surrounded by quotes.  

<a id="custom_supported_statuses_on"></a>
**custom_supported_statuses_on**  
&nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; List of strings to consider as sensor's `on` states in addition to standard ones.  
&nbsp;&nbsp;&nbsp; Allows to use sensors that do not have standard (`on`, `True`, `detected` etc) `on` states.  

<a id="custom_supported_statuses_off"></a>
**custom_supported_statuses_off**  
&nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; List of strings to consider as sensor's `off` states in addition to standard ones.  
&nbsp;&nbsp;&nbsp; Allows to use sensors that do not have standard (`off`, `False`, `closed` etc) `off` states.  

<a id="warning"></a>
**warning**  
&nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; Entity ID to turn on when the alarm has been tripped.  

<a id="alarm"></a>
**alarm**  
&nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; Entity ID to turn on when the alarm has been triggered.  

<a id="enable_log"></a>
**enable_log**  
&nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; If `true`, the alarm saves log of actions to a file. Its content is available in the `Activity Log`  
&nbsp;&nbsp;&nbsp; tab at the bottom of the panel.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; `true`  

<a id="log_size"></a>
**log_size**  
&nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; Maximum number of the last events to display in the log file.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; 10  

<a id="states"></a>
**states**  
&nbsp;&nbsp;&nbsp; _(map) (Optional)_  
&nbsp;&nbsp;&nbsp; Configurations for supported alarm modes.  
&nbsp;  
<a id="states-armed_away"></a>
&nbsp;&nbsp;&nbsp; **armed_away**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(map) (Required)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Configuration variables for the `Away` mode.  
&nbsp;  
<a id="states-armed_away-immediate"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **immediate**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
&nbsp;  
<a id="states-armed_away-delayed"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **delayed**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Tripping sensors from this list starts warning countdown and changes the alarm's mode  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; to `Warning` before triggering.  
&nbsp;  
<a id="states-armed_away-pending_time"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **override**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; By default upon setting the alarm it checks if any the of sensors from `immediate`  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; and `delayed` lists are `on` and prevents from proceeding if any of them are `on`.  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; To exclude some sensors from that check (motion sensor at the front door, for example)  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; add those sensors to this list.  
&nbsp;  
<a id="states-armed_away-"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **pending_time**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Grace time _(in seconds)_ to allow for exit/entry.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; [appropriate top-level value](#pending_time)  
&nbsp;  
<a id="states-armed_away-warning_time"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **warning_time**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; [appropriate top-level value](#warning_time)  
&nbsp;  
<a id="states-armed_away-trigger_time"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **trigger_time**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; to the previously set alarm mode.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; [appropriate top-level value](#trigger_time)  
&nbsp;  
<a id="states-armed_home"></a>
&nbsp;&nbsp;&nbsp; **armed_home**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(map) (Required)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Configuration variables for the `Home` mode.  
&nbsp;  
<a id="states-armed_home-immediate"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **immediate**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
&nbsp;  
<a id="states-armed_home-delayed"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **delayed**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Tripping sensors from this list starts warning countdown and changes the alarm's mode  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; to `Warning` before triggering.  
&nbsp;  
<a id="states-armed_home-override"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **override**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; By default upon setting the alarm it checks if any the of sensors from `immediate`  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; and `delayed` lists are `off` and prevents from proceeding if any of them are `on`.  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; To exclude some sensors from that check (motion sensor at the front door, for example)  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; add those sensors to this list.  
&nbsp;  
<a id="states-armed_home-pending_time"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **pending_time**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Grace time _(in seconds)_ to allow for exit/entry.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; [appropriate top-level value](#pending_time)  
&nbsp;  
<a id="states-armed_home-warning_time"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **warning_time**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; [appropriate top-level value](#warning_time)  
&nbsp;  
<a id="states-armed_home-trigger_time"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **trigger_time**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; to the previously set alarm mode.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; [appropriate top-level value](#trigger_time)  
&nbsp;  
<a id="states-armed_night"></a>
&nbsp;&nbsp;&nbsp; **armed_night**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(map) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Configuration variables for the `Night` mode.  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Check [`enable_night_mode`](#enable_night_mode) variable description for details.  
&nbsp;  
<a id="states-armed_night-immediate"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **immediate**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
&nbsp;  
<a id="states-armed_night-delayed"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **delayed**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Tripping sensors from this list starts warning countdown and changes the alarm's mode  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; to `Warning` before triggering.  
&nbsp;  
<a id="states-armed_night-override"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **override**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; By default upon setting the alarm it checks if any the of sensors from `immediate`  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; and `delayed` lists are `off` and prevents from proceeding if any of them are `on`.  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; To exclude some sensors from that check (motion sensor at the front door, for example)  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; add those sensors to this list.  
&nbsp;  
<a id="states-armed_night-pending_time"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **pending_time**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Grace time _(in seconds)_ to allow for exit/entry.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; [appropriate top-level value](#pending_time)  
&nbsp;  
<a id="states-armed_night-warning_time"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **warning_time**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; [appropriate top-level value](#warning_time)  
&nbsp;  
<a id="states-armed_night-trigger_time"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **trigger_time**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; to the previously set alarm mode.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; [appropriate top-level value](#trigger_time)  

<a id="enable_night_mode"></a>
**enable_night_mode**  
&nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; If `true`, adds `NIGHT` button to the panel and allows setting the alarm to Night mode via MQTT/service call.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; `false`  

<a id="enable_persistence"></a>
**enable_persistence**  
&nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; If `true`, allows the alarm to save its state to file and then reinstate it in the event of power loss.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; `false`

<a id="ignore_open_sensors"></a>
**ignore_open_sensors**  
&nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; If `false`, set the alarm only if there is no active sensors. Otherwise set the alarm without checking sensors' states.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; `false`

<a id="users"></a>
**users**  
&nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; List of users' configuration variables grouped by their IDs.  
&nbsp;  
<a id="users-id"></a>
&nbsp;&nbsp;&nbsp; **id**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(map) (Required)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Unique user ID.  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The integration gathers all necessary information automatically if the panel uses admin credentials when accessing  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Home Assistant.  
&nbsp;  
<a id="users-name"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **name**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Required)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Human-friendly user name.  
&nbsp;  
<a id="users-picture"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **picture**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Filename of a badge to be used in the `Activity Log` next to this user's name.  
&nbsp;  
<a id="users-code"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **code**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Required)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Unique user passcode to set/disarm the alarm that fulfills the [passcode requirements](#passcode_requirements).  
&nbsp;  
<a id="users-enabled"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **enabled**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, this user can control the alarm.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `true`  

<a id="mqtt"></a>
**mqtt**  
&nbsp;&nbsp;&nbsp;_(map) (Optional)_  
&nbsp;&nbsp;&nbsp; MQTT configuration variables.  
&nbsp;&nbsp;&nbsp; See more details about MQTT interface [below](#mqtt-interface).  
&nbsp;  
<a id="mqtt-enable_mqtt"></a>
&nbsp;&nbsp;&nbsp; **enable_mqtt**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Required)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Enables/disables MQTT interface of the alarm, i.e ability to control it with MQTT messages and get its status  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; by subscribing to the state topic.  
&nbsp;  
<a id="mqtt-qos"></a>
&nbsp;&nbsp;&nbsp; **qos**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The maximum QoS level for MQTT messages.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; 0  
&nbsp;  
<a id="mqtt-state_topic"></a>
&nbsp;&nbsp;&nbsp; **state_topic**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The MQTT topic the alarm will publish its state updates to.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; home/alarm  
&nbsp;  
<a id="mqtt-command_topic"></a>
&nbsp;&nbsp;&nbsp; **command_topic**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The MQTT topic the alarm will subscribe to, to receive commands.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; home/alarm/set  
&nbsp;  
<a id="mqtt-payload_arm_away"></a>
&nbsp;&nbsp;&nbsp; **payload_arm_away**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The MQTT payload to set the alarm to `Away` mode.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; ARM\_AWAY  
&nbsp;  
<a id="mqtt-payload_arm_home"></a>
&nbsp;&nbsp;&nbsp; **payload_arm_home**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The MQTT payload to set the alarm to `Home` mode.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; ARM\_HOME  
&nbsp;  
<a id="mqtt-payload_arm_night"></a>
&nbsp;&nbsp;&nbsp; **payload_arm_night**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The MQTT payload to set the alarm to `Night` mode.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; ARM\_NIGHT  
&nbsp;  
<a id="mqtt-payload_disarm"></a>
&nbsp;&nbsp;&nbsp; **payload_disarm**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The MQTT payload to disarm the alarm.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; DISARM  
&nbsp;  
<a id="mqtt-override_code"></a>
&nbsp;&nbsp;&nbsp; **override_code**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, allows MQTT commands to disarm the alarm without a code.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `false`  
&nbsp;  
<a id="mqtt-pending_on_warning"></a>
&nbsp;&nbsp;&nbsp; **pending_on_warning**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, publishes `pending` state when the alarm is tripped instead of `warning`.  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; This is to allow integration with other MQTT panels which react to this state.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `false`  

<a id="panel"></a>
**panel**  
&nbsp;&nbsp;&nbsp;_(map) (Optional)_  
&nbsp;&nbsp;&nbsp; Panel (GUI) configuration variables.  
&nbsp;  
<a id="panel-panel_title"></a>
&nbsp;&nbsp;&nbsp; **panel_title**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;The text to show as the top of the window.  
&nbsp;  
<a id="panel-enable_clock"></a>
&nbsp;&nbsp;&nbsp; **enable_clock**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, displays current time in the status bar.  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Note that `sensor.time` must exist within your Home Assistant configuration for this option to work.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `true`  
&nbsp;  
<a id="panel-enable_clock_12hr"></a>
&nbsp;&nbsp;&nbsp; **enable_clock_12hr**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, displays clock in 12hour mode.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `false`  
&nbsp;  
<a id="panel-enable_weather"></a>
&nbsp;&nbsp;&nbsp; **enable_weather**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, displays the weather summary in the status bar.  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Note that `sensor.weather_summary` or `sensor.dark_sky_summary` must exist within your  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Home Assistant configuration for this option to work.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `false`  
&nbsp;  
<a id="panel-enable_sensors_panel"></a>
&nbsp;&nbsp;&nbsp; **enable_sensors_panel**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, adds `Alarm Sensors` tab to the bottom of the panel.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `true`  
&nbsp;  
<a id="panel-enable_fahrenheit"></a>
&nbsp;&nbsp;&nbsp; **enable_fahrenheit**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, displays the temperature in Fahrenheit.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `false`  
&nbsp;  
<a id="panel-hide_passcode"></a>
&nbsp;&nbsp;&nbsp; **hide_passcode**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, masks the passcode within the panel input box when typing.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `false`  
&nbsp;  
<a id="panel-hide_sidebar"></a>
&nbsp;&nbsp;&nbsp; **hide_sidebar**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, this security feature hides the Home Assistant sidebar to prevent access to  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Home Assistant settings when the alarm is set. The sidebar re-appears when the alarm is disarmed.  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Note: if your Home Assistant is v96.3 or newer, go to your `Profile settings` in Home Assistant  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; and select `Always hide the sidebar` for this option to work correctly.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `true`  
&nbsp;  
<a id="panel-hide_sensors"></a>
&nbsp;&nbsp;&nbsp; **hide_sensors**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, this security feature hides the `Alarm Sensors` tab while the alarm is set.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `true`  
&nbsp;  
<a id="panel-round_buttons"></a>
&nbsp;&nbsp;&nbsp; **round_buttons**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Choose whether the alarm buttons should be round or rectangular.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `false`  
&nbsp;  
<a id="panel-shadow_effect"></a>
&nbsp;&nbsp;&nbsp; **shadow_effect**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, adds shadow effect to text.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `false`  
&nbsp;  
<a id="panel-enable_serif_font"></a>
&nbsp;&nbsp;&nbsp; **enable_serif_font**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, `Lobster` serif font will be used to display the title, time and weather.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `false`  
&nbsp;  
<a id="panel-enable_camera_panel"></a>
&nbsp;&nbsp;&nbsp; **enable_camera_panel**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If `true`, cameras listed below to be displayed as a panel.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `false`  
&nbsp;  
<a id="panel-cameras"></a>
&nbsp;&nbsp;&nbsp; **cameras**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; List of cameras' entity IDs to display their feeds.  
&nbsp;  
<a id="panel-camera_update_interval"></a>
&nbsp;&nbsp;&nbsp; **camera_update_interval**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(number) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Time _(in seconds)_ the camera(s)' image updates.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; 5  

<a id="themes"></a>
**themes**  
&nbsp;&nbsp;&nbsp; _(map) (Optional)_  
&nbsp;&nbsp;&nbsp; Themes allow you to override the default Home Assistant colors.  
&nbsp;&nbsp;&nbsp; See more details about defining colors [below](#themes-colors).  
&nbsp;  
<a id="themes-name"></a>
&nbsp;&nbsp;&nbsp; **name**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Required)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Unique name of the theme.  
&nbsp;  
<a id="themes-name-active"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **active**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(boolean) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Only active theme overrides default Home Assistant colors.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; `false`  
&nbsp;  
<a id="themes-name-disarmed_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **disarmed_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; When the alarm is disarmed the panel will display this color in both the top  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; header background and the centre panel background.  
&nbsp;  
<a id="themes-name-pending_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **pending_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; When the alarm is arming the panel will display this color in both the top  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; header and the centre panel background.  
&nbsp;  
<a id="themes-name-armed_away_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **armed_away_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; When the alarm is in `Away` mode the panel will display this color in both the top  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; header background and the centre panel background.  
&nbsp;  
<a id="themes-name-armed_home_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **armed_home_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; When the alarm is in `Home` mode the panel will display this color in both the top  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; header background and the centre panel background.  
&nbsp;  
<a id="themes-name-armed_night_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **armed_night_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; When the alarm is in `Night` mode the panel will display this color in both the top  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; header background and the centre panel background.  
&nbsp;  
<a id="themes-name-warning_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **warning_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; If a sensor is tripped when the alarm is set the panel will display this color in both the top  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; header background and the centre panel background.  
&nbsp;  
<a id="themes-name-triggered_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **triggered_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; When the alarm has been triggered the panel will display this color in both the top  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; header background and the centre panel background.  
&nbsp;  
<a id="themes-name-panel_background_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **panel_background_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The background color of the main content section.  
&nbsp;  
<a id="themes-name-panel_outer_background_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **panel_outer_background_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The background color of both the status bar and the menu bar.  
&nbsp;  
<a id="themes-name-panel_text_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **panel_text_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The color of the general text within the panel.  
&nbsp;  
<a id="themes-name-header_background_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **header_background_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The background color of very top header bar.  
&nbsp;  
<a id="themes-name-header_text_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **header_text_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The text color on very top header bar.  
&nbsp;  
<a id="themes-name-alarmstatus_text_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **alarmstatus_text_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The text color to display the alarm status.  
&nbsp;  
<a id="themes-name-time_text_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **time_text_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The text color to display time.  
&nbsp;  
<a id="themes-name-weather_text_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **weather_text_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The text color to display weather summary.  
&nbsp;  
<a id="themes-name-weather_image_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **weather_image_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The color of weather image.  
&nbsp;  
<a id="themes-name-info_header_text_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **info_header_text_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The color of the heading within a particular section.  
&nbsp;  
<a id="themes-name-info_detail_text_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **info_detail_text_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The color of the descriptive text within a particular section.  
&nbsp;  
<a id="themes-name-title_text_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **title_text_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The color of the title text within a particular section.  
&nbsp;  
<a id="themes-name-subtitle_text_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **subtitle_text_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The color of the subtitle text within a particular section.  
&nbsp;  
<a id="themes-name-opensensors_title_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **opensensors_title_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The color of the `Open Sensors` dialog.  
&nbsp;  
<a id="themes-name-button_background_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **button_background_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The background color of the alarm buttons.  
&nbsp;  
<a id="themes-name-cancel_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **cancel_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The background color of the `Cancel` button.  
&nbsp;  
<a id="themes-name-override_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **override_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The background color of the `Override` button.  
&nbsp;  
<a id="themes-name-info_panel_buttons_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **info_panel_buttons_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The color of the menu buttons.  
&nbsp;  
<a id="themes-name-arm_button_border_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **arm_button_border_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The border color of the alarm buttons.  
&nbsp;  
<a id="themes-name-arm_button_text_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **arm_button_text_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The color of the text within the alarm buttons.  
&nbsp;  
<a id="themes-name-paper_listbox_background_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **paper_listbox_background_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The background color of the listboxes.  
&nbsp;  
<a id="themes-name-paper_listbox_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **paper_listbox_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The text color within the listboxes.  
&nbsp;  
<a id="themes-name-paper_item_selected___color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **paper_item_selected___color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The text color of the item selected within a selection box.  
&nbsp;  
<a id="themes-name-action_button_border_color"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **action_button_border_color**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; The color of the border surrounding the action buttons.  

<a id="admin_password"></a>
**admin_password**  
&nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; Password to access the `Settings` tab.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; HG28!!&dn  
<br>
### BOOLEAN VALUES CONVENTION
Boolean values `true` and `false` are **case-sensitive**.  
Boolean `true` can be substituted by its **case-insensitive** string equivalent "1", "true", "yes", "on" or "enable", or any non-zero number.  
Boolean `false` can be substituted by any string apart from string equivalents of `true`, or number `0`.  

### SERVICE CALLS
All service calls use domain `alarm_control_panel` and accept the `entity_id` parameter:  
**entity_id**  
&nbsp;&nbsp;&nbsp; _(string) (Optional)_  
&nbsp;&nbsp;&nbsp; Full name _(domain.object\_id)_ of the alarm integration entity to control.  
&nbsp;&nbsp;&nbsp; If no such variable used, the service call will applicable to all entities of this integration.  

**ARM PASSCODE REQUIREMENTS**  
Service calls `alarm_arm_home`, `alarm_arm_away` and `alarm_arm_night` accept optional `code` parameter that has extended specification compared to [passcode requirements](#passcode_requirements) by allowing a special code "override".  
This special code tells the alarm to set immediately, while with a normal code the alarm will change its state to `pending` first for the corresponding `pending_time` and then change to a corresponding Armed state.  
These service calls also take into account value of [`ignore_open_sensors`](#ignore_open_sensors) configuration variable. If it is `false` (default value, i.e safe arming), the alarm will be set only if there is no active sensors detected.  

There is `set_ignore_open_sensors` service call that allows to change value of `ignore_open_sensors` configuration variable.  
Please refer to the [services' description](../../services.yaml) and [examples](examples.md#service-calls) for more details.  

### MQTT INTERFACE
When MQTT interface is [enabled](#mqtt-enable_mqtt), the alarm publishes its status to the [state topic](#mqtt-state_topic) and listens to commands on the [command topic](#mqtt-command_topic).  
There are three arm commands (for [`Away`](#mqtt-payload_arm_away), [`Home`](#mqtt-payload_arm_home) and [`Night`](#mqtt-payload_arm_night)) and one [disarm](#mqtt-payload_disarm) command and they behave exactly as corresponding [service calls](#service-calls) do.
All commands are case-insensitive and accept parameters in a form of a [JSON object](http://www.json.org).  
Please refer to the [Examples](examples.md#mqtt-interface) page for more details.

### SETTING ALARM FROM THE PANEL
Note that if you set the alarm from the panel, it always checks for active sensors and let you choose between `Arm anyway` and `Cancel arming` if any detected.

### THEMES COLORS
Color string should contain a [standard HTML color name, hex color code or RGB value](https://htmlcolorcodes.com).  
All optional themes' colors are `black` by default.  
