# Home Assistant - Custom Alarm Interface!
## Intro :-)

Welcome my fellow modders, tinkerers, home assistant wizards!!

Follow the thread [here](https://community.home-assistant.io/t/yet-another-take-on-an-alarm-system/32386)

Consider donating to this project to keep it going as anything contributed will be placed back in to enable more hardware integration, new features and bug squashing.

This is very much a community project so if you wish to chip in then please do!! I could really use a CSS, animation, design guru to make this look amazing. Also please feel free to leave comments, suggestions, enhancements and fixes!!

** NOTE!!! MAJOR CHANGE ** It's time to publish the New UI and settings into the master release.

You may need to restart HA if the component doesn't load first time as HA will install a dependency (ruamel.yaml)

This new UI allows you to start with pretty much a blank alarm.yaml as this component can write to your yaml file!!! all you need to define is:

```
platform: bwalarm
name: House
```

The default password to access the settings page is: HG28!!&dn

There are many improvements to be made in the code still and this is very much an alpha release and should not be used in a live environment!!

Please test and provide feedback/suggestions.

### Features:
- Multi Language Support (NEW)
- State specific groups and times (NEW)
- Panic Mode
- MQTT Integration
- Alarm State Persistence on reboots/power restore
- Lockout of HA sidebar when armed
- Custom Panel allowing your own html to display whatever you choose (Cameras, Sliding Images etc)
- Passcode Attemps/Lockout
- Support for custom device states
- Code panel 0-9 on disarm only
- Weather Status (Optional) - **NOTE:** Weather sensor nows supports generic sensors (sensor.weather_summary & sensor.weather_temperature) if these are not found then it will default to the dark sky sensors (sensor.dark_sky_summary & sensor.dark_sky_temperature)
- Perimeter Mode (Optional) - I use this to only arm a particular set of sensors (doors) whilst I'm using all floors.
- Masks passcode on entry
- clock display (Optional)
- Digit code entry on disarm
- Themed colours depending on alarm state
- Countdown timer on 'Pending' state
- Notification of Open Sensors with the option to override
- Information/Debug panel

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
