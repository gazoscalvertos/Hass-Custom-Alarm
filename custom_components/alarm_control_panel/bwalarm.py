"""
  GazosCalvertos: Yet another take on a custom alarm for Home Assistant
"""
import asyncio
import datetime
import logging
import enum
import os
import re
import json
import voluptuous as vol
from   operator   import attrgetter

from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMED_HOME, STATE_ALARM_DISARMED,
    STATE_ALARM_PENDING, STATE_ALARM_TRIGGERED, CONF_PLATFORM, CONF_NAME,
    CONF_CODE, CONF_PENDING_TIME, CONF_TRIGGER_TIME, CONF_DISARM_AFTER_TRIGGER,
    EVENT_STATE_CHANGED, EVENT_TIME_CHANGED, 
    STATE_ON)

from homeassistant.core          import callback
from homeassistant.util.dt       import utcnow                       as now
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.util          import sanitize_filename
from homeassistant.helpers.event import async_track_state_change

import homeassistant.components.alarm_control_panel                  as alarm
import homeassistant.components.switch                               as switch
import homeassistant.helpers.config_validation                       as cv
import homeassistant.components.mqtt                                 as mqtt

DOMAIN                       = 'alarm_control_panel'
#//--------------------SUPPORTED STATES----------------------------
STATE_ALARM_WARNING          = 'warning'
STATE_ALARM_ARMED_PERIMETER  = 'armed_perimeter'
SUPPORTED_STATES             = [STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMED_HOME,
                                STATE_ALARM_DISARMED, STATE_ALARM_PENDING,
                                STATE_ALARM_TRIGGERED, STATE_ALARM_WARNING,
                                STATE_ALARM_ARMED_PERIMETER]
#-----------------------------END-----------------------------------

#//-------------------STATES TO CHECK------------------------------
STATE_TRUE                   = 'true'
STATE_UNLOCKED               = 'unlocked'
STATE_OPEN                   = 'open'
STATE_DETECTED               = 'detected'
#//---------------------------END----------------------------------

#//-----------------YAML CONFIG OPTIONS----------------------------
CONF_PANIC_CODE              = 'panic_code'
#//-------------------SENSOR GROUPS--------------------------------
CONF_IMMEDIATE               = 'immediate'
CONF_DELAYED                 = 'delayed'
CONF_IGNORE                  = 'homemodeignore'
CONF_NOTATHOME               = 'notathome'
CONF_OVERRIDE                = 'override'
CONF_PERIMETER               = 'perimeter'
#//-------------------------END-------------------------------------
#//-----------------DEVICES TO ENABLE/DISBALE-----------------------
CONF_ALARM                   = 'alarm'
CONF_WARNING                 = 'warning'
#//------------------------END---------------------------------------

#//----------------------OPTIONAL MODES------------------------------
CONF_PERIMETER_MODE          = 'perimeter_mode'
CONF_MQTT                    = 'mqtt'
CONF_CLOCK                   = 'clock'
CONF_WEATHER                 = 'weather'
CONF_SETTINGS                = 'settings'
CONF_HIDE_ALL_SENSORS        = 'hide_all_sensors'
#//------------------------END---------------------------------------
#//-----------------------COLOURS------------------------------------
CONF_WARNING_COLOUR          = 'warning_colour'
CONF_PENDING_COLOUR          = 'pending_colour'
CONF_DISARMED_COLOUR         = 'disarmed_colour'
CONF_TRIGGERED_COLOUR        = 'triggered_colour'
CONF_ARMED_AWAY_COLOUR       = 'armed_away_colour'
CONF_ARMED_HOME_COLOUR       = 'armed_home_colour'
#//-------------------------END--------------------------------------
#//------------------------END OF YAML-------------------------------

#//-----------------------MQTT RELATED-------------------------------
CONF_PAYLOAD_DISARM          = 'payload_disarm'
CONF_PAYLOAD_ARM_HOME        = 'payload_arm_home'
CONF_PAYLOAD_ARM_AWAY        = 'payload_arm_away'
CONF_PAYLOAD_ARM_NIGHT       = 'payload_arm_night'
#//--------------------------EO MQTT---------------------------------

class Events(enum.Enum):
    ImmediateTrip            = 1
    DelayedTrip              = 2
    ArmHome                  = 3
    ArmAway                  = 4
    Timeout                  = 5
    Disarm                   = 6
    Trigger                  = 7
    ArmPerimeter             = 8
    
PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_PLATFORM):                           'bwalarm',
    vol.Required(CONF_NAME, default='House'):              cv.string,
    vol.Required(CONF_PENDING_TIME):                       vol.All(vol.Coerce(int), vol.Range(min=0)),
    vol.Required(CONF_TRIGGER_TIME):                       vol.All(vol.Coerce(int), vol.Range(min=1)),
    vol.Required(CONF_ALARM):                              cv.entity_id,  # switch/group to turn on when alarming [TODO]
    vol.Required(CONF_WARNING):                            cv.entity_id,  # switch/group to turn on when warning [TODO]
    vol.Optional(CONF_CODE):                               cv.string,
    vol.Optional(CONF_PANIC_CODE):                         cv.string,
    vol.Optional(CONF_IMMEDIATE):                          cv.entity_ids, # things that cause an immediate alarm
    vol.Optional(CONF_DELAYED):                            cv.entity_ids, # things that allow a delay before alarm
    vol.Optional(CONF_IGNORE):                             cv.entity_ids, # things that we ignore when at home
    vol.Optional(CONF_NOTATHOME):                          cv.entity_ids, # things that we ignore when at home BACKWARDS COMPAT
    vol.Optional(CONF_OVERRIDE):                           cv.entity_ids, # sensors that can be ignored if open when trying to set alarm in away mode
    vol.Optional(CONF_PERIMETER_MODE):                     cv.boolean,    # Enable perimeter mode?
    vol.Optional(CONF_PERIMETER):                          cv.entity_ids, # things monitored under perimeter mode
    vol.Optional(CONF_WARNING_COLOUR, default='orange'):   cv.string,     # Custom colour of warning display
    vol.Optional(CONF_PENDING_COLOUR, default='orange'):   cv.string,     # Custom colour of pending display
    vol.Optional(CONF_DISARMED_COLOUR, default='#03A9F4'): cv.string,     # Custom colour of disarmed display
    vol.Optional(CONF_TRIGGERED_COLOUR, default='red'):    cv.string,     # Custom colour of triggered display
    vol.Optional(CONF_ARMED_AWAY_COLOUR, default='black'): cv.string,     # Custom colour of armed away display
    vol.Optional(CONF_ARMED_HOME_COLOUR, default='black'): cv.string,     # Custom colour of armed home display
    vol.Optional(CONF_SETTINGS, default=False):            cv.boolean,    # Allow settings mode to become active and allow saving of settings config file
    vol.Optional(CONF_CLOCK):                              cv.boolean,    # DIsplay clock on panel
    vol.Optional(CONF_WEATHER):                            cv.boolean,    # DIsplay weather on panel
    vol.Optional(CONF_HIDE_ALL_SENSORS, default=False):    cv.boolean,    # Show all sensors in group?
    #//------------------------MQTT RELATED----------------------------//
    vol.Optional(CONF_MQTT, default=False):                cv.boolean, # Allows MQTT functionality
    vol.Optional(CONF_PAYLOAD_ARM_AWAY, default='ARM_AWAY'): cv.string,
    vol.Optional(CONF_PAYLOAD_ARM_HOME, default='ARM_HOME'): cv.string,
    vol.Optional(CONF_PAYLOAD_ARM_NIGHT, default='ARM_NIGHT'): cv.string,
    vol.Optional(CONF_PAYLOAD_DISARM, default='DISARM'): cv.string
    #//---------------------------END-----------------------------------//
})

_LOGGER = logging.getLogger(__name__)

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    alarm = BWAlarm(hass, config)
    hass.bus.async_listen(EVENT_STATE_CHANGED, alarm.state_change_listener)
    hass.bus.async_listen(EVENT_TIME_CHANGED, alarm.time_change_listener)
    async_add_devices([alarm])

    @callback
    def alarm_settings_save(service, settings=None):
        _LOGGER.error("[ALARM] test %s", settings)
        alarm.test(settings)
     
    hass.services.async_register(DOMAIN, 'ALARM_SETTINGS_SAVE', alarm_settings_save)
    
    return True
   
