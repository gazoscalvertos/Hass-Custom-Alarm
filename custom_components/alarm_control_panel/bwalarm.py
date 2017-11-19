"""
  My take on the manual alarm control panel
"""
import asyncio
import datetime
import logging
import enum
import re
import voluptuous as vol
from operator import attrgetter

from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMED_HOME, STATE_ALARM_DISARMED,
    STATE_ALARM_PENDING, STATE_ALARM_TRIGGERED, CONF_PLATFORM, CONF_NAME,
    CONF_CODE, CONF_PENDING_TIME, CONF_TRIGGER_TIME, CONF_DISARM_AFTER_TRIGGER,
    EVENT_STATE_CHANGED, EVENT_TIME_CHANGED, 
    STATE_ON)
from homeassistant.util.dt import utcnow as now
from homeassistant.helpers.event import async_track_point_in_time
import homeassistant.components.alarm_control_panel as alarm
import homeassistant.components.switch as switch
import homeassistant.helpers.config_validation as cv

#CONF_HEADSUP        = 'headsup'
CONF_IMMEDIATE      = 'immediate'
CONF_DELAYED        = 'delayed'
CONF_IGNORE         = 'homemodeignore'
CONF_NOTATHOME      = 'notathome'
CONF_OVERRIDE       = 'override'
CONF_PERIMETER_MODE = 'perimeter_mode'
CONF_PERIMETER      = 'perimeter'
CONF_ALARM          = 'alarm'
CONF_WARNING        = 'warning'

CONF_WARNING_COLOUR  = 'warning_colour'
CONF_PENDING_COLOUR  = 'pending_colour'
CONF_DISARMED_COLOUR  = 'disarmed_colour'
CONF_TRIGGERED_COLOUR  = 'triggered_colour'
CONF_ARMED_AWAY_COLOUR  = 'armed_away_colour'
CONF_ARMED_HOME_COLOUR  = 'armed_home_colour'

CONF_CLOCK = 'clock'
CONF_WEATHER = 'weather'

# Add a new state for the time after an delayed sensor and an actual alarm
STATE_ALARM_WARNING = 'warning'
STATE_ALARM_ARMED_PERIMETER = 'armed_perimeter'
class Events(enum.Enum):
    ImmediateTrip = 1
    DelayedTrip   = 2
    ArmHome       = 3
    ArmAway       = 4
    Timeout       = 5
    Disarm        = 6
    Trigger       = 7
    ArmPerimeter  = 8
    
PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_PLATFORM):  'bwalarm',
    vol.Required(CONF_NAME):      cv.string,
    vol.Required(CONF_PENDING_TIME): vol.All(vol.Coerce(int), vol.Range(min=0)),
    vol.Required(CONF_TRIGGER_TIME): vol.All(vol.Coerce(int), vol.Range(min=1)),
    vol.Required(CONF_ALARM):     cv.entity_id,  # switch/group to turn on when alarming
    vol.Required(CONF_WARNING):   cv.entity_id,  # switch/group to turn on when warning
    vol.Optional(CONF_CODE):      cv.string,
    #vol.Optional(CONF_HEADSUP):   cv.entity_ids, # things to show as a headsup, not alarm on
    vol.Optional(CONF_IMMEDIATE): cv.entity_ids, # things that cause an immediate alarm
    vol.Optional(CONF_DELAYED):   cv.entity_ids, # things that allow a delay before alarm
    vol.Optional(CONF_IGNORE): cv.entity_ids,  # things that we ignore when at home
    vol.Optional(CONF_NOTATHOME): cv.entity_ids,  # things that we ignore when at home BACKWARDS COMPAT
    vol.Optional(CONF_OVERRIDE): cv.entity_ids,  # sensors that can be ignored if open when trying to set alarm in away mode
    vol.Optional(CONF_PERIMETER_MODE): cv.boolean,  # Enable perimeter mode?
    vol.Optional(CONF_PERIMETER): cv.entity_ids,  # things monitored under perimeter mode
    vol.Optional(CONF_WARNING_COLOUR):   cv.string, # Custom colour of warning display
    vol.Optional(CONF_PENDING_COLOUR): cv.string, # Custom colour of pending display
    vol.Optional(CONF_DISARMED_COLOUR):   cv.string, # Custom colour of disarmed display
    vol.Optional(CONF_TRIGGERED_COLOUR): cv.string,  # Custom colour of triggered display
    vol.Optional(CONF_ARMED_AWAY_COLOUR): cv.string,  # Custom colour of armed away display
    vol.Optional(CONF_ARMED_HOME_COLOUR): cv.string,  # Custom colour of armed home display
    vol.Optional(CONF_CLOCK): cv.boolean,  # DIsplay clock on panel
    vol.Optional(CONF_WEATHER): cv.boolean  # DIsplay weather on panel
})

