# Configuration variables (in bwalarm.yaml)

#### platform
<s></s> _(string) (Required)_  
<s></s> Domain name of this integration. **Please do not change**.  
<s></s>  
<s></s> _Default value:_  
<s></s> bwalarm  

#### name
<s></s> _(string) (Optional)_  
<s></s> Name of the integration entity.  
<s></s>  
<s></s> _Default value:_  
<s></s> House  

#### pending\_time
<s></s> _(integer) (Optional)_  
<s></s> Grace time _(in seconds)_ to allow for exit/entry.  
<s></s>  
<s></s> _Default value:_  
<s></s> 25  

#### warning\_time
<s></s> _(integer) (Optional)_  
<s></s> Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
<s></s>  
<s></s> _Default value:_  
<s></s> 25  

#### trigger\_time
<s></s> _(integer) (Optional)_  
<s></s> Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back to previously set alarm mode.  
<s></s>  
<s></s> _Default value:_  
<s></s> 600  

#### code
<s></s> _(string) (Required)_  
<s></s> Master passcode to set/disarm the alarm. It must consist of one or more digits surrounded by quotes.  
<s></s>  
<s></s> _Default value:_  
<s></s> 600  

#### code\_to\_arm
<s></s> _(boolean) (Optional)_  
<s></s> If `true`, a master/user passcode is required to set the alarm via panel/MQTT command/service call.  
<s></s>  
<s></s> _Default value:_  
<s></s> `false`  

#### passcode\_attempts
<s></s> _(integer) (Optional)_  
<s></s> If greater than 0, the system will only allow the set amount of password attempts before timing out.  
<s></s> -1 allows for unlimited number of attempts.  
<s></s>  
<s></s> _Default value:_  
<s></s> -1  

#### passcode\_attempts\_timeout
<s></s> _(integer) (Optional)_  
<s></s> When `passcode_attempts`>0 and the passcode is entered incorrectly `passcode_attempts` times,    
<s></s> the panel will timeout for the amount set _(in seconds)_ and then reset the number of passcode attempts.  
<s></s>  
<s></s> _Default value:_  
<s></s> 30  

#### panic\_code
<s></s> _(string) (Optional)_  
<s></s> Panic passcode disarms the alarm and set a special panic mode attribute that could be used in your automations  
<s></s> to send a notification to the police/spouse/neighbour that you are under duress.  
<s></s> To clear this attribute arm and then disarm your alarm in the usual manner.  
<s></s> It must consist of one or more digits surrounded by quotes.  

#### custom\_supported\_statuses\_on
<s></s> _(list) (Optional)_  
<s></s> List of strings to consider as sensor's `on` states in addition to standard ones.  
<s></s> Allows to use sensors that do not have standard (`on`, `True`, `detected` etc) `on` states.  

#### custom\_supported\_statuses\_off
<s></s> _(list) (Optional)_  
<s></s> List of strings to consider as sensor's `off` states in addition to standard ones.  
<s></s> Allows to use sensors that do not have standard (`off`, `False`, `closed` etc) `off` states.  

#### warning
<s></s> _(string) (Optional)_  
<s></s> Entity ID to turn on when the alarm has been tripped.  

#### alarm
<s></s> _(string) (Optional)_  
<s></s> Entity ID to turn on when the alarm has been triggered.  

#### enable\_log
<s></s> _(boolean) (Optional)_  
<s></s> If `true`, the alarm saves log of actions to a file. Its content is available in the `Activity Log` tab at the bottom of the panel.   
<s></s>  
<s></s> _Default value:_  
<s></s> `true`  

#### log\_size
<s></s> _(integer) (Optional)_  
<s></s> Maximum number of the last events to display in the log file.  
<s></s>  
<s></s> _Default value:_  
<s></s> 10  

