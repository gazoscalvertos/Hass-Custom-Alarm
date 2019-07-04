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
For compatibility reasons there are currently 2 groups of service calls to set alarm:
1. bwalarm.alarm_safe_arm_home, bwalarm.alarm_safe_arm_away and bwalarm.alarm_safe_arm_night
2. alarm_control_panel.alarm_arm_home, alarm_control_panel.alarm_arm_away and alarm_control_panel.alarm_arm_night
The difference is the services from the first group don't set the alarm if there are active sensors detected whilst the services from the second group always set alarm.

## MQTT

When MQTT enabled, the integration publishes its status to the state topic and listens to commands on the command topic (configurable via Settings -> MQTT or manually in bwalarm.yaml).
It supports three arm commands, three safe_arm and one disarm command (actual command names are configurable via Settings -> MQTT or manually in bwalarm.yaml). All commands are case-insnsitive.
Please note that SAFE_ARM_HOME, SAFE_ARM_AWAY and SAFE_ARM_NIGHT commands set alarm using corresponding service call from the 1st group of service calls described above, i.e it doesn't set alarm if there are active sensors detected or ```ignore_open_sensors``` attribute is ```True```.
On the other hans, ARM_HOME, ARM_AWAY and ARM_NIGHT commands ALWAYS set alarm.
You can always check if alarm was set by checking its state in ```wait_template``` or reacting to state change in its state topic.

There is an option to disarm  alarm via MQTT message without passcode (Disabled by default).


All MQTT commands get their parameters in JSON format.

ARM_XXX and ARM_DISARM commands support the following optional parameters:
entity_id: <string> # Full name (domain.object_id) of the bwalarm entity to control
code: <string*> | <int>  # A code to arm alarm control panel with

SAFE_ARM_XXX commands also support the following optional parameters:
ignore_open_sensors: True | False # Arm even if there are active sensors detected. Default: False

* if 'override' used, it sets alarm immediately, otherwise the alarm changes its state to Pending for Pending Time and then to a corresponding Armed_XXX state.

For example,

```home/alarm/set ARM_AWAY```
  always arms the Away mode after a configured Pending Time

```home/alarm/set SAFE_ARM_AWAY```
  arms the Away mode after a configured Pending Time if there is no active sensors detected

```home/alarm/set ARM_HOME {"code":"override"}'```
  arms the Home mode immediately if there is no active sensors detected

```home/alarm/set ARM_HOME {"code": 1234}```
  arms the Home mode using user/master code after a configured Pending Time if there is no active sensors detected

```home/alarm/set SAFE_ARM_AWAY {"ignore_open_sensors":True}```
  arms the Away mode using user/master code after a configured Pending Time even if there are active sensors detected

```home/alarm/set DISARM```
  disarms the alarm if Disarm Without Code is Enabled

```home/alarm/set DISARM {"code": "shazam"}```
  disarms the alarm if Disarm Without Code is Disabled
