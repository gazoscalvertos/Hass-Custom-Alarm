# This is a temporary fork of bwalarm
The original HA thread [here](https://community.home-assistant.io/t/yet-another-take-on-an-alarm-system/32386)

## Installation

Copy the following files/complete folders into your home assistant configuration directory:
```
  alarm.yaml                  This file stores your alarm configuration
  custom_components/bwalarm/  The brains of the operation. This is the logic of the custom alarm system
  panel_custom.yaml           Needed by HA. NOTE: If you already have a panel_custom.yaml for say floorplan then just copy and paste the code from this repo file into your own panel_custom.yaml to prevent floorplan from being overritten.
  panels/alarm.html           This is the interface for the custom alarm component. It's actually optional as the alarm will function without it but recommended for ease of setup
  www/alarm/                  These files control how the interface looks and feels
  www/lib/                    These files add additional functionality to the interface in order to work
  www/images/ha.png           An image file used for the interface log
```

To get things working with Home Assistant (HA) you need to add the following to your configuration.yaml:
```
alarm_control_panel: !include alarm.yaml
```
You will also need to tell HA where your new panel interface file is. Also add the following to your configuration.yaml:
```
panel_custom: !include panel_custom.yaml
```

**NOTE:** If you experience issues with the page not displaying then add the following:
```
#configuration.yaml
frontend:
  javascript_version: latest
```
You may need to restart HA if the component doesn't load first time as HA will need to install a dependency (ruamel.yaml).

It's advisable to start with a new alarm.yaml file with the minimum configuration set (alarm.yaml from this repo):
```
platform: bwalarm
name: House
```
You can always configure your alarm using web interface or by modifying your alarm.yaml directly.

The default password to access the settings page is: **HG28!!&dn**

For more details please refer to the [configuration description](https://github.com/akasma74/Hass-Custom-Alarm/blob/master/guidance/configuration.md).

Please test and provide feedback/suggestions.