#### states
<s></s> _(map) (Optional)_  
<s></s> Configurations for supported alarm modes.  
<s></s>  
<s></s>#### armed\_away
<s></s><s></s> _(map) (Required)_  
<s></s><s></s> Configuration variables for the `Away` mode.  
<s></s>  
<s></s><s></s>#### immediate
<s></s><s></s><s></s> _(list) (Optional)_  
<s></s><s></s><s></s> Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
<s></s>  
<s></s><s></s>#### delayed
<s></s><s></s><s></s> _(list) (Optional)_  
<s></s><s></s><s></s> Tripping sensors from this list starts warning countdown and changes the alarm's mode to `Warning` before triggering.  
<s></s>  
<s></s><s></s>#### override
<s></s><s></s><s></s> _(list) (Optional)_  
<s></s><s></s><s></s> By default upon setting the alarm it checks if any the of sensors from `immediate` and `delayed` lists are `on` and does not proceed without user confirmation if any of them are `on`.  
<s></s><s></s><s></s> To exclude some sensors from that check (motion sensor at the front door, for example) add those sensors to this list.  
<s></s>  
<s></s><s></s>#### pending\_time
<s></s><s></s><s></s> _(integer) (Optional)_  
<s></s><s></s><s></s> Grace time _(in seconds)_ to allow for exit/entry.  
<s></s>  
<s></s><s></s><s></s> _Default value:_  
<s></s><s></s><s></s> [appropriate top-level value](#pending_time)  
<s></s>  
<s></s><s></s>#### warning\_time
<s></s><s></s><s></s> _(integer) (Optional)_  
<s></s><s></s><s></s> Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
<s></s>  
<s></s><s></s><s></s> _Default value:_  
<s></s><s></s><s></s> [appropriate top-level value](#warning_time)  
<s></s>  
<s></s><s></s>#### trigger\_time
<s></s><s></s><s></s> _(integer) (Optional)_  
<s></s><s></s><s></s> Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back to previously set alarm mode.  
<s></s>  
<s></s><s></s><s></s> _Default value:_  
<s></s><s></s><s></s> [appropriate top-level value](#trigger_time)  
<s></s>  
<s></s>#### armed\_home
<s></s><s></s> _(map) (Required)_  
<s></s><s></s> Configuration variables for the `Home` mode.  
<s></s>  
<s></s><s></s>#### immediate
<s></s><s></s><s></s> _(list) (Optional)_  
<s></s><s></s><s></s> Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
<s></s>  
<s></s><s></s>#### delayed
<s></s><s></s><s></s> _(list) (Optional)_  
<s></s><s></s><s></s> Tripping sensors from this list starts warning countdown and changes the alarm's mode to `Warning` before triggering.  
<s></s>  
<s></s><s></s>#### override
<s></s><s></s><s></s> _(list) (Optional)_  
<s></s><s></s><s></s> By default upon setting the alarm the integration checks if any of sensors from `immediate` and `delayed` lists are `off` and prevents from proceeding if any of them are `on`.  
<s></s><s></s><s></s> To exclude some sensors from that check (motion sensor at the front door, for example) add those sensors to this list.  
<s></s>  
<s></s><s></s>#### pending\_time
<s></s><s></s><s></s> _(integer) (Optional)_  
<s></s><s></s><s></s> Grace time _(in seconds)_ to allow for exit/entry.  
<s></s>  
<s></s><s></s><s></s> _Default value:_  
<s></s><s></s><s></s> [appropriate top-level value](#pending_time)  
<s></s>  
<s></s><s></s>#### warning\_time
<s></s><s></s><s></s> _(integer) (Optional)_  
<s></s><s></s><s></s> Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
<s></s>  
<s></s><s></s><s></s> _Default value:_  
<s></s><s></s><s></s> [appropriate top-level value](#warning_time)  
<s></s>  
<s></s><s></s>#### trigger\_time
<s></s><s></s><s></s> _(integer) (Optional)_  
<s></s><s></s><s></s> Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back to previously set alarm mode.  
<s></s>  
<s></s><s></s><s></s> _Default value:_  
<s></s><s></s><s></s> [appropriate top-level value](#trigger_time)  
<s></s>  
<s></s>#### armed\_night
<s></s><s></s> _(map) (Optional)_  
<s></s><s></s> Configuration variables for the `Night` mode. Check [`enable_night_mode`]("#enable_night_mode") variable for details.  
<s></s>  
<s></s><s></s>#### immediate
<s></s><s></s><s></s> _(list) (Optional)_  
<s></s><s></s><s></s> Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
<s></s>  
<s></s><s></s>#### delayed
<s></s><s></s><s></s> _(list) (Optional)_  
<s></s><s></s><s></s> Tripping sensors from this list starts warning countdown and changes the alarm's mode to `Warning` before triggering.  
<s></s>  
<s></s><s></s>#### override
<s></s><s></s><s></s> _(list) (Optional)_  
<s></s><s></s><s></s> By default upon setting the alarm the integration checks if any of sensors from `immediate` and `delayed` lists are `off` and prevents from proceeding if any of them are `on`.  
<s></s><s></s><s></s> To exclude some sensors from that check (motion sensor at the front door, for example) add those sensors to this list.  
<s></s>  
<s></s><s></s>#### pending\_time
<s></s><s></s><s></s> _(integer) (Optional)_  
<s></s><s></s><s></s> Grace time _(in seconds)_ to allow for exit/entry.  
<s></s>  
<s></s><s></s><s></s> _Default value:_  
<s></s><s></s><s></s> [appropriate top-level value](#pending_time)  
<s></s>  
<s></s><s></s>#### warning\_time
<s></s><s></s><s></s> _(integer) (Optional)_  
<s></s><s></s><s></s> Time _(in seconds)_ before triggering the alarm if a sensor has been tripped.  
<s></s>  
<s></s><s></s><s></s> _Default value:_  
<s></s><s></s><s></s> [appropriate top-level value](#warning_time)  
<s></s>  
<s></s><s></s>#### trigger\_time
<s></s><s></s><s></s> _(integer) (Optional)_  
<s></s><s></s><s></s> Time _(in seconds)_ the alarm remains in `Triggered` mode. After that it returns back to previously set alarm mode.  
<s></s>  
<s></s><s></s><s></s> _Default value:_  
<s></s><s></s><s></s> [appropriate top-level value](#trigger_time)  

#### enable\_night\_mode  
<s></s> _(boolean) (Optional)_  
<s></s> If `true`, adds `NIGHT` button to the panel and allows setting the alarm to Night mode via MQTT/service call.  
<s></s>  
<s></s> _Default value:_  
<s></s> `false`  

#### enable\_persistence
<s></s> _(boolean) (Optional)_  
<s></s> If `true`, allows the alarm to save its state to file and then reinstate it in the event of power loss.  
<s></s>  
<s></s> _Default value:_  
<s></s> `false`

#### ignore\_open\_sensors  
<s></s> _(boolean) (Optional)_  
<s></s> If `false`, set the alarm only if there is no active sensors. Otherwise set alarm without checking sensors' states.  
<s></s>  
<s></s> _Default value:_  
<s></s> `false`

#### users
<s></s> _(list) (Optional)_  
<s></s> List of users' configuration variables grouped by their IDs.  
<s></s>  
<s></s>#### id
<s></s><s></s> _(map) (Required)_  
<s></s><s></s>  Unique user ID.  
<s></s><s></s>  The integration gathers all necessary information automatically if the panel uses admin credentials when accessing Home Assistant.  
<s></s>  
<s></s><s></s>#### name
<s></s><s></s><s></s> _(string) (Required)_  
<s></s><s></s><s></s> Human-friendly user name.  
<s></s>  
<s></s><s></s>#### picture
<s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s> Badge _(filename)_ to be used in the `Activity Log` next to this user's name.  
<s></s>  
<s></s><s></s>#### code
<s></s><s></s><s></s> _(string) (Required)_  
<s></s><s></s><s></s> **Unique** individual passcode to set/disarm the alarm that fulfills the [passcode requirements](#passcode_requirements).  
<s></s>  
<s></s><s></s>#### enabled
<s></s><s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s><s></s> If `true`, this user can control the alarm.  
<s></s>  
<s></s><s></s><s></s> _Default value:_  
<s></s><s></s><s></s> `true`  

#### mqtt
<s></s> _(map) (Optional)_  
<s></s> MQTT configuration variables. See more details about MQTT interface [below](#mqtt_interface).  
<s></s>  
<s></s>#### enable\_mqtt  
<s></s><s></s> _(boolean) (Required)_  
<s></s><s></s> Enables/disables MQTT interface of the alarm, i.e ability to control it with MQTT messages and get its status by subscribing to its state topic.  
<s></s>  
<s></s>#### qos
<s></s><s></s> _(integer) (Optional)_  
<s></s><s></s> The maximum QoS level for MQTT messages.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> 0  
<s></s>  
<s></s>#### state\_topic
<s></s><s></s> _(string) (Optional)_  
<s></s><s></s> The MQTT topic the alarm will publish its state updates to.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> home/alarm  
<s></s>  
<s></s>#### command\_topic
<s></s><s></s> _(string) (Optional)_  
<s></s><s></s> The MQTT topic the alarm will subscribe to, to receive commands.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> home/alarm/set  
<s></s>  
<s></s>#### payload\_arm\_away
<s></s><s></s> _(string) (Optional)_  
<s></s><s></s> The MQTT payload to set the alarm to `Away` mode.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> ARM\_AWAY  
<s></s>  
<s></s>#### payload\_arm\_home
<s></s><s></s> _(string) (Optional)_  
<s></s><s></s> The MQTT payload to set the alarm to `Home` mode.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> ARM\_HOME  
<s></s>  
<s></s>#### payload\_arm\_night
<s></s><s></s> _(string) (Optional)_  
<s></s><s></s> The MQTT payload to set the alarm to `Night` mode.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> ARM\_NIGHT  
<s></s>  
<s></s>#### payload\_disarm
<s></s><s></s> _(string) (Optional)_  
<s></s><s></s> The MQTT payload to disarm the alarm.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> DISARM  
<s></s>  
<s></s>#### override\_code
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, allows MQTT commands to disarm the alarm without a code.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `false`  
<s></s>  
<s></s>#### pending\_on\_warning
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, publishes `pending` state when the alarm is tripped instead of `warning`.  
<s></s><s></s> This is to allow integration with other MQTT panels which react to this state.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `false`  

#### panel
<s></s> _(map) (Optional)_  
<s></s> Panel (GUI) configuration variables.  
<s></s>  
<s></s>#### panel\_title
<s></s><s></s> _(string) (Optional)_  
<s></s><s></s> The text that shows on the header bar.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> Home Alarm  
<s></s>  
<s></s>#### enable\_clock
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, displays current time in the status bar.  
<s></s><s></s> Note that `sensor.time` must exist within your Home Assistant configuration for this option to work.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `true`  
<s></s>  
<s></s>#### enable\_clock\_12hr
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, displays clock in 12hour mode.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `false`  
<s></s>  
<s></s>#### enable\_weather
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, displays the weather summary in the status bar.  
<s></s><s></s> Note that `sensor.weather_summary` or `sensor.dark_sky_summary` must exist within your Home Assistant configuration for this option to work.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `false`  
<s></s>  
<s></s>#### enable\_sensors\_panel
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, adds `Alarm Sensors` tab to the bottom of the panel.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `true`  
<s></s>  
<s></s>#### enable\_fahrenheit
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, displays the temperature in Fahrenheit.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `false`  
<s></s>  
<s></s>#### hide\_passcode
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, masks the passcode within the panel input box when typing.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `false`  
<s></s>  
<s></s>#### hide\_sidebar
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, this security feature hides the Home Assistant sidebar to prevent access to Home Assistant settings when the alarm is set. The sidebar re-appears when the alarm is disarmed.  
<s></s><s></s> Note: if your Home Assistant is v96.3 or newer, go to your `Profile settings` in Home Assistant and select `Always hide the sidebar` for this option to work correctly.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `true`  
<s></s>  
<s></s>#### hide\_sensors
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, this security feature hides the `Alarm Sensors` tab while the alarm is set.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `true`  
<s></s>  
<s></s>#### round\_buttons
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> Choose whether the alarm buttons should be round or rectangular.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `false`  
<s></s>  
<s></s>#### shadow\_effect
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, adds shadow effect to text.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `false`  
<s></s>  
<s></s>#### enable\_serif\_font
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, `Lobster` serif font will be used to display the title, time and weather.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `false`  
<s></s>  
<s></s>#### enable\_camera\_panel
<s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s> If `true`, cameras listed below to be displayed as a panel.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> `false`  
<s></s>  
<s></s>#### cameras
<s></s><s></s> _(list) (Optional)_  
<s></s><s></s> List of cameras' entity IDs to display their feeds.  
<s></s>  
<s></s>#### camera\_update\_interval
<s></s><s></s> _(string) (Optional)_  
<s></s><s></s> Time _(in seconds)_ the camera(s)' image updates.  
<s></s>  
<s></s><s></s> _Default value:_  
<s></s><s></s> 5  

<s></s>#### themes
<s></s><s></s> _(map) (Optional)_  
<s></s><s></s> Themes allow you to override the default Home Assistant colors. See more details about defining colors [below](#themes_colors).  
<s></s>  
<s></s><s></s><s></s>#### name
<s></s><s></s><s></s><s></s> _(string) (Required)_  
<s></s><s></s><s></s><s></s> Unique name of the theme.  
<s></s>  
<s></s><s></s><s></s>#### active
<s></s><s></s><s></s><s></s> _(boolean) (Optional)_  
<s></s><s></s><s></s><s></s> Only active theme overrides default Home Assistant colors.  
<s></s>  
<s></s><s></s><s></s><s></s> _Default value:_  
<s></s><s></s><s></s><s></s> `false`  
<s></s>  
<s></s><s></s><s></s>#### disarmed\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> When the alarm is disarmed the panel will display this color in both the top header background and the centre panel background.  
<s></s>  
<s></s><s></s><s></s>#### pending\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> When the alarm is arming the panel will display this color in both the top header background and the centre panel background.  
<s></s>  
<s></s><s></s><s></s>#### armed\_away\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> When the alarm is in `Away` mode the panel will display this color in both the top header background and the centre panel background.  
<s></s>  
<s></s><s></s><s></s>#### armed\_home\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> When the alarm is in `Home` mode the panel will display this color in both the top header background and the centre panel background.  
<s></s>  
<s></s><s></s><s></s>#### armed\_night\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> When the alarm is in `Night` mode the panel will display this color in both the top header background and the centre panel background.  
<s></s>  
<s></s><s></s><s></s>#### warning\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> If a sensor is tripped when the alarm is set the panel will display this color in both the top header background and the centre panel background.  
<s></s>  
<s></s><s></s><s></s>#### triggered\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> When the alarm has been triggered the panel will display this color in both the top header background and the centre panel background.  
<s></s>  
<s></s><s></s><s></s>#### panel\_background\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The background color of the main content section.  
<s></s>  
<s></s><s></s><s></s>#### panel\_outer\_background\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The background color of both the status bar and the menu bar.  
<s></s>  
<s></s><s></s><s></s>#### panel\_text\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The color of the general text within the panel.  
<s></s>  
<s></s><s></s><s></s>#### header\_background\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The background color of very top header bar.  
<s></s>  
<s></s><s></s><s></s>#### header\_text\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The text color on very top header bar.  
<s></s>  
<s></s><s></s><s></s>#### alarmstatus\_text\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The text color to display the alarm status.  
<s></s>  
<s></s><s></s><s></s>#### time\_text\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The text color to display time.  
<s></s>  
<s></s><s></s><s></s>#### weather\_text\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The text color to display weather summary.  
<s></s>  
<s></s><s></s><s></s>#### weather\_image\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The color of weather image.  
<s></s>  
<s></s><s></s><s></s>#### info\_header\_text\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The color of the heading within a particular section.  
<s></s>  
<s></s><s></s><s></s>#### info\_detail\_text\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The color of the descriptive text within a particular section.  
<s></s>  
<s></s><s></s><s></s>#### title\_text\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The color of the title text within a particular section.  
<s></s>  
<s></s><s></s><s></s>#### subtitle\_text\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The color of the subtitle text within a particular section.  
<s></s>  
<s></s><s></s><s></s>#### opensensors\_title\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The color of the `Open Sensors` dialog.  
<s></s>  
<s></s><s></s><s></s>#### button\_background\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The background color of the alarm buttons.  
<s></s>  
<s></s><s></s><s></s>#### cancel\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The background color of the `Cancel` button.  
<s></s>  
<s></s><s></s><s></s>#### override\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The background color of the `Override` button.  
<s></s>  
<s></s><s></s><s></s>#### info\_panel\_buttons\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The color of the menu buttons.  
<s></s>  
<s></s><s></s><s></s>#### arm\_button\_border\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The border color of the alarm buttons.  
<s></s>  
<s></s><s></s><s></s>#### arm\_button\_text\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The color of the text within the alarm buttons.  
<s></s>  
<s></s><s></s><s></s>#### paper\_listbox\_background\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The background color of the listboxes.  
<s></s>  
<s></s><s></s><s></s>#### paper\_listbox\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The text color within the listboxes.  
<s></s>  
<s></s><s></s><s></s>#### paper\_item\_selected\_\_\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The text color of the item selected within a selection box.  
<s></s>  
<s></s><s></s><s></s>#### action\_button\_border\_color
<s></s><s></s><s></s><s></s> _(string) (Optional)_  
<s></s><s></s><s></s><s></s> The color of the border surrounding the action buttons.  

#### admin\_password
<s></s> _(string) (Optional)_  
<s></s> Password to access the `Settings` tab.  
<s></s>  
<s></s> _Default value:_  
<s></s> HG28!!&dn  


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
Please refer to the [services' description](../services.yaml) and the [Examples](examples.yaml#service_calls) page for more details.  

### MQTT INTERFACE
When MQTT interface is [enabled](#enable_mqtt), the alarm publishes its status to the [state topic](#state_topic) and listens to commands on the [command topic](#command_topic).  
There are three arm commands (for [`Away`](#payload_arm_away), [`Home`](#payload_arm_home) and [`Night`](#payload_arm_night)) and one [disarm](#payload_disarm) command and they behave exactly as corresponding [service calls](#service_calls) do.
All commands are case-insensitive and accept parameters in a form of a [JSON object](http://www.json.org).  
Please refer to the [Examples](examples.yaml#mqtt_interface) page for more details.

### SETTING ALARM FROM THE PANEL
Note that if you set the alarm from the panel, it always checks for active sensors and let you choose between `Arm anyway` and `Cancel arming` if any detected.

### THEMES COLORS
Color string should contain a [standard HTML color name, hex color code or RGB value](https://htmlcolorcodes.com).  
All optional themes' colors are `black` by default.  