class BWAlarm(alarm.AlarmControlPanel):

    def __init__(self, hass, config):
        """ Initalize the alarm system """
        self._hass         = hass
        self._name         = config[CONF_NAME]
        self._immediate    = set(config.get(CONF_IMMEDIATE, []))
        self._delayed      = set(config.get(CONF_DELAYED, []))
        self._ignore       = set(config.get(CONF_IGNORE, []) if config.get(CONF_IGNORE, []) != [] else config.get(CONF_NOTATHOME, []))
        self._override      = set(config.get(CONF_OVERRIDE, []))
        self._perimeter_mode = config.get(CONF_PERIMETER_MODE, False)
        self._perimeter      = set(config.get(CONF_PERIMETER, []))
        self._allsensors   = self._immediate | self._delayed | self._ignore
        #self._allsensors   = self._allinputs 
        self._alarm        = config[CONF_ALARM]
        self._warning      = config[CONF_WARNING]
        self._code         = config[CONF_CODE] if config[CONF_CODE] else None
        self._panic_code   = config.get(CONF_PANIC_CODE, None)
        self._hide_all_sensors = config.get(CONF_HIDE_ALL_SENSORS, False)

        self._countdown_time = config[CONF_PENDING_TIME]
        self._pending_time = datetime.timedelta(seconds=config[CONF_PENDING_TIME])
        self._trigger_time = datetime.timedelta(seconds=config[CONF_TRIGGER_TIME])

        self._lasttrigger  = ""
        self._state        = STATE_ALARM_DISARMED
        self._returnto     = STATE_ALARM_DISARMED
        self._timeoutat    = None
       
        self._warning_colour = config[CONF_WARNING_COLOUR]
        self._pending_colour = config[CONF_PENDING_COLOUR]
        self._disarmed_colour = config[CONF_DISARMED_COLOUR]
        self._triggered_colour = config[CONF_TRIGGERED_COLOUR]
        self._armed_away_colour = config[CONF_ARMED_AWAY_COLOUR]
        self._armed_home_colour = config[CONF_ARMED_HOME_COLOUR]
        
        self._panic_mode = "deactivated"

        self._clock = config.get(CONF_CLOCK, False)
        self._weather = config.get(CONF_WEATHER, False)

        self.clearsignals()

        self._settings = config.get(CONF_SETTINGS)
        self._settings_list = []

        #-------------------------------------MQTT--------------------------------------------------
        self._mqtt           = config[CONF_MQTT]
        self._payload_disarm = config.get(CONF_PAYLOAD_DISARM)
        self._payload_arm_home = config.get(CONF_PAYLOAD_ARM_HOME)
        self._payload_arm_away= config.get(CONF_PAYLOAD_ARM_AWAY)
        self._payload_arm_night = config.get(CONF_PAYLOAD_ARM_NIGHT)
        self._qos = config.get(mqtt.CONF_QOS, 0)
        self._state_topic = config.get(mqtt.CONF_STATE_TOPIC, 'home/alarm')
        self._command_topic = config.get(mqtt.CONF_COMMAND_TOPIC, 'home/alarm/set')
        #--------------------------------------END--------------------------------------------

        #------------------------------------SETTINGS----------------------------------------------------
        if (self._settings):
           settings_path = "alarm_settings"

           # If path is relative, we assume relative to HASS config dir
           if not os.path.isabs(settings_path):
              settings_path = hass.config.path(settings_path)

           if not os.path.isdir(settings_path):
              _LOGGER.error("[ALARM] Settings path %s does not exist.", settings_path)
           else:
              self._settings_final_path = os.path.join(settings_path, "settings.json")
              self.load_settings()
        #---------------------------------------END-------------------------------------------------------

    ### Alarm properties
    @property
    def should_poll(self) -> bool: return False
    @property
    def name(self) -> str:         return self._name
    @property
    def changed_by(self) -> str:   return self._lasttrigger
    @property
    def state(self) -> str:        return self._state
    @property
    def device_state_attributes(self):
        return {
            'immediate':  sorted(list(self.immediate)),
            'delayed':    sorted(list(self.delayed)),
            'override':   sorted(list(self._override)),
            'ignored':    sorted(list(self.ignored)),
            'allsensors': sorted(list(self._allsensors)),
            'perimeter_mode':    self._perimeter_mode,
            'perimeter':    sorted(list(self._perimeter)),
            'changedby':  self.changed_by,
            'warning_colour':  self._warning_colour,
            'pending_colour':  self._pending_colour,
            'disarmed_colour':  self._disarmed_colour,
            'triggered_colour':  self._triggered_colour,
            'armed_home_colour':  self._armed_home_colour,
            'armed_away_colour':  self._armed_away_colour,
            'panic_mode': self._panic_mode,
            'countdown_time':  self._countdown_time,
            'clock':  self._clock,
            'weather':  self._weather,
            'settings': self._settings,
            'settings_list': self._settings_list,
            'hide_all_sensors': self._hide_all_sensors
        }
    def test(self, settings=None):
        _LOGGER.error("[ALARM] test triggered %s", settings)
        self._settings_list = '{"bacon2":"yes"}'
        self.schedule_update_ha_state()

    ### LOAD Settings previously saved
    def load_settings(self):
        try:
           if os.path.isfile(self._settings_final_path):  #Find the settings JSON file and load. Once found update the alarm_control_panel object
              _LOGGER.error("[ALARM] Settings file exists")
              self._settings_list = json.load(open(self._settings_final_path, 'r'))
           else: #No Settings file found
              _LOGGER.error("[ALARM] Settings file doesnt exist")
              self._settings_list = None

        except Exception as e:
           _LOGGER.error("[ALARM] Error occured loading: %s", str(e))

    ### UPDATE Settings
    def save_settings(self): #, settings):
        try:
           if self._settings_list is not None: #Check we have genuine settings to save if so dump to file
              with open(self._settings_final_path, 'w') as fil:
                 fil.write(json.dumps(self._settings_list, ensure_ascii=False))
           else:
              _LOGGER.error("[ALARM] No settings to save!")
        except Exception as e:
           _LOGGER.error("[ALARM] Error occured saving: %s", str(e))
    
    ### Actions from the outside world that affect us, turn into enum events for internal processing
    def time_change_listener(self, eventignored):
        """ I just treat the time events as a periodic check, its simpler then (re-/un-)registration """
        if self._timeoutat is not None:
            if now() > self._timeoutat:
                self._timeoutat = None
                self.process_event(Events.Timeout)

    def state_change_listener(self, event):
        """ Something changed, we only care about things turning on at this point """
        new = event.data.get('new_state', None)
        if new is None:
            return
        if new.state.lower() == STATE_ON or new.state.lower() == STATE_TRUE or new.state.lower() == STATE_UNLOCKED or new.state.lower() == STATE_OPEN or new.state.lower() == STATE_DETECTED:
            eid = event.data['entity_id']
            if eid in self.immediate:
                self._lasttrigger = eid
                self.process_event(Events.ImmediateTrip)
            elif eid in self.delayed:
                self._lasttrigger = eid
                self.process_event(Events.DelayedTrip)

    @property
    def code_format(self):
        """One or more characters."""
        return None if self._code is None else '.+'

    def alarm_disarm(self, code=None):
        
        #If the provided code matches the panic alarm then deactivate the alarm but set the state of the panic mode to active.
        if self._validate_panic_code(code):
            self.process_event(Events.Disarm)
            self._panic_mode = "ACTIVE"
            # Let HA know that something changed
            self.schedule_update_ha_state()
            return

        if not self._validate_code(code, STATE_ALARM_DISARMED):
            return
        self.process_event(Events.Disarm)

    def alarm_arm_home(self, code):
        self.process_event(Events.ArmHome)

    def alarm_arm_away(self, code=None):
        self.process_event(Events.ArmAway)

    def alarm_arm_night(self, code=None):
        self.process_event(Events.ArmPerimeter)

    def alarm_trigger(self, code=None):
        self.process_event(Events.Trigger)

    ### Internal processing
    def setsignals(self, alarmMode):
        """ Figure out what to sense and how """
        if alarmMode == Events.ArmHome or alarmMode == Events.ArmAway:
            self.immediate = self._immediate.copy()
            self.delayed = self._delayed.copy()
        if alarmMode == Events.ArmHome:
            self.immediate -= self._ignore
            self.delayed -= self._ignore
        if alarmMode == Events.ArmPerimeter:
           self.immediate = self._perimeter.copy()
        self.ignored = self._allsensors - (self.immediate | self.delayed)

    def clearsignals(self):
        """ Clear all our signals, we aren't listening anymore """
        self._panic_mode = "deactivated"
        self.immediate = set()
        self.delayed = set()
        self.ignored = self._allsensors.copy()

    def process_event(self, event):
        old = self._state

        # Update state if applicable
        if event == Events.Disarm:
            self._state = STATE_ALARM_DISARMED
        elif event == Events.Trigger:
            self._state = STATE_ALARM_TRIGGERED 
        elif old == STATE_ALARM_DISARMED:
            if   event == Events.ArmHome:       self._state = STATE_ALARM_ARMED_HOME
            elif event == Events.ArmAway:       self._state = STATE_ALARM_PENDING
            elif event == Events.ArmPerimeter:       self._state = STATE_ALARM_ARMED_PERIMETER
        elif old == STATE_ALARM_PENDING:
            if   event == Events.Timeout:       self._state = STATE_ALARM_ARMED_AWAY
        elif old == STATE_ALARM_ARMED_HOME or \
             old == STATE_ALARM_ARMED_AWAY or \
             old == STATE_ALARM_ARMED_PERIMETER:
            if   event == Events.ImmediateTrip: self._state = STATE_ALARM_TRIGGERED
            elif event == Events.DelayedTrip:   self._state = STATE_ALARM_WARNING
        elif old == STATE_ALARM_WARNING:
            if   event == Events.Timeout:       self._state = STATE_ALARM_TRIGGERED
        elif old == STATE_ALARM_TRIGGERED:
            if   event == Events.Timeout:       self._state = self._returnto

        new = self._state
        if old != new: 
            _LOGGER.debug("Alarm changing from {} to {}".format(old, new))
            # Things to do on entering state
            if new == STATE_ALARM_WARNING:
                _LOGGER.debug("Turning on warning")
                switch.turn_on(self._hass, self._warning)
                self._timeoutat = now() + self._pending_time
            elif new == STATE_ALARM_TRIGGERED:
                _LOGGER.debug("Turning on alarm")
                switch.turn_on(self._hass, self._alarm)
                self._timeoutat = now() + self._trigger_time
            elif new == STATE_ALARM_PENDING:
                _LOGGER.debug("Pending user leaving house")
                switch.turn_on(self._hass, self._warning)
                self._timeoutat = now() + self._pending_time
                self._returnto = STATE_ALARM_ARMED_AWAY
                self.setsignals(Events.ArmAway)
            elif new == STATE_ALARM_ARMED_HOME:
                self._returnto = new
                self.setsignals(Events.ArmHome)
            elif new == STATE_ALARM_ARMED_AWAY:
                self._returnto = new
                self.setsignals(Events.ArmAway)
            elif new == STATE_ALARM_ARMED_PERIMETER:
                self._returnto = new
                self.setsignals(Events.ArmPerimeter)
            elif new == STATE_ALARM_DISARMED:
                self._returnto = new
                self.clearsignals()
  
            # Things to do on leaving state
            if old == STATE_ALARM_WARNING or old == STATE_ALARM_PENDING:
                _LOGGER.debug("Turning off warning")
                switch.turn_off(self._hass, self._warning)
            elif old == STATE_ALARM_TRIGGERED:
                _LOGGER.debug("Turning off alarm")
                switch.turn_off(self._hass, self._alarm)

            # Let HA know that something changed
            self.schedule_update_ha_state()

    def _validate_code(self, code, state):
        """Validate given code."""
        check = self._code is None or code == self._code
        if not check:
            _LOGGER.debug("Invalid code given for %s", state)
        return check

    def _validate_panic_code(self, code):
        """Validate given code."""
        check = code == self._panic_code
        if check:
           _LOGGER.warning("[ALARM] PANIC MODE ACTIVATED!!!")
        return check

    def async_added_to_hass(self):
        """Subscribe mqtt events.
        This method must be run in the event loop and returns a coroutine.
        """
        async_track_state_change(
            self.hass, self.entity_id, self._async_state_changed_listener
        )

        @callback
        def message_received(topic, payload, qos):
            """Run when new MQTT message has been received."""
            _LOGGER.error("[ALARM] MQTT Topic: %s Payload: %s", topic, payload)
            if payload == self._payload_disarm:
                self.alarm_disarm(self._code)
            elif payload == self._payload_arm_home:
                self.alarm_arm_home(self._code)
            elif payload == self._payload_arm_away:
                self.alarm_arm_away(self._code)
            elif payload == self._payload_arm_night:
                self.alarm_arm_night(self._code)
            else:
                _LOGGER.warning("Received unexpected payload: %s", payload)
                return

        return mqtt.async_subscribe(
            self.hass, self._command_topic, message_received, self._qos)

    @asyncio.coroutine
    def _async_state_changed_listener(self, entity_id, old_state, new_state):
        """Publish state change to MQTT."""
        mqtt.async_publish(self.hass, self._state_topic, new_state.state,
                           self._qos, True)
        _LOGGER.debug("[ALARM] MQTT state changed")
