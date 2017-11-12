# Home Assistant - Custom Alarm Interface!
## Intro :-)
Welcome my fellow modders, tinkerers, home assistant wizards!!

This repo is a custom take on the default alarm provided in [https://home-assistant.io/components/alarm_control_panel.manual/]

First of all a big thanks to drytoastman for getting this off the ground [https://community.home-assistant.io/t/a-different-take-on-an-alarm-system/7809]

This is very much a community project so if you wish to chip in then please do!! I could really use a CSS, animation, design guru to make this look amazing. Also please feel free to leave comments, suggestions, enhancements and fixes!!

## Installation Guide

To get this running add the files from this repo into your home assistant configuration directory, then add the following to your configuration.yaml file:

**NOTE:** If you already have a panel_custom.yaml for say floorplan then just copy and paste the code from this repo file into your own panel_custom.yaml to prevent floorplan from being overritten.

```
alarm_control_panel: !include alarm.yaml
panel_custom: !include panel_custom.yaml

```

### Features:

- Optional clock display

- Digit code entry on disarm

- Themed colours depending on alarm state

- Countdown timer on 'Pending' state

### To be implemented:

- List of open sensors with overide option

- Customisable Themes
  - Time Based themes (Dark at Night - Light during day)
  - Possibly a full black one with a Cylon style bar when activated?
  - Please submit some ideas here

- Guest mode / reduced feature set

- Anything anyone else can think of

## Note!

Beware, here be dragons! There may be bugs, issues whilst I get this off the ground and there will definately be design problems when used with different size browsers etc. Hopefully we can conquer these in due course!..

## Thanks!

Thanks to the community for all the input into this.

All of this modding, coding, tinkering is very thirsty work. Consider buying me a beer :-D

BTC Address: 1HNCMM6psd3VJjhLJR9xmKcE6ykcYyhUEy

## Credits

A great countdown JS that I have slightly modded [https://github.com/johnschult/jquery.countdown360]
