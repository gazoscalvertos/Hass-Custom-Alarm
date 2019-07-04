# bwalarm (akasma74 edition)

## Disclaimer
This fork was created to maintain the original [bwalarm](https://github.com/gazoscalvertos/Hass-Custom-Alarm) custom component until its author is back.
Feel free to create a new issue or pull request here **if you downloaded code from my repo**.
The corresponding HA thread [here](https://community.home-assistant.io/t/bwalarm-akasma74-edition/113666)

## How to: installation

Manually:
Copy the following folders into your home assistant configuration directory:
```
  custom_components/bwalarm/  The alarm system code, resources and documentation there
  resources                  This folder stores your alarm configuration and some user data (i.e badges)
```

Using [HASC](https://github.com/custom-components/hacs):
If you have HACS custom component already installed, do the following:
1. Click on Community in the left hand side menu on Home Assistant frontend
2. Click Store
3. Scroll down until you see Fork of Yet another take on alarm and click on it
4. If necessary, select Show Beta from the drop-down menu under SETTINGS
5. Optionally, select version from Available versions drop-down list (it has the latest one selected by default).
6. Click INSTALL
7. The integration is ready and you just need to copy resources and configure your integration.

Copy the this folder into your home assistant configuration directory:
```
  resources                  This folder stores your alarm configuration and some user data (i.e badges)
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

## How to: update

Manually:
Currently the update process is pretty much similar to installation:
1. Copy a new release archive/clone the repository from GotHub to a local folder on your computer.
2. You only need to copy ```custom_components/bwalarm/``` folder from the downloaded release to the same folder in Home Assistant structure.
3. Please note that you DON'T need to overwrite ```resources``` folder in Home Assistant structure as it contains your integration's configuration file (and possibly some additional resources).

Using [HASC](https://github.com/custom-components/hacs):
1. Click on Community in the left hand side menu on Home Assistant frontend
2. Click on Fork of Yet another take on alarm in Integrations
3. Click UPGRADE

Bear in mind that if you use this method, it only updates ```custom_components/bwalarm/``` folder and ALL user data inside that folder will be lost upon every update.

## After update (for all methods)

Please note that the component's code is loaded on Home Assistant startup and the panels' code (```panel.html```) is cached by browser.
Therefore, every time you update no matter how, you HAVE to clear cache of ALL of your browsers and then RESTART Home Assistant for changes to happen.


Please test and provide feedback/suggestions.
