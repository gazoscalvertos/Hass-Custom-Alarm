#### states
&nbsp;&nbsp;&nbsp; _(map) (Optional)_  
&nbsp;&nbsp;&nbsp; Configurations for supported alarm modes.  
  <s></s>  
  &nbsp;&nbsp;&nbsp; <h4> armed_away </h4>

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _(map) (Required)_  
  &nbsp;&nbsp;&nbsp; Configuration variables for the `Away` mode.  
  <s></s>  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <h4> immediate </h4>

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _(list) (Optional)_  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
  <s></s>  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<h4> delayed </h4>

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _(list) (Optional)_  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Tripping sensors from this list starts warning countdown and changes the alarm's mode to `Warning` before triggering.  
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
