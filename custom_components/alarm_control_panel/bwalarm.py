"""
  GazosCalvertos: Yet another take on a custom alarm for Home Assistant
"""
import asyncio
import copy
import datetime
import logging
import enum
import os
import re
import json
import pytz
import voluptuous as vol
from   operator   import attrgetter

from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMED_HOME, STATE_ALARM_DISARMED,
    STATE_ALARM_PENDING, STATE_ALARM_TRIGGERED, CONF_PLATFORM, CONF_NAME,
    CONF_CODE, CONF_PENDING_TIME, CONF_TRIGGER_TIME, CONF_DISARM_AFTER_TRIGGER,
    CONF_DELAY_TIME, EVENT_STATE_CHANGED, EVENT_TIME_CHANGED, 
    STATE_ON, STATE_OFF)

from homeassistant.core          import callback
from homeassistant.util.dt       import utcnow                       as now
from homeassistant.loader 		 import bind_hass
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.helpers.event import async_track_state_change
from homeassistant.util          import sanitize_filename

import homeassistant.components.alarm_control_panel                  as alarm
import homeassistant.components.switch                               as switch
import homeassistant.helpers.config_validation                       as cv

DOMAIN                      = 'alarm_control_panel'
#//--------------------SUPPORTED STATES----------------------------
STATE_ALARM_WARNING         = 'warning'
STATE_ALARM_ARMED_PERIMETER = 'armed_perimeter'
SUPPORTED_STATES            = [STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMED_HOME, STATE_ALARM_DISARMED, STATE_ALARM_PENDING,
                                STATE_ALARM_TRIGGERED, STATE_ALARM_WARNING, STATE_ALARM_ARMED_PERIMETER]

#SUPPORTED_PRETRIGGER_STATES = [state for state in SUPPORTED_STATES if state != STATE_ALARM_TRIGGERED]
SUPPORTED_PENDING_STATES    = [STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMED_HOME, STATE_ALARM_ARMED_PERIMETER]

#//-------------------STATES TO CHECK------------------------------
STATE_TRUE                         = 'true'
STATE_UNLOCKED                     = 'unlocked'
STATE_OPEN                         = 'open'
STATE_DETECTED                     = 'detected'
STATE_MOTION                       = 'motion'
STATE_MOTION_DETECTED              = 'motion_detected'
STATE_MOTION_DETECTED2             = 'motion detected'

STATE_FALSE                        = 'false'
STATE_LOCKED                       = 'locked'
STATE_CLOSED                       = 'closed'
STATE_UNDETECTED                   = 'undetected'
STATE_NO_MOTION                    = 'no_motion'
STATE_STANDBY                      = 'standby'

CONF_CUSTOM_SUPPORTED_STATUSES_ON  = 'custom_supported_statuses_on'
CONF_CUSTOM_SUPPORTED_STATUSES_OFF = 'custom_supported_statuses_off'

SUPPORTED_STATUSES_ON              = [STATE_ON, STATE_TRUE, STATE_UNLOCKED, STATE_OPEN, STATE_DETECTED, STATE_MOTION, STATE_MOTION_DETECTED, STATE_MOTION_DETECTED2]
SUPPORTED_STATUSES_OFF             = [STATE_OFF, STATE_FALSE, STATE_LOCKED, STATE_CLOSED, STATE_UNDETECTED, STATE_NO_MOTION, STATE_STANDBY]

#//-----------------YAML CONFIG OPTIONS----------------------------
CONF_CODES                     = 'codes'
CONF_NAME                      = 'name'
CONF_PANIC_CODE                = 'panic_code'
CONF_PASSCODE_ATTEMPTS         = 'passcode_attempts'
CONF_PASSCODE_ATTEMPTS_TIMEOUT = 'passcode_attempts_timeout'

#//-------------------SENSOR GROUPS--------------------------------
CONF_IMMEDIATE               = 'immediate'
CONF_DELAYED                 = 'delayed'
CONF_IGNORE                  = 'homemodeignore'
CONF_NOTATHOME               = 'notathome'
CONF_OVERRIDE                = 'override'
CONF_PERIMETER               = 'perimeter'

