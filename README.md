# Home Assistant - Custom Alarm Interface!
## Intro :-)
<img align="right" width="376.5" height="525" src="https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/BTC.png">

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

### Features:
- Too many to put in writing at this point!!