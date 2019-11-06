# Examples

### CONFIGURATION
[Here](examples/my_bwalarm.yaml) is one of my configurations.

### HOME ASSISTANT AUTOMATIONS
[Here](examples/automations.yaml) you can find out how to react to the alarm states in Home Assistant using automations.  
#### 4
##### 5
####### 6
### SERVICE CALLS  
Set value of `ignore_open_sensors` configuration variable:
<code><pre>
    service: alarm\_control\_panel.set\_ignore\_open\_sensors
    data:
      value: true
</pre></code>
The default for `value` is `false`, i.e making a service call without `data`
<code><pre>
    service: alarm\_control\_panel.set\_ignore\_open\_sensors
</pre></code>
has the same effect as
<code><pre>
    service: alarm\_control\_panel.set\_ignore\_open\_sensors
    data:
     value: false
</pre></code>

### MQTT INTERFACE
Set the `Away` mode after a configured `pending_time`:
<code><pre>
  home/alarm/set ARM\_AWAY
</pre></code>
Set the `Home` mode immediately:
<code><pre>
  home/alarm/set ARM\_HOME {"code":"override"}
</pre></code>
Set the `Home` mode using a code after a configured `pending_time`:
<code><pre>
  home/alarm/set ARM\_HOME {"code": 1234}
</pre></code>
Disarms the alarm if `override_code` is `true`:
<code><pre>
  home/alarm/set DISARM
</pre></code>
Disarm the alarm if `override_code` is `false`:
<code><pre>
  home/alarm/set DISARM {"code": 1234}
</pre></code>
