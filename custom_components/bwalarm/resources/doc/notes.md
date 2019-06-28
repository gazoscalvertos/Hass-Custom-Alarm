Users

The component supports multiple users. To avoid any collisions they should have different names and passcodes.

Options

The components can be configured to request a passcode to set the alarm to prevent unauthorized access (Disabled by default).
The passcode can be either master passcode or user passcode.
There is a special code 'override' that can be used to arm immediately, i.e without waiting for Pendind Time configured. It works even if Request passcode to set the alarm is Disabled.
This HA automation arms the alarm immediately
```
alarm_arm_instant:
  sequence:
    service: alarm_control_panel.alarm_arm_away
    entity_id: alarm_control_panel.house
    data:
      code: 'override'
```

Arm modes
There are Night (perimeter), Home and Away arm modes. They can be used as follows:
Night: only entry/exit doors would trigger an alarm + outbuilding motion
Home: all DOWNSTAIRS sensors would trigger an alarm
Away: any/all sensors would trigger an alarm, entry/exit doors would be a delayed alarm
The corresponding service calls are alarm_arm_perimeter, alarm_arm_home and alarm_arm_night.

MQTT

When MQTT enabled, the component publishes its status to the state topic and listens to commands on the command topic (configurable via GUI/bwalarm.yaml).
It supports three variations of arm and disarm commands (actual command names configurable via GUI/bwalarm.yaml).
There is an option to disarm the alarm via MQTT message without passcode (Disabled by default).

For example,
  home/alarm/set ARM_AWAY
arms the Away mode after a configured Pending Time,
  home/alarm/set ARM_HOME 1234
arms the Home mode using code after a configured Pending Time,
  home/alarm/set DISARM
disarms the alarm if Disarm Without Code is Enabled or
  home/alarm/set DISARM 1234
if it is Disabled