#//-----------------DEVICES TO ENABLE/DISBALE-----------------------
CONF_ALARM                   = 'alarm'
CONF_WARNING                 = 'warning'

#//----------------------OPTIONAL MODES------------------------------
CONF_PERIMETER_MODE          = 'perimeter_mode'
CONF_MQTT                    = 'mqtt'
CONF_CLOCK                   = 'clock'
CONF_WEATHER                 = 'weather'
CONF_PERSISTENCE             = 'persistence'
CONF_HIDE_SENSOR_GROUPS      = 'hide_sensor_groups'
CONF_HIDE_CUSTOM_PANEL       = 'hide_custom_panel'
CONF_HIDE_PASSCODE           = 'hide_passcode'
CONF_HIDE_SIDEBAR            = 'hide_sidebar'

#//-----------------------COLOURS------------------------------------
CONF_WARNING_COLOUR          = 'warning_colour'
CONF_PENDING_COLOUR          = 'pending_colour'
CONF_DISARMED_COLOUR         = 'disarmed_colour'
CONF_TRIGGERED_COLOUR        = 'triggered_colour'
CONF_ARMED_AWAY_COLOUR       = 'armed_away_colour'
CONF_ARMED_HOME_COLOUR       = 'armed_home_colour'

#//-----------------------MQTT RELATED-------------------------------
CONF_OVERRIDE_CODE           = 'override_code'
CONF_PAYLOAD_DISARM          = 'payload_disarm'
CONF_PAYLOAD_ARM_HOME        = 'payload_arm_home'
CONF_PAYLOAD_ARM_AWAY        = 'payload_arm_away'
CONF_PAYLOAD_ARM_NIGHT       = 'payload_arm_night'
CONF_QOS                     = 'qos'
CONF_STATE_TOPIC             = 'state_topic'
CONF_COMMAND_TOPIC           = 'command_topic'

class Events(enum.Enum):
    ImmediateTrip            = 1
    DelayedTrip              = 2
    ArmHome                  = 3
    ArmAway                  = 4
    Timeout                  = 5
    Disarm                   = 6
    Trigger                  = 7
    ArmPerimeter             = 8

_CODES_SCHEMA = vol.All(
    vol.Schema({
        vol.Required(CONF_NAME): 							cv.string,
        vol.Required(CONF_CODE): 							cv.string
    })
)

DEFAULT_STATE_PENDING_TIME = 0
DEFAULT_TRIGGER_TIME = 600 #Ten Minutes

def _state_validator(config): #Place a default value in that timers if there isnt specific ones set
    """Validate the state."""
    config = copy.deepcopy(config)
    for state in SUPPORTED_PENDING_STATES:
        if CONF_TRIGGER_TIME not in config[state]:
            config[state][CONF_TRIGGER_TIME] = config[CONF_TRIGGER_TIME]
        if CONF_PENDING_TIME not in config[state]:
            config[state][CONF_PENDING_TIME] = DEFAULT_STATE_PENDING_TIME if state != STATE_ALARM_ARMED_AWAY else config[CONF_PENDING_TIME]
    return config

def _state_schema(state):
    """Validate the state."""
    schema = {}
    if state in SUPPORTED_PENDING_STATES:
        schema[vol.Optional(CONF_TRIGGER_TIME)] = vol.All(vol.Coerce(int), vol.Range(min=1))
        schema[vol.Optional(CONF_PENDING_TIME)] = vol.All(vol.Coerce(int), vol.Range(min=0))
    return vol.Schema(schema)

