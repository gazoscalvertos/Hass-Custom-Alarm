# Home Assistant - Custom Alarm Interface!
## Intro :-)
<img align="right" width="376.5" height="525" src="https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/BTC.png">

Welcome my fellow modders, tinkerers, home assistant wizards!!

Follow the thread [here](https://community.home-assistant.io/t/yet-another-take-on-an-alarm-system/32386)

Consider donating to this project to keep it going as anything contributed will be placed back in to enable more hardware integration, new features and bug squashing.

This is very much a community project so if you wish to chip in then please do!! I could really use a CSS, animation, design guru to make this look amazing. Also please feel free to leave comments, suggestions, enhancements and fixes!!

### Features:
- State specific groups and times (NEW)
- Panic Mode
- MQTT Integration
- Alarm State Persistence on reboots/power restore
- Lockout of HA sidebar when armed
- Custom Panel allowing your own html to display whatever you choose (Cameras, Sliding Images etc)
- Passcode Attemps/Lockout
- Support for custom device states
- Code panel 0-9 on disarm only
- Weather Status (Optional) - **NOTE:** Weather sensor nows supports generic sensors (sensor.weather_summary & sensor.weather_temperature) if these are not found then it will deault to the dark sky sensors (sensor.dark_sky_summary & sensor.dark_sky_temperature)
- Perimeter Mode (Optional) - I use this to only arm a particular set of sensors (doors) whilst im using all floors.
- Masks passcode on entry
- clock display (Optional)
- Digit code entry on disarm
- Themed colours depending on alarm state
- Countdown timer on 'Pending' state
- Notification of Open Sensors with the option to override
- Information/Debug panel

### To be implemented:
- Settings page to adjust non-critical features (colours/information)
- Information/Debug Mode to be enhanced
- Screensaver
- Customisable Themes
  - Time Based themes (Dark at Night - Light during day)
  - Possibly a full black one with a Cylon style bar when activated?
  - Please submit some ideas here
- Guest mode / reduced feature set
- Clean up of code (html/css/python)
- Anything anyone else can think of?

[Installation/Configuration Instructions](guidance/configuration.md)

### Testing
- Tested on HA v0.65.5 and below.

### Recent Changelog
- (28/03/18) Major Update - Moved the entire codebase of the panel (alarm.html v1.1.0) over to Polymer2 so that translations can be included and the panel can be integrated into the HA codebase at some point once its ready. Please note that depending on your browser you will likely need to set the javascript version to the latest version using the config below. I don't know how this will effect older browsers but this has been tested on a Samsung Galaxy Tab 10 (Original), S7 Edge, Iphone 6, Firefox, Chrome
```
#CONFIGURATION.YAML
frontend:
  javascript_version: latest
```
- (28/03/18) BUG FIX - MQTT issue not working resolved (bwalarm 1.0.2)
- (28/03/18) BUG FIX - Re-included ignored sensors (Panel 1.0.1), (Bwalarm 1.0.2)
- (28/03/18) UPDATES - Began to clean up panel css file to enhance firefox/opera support. Let me know if there are still issues. A browser cache wipe will be required (alarm.css 1.0.1)
- (25/03/18) BUG FIX - Moved comments line above the actual config to resolve the hassio issues
- (25/03/18) BUG FIX - Fix to resolve slidebar constantly opening when using mobile devices (Panel 1.0.1 / Bwalarm 1.0.1)

- (24/03/18) A Massive Thanks to those that have donated!!! IT is very much appreciated and helps to keep this project alive. Also keep the suggestions flowing and lets make this the best alarm system ever!!!!!!!!!!!!!!!
- (24/03/18) MAJOR UPDATE! - State specific groups/times. Each state must! configure it's own groups. Home and Away are mandatory with Perimeter mode optional. The top level groups have been dropped so you will need to remove these from your alarm.yaml. You will need to update your alarm.yaml!. The ignore/notathome groups have been dropped from the setup. Please see the default alarm.yaml to inform your own setup. An example of the configuration below (if you get stuck then post an issue or ask in the forum):
```
armed_home: #Either home/away with perimeter as optional
  pending_time: 10  #[OPTIONAL] State specific overrides default time
  trigger_time: 600 #[OPTIONAL] State specific overrides default time
  immediate:  #[OPTIONAL however either an immediate or delayed group must exist]
     - binary_sensor.whatever
  delayed: #[OPTIONAL]
     - binary_sensor.whatever
  override: #[OPTIONAL]
     - binary_sensor.whatever
```
- (24/03/18) FEATURE - Added an information button in the bottom right of the panel which shows any detected errors and version information for debugging, needs a little finesse
- (24/03/18) UPDATE - Weather sensor nows supports generic sensors (sensor.weather_summary & sensor.weather_temperature) if these are not found then it will deault to the dark sky sensors (sensor.dark_sky_summary & sensor.dark_sky_temperature)
- (24/03/18) UPDATE - Code cleanup in alarm.html
- (24/03/18) BUG FIX - Removed the need for alarm_script.js (this may re-appear in a later release if we need extra js code) as the hide sidebar feature now natively supports HA close/open sidebar rather than a javascript hack.

- (14/03/18) BUG FIX - UI fix on the sensor groups moving all active sensors into the immediate group when no pending time is set for that particular state.
- (14/03/18) BUG FIX - Custom pending times now accurate set the countdown clock in the panel UI
- (14/03/18) UPDATE - Perimeter Colours added to customisation

[Historic Changelog](historic_changelog.md)

## Note!
Beware, here be dragons! There may be bugs, issues whilst I get this off the ground and there will definately be design problems when used with different size browsers etc. Hopefully we can conquer these in due course!..

## Thanks!
Thanks to the community for all the input into this.

Consider supporting this project and donate! All funds will go towards bringing new features, hardware support and bug squashing!!

- BTC Address: 1NFeyzpKKiKbBYSmCLQZQLxBqJbhSbqmwd
- LTC Address: LTUViN3QUESkQk3mG2hvTzhLRQPVAd269f
- XRP Address: rwuMp76ht6dmGvipxwKr5ZE6VpF7ZKC7qs
- ETH Address: 0xCbeD2D2cf0434370c1ca126707009b876b736609
- Paypal: ha.custom.alarm@gmail.com

## Credits
[A great countdown JS that I have slightly modded](https://github.com/johnschult/jquery.countdown360)
