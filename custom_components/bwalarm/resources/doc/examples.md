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
