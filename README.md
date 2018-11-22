# Home Assistant - Custom Alarm Interface!
## Intro :-)

### Branch DEV:
Hi everyone, I thought it was time to show the progress of the new UI. Still very much a work in progress but its close!! There are bugs which I'll log in github to allow me to keep track, please feel free to share. Mobile responsiveness needs looking at as does a few other bits and pieces such as default HA colours, status colours, user defined codes.

You may need to restart HA if the component doesnt load first time as HA will install a dependancy (ruamel.yaml)

This new UI allows you to start with pretty much a blank alarm.yaml as this component can write to your yaml file!!! all you need to define is:

```
platform: bwalarm
name: House
```

The default password to access the settings page is: HG28!!&dn

There are many improvements to be made in the code still and this is very much an alpha release and should not be used in a live enviroment!!

Please test and provide feedback/suggestions.

### Change Log:
- 22/11/2018:
- Quite a few bugs and issues have been resolved on this release. There has also been a number of changes to the config file layout so you are likely required to start from scratch as the users, themes and panel settings have changed.

- Updated alarm.html to 1.3.3
- Updated bwalarm.py to 1.1.3

- fixed duplicate sensors in settings panel
- fixed passcode attempts setting
- fixed code to arm display issues
- fixed persistant mode
- fixed sesnor groups
- fixed code to arm panel display and alignment
- reformated logs
- fixed log (displaying name and image)
- removed windows line feed
- integrated HASS users into alarm automatically however these initially are disabled
- fixed switch breaks on service call
- fixed themes



- Updated alarm.html to 1.3.2
- Fixed SVG slowdown

- Updated alarm.html to 1.3.1
- Fixed Mobile buttons

- Updated alarm.html to 1.3.0
- Added user specific codes to settings page and they now work correctly with the logs.
- The logs have been changed around and a few extra logs captured. I plan on expanding this.
- Theres a bug in the persistance mode which I'm working on.
- bwalarm.py updated to 1.1.0


### Features:
- Too many to put in writing at this point!!
