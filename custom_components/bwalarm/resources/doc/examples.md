<div id="#test">abc</div>

<a id="states"></a>
**states**
&nbsp;&nbsp;&nbsp; _(map) (Optional)_  
&nbsp;&nbsp;&nbsp; Configurations for supported alarm modes.  
&nbsp;  
<a id="armed_away"></a>
&nbsp;&nbsp;&nbsp; **armed_away**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(map) (Required)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Configuration variables for the `Away` mode.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **immediate**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Tripping sensors from this list immediately changes the alarm's mode to `Triggered`.  
&nbsp;  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **delayed**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(list) (Optional)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Tripping sensors from this list starts warning countdown and changes the alarm's mode to `Warning` before triggering.  


<a id="platform"></a>
**platform\_abc**  
&nbsp;&nbsp;&nbsp; _(string) (Required)_  
&nbsp;&nbsp;&nbsp; Domain name of this integration. **Please do not change**.  
&nbsp;  
&nbsp;&nbsp;&nbsp; _Default value:_  
&nbsp;&nbsp;&nbsp; bwalarm  
  
<a id="states"></a>
**states**  
&nbsp;&nbsp;&nbsp; _(map) (Optional)_  
&nbsp;  
&nbsp;&nbsp;&nbsp; Configurations for supported alarm modes.  
  
<a id="armed_away"></a>
&nbsp;&nbsp;&nbsp; **armed_away**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(map) (Required)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Configuration variables for the `Away` mode.  
  
<a id="states-armed_away-t2"></a>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; **t2**  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; _(map) (Required)_  
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Descr    
<s></s>  

# Examples
<a id="cba2" class="anchor" aria-hidden="true" href="#cba2"></a>

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
[link](examples.md#armed_away)
[link](#armed_away)
[link](#states-armed_away-t2)
