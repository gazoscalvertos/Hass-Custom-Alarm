# bwalarm (akasma74 edition)

## Disclaimer
This fork was created to maintain the original [bwalarm](https://github.com/gazoscalvertos/Hass-Custom-Alarm) custom component until its author is back.
Feel free to create a new issue or pull request here **if you downloaded code from my repo**.
The corresponding HA thread [here](https://community.home-assistant.io/t/bwalarm-akasma74-edition/113666)

## How to - installation

Copy the following folders into your home assistant configuration directory:
```
  resources                  This folder stores your alarm configuration and some user data (i.e badges)
  custom_components/bwalarm/  The alarm system code, resources and documentation there
```

To get things working with Home Assistant (HA) you need to add the following to your configuration.yaml:
```
alarm_control_panel: !include resources/bwalarm/bwalarm.yaml
```
You may need to restart HA if the component doesn't load first time as HA will need to install a dependency (ruamel.yaml).

It's advisable to start with a new ```bwalarm.yaml``` file (included in ```resources/bwalarm``` folder) with the minimum configuration set:
```
platform: bwalarm
```
You can always configure your alarm using web interface or by editing your ```bwalarm.yaml``` directly.

The default password to access the settings page is: **HG28!!&dn**

For more details please refer to the [configuration description](https://github.com/akasma74/Hass-Custom-Alarm/blob/master/guidance/configuration.md).

## How to - update
Currently the update process is pretty much similar to installation - you copy a new release archive/clone the repository from here and save the files into ```custom_components/bwalarm/``` folder. You don't need to overwrite ```resources``` folder as it contains your config (and possibly some additional resources).

Soon the component will be supported by [HASC](https://github.com/custom-components/hacs) and there will be no need to update it manually. Bear in mind that ALL user data inside ```custom_components/bwalarm/``` will be lost upon every update via HACS.

Please note that the component's code is loaded on Home Assistant startup and the panels' code (```panel.html```) is cached by browser.
Therefore, every time you update no matter how, you HAVE to clear chache of ALL of your browsers and then RESTART Home Assistant for changes to happen. 

Please test and provide feedback/suggestions.
