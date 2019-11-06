# Examples
| H1 | H2 | H3 | H4 | H5 | H6
| :--- | :--- | :--- | :--- | :--- | :---
| t1 | t2 | t3 | t4 | t5 | t6



|:---           |:---            |:---|:---|:---|
|#### log\_size |                |                  |             | |
|               |_(integer) (Optional)_| | | |
|               |Maximum number of the last events to display in the log file.  | | | |
|               | | | | |
|               |_Default value:_| | | |
|               |10| | | |
|               | | | | |
|#### states    | | | | |
|               |_(map) (Optional)_| | | |
|               |Configurations for supported alarm modes. | | | |
|               |  | | | |
|               |                   |#### armed\_away| | |
|               |                   |                 |_(map) (Required)_| |
|               |                   |                 |Configuration variables for the `Away` mode.| |
|               |                   |                 |                  |#### immediate|
|               |                   |                 |                  |_(list) (Optional)_|
|               |                   |                 |                  |Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.|

### CONFIGURATION
[Here](examples/my_bwalarm.yaml) is one of my configurations.

### HOME ASSISTANT AUTOMATIONS
[Here](examples/automations.yaml) you can find out how to react to the alarm states in Home Assistant using automations.  

### SERVICE CALLS  
Set value of `ignore_open_sensors` configuration variable:
```yaml
    service: alarm_control_panel.set_ignore_open_sensors
    data:
      value: true
```
The default for `value` is `false`, i.e making a service call without `data`
```yaml
    service: alarm_control_panel.set_ignore_open_sensors
```
has the same effect as
```yaml
    service: alarm_control_panel.set_ignore_open_sensors
    data:
     value: false
```

### MQTT INTERFACE
Set the `Away` mode after a configured `pending_time`:
```javascript
  home/alarm/set ARM_AWAY
```
Set the `Home` mode immediately:
```javascript
  home/alarm/set ARM_HOME {"code":"override"}
```
Set the `Home` mode using a code after a configured `pending_time`:
```javascript
  home/alarm/set ARM_HOME {"code": 1234}
```
Disarms the alarm if `override_code` is `true`:
```javascript
  home/alarm/set DISARM
```
Disarm the alarm if `override_code` is `false`:
```javascript
  home/alarm/set DISARM {"code": 1234}
```