PLATFORM_SCHEMA = vol.Schema(vol.All({
    vol.Required(CONF_PLATFORM):                                   'bwalarm',
    vol.Required(CONF_NAME, default='House'):                      cv.string,
    vol.Required(CONF_PENDING_TIME, default=25):                   vol.All(vol.Coerce(int), vol.Range(min=0)),
    vol.Required(CONF_TRIGGER_TIME, default=DEFAULT_TRIGGER_TIME): vol.All(vol.Coerce(int), vol.Range(min=1)),
    vol.Required(CONF_ALARM):                              cv.entity_id,  # switch/group to turn on when alarming [TODO]
    vol.Required(CONF_WARNING):                            cv.entity_id,  # switch/group to turn on when warning [TODO]
    vol.Optional(CONF_CUSTOM_SUPPORTED_STATUSES_ON):       vol.Schema([cv.string]),
    vol.Optional(CONF_CUSTOM_SUPPORTED_STATUSES_OFF):      vol.Schema([cv.string]),
    vol.Optional(CONF_CODE):                               cv.string,
    vol.Optional(CONF_CODES):                              vol.Schema([_CODES_SCHEMA]), # Schema to hold the list of names with codes allowed to disarm the alarm
    vol.Optional(CONF_PANIC_CODE):                         cv.string,
    vol.Optional(CONF_IMMEDIATE):                          cv.entity_ids, # things that cause an immediate alarm
    vol.Optional(CONF_DELAYED):                            cv.entity_ids, # things that allow a delay before alarm
    vol.Optional(CONF_IGNORE):                             cv.entity_ids, # things that we ignore when at home
    vol.Optional(CONF_NOTATHOME):                          cv.entity_ids, # things that we ignore when at home BACKWARDS COMPAT
    vol.Optional(CONF_OVERRIDE):                           cv.entity_ids, # sensors that can be ignored if open when trying to set alarm in away mode
    vol.Optional(CONF_PERIMETER):                          cv.entity_ids, # things monitored under perimeter mode
    #------------------------------STATE RELATED-------------------------
    vol.Optional(STATE_ALARM_ARMED_AWAY, default={}):      _state_schema(STATE_ALARM_ARMED_AWAY),  #state specific times
    vol.Optional(STATE_ALARM_ARMED_HOME, default={}):      _state_schema(STATE_ALARM_ARMED_HOME),  #state specific times
    vol.Optional(STATE_ALARM_ARMED_PERIMETER, default={}): _state_schema(STATE_ALARM_ARMED_PERIMETER), #state specific times
    vol.Optional(STATE_ALARM_DISARMED, default={}):        _state_schema(STATE_ALARM_DISARMED),    #state specific times
    vol.Optional(STATE_ALARM_TRIGGERED, default={}):       _state_schema(STATE_ALARM_TRIGGERED),   #state specific times
    #------------------------------GUI-----------------------------------
    vol.Optional(CONF_WARNING_COLOUR, default='orange'):   cv.string,     # Custom colour of warning display
    vol.Optional(CONF_PENDING_COLOUR, default='orange'):   cv.string,     # Custom colour of pending display
    vol.Optional(CONF_DISARMED_COLOUR, default='#03A9F4'): cv.string,     # Custom colour of disarmed display
    vol.Optional(CONF_TRIGGERED_COLOUR, default='red'):    cv.string,     # Custom colour of triggered display
    vol.Optional(CONF_ARMED_AWAY_COLOUR, default='black'): cv.string,     # Custom colour of armed away display
    vol.Optional(CONF_ARMED_HOME_COLOUR, default='black'): cv.string,     # Custom colour of armed home display
    #---------------------------OPTIONAL MODES---------------------------
    vol.Optional(CONF_PERIMETER_MODE, default=False):      cv.boolean,    # Enable perimeter mode?
    vol.Optional(CONF_PERSISTENCE, default=False):         cv.boolean,    # Enables persistence for alarm state
    vol.Optional(CONF_CLOCK, default=False):               cv.boolean,    # Display clock on panel
    vol.Optional(CONF_WEATHER, default=False):             cv.boolean,    # Display weather on panel
    vol.Optional(CONF_HIDE_SENSOR_GROUPS, default=False):  cv.boolean,    # Show sensor groups?
    vol.Optional(CONF_HIDE_CUSTOM_PANEL, default=True):    cv.boolean,    # Hides custom panel?
    vol.Optional(CONF_HIDE_PASSCODE, default=True):        cv.boolean,    # Show passcode entry during disarm?
    vol.Optional(CONF_HIDE_SIDEBAR, default=False):        cv.boolean,    # Show all sensors in group?
    #--------------------------PASSWORD ATTEMPTS--------------------------
    vol.Optional(CONF_PASSCODE_ATTEMPTS, default=-1):         vol.All(vol.Coerce(int), vol.Range(min=-1)),
    vol.Optional(CONF_PASSCODE_ATTEMPTS_TIMEOUT, default=-1): vol.All(vol.Coerce(int), vol.Range(min=-1)),
    #---------------------------MQTT RELATED------------------------------
    vol.Optional(CONF_MQTT, default=False):                     cv.boolean, # Allows MQTT functionality
    vol.Optional(CONF_QOS, default=0):                          vol.All(vol.Coerce(int), vol.Range(min=0)),
    vol.Optional(CONF_STATE_TOPIC, default='home/alarm'):       cv.string,
    vol.Optional(CONF_COMMAND_TOPIC, default='home/alarm/set'): cv.string,
    vol.Optional(CONF_PAYLOAD_ARM_AWAY, default='ARM_AWAY'):    cv.string,
    vol.Optional(CONF_PAYLOAD_ARM_HOME, default='ARM_HOME'):    cv.string,
    vol.Optional(CONF_PAYLOAD_ARM_NIGHT, default='ARM_NIGHT'):  cv.string,
    vol.Optional(CONF_PAYLOAD_DISARM, default='DISARM'):        cv.string,
    vol.Optional(CONF_OVERRIDE_CODE, default=False):            cv.boolean,
    #-----------------------------END------------------------------------
}, _state_validator))

