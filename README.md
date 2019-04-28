# This is a temporary fork of bwalarm!
## Intro :-)

The original HA thread [here](https://community.home-assistant.io/t/yet-another-take-on-an-alarm-system/32386)

## Installation

You will need to copy the following files/complete folders into your home assistant configuration directory

alarm.yaml	*This file stores your alarm configuration*
custom_components/bwalarm/ *The brains of the operation. This is the logic of the custom alarm system*
panels/alarm.html *This is the interface for the custom alarm component. It's actually optional as the alarm will function without it but recommended for ease of setup*
www/alarm/ *These files control how the interface looks and feels*
www/lib/ *These files add additional functionality to the interface in order to work*
www/images/ha.png *An image file used for the interface log*

To get things working with Home Assistant (HA) you will need to adjust your configuration.yaml to instruct HA to use your new custom alarm component, add the following to this file:
```
alarm_control_panel: !include alarm.yaml
```
You will also need to tell HA where your new panel interface file is. Also add the following to your configuration.yaml:
```
panel_custom: !include panel_custom.yaml
```
You may need to restart HA if the component doesn't load first time as HA will need to install a dependency (ruamel.yaml).

It's advisable to start with a new alarm.yaml file with the minimum configuration set (alarm.yaml from this repo):
```
platform: bwalarm
name: House
```
Your new interface can be used to modify your alarm.yaml directly.

The default password to access the settings page is: **HG28!!&dn**

Please test and provide feedback/suggestions.
