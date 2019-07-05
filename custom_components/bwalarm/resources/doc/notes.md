## Users

The integration supports multiple users. To avoid any collisions they should have different names and passcodes.

## Options

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

## Arm modes
There are Night (perimeter), Home and Away arm modes. They can be used as follows:
Night: only entry/exit doors would trigger an alarm + outbuilding motion
Home: all DOWNSTAIRS sensors would trigger an alarm
Away: any/all sensors would trigger an alarm, entry/exit doors would be a delayed alarm

Please note that you can only set alarm to Night mode if it is enabled in the configuration file (manually in bwalarm.yaml or via Settings -> Sensors).

## Service calls
When you call alarm_control_panel.alarm_arm_home, alarm_control_panel.alarm_arm_away or alarm_control_panel.alarm_arm_night, they all take into account value of ```ignore_open_sensors``` attribute.
If False, it will set the alarm only if there is no active sensors detected, otherwise it will always set alarm.

By default its value is False (safe arming), but you can change it using ```set_ignore_open_sensors``` service call:
```
service: alarm_control_panel.set_ignore_open_sensors
data:
  value: "True"
```
When called without any data, the result is the same as calling with default value (False), i.e:
```
service: alarm_control_panel.set_ignore_open_sensors
```
is the same as
```
service: alarm_control_panel.set_ignore_open_sensors
data:
  value: "False"
```

## MQTT

When MQTT enabled, the integration publishes its status to the state topic and listens to commands on the command topic (configurable via Settings -> MQTT or manually in bwalarm.yaml).

It supports three arm commands and one disarm command (actual command names are configurable via Settings -> MQTT or manually in bwalarm.yaml). All commands are case-insensitive.

Please note that ARM_HOME, ARM_AWAY and ARM_NIGHT commands set alarm exctly as corresponding service call, i.e they don't set alarm if there are active sensors detected and ```ignore_open_sensors``` attribute is ```False```.

You can always check if alarm was set by checking its state in ```wait_template``` or reacting to state change in its state topic.

There is an option to disarm  alarm via MQTT message without passcode (Disabled by default).


All MQTT commands get their parameters in JSON format.

ARM_XXX and ARM_DISARM commands support the following optional parameters:

```
entity_id: <string> # Full name (domain.object_id) of the bwalarm entity to control
code: <string*> | <int>  # A code to arm alarm control panel with
```
(\*) if 'override' is used, it sets alarm immediately, otherwise the alarm changes its state to Pending for Pending Time and then to a corresponding Armed_XXX state.

For example,

```home/alarm/set ARM_AWAY```
  always arms the Away mode after a configured Pending Time

```home/alarm/set ARM_HOME {"code":"override"}'```
  arms the Home mode immediately

```home/alarm/set ARM_HOME {"code": 1234}```
  arms the Home mode using user/master code after a configured Pending Time

```home/alarm/set DISARM```
  disarms the alarm if Disarm Without Code is Enabled

```home/alarm/set DISARM {"code": "shazam"}```
  disarms the alarm if Disarm Without Code is Disabled

## Set alarm from panel
Please note that if you set alarm from web panel, it always checks for active sensors and let you choose to arm anyway or cancel arming if any detected.