_LOGGER = logging.getLogger(__name__)

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    #Setup MQTT if enabled
    mqtt = None
    if (config[CONF_MQTT]):
        import homeassistant.components.mqtt as mqtt
    alarm = BWAlarm(hass, config, mqtt)
    hass.bus.async_listen(EVENT_STATE_CHANGED, alarm.state_change_listener)
    hass.bus.async_listen(EVENT_TIME_CHANGED, alarm.time_change_listener)
    hass.bus.async_listen(EVENT_TIME_CHANGED, alarm.passcode_timeout_listener)
    async_add_devices([alarm])
  
class BWAlarm(alarm.AlarmControlPanel):

    def __init__(self, hass, config, mqtt):
        #------------------------------Initalize the alarm system----------------------------------
        self.mqtt                    = mqtt
        self._hass                   = hass
        self._name                   = config[CONF_NAME]
        self._alarm                  = config[CONF_ALARM]
        self._warning                = config[CONF_WARNING]
        self._panic_mode             = 'deactivated'

        self._countdown_time         = config[CONF_PENDING_TIME] #TODO: Modify this
        # self._pending_time           = datetime.timedelta(seconds=config[CONF_PENDING_TIME])
        # self._trigger_time           = datetime.timedelta(seconds=config[CONF_TRIGGER_TIME])

        self._trigger_time_by_state = {state: datetime.timedelta(seconds=config[state][CONF_TRIGGER_TIME]) for state in SUPPORTED_PENDING_STATES}
        self._pending_time_by_state = {state: datetime.timedelta(seconds=config[state][CONF_PENDING_TIME]) for state in SUPPORTED_PENDING_STATES}

        self._lasttrigger            = ""
        self._state                  = STATE_ALARM_DISARMED
        self._returnto               = STATE_ALARM_DISARMED
        self._armstate              = STATE_ALARM_DISARMED
        self._timeoutat              = None
        self._passcode_timeoutat     = None

        self._supported_statuses_on  = config.get(CONF_CUSTOM_SUPPORTED_STATUSES_ON, []) + SUPPORTED_STATUSES_ON
        self._supported_statuses_off = config.get(CONF_CUSTOM_SUPPORTED_STATUSES_OFF, []) + SUPPORTED_STATUSES_OFF

        #---------------------------------------SENSORS--------------------------------------------
        self._immediate              = set(config.get(CONF_IMMEDIATE, []))
        self._delayed                = set(config.get(CONF_DELAYED, []))
        self._ignore                 = set(config.get(CONF_IGNORE, []) if config.get(CONF_IGNORE, []) != [] else config.get(CONF_NOTATHOME, []))
        self._override               = set(config.get(CONF_OVERRIDE, []))
        self._perimeter              = set(config.get(CONF_PERIMETER, []))
        self._allsensors             = self._immediate | self._delayed | self._ignore
        self._opensensors            = None

        #------------------------------------PASSCODE RELATED------------------------------------- 
        self._code                   = config.get(CONF_CODE, None)
        #self._codes                  = set(config.get
        self._panic_code             = config.get(CONF_PANIC_CODE, None)
        self._panel_locked           = False
        self._passcodeAttemptNo      = 0
        self._passcodeAttemptAllowed = config[CONF_PASSCODE_ATTEMPTS]
        self._passcodeAttemptTimeout = config[CONF_PASSCODE_ATTEMPTS_TIMEOUT]

        #------------------------------------OPTIONAL MODES---------------------------------------
        self._perimeter_mode         = config[CONF_PERIMETER_MODE]
        self._persistence            = config[CONF_PERSISTENCE]
        self._hide_sensor_groups     = config[CONF_HIDE_SENSOR_GROUPS]
        self._hide_custom_panel      = config[CONF_HIDE_CUSTOM_PANEL]
        self._hide_passcode          = config[CONF_HIDE_PASSCODE]
        self._hide_sidebar           = config[CONF_HIDE_SIDEBAR]
        self._clock                  = config[CONF_CLOCK]
        self._weather                = config[CONF_WEATHER]

        #--------------------------------------GUI RELATED----------------------------------------       
        self._warning_colour         = config[CONF_WARNING_COLOUR]
        self._pending_colour         = config[CONF_PENDING_COLOUR]
        self._disarmed_colour        = config[CONF_DISARMED_COLOUR]
        self._triggered_colour       = config[CONF_TRIGGERED_COLOUR]
        self._armed_away_colour      = config[CONF_ARMED_AWAY_COLOUR]
        self._armed_home_colour      = config[CONF_ARMED_HOME_COLOUR]

        self.clearsignals()

        #-------------------------------------MQTT--------------------------------------------------
        self._mqtt                   = config[CONF_MQTT]
        self._qos                    = config[CONF_QOS]
        self._state_topic            = config[CONF_STATE_TOPIC]
        self._command_topic          = config[CONF_COMMAND_TOPIC]
        self._payload_disarm         = config[CONF_PAYLOAD_DISARM]
        self._payload_arm_home       = config[CONF_PAYLOAD_ARM_HOME]
        self._payload_arm_away       = config[CONF_PAYLOAD_ARM_AWAY]
        self._payload_arm_night      = config[CONF_PAYLOAD_ARM_NIGHT]
        self._override_code          = config[CONF_OVERRIDE_CODE]

        #------------------------------------persistence----------------------------------------------------
        self._persistence_list  = []
        if (self._persistence):
           persistence_path     = hass.config.path() #"alarm_persistence"

           if not os.path.isdir(persistence_path):
              _LOGGER.error("[ALARM] Persistence path %s does not exist.", persistence_path)
           else:
              self._persistence_final_path = os.path.join(persistence_path, "alarm.json")
              self.persistence_load()

              self._state     = self._persistence_list["state"]
              self._timeoutat = pytz.UTC.localize(datetime.datetime.strptime(self._persistence_list["timeoutat"].split(".")[0].replace("T"," "), '%Y-%m-%d %H:%M:%S')) if self._persistence_list["timeoutat"] != None else None
              self._returnto  = self._persistence_list["returnto"]

              self.save_alarm_state()

    # Alarm properties
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
            'immediate':                sorted(list(self.immediate)),
            'delayed':                  sorted(list(self.delayed)),
            'override':                 sorted(list(self._override)),
            'ignored':                  sorted(list(self.ignored)),
            'allsensors':               sorted(list(self._allsensors)),
            'perimeter':                sorted(list(self._perimeter)),
            'perimeter_mode':           self._perimeter_mode,
            'changedby':                self.changed_by,
            'warning_colour':           self._warning_colour,
            'pending_colour':           self._pending_colour,
            'disarmed_colour':          self._disarmed_colour,
            'triggered_colour':         self._triggered_colour,
            'armed_home_colour':        self._armed_home_colour,
            'armed_away_colour':        self._armed_away_colour,
            'panic_mode':               self._panic_mode,
            'countdown_time':           self._countdown_time,
            'clock':                    self._clock,
            'weather':                  self._weather,
            'persistence':              self._persistence,
        #    'settings_list':            self._persistence_list,
            'hide_sensor_groups':       self._hide_sensor_groups,
            'hide_custom_panel':        self._hide_custom_panel,
            'hide_passcode':            self._hide_passcode,
            'hide_sidebar':             self._hide_sidebar,
            'panel_locked':             self._panel_locked,
            'passcode_attempt_timeout': self._passcodeAttemptTimeout,
            'supported_statuses_on':    self._supported_statuses_on,
            'supported_statuses_off':   self._supported_statuses_off
        }

    ### LOAD persistence previously saved
    def persistence_load(self):
        try:
           if os.path.isfile(self._persistence_final_path):  #Find the persistence JSON file and load. Once found update the alarm_control_panel object
              self._persistence_list = json.load(open(self._persistence_final_path, 'r'))
           else: #No persistence file found
              _LOGGER.warning("[ALARM] Persistence file doesnt exist")
              self._persistence_list = json.loads('{"state":"disarmed", "timeoutat":null, "returnto":null}')

        except Exception as e:
           _LOGGER.error("[ALARM] Error occured loading: %s", str(e))

    ### UPDATE persistence
    def persistence_save(self, persistence): 
        if persistence is not None: #Check we have something to save [TODO] validate this is a persistence object
            self._persistence_list = persistence
            try:
               if self._persistence_list is not None: #Check we have genuine persistence to save if so dump to file
                  with open(self._persistence_final_path, 'w') as fil:
                     fil.write(json.dumps(self._persistence_list, ensure_ascii=False))
               else:
                  _LOGGER.error("[ALARM] No persistence to save!")
            except Exception as e:
               _LOGGER.error("[ALARM] Error occured saving: %s", str(e))


    ### Save alarm state
    def save_alarm_state(self):
        self._persistence_list["state"]     = self._state
        self._persistence_list["timeoutat"] = self._timeoutat.isoformat() if self._timeoutat != None else None
        self._persistence_list["returnto"]  = self._returnto
        self.persistence_save(self._persistence_list)
    
    ### Actions from the outside world that affect us, turn into enum events for internal processing
    def time_change_listener(self, eventignored):
        """ I just treat the time events as a periodic check, its simpler then (re-/un-)registration """
        if self._timeoutat is not None:
            if now() > self._timeoutat:
                self._timeoutat = None
                self.process_event(Events.Timeout)

    def state_change_listener(self, event):
        """ Something changed, we only care about things turning on at this point """

        if self._state != STATE_ALARM_DISARMED:
            new = event.data.get('new_state', None)
            if new is None:
                return

            if new.state != None:
                if new.state.lower() in self._supported_statuses_on:
                    eid = event.data['entity_id']
                    if eid in self.immediate:
                        self._lasttrigger = eid
                        self.process_event(Events.ImmediateTrip)
                    elif eid in self.delayed:
                        self._lasttrigger = eid
                        self.process_event(Events.DelayedTrip)

    def check_open_sensors(self):
        for sensor in self._allsensors:    
            if self._hass.states.get(sensor).state != None:
                if self._hass.states.get(sensor).state in self._supported_statuses_on:
                    _LOGGER.error(self._hass.states.get(sensor)) # do summit

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
        return 'DISARMED'

    def alarm_arm_home(self, code=None):
        if code == "-1":
            self.process_event(Events.ArmHome, True)
        else:
            self.process_event(Events.ArmHome)

    def alarm_arm_away(self, code=None):
        if code == "-1":
            self.process_event(Events.ArmAway, True)
        else:
            self.process_event(Events.ArmAway)

    def alarm_arm_night(self, code=None):
        if code == "-1":
            self.process_event(Events.ArmPerimeter, True)
        else:
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
        self._armstate = STATE_ALARM_DISARMED
        self.immediate = set()
        self.delayed = set()
        self.ignored = self._allsensors.copy()
        self._timeoutat = None

    def process_event(self, event, override_pending_time=False):
        old_state = self._state
        
        #Update the state of the alarm panel
        if event == Events.Disarm:
            self._state = STATE_ALARM_DISARMED

        elif event == Events.Trigger:
            self._state = STATE_ALARM_TRIGGERED 

        #If there is a pending time set in either of the state configs then drop into pending mode else simply arm the alarm
        elif old_state == STATE_ALARM_DISARMED:
            if   event == Events.ArmHome:       
                if (self._pending_time_by_state[STATE_ALARM_ARMED_HOME] and override_pending_time == False):
                    self._state = STATE_ALARM_PENDING
                else:
                    self._state = STATE_ALARM_ARMED_HOME
                self._armstate = STATE_ALARM_ARMED_HOME
            
            elif event == Events.ArmAway:       
                if (self._pending_time_by_state[STATE_ALARM_ARMED_AWAY] and override_pending_time == False):
                    self._armstate = STATE_ALARM_ARMED_AWAY
                    self._state = STATE_ALARM_PENDING
                else:
                    self._state = STATE_ALARM_ARMED_AWAY
                self._armstate = STATE_ALARM_ARMED_AWAY

            elif event == Events.ArmPerimeter:  
                if (self._pending_time_by_state[STATE_ALARM_ARMED_PERIMETER] and override_pending_time == False):
                    self._armstate = STATE_ALARM_ARMED_PERIMETER
                    self._state = STATE_ALARM_PENDING
                else:
                    self._state = STATE_ALARM_ARMED_PERIMETER
                self._armstate = STATE_ALARM_ARMED_PERIMETER

        elif old_state == STATE_ALARM_PENDING:
            if   event == Events.Timeout:       self._state = self._armstate

        elif old_state == STATE_ALARM_ARMED_HOME or \
             old_state == STATE_ALARM_ARMED_AWAY or \
             old_state == STATE_ALARM_ARMED_PERIMETER:
            if   event == Events.ImmediateTrip: self._state = STATE_ALARM_TRIGGERED
            elif event == Events.DelayedTrip:   self._state = STATE_ALARM_WARNING

        elif old_state == STATE_ALARM_WARNING:
            if   event == Events.Timeout:       self._state = STATE_ALARM_TRIGGERED

        elif old_state == STATE_ALARM_TRIGGERED:
            if   event == Events.Timeout:       self._state = self._returnto

        new_state = self._state
        if old_state != new_state: 
            _LOGGER.debug("[ALARM] Alarm changing from {} to {}".format(old_state, new_state))
            # Things to do on entering state
            if new_state == STATE_ALARM_WARNING:
                _LOGGER.debug("[ALARM] Turning on warning")
                switch.turn_on(self._hass, self._warning)
                self._timeoutat = now() +  self._pending_time_by_state[self._armstate]
            elif new_state == STATE_ALARM_TRIGGERED:
                _LOGGER.debug("[ALARM] Turning on alarm")
                switch.turn_on(self._hass, self._alarm)
                self._timeoutat = now() + self._trigger_time_by_state[self._armstate]
            elif new_state == STATE_ALARM_PENDING:
                _LOGGER.debug("[ALARM] Pending user leaving house")
                switch.turn_on(self._hass, self._warning)
                self._timeoutat = now() + self._pending_time_by_state[self._armstate]
                #self._returnto = STATE_ALARM_ARMED_AWAY
                self.setsignals(event)
            elif new_state == STATE_ALARM_ARMED_HOME:
                self._returnto = new_state
                self.setsignals(Events.ArmHome)
            elif new_state == STATE_ALARM_ARMED_AWAY:
                self._returnto = new_state
                self.setsignals(Events.ArmAway)
            elif new_state == STATE_ALARM_ARMED_PERIMETER:
                self._returnto = new_state
                self.setsignals(Events.ArmPerimeter)
            elif new_state == STATE_ALARM_DISARMED:
                self._returnto = new_state
                self.clearsignals()
  
            # Things to do on leaving state
            if old_state == STATE_ALARM_WARNING or old_state == STATE_ALARM_PENDING:
                _LOGGER.debug("[ALARM] Turning off warning")
                switch.turn_off(self._hass, self._warning)
                
            elif old_state == STATE_ALARM_TRIGGERED:
                _LOGGER.debug("[ALARM] Turning off alarm")
                switch.turn_off(self._hass, self._alarm)

            # Let HA know that something changed
            if self._persistence:
                self.save_alarm_state()
            self.schedule_update_ha_state()

    def _validate_code(self, code, state):
        """Validate given code."""
        if ((self._passcodeAttemptAllowed == -1) or (self._passcodeAttemptNo <= self._passcodeAttemptAllowed)):
            check = self._code is None or code == self._code
            if check:
                self._passcodeAttemptNo = 0
            else:
                _LOGGER.debug("[ALARM] Invalid code given for %s", state)
                self._passcodeAttemptNo += 1   
                if (self._passcodeAttemptAllowed != -1 and self._passcodeAttemptNo > self._passcodeAttemptAllowed):
                    self._panel_locked = True
                    self._passcode_timeoutat = now() + datetime.timedelta(seconds=self._passcodeAttemptTimeout)
                    _LOGGER.warning("[ALARM] Panel locked, too many passcode attempts!")
            self.schedule_update_ha_state()
            return check
        else:
            _LOGGER.warning("[ALARM] Too many passcode attempts, try again later")
            return False

    def _validate_panic_code(self, code):
        """Validate given code."""
        check = code == self._panic_code
        if check:
            _LOGGER.warning("[ALARM] PANIC MODE ACTIVATED!!!")
            self._passcodeAttemptNo = 0
        return check

    ### Actions from the outside world that affect us, turn into enum events for internal processing
    def passcode_timeout_listener(self, eventignored):
        if self._passcode_timeoutat is not None:
            if now() > self._passcode_timeoutat:
                self._panel_locked = False
                self._passcode_timeoutat = None
                self._passcodeAttemptNo = 0
                self.schedule_update_ha_state()

    @asyncio.coroutine
    def async_added_to_hass(self):
        """Subscribe mqtt events.
        This method must be run in the event loop and returns a coroutine.
        """
        if (self._mqtt):
            async_track_state_change(
                self.hass, self.entity_id, self._async_state_changed_listener
            )

        @callback
        def message_received(topic, payload, qos):
            """Run when new MQTT message has been received."""
            #_LOGGER.warning("[ALARM] MQTT Topic: %s Payload: %s", topic, payload)
            if payload.split(" ")[0] == self._payload_disarm:
                #_LOGGER.warning("Disarming %s", payload)
                #TODO self._hass.states.get('binary_sensor.siren_sensor') #Use this method to relay open states
                if (self._override_code):
                    self.alarm_disarm(self._code)
                else:
                    self.alarm_disarm(payload.split(" ")[1])
            elif payload == self._payload_arm_home:
                self.alarm_arm_home('')
            elif payload == self._payload_arm_away:
                self.alarm_arm_away('')
            elif payload == self._payload_arm_night:
                self.alarm_arm_night('')
            else:
                _LOGGER.warning("[ALARM/MQTT] Received unexpected payload: %s", payload)
                return
        if (self._mqtt):
            return self.mqtt.async_subscribe(
                self.hass, self._command_topic, message_received, self._qos)
        
    @asyncio.coroutine
    def _async_state_changed_listener(self, entity_id, old_state, new_state):
        """Publish state change to MQTT."""
        if (self._mqtt):
            self.mqtt.async_publish(self.hass, self._state_topic, new_state.state,
                           self._qos, True)
            _LOGGER.debug("[ALARM/MQTT] State changed")