_LOGGER = logging.getLogger(__name__)

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    alarm = BWAlarm(hass, config)
    hass.bus.async_listen(EVENT_STATE_CHANGED, alarm.state_change_listener)
    hass.bus.async_listen(EVENT_TIME_CHANGED, alarm.time_change_listener)
    async_add_devices([alarm])


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
       
        self._countdown_time = config[CONF_PENDING_TIME]
        self._pending_time = datetime.timedelta(seconds=config[CONF_PENDING_TIME])
        self._trigger_time = datetime.timedelta(seconds=config[CONF_TRIGGER_TIME])

        self._lasttrigger  = ""
        self._state        = STATE_ALARM_DISARMED
        self._returnto     = STATE_ALARM_DISARMED
        self._timeoutat    = None
       
        self._warning_colour = config.get(CONF_WARNING_COLOUR, 'orange')
        self._pending_colour = config.get(CONF_PENDING_COLOUR, 'orange')
        self._disarmed_colour = config.get(CONF_DISARMED_COLOUR, '#03A9F4')
        self._triggered_colour = config.get(CONF_TRIGGERED_COLOUR, 'red')
        self._armed_away_colour = config.get(CONF_ARMED_AWAY_COLOUR, 'black')
        self._armed_home_colour = config.get(CONF_ARMED_HOME_COLOUR, 'black')
       
        self._clock = config.get(CONF_CLOCK, False)
        self._weather = config.get(CONF_WEATHER, False)

        self.clearsignals()

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
            'immediate':  sorted(list(self._immediate)),
            'delayed':    sorted(list(self._delayed)),
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
            'countdown_time':  self._countdown_time,
            'clock':  self._clock,
            'weather':  self._weather
        }


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
        if new is None or new.state.lower() != STATE_ON:
            return
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
        if not self._validate_code(code, STATE_ALARM_DISARMED):
            return
        self.process_event(Events.Disarm)

    def alarm_arm_home(self, code):
        _LOGGER.warning(code)
        #if not self._validate_code(code, STATE_ALARM_ARMED_HOME):
        #    return
        self.process_event(Events.ArmHome)

    def alarm_arm_away(self, code=None):
        #if not self._validate_code(code, STATE_ALARM_ARMED_AWAY):
        #    return
        self.process_event(Events.ArmAway)

    def alarm_arm_night(self, code=None):
        self.process_event(Events.ArmPerimeter)

    def alarm_trigger(self, code=None):
        self.process_event(Events.Trigger)


    ### Internal processing

    def setsignals(self, alarmMode):
        """ Figure out what to sense and how """
        if alarmMode == Events.ArmHome or alarmMode == Events.ArmAway:
            self.immediate = self._immediate
            self.delayed = self._delayed
        if alarmMode == Events.ArmHome:
            self.immediate -= self._ignore
            self.delayed -= self._ignore
        if alarmMode == Events.ArmPerimeter:
           self.immediate = self._perimeter
        self.ignored = self._allsensors - (self.immediate | self.delayed)

    def clearsignals(self):
        """ Clear all our signals, we aren't listening anymore """
        self.immediate = set()
        self.delayed = set()
        self.ignored = self._allsensors.copy()

    def process_event(self, event):
        """ 
           WARNING THIS CODE HAS CHANGED. NOTE LIKELY INCORRECT. 
           This is the core logic function.
           The possible states and things that can change our state are:
                 Actions:  isensor dsensor timeout arm_home arm_away disarm trigger
           Current State: 
             disarmed         X       X       X      armh     pend     *     trig
             pending(T1)      X       X      arma     X        X      dis    trig
             armed(h/a)      trig    warn     X       X        X      dis    trig
             warning(T1)      X       X      trig     X        X      dis    trig
             triggered(T2)    X       X      last     X        X      dis     *
           As the only non-timed states are disarmed, armed_home and armed_away,
           they are the only ones we can return to after an alarm.
        """
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
                #self.setsignals(False)
                self.setsignals(Events.ArmAway)
            elif new == STATE_ALARM_ARMED_HOME:
                self._returnto = new
                #self.setsignals(True)
                self.setsignals(Events.ArmHome)
            elif new == STATE_ALARM_ARMED_AWAY:
                self._returnto = new
                #self.setsignals(False)
                self.setsignals(Events.ArmAway)
            elif new == STATE_ALARM_ARMED_PERIMETER:
                self._returnto = new
                #self.setsignals(False)
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
            _LOGGER.warning("Invalid code given for %s", state)
        return check
