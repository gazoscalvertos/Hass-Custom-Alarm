# BWAlarm (ak74 edition)

## Disclaimer
This fork was created to maintain the original [bwalarm](https://github.com/gazoscalvertos/Hass-Custom-Alarm) custom component until its author is back.
Feel free to create a new issue or pull request here **if you use code from this repository**.
The corresponding HA thread is [here](https://community.home-assistant.io/t/bwalarm-akasma74-edition/113666)

## How to: installation

Manually:
Copy the following folders into your home assistant configuration directory:
```
  custom_components/bwalarm/  The alarm system code, resources and documentation there
  resources                   This folder stores your alarm configuration file and some user data (i.e badges)
```

Using [HACS](https://github.com/custom-components/hacs)(you need to have HACS already installed and configured):
1. Click on **Community** in the left hand side menu on Home Assistant frontend
2. Click **Store**
3. Scroll down until you see _BWAlarm (ak74 edition)_ and  click on it
4. If necessary, select **Show Beta** from the drop-down menu under **SETTINGS**
5. Optionally, select version from **Available versions** drop-down list (_it has the latest one selected by default_).
6. Click **INSTALL** and wait until it's done
7. **If you don't have `resources` folder in your HA `config` folder**, you may need to create one
8. Save [bwalarm](https://github.com/akasma74/Hass-Custom-Alarm/tree/master/resources/) folder into `resources` folder
8. [Configure](https://github.com/akasma74/Hass-Custom-Alarm/blob/master/custom_components/bwalarm/resources/doc/configuration.md) your integration.

To get things working with Home Assistant (HA) you need to add the following to your `configuration.yaml`:
```
alarm_control_panel: !include resources/bwalarm/bwalarm.yaml
```
You may need to restart HA if the integration doesn't load first time as HA will need to install a dependency (`ruamel.yaml`).

It's advisable to start with a new ```bwalarm.yaml``` file (located in ```resources/bwalarm``` folder) with the minimum configuration set:
```
platform: bwalarm
```
You can always configure your alarm using web interface or by editing your ```bwalarm.yaml``` directly.

The default password to access the settings page is: **HG28!!&dn**

For more details please refer to the [configuration description](https://github.com/akasma74/Hass-Custom-Alarm/blob/master/custom_components/bwalarm/resources/doc/configuration.md) and [notes](https://github.com/akasma74/Hass-Custom-Alarm/blob/master/custom_components/bwalarm/resources/doc/notes.md).
Some automation examples are available [here](https://github.com/akasma74/Hass-Custom-Alarm/tree/master/custom_components/bwalarm/resources/doc/examples).

## How to: update

Manually:
Currently the update process is pretty much similar to installation:
1. Copy a new release archive/clone the repository from GotHub to a local folder on your computer.
2. You only need to copy ```custom_components/bwalarm/``` folder from the downloaded release to the same folder in Home Assistant structure.
3. Please note that you DON'T need to overwrite ```resources``` folder in Home Assistant structure as it contains your integration's configuration file (and possibly some additional resources).

Using [HACS](https://github.com/custom-components/hacs):
1. Click on **Community** in the left hand side menu on Home Assistant frontend
2. Click on _BWAlarm (ak74 edition)_ in Integrations
3. Click **UPGRADE**

**Bear in mind that if you use this method, it only updates ```custom_components/bwalarm/``` folder and **ALL** user data inside that folder will be lost upon every update!**  

Updating by using HACS (even if you initially installed the integraton manually) does not overwrite user settings as these are stored in the ```resources``` folder.

## After update (for all methods)

Please note that the component's code is loaded on Home Assistant startup and the panels' code (```panel.html```) is cached by browser.  
Therefore, **every time you update** no matter how, **you HAVE to clear cache of ALL of your browsers and then RESTART Home Assistant** for changes to take effect.


Please test and provide feedback/suggestions.
