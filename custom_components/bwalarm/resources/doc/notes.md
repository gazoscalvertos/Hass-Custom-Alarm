##Users

The integration supports multiple users. To avoid any collisions they should have different names and passcodes.

##Options

The integration can be configured to request a passcode to set alarm to prevent unauthorized access (Disabled by default).
The passcode can be either master passcode or user passcode.
There is a special code 'override' that can be used to set alarm immediately, i.e without waiting for Pending Time configured. It works even if Request passcode to set alarm is Disabled.

This HA automation sets the alarm immediately
```
alarm_arm_instant:
  sequence:
    service: alarm_control_panel.alarm_arm_away
    entity_id: alarm_control_panel.house
    data:
      code: 'override'
```

##Arm modes
There are Night (perimeter), Home and Away arm modes. They can be used as follows:
Night: only entry/exit doors would trigger an alarm + outbuilding motion
Home: all DOWNSTAIRS sensors would trigger an alarm
Away: any/all sensors would trigger an alarm, entry/exit doors would be a delayed alarm

Please note that you can only set alarm to Night mode if it is enabled in the configuration file (manually in bwalarm.yaml or via Settings -> Sensors).

##Service calls
For compatibility reasons there are currently 2 groups of service calls to set alarm:
1. bwalarm.alarm_safe_arm_home, bwalarm.alarm_safe_arm_away and bwalarm.alarm_safe_arm_night
2. alarm_control_panel.alarm_arm_home, alarm_control_panel.alarm_arm_away and alarm_control_panel.alarm_arm_night
The difference is the services from the first group don't set the alarm if there are active sensors detected whilst the services from the second group always set alarm.

##MQTT

When MQTT enabled, the component publishes its status to the state topic and listens to commands on the command topic (configurable via Settings -> MQTT or manually in bwalarm.yaml).
It supports three arm commands and one disarm command (actual command names are configurable via Settings -> MQTT or manually in bwalarm.yaml).
There is an option to disarm  alarm via MQTT message without passcode (Disabled by default).
Please note that MQTT ARM_HOME, ARM_AWAY and ARM_NIGHT commands set alarm using corresponding service call from the 1st group of service calls described above, i.e it doesn't set alarm if there are active sensors detected.

All MQTT commands get their parameters in JSON format.

ARM_XXX commands support the following optional parameters:
entity_id: <string> # Full name (domain.object_id) of the bwalarm entity to control
code: <string*> | <int>  # A code to arm alarm control panel with
ignore_open_sensors: True | False # Arm even if there are active sensors detected. Default: False

* if 'override' used, it sets alarm immediately, otherwise the alarm changes its state to Pending for Pending Time and then to a corresponding Armed_XXX state.

ARM_DISARM command is similar and supports the following optional parameters:
entity_id: <string> # Full name (domain.object_id) of the bwalarm entity to control
code: <string> | <int>  # A code to arm alarm control panel with


For example,

```home/alarm/set ARM_AWAY```
  arms the Away mode after a configured Pending Time if there is no active sensors detected

```home/alarm/set ARM_HOME {"code":"override"}'```
  arms the Home mode immediately if there is no active sensors detected

```home/alarm/set ARM_HOME {"code": 1234}```
  arms the Home mode using user/master code after a configured Pending Time if there is no active sensors detected

```home/alarm/set ARM_AWAY {"ignore_open_sensors":True}```
  arms the Away mode using user/master code after a configured Pending Time even if there are active sensors detected

```home/alarm/set DISARM```
  disarms the alarm if Disarm Without Code is Enabled

```home/alarm/set DISARM {"code": "shazam"}```
  disarms the alarm if Disarm Without Code is Disabled
