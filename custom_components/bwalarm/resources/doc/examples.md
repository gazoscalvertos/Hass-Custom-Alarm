#### platform
&nbsp;&nbsp;&nbsp; _(string) (Required)_  
&nbsp;&nbsp;&nbsp; Domain name of this integration. **Please do not change**.  
<s></s>  
&nbsp;&nbsp;&nbsp; Default value:_  
&nbsp;&nbsp;&nbsp; bwalarm  

#### log\_size
&nbsp;&nbsp;&nbsp; _(integer) (Optional)_  
&nbsp;&nbsp;&nbsp; Maximum number of the last events to display in the log file.  
<s></s>  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; 10  

#### states
&nbsp;&nbsp;&nbsp; _(map) (Optional)_  
&nbsp;&nbsp;&nbsp; Configurations for supported alarm modes.  
  <s></s>  
  <h4 style="margin-left:1em;"> armed_away </h4>

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _(map) (Required)_  
  &nbsp;&nbsp;&nbsp; Configuration variables for the `Away` mode.  
  <s></s>  
  <h4 style="margin-left:2em;"> immediate </h4>

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _(list) (Optional)_  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
  <s></s>  
  <h4 style="margin-left:2em;"> delayed </h4>

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _(list) (Optional)_  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Tripping sensors from this list starts warning countdown and changes the alarm's mode to `Warning` before triggering.  
  <s></s>  

# Examples

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
