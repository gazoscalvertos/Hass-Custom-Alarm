"""
  CUSTOM ALARM COMPONENT BWALARM
  https://github.com/gazoscalvertos/Hass-Custom-Alarm
  VERSION:  1.0.4
  MODIFIED: 18/04/18
  GazosCalvertos: Yet another take on a custom alarm for Home Assistant

  CHANGE LOG:
  -Custom 'Home Alarm' message
  -Multicodes inc name & pictures
  -Activity Log
  -Log size as alarm option (default 10)
  -Panic mode only shows a deafult disarm message
  -Camera options added
  -Added optional code to arm mode
  -Added changed by user for UI/automation purposes
  -Removed duplicate change by
  -Override code added to immediate arm
  -Added YAML Editor

  TODO

"""

REQUIREMENTS = ['ruamel.yaml==0.15.42']

import asyncio
import sys
import copy
import datetime
import logging
import enum
import os
import re
import json
import pytz
import copy
import hashlib

from homeassistant.const         import (
    STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMED_HOME, STATE_ALARM_DISARMED,
    STATE_ALARM_PENDING, STATE_ALARM_TRIGGERED, CONF_PLATFORM, CONF_NAME,
    CONF_CODE, CONF_PENDING_TIME, CONF_TRIGGER_TIME, CONF_DISARM_AFTER_TRIGGER,
    CONF_DELAY_TIME, EVENT_STATE_CHANGED, EVENT_TIME_CHANGED, 
    STATE_ON, STATE_OFF)

from operator                    import attrgetter
from homeassistant.core          import callback
from homeassistant.util.dt       import utcnow                       as now
from homeassistant.loader        import bind_hass
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.helpers.event import async_track_state_change
from homeassistant.util          import sanitize_filename

import voluptuous                                                    as vol
import homeassistant.components.alarm_control_panel                  as alarm
import homeassistant.components.switch                               as switch
import homeassistant.helpers.config_validation                       as cv

VERSION                            = '1.0.4'

DOMAIN                             = 'alarm_control_panel'
#//--------------------SUPPORTED STATES----------------------------
STATE_ALARM_WARNING                = 'warning'
STATE_ALARM_ARMED_PERIMETER        = 'armed_perimeter'
SUPPORTED_STATES                   = [STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMED_HOME, STATE_ALARM_DISARMED, STATE_ALARM_PENDING,
                                     STATE_ALARM_TRIGGERED, STATE_ALARM_WARNING, STATE_ALARM_ARMED_PERIMETER]

SUPPORTED_PENDING_STATES           = [STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMED_HOME, STATE_ALARM_ARMED_PERIMETER]

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
CONF_STATES                        = 'states'
CONF_USERS                         = 'users'
CONF_NAME                          = 'name'
CONF_PICTURE                       = 'picture'
CONF_ENABLED                       = 'enabled'
CONF_CODE_TO_ARM                   = 'code_to_arm'
CONF_PANIC_CODE                    = 'panic_code'
CONF_PASSCODE_ATTEMPTS             = 'passcode_attempts'
CONF_PASSCODE_ATTEMPTS_TIMEOUT     = 'passcode_attempts_timeout'
CONF_WARNING_TIME                  = 'warning_time'

#//-------------------SENSOR GROUPS--------------------------------
CONF_IMMEDIATE                     = 'immediate'
CONF_DELAYED                       = 'delayed'
CONF_IGNORE                        = 'homemodeignore'
CONF_NOTATHOME                     = 'notathome'
CONF_OVERRIDE                      = 'override'
CONF_PERIMETER                     = 'perimeter'

#//-----------------DEVICES TO ENABLE/DISBALE-----------------------
CONF_ALARM                         = 'alarm'
CONF_WARNING                       = 'warning'

#//----------------------OPTIONAL MODES------------------------------
CONF_ENABLE_PERIMETER_MODE         = 'enable_perimeter_mode'
CONF_ENABLE_PERSISTENCE            = 'enable_persistence'

#//----------------------PANEL RELATED------------------------------
CONF_GUI                           = 'gui'
CONF_PANEL                         = 'panel'
CONF_ColorS                       = 'colors'
CONF_THEMES                        = 'themes'
# CONF_ENABLE_SENSORS_PANEL          = 'enable_sensors_panel'
# CONF_ENABLE_CUSTOM_PANEL           = 'enable_custom_panel'
# CONF_ENABLE_CAMERA_PANEL           = 'enable_camera_panel'
# CONF_ENABLE_FLOORPLAN_PANEL        = 'enable_floorplan_panel'
# CONF_HIDE_PASSCODE                 = 'hide_passcode'
# CONF_HIDE_SIDEBAR                  = 'hide_sidebar'
# CONF_CLOCK                         = 'clock'
# CONF_WEATHER                       = 'weather'
# CONF_LANGUAGE                      = 'language'
# CONF_FLOORPLAN                     = 'floorplan'
# CONF_ROUND_BUTTONS                 = 'round_buttons'
# CONF_PANEL_TITLE                   = 'panel_title'
# CONF_ENABLE_SERIF_FONT             = 'panel_enable_serif_font'
CONF_ADMIN_PASSWORD                = 'admin_password'

#//-----------------------ColorS------------------------------------
CONF_WARNING_Color                = 'warning_color'
CONF_PENDING_Color                = 'pending_color'
CONF_DISARMED_Color               = 'disarmed_color'
CONF_TRIGGERED_Color              = 'triggered_color'
CONF_ARMED_AWAY_Color             = 'armed_away_color'
CONF_ARMED_HOME_Color             = 'armed_home_color'
CONF_PERIMETER_Color              = 'perimeter_color'

#//-----------------------MQTT RELATED-------------------------------
CONF_MQTT                          = 'mqtt'
CONF_OVERRIDE_CODE                 = 'override_code'
CONF_PAYLOAD_DISARM                = 'payload_disarm'
CONF_PAYLOAD_ARM_HOME              = 'payload_arm_home'
CONF_PAYLOAD_ARM_AWAY              = 'payload_arm_away'
CONF_PAYLOAD_ARM_NIGHT             = 'payload_arm_night'
CONF_QOS                           = 'qos'
CONF_STATE_TOPIC                   = 'state_topic'
CONF_COMMAND_TOPIC                 = 'command_topic'
CONF_PENDING_ON_WARNING            = 'pending_on_warning'

#//-----------------------LOG RELATED--------------------------------
CONF_LOG                           = 'log'
CONF_LOG_SIZE                      = 'log_size'

#//-----------------------CAMERA RELATED--------------------------------
CONF_CAMERAS                       = 'cameras'

#//-----------------------YAML RELATED--------------------------------
# 
CONF_YAML_ALLOW_EDIT               = 'yaml_allow_edit'

class Events(enum.Enum):
    ImmediateTrip            = 1
    DelayedTrip              = 2
    ArmHome                  = 3
    ArmAway                  = 4
    Timeout                  = 5
    Disarm                   = 6
    Trigger                  = 7
    ArmPerimeter             = 8

_USER_SCHEMA = vol.All(
    vol.Schema({
        vol.Required(CONF_NAME):                            cv.string,
        vol.Optional(CONF_PICTURE):                         cv.string,
        vol.Required(CONF_CODE):                            cv.string,
        vol.Optional(CONF_ENABLED, default=True):           cv.boolean
        ##ADD TIME BASED SETTINGS
    })
)

DEFAULT_PENDING_TIME = 0   #0 Seconds
DEFAULT_WARNING_TIME = 0   #0 Seconds
DEFAULT_TRIGGER_TIME = 600 #Ten Minutes

def _state_validator(config): #Place a default value in that timers if there isnt specific ones set
    """Validate the state."""
    config = copy.deepcopy(config)
    for state in SUPPORTED_PENDING_STATES:
        if CONF_TRIGGER_TIME not in config[state]:
            config[state][CONF_TRIGGER_TIME] = config[CONF_TRIGGER_TIME]
        if CONF_PENDING_TIME not in config[state]:
            config[state][CONF_PENDING_TIME] = DEFAULT_STATE_PENDING_TIME if state != STATE_ALARM_ARMED_AWAY else config[CONF_PENDING_TIME]
        if CONF_WARNING_TIME not in config[state]:
            config[state][CONF_WARNING_TIME] = DEFAULT_STATE_WARNING_TIME if state != STATE_ALARM_ARMED_AWAY else config[CONF_WARNING_TIME]
    return config

def _state_schema():
    """Validate the state."""
    schema = {}
    # if state in SUPPORTED_PENDING_STATES:
    schema[vol.Optional(CONF_TRIGGER_TIME, default=DEFAULT_TRIGGER_TIME)] = vol.All(vol.Coerce(int), vol.Range(min=-1))
    schema[vol.Optional(CONF_PENDING_TIME, default=DEFAULT_PENDING_TIME)] = vol.All(vol.Coerce(int), vol.Range(min=0))
    schema[vol.Optional(CONF_WARNING_TIME, default=DEFAULT_WARNING_TIME)] = vol.All(vol.Coerce(int), vol.Range(min=0))
    schema[vol.Optional(CONF_IMMEDIATE,    default=[])]                   = cv.entity_ids # things that cause an immediate alarm
    schema[vol.Optional(CONF_DELAYED,      default=[])]                   = cv.entity_ids # things that allow a delay before alarm
    schema[vol.Optional(CONF_OVERRIDE,     default=[])]                   = cv.entity_ids # sensors that can be ignored if open when trying to set alarm
    return vol.Schema(schema)

# ColorS_SCHEMA = vol.Schema({
#     vol.Optional(CONF_WARNING_Color,    default='orange'):       cv.string,     # Custom color of warning
#     vol.Optional(CONF_PENDING_Color,    default='orange'):       cv.string,     # Custom color of pending
#     vol.Optional(CONF_DISARMED_Color,   default='#03A9F4'):      cv.string,     # Custom color of disarmed
#     vol.Optional(CONF_TRIGGERED_Color,  default='red'):          cv.string,     # Custom color of triggered
#     vol.Optional(CONF_ARMED_AWAY_Color, default='black'):        cv.string,     # Custom color of armed away
#     vol.Optional(CONF_ARMED_HOME_Color, default='black'):        cv.string,     # Custom color of armed home
#     vol.Optional(CONF_PERIMETER_Color,  default='black'):        cv.string,     # Custom color of perimeter
#     vol.Optional(cv.slug):                                        cv.string,
# })

PANEL_SCHEMA = vol.Schema({
	vol.Optional(CONF_CAMERAS):                                   cv.entity_ids,
	vol.Optional(CONF_ADMIN_PASSWORD, default='HG28!!&dn'):       cv.string,     # Admin panel password
    vol.Optional(cv.slug):                                        cv.string,
})

THEMES_SCHEMA = vol.Schema({
    vol.Optional(cv.slug):                                        vol.Schema({vol.Optional(cv.slug): cv.string,}),
})

MQTT_SCHEMA = vol.Schema({
    vol.Optional(CONF_QOS):                                       vol.All(vol.Coerce(int), vol.Range(min=0)),
    vol.Optional(CONF_STATE_TOPIC):                               cv.string,
    vol.Optional(CONF_COMMAND_TOPIC):                             cv.string,
    vol.Optional(CONF_PAYLOAD_ARM_AWAY):                          cv.string,
    vol.Optional(CONF_PAYLOAD_ARM_HOME):                          cv.string,
    vol.Optional(CONF_PAYLOAD_ARM_NIGHT):                         cv.string,
    vol.Optional(CONF_PAYLOAD_DISARM):                            cv.string,
    vol.Optional(CONF_OVERRIDE_CODE):                             cv.boolean,
    vol.Optional(CONF_PENDING_ON_WARNING):                        cv.boolean,
})

PLATFORM_SCHEMA = vol.Schema(vol.All({
    vol.Required(CONF_PLATFORM):                                  'bwalarm',
    vol.Optional(CONF_NAME, default='House'):                      cv.string,
    vol.Optional(CONF_PENDING_TIME, default=25):                   vol.All(vol.Coerce(int), vol.Range(min=0)),
    vol.Optional(CONF_WARNING_TIME, default=25):                   vol.All(vol.Coerce(int), vol.Range(min=0)),
    vol.Optional(CONF_TRIGGER_TIME, default=DEFAULT_TRIGGER_TIME): vol.All(vol.Coerce(int), vol.Range(min=1)),
    vol.Optional(CONF_ALARM):                                      cv.entity_id,  # switch/group to turn on when alarming [TODO]
    vol.Optional(CONF_WARNING):                                    cv.entity_id,  # switch/group to turn on when warning [TODO]
    vol.Optional(CONF_CUSTOM_SUPPORTED_STATUSES_ON):               vol.Schema([cv.string]),
    vol.Optional(CONF_CUSTOM_SUPPORTED_STATUSES_OFF):              vol.Schema([cv.string]),
    vol.Optional(CONF_CODE):                                       cv.string,
    vol.Optional(CONF_USERS):                                      vol.Schema([_USER_SCHEMA]), # Schema to hold the list of names with codes allowed to disarm the alarm
    vol.Optional(CONF_PANIC_CODE):                                 cv.string,

    #------------------------------STATE RELATED-------------------------
    vol.Optional(CONF_STATES):                                     vol.Schema({cv.slug: _state_schema()}),
    vol.Optional(STATE_ALARM_ARMED_AWAY, default={}):              _state_schema(),  #state specific times ###REMOVE###
    vol.Optional(STATE_ALARM_ARMED_HOME, default={}):              _state_schema(),  #state specific times ###REMOVE###
    vol.Optional(STATE_ALARM_ARMED_PERIMETER, default={}):         _state_schema(), #state specific times ###REMOVE###
    # vol.Optional(STATE_ALARM_DISARMED, default={}):                _state_schema(STATE_ALARM_DISARMED),    #state specific times ###REMOVE###
    # vol.Optional(STATE_ALARM_TRIGGERED, default={}):               _state_schema(STATE_ALARM_TRIGGERED),   #state specific times ###REMOVE###

    #------------------------------GUI-----------------------------------
    vol.Optional(CONF_PANEL):                                        PANEL_SCHEMA,
    vol.Optional(CONF_THEMES):                                       THEMES_SCHEMA,
    # vol.Optional(CONF_WARNING_Color, default='orange'):           cv.string,     # Custom color of warning display ###REMOVE###
    # vol.Optional(CONF_PENDING_Color, default='orange'):           cv.string,     # Custom color of pending display ###REMOVE###
    # vol.Optional(CONF_DISARMED_Color, default='#03A9F4'):         cv.string,     # Custom color of disarmed display ###REMOVE###
    # vol.Optional(CONF_TRIGGERED_Color, default='red'):            cv.string,     # Custom color of triggered display ###REMOVE###
    # vol.Optional(CONF_ARMED_AWAY_Color, default='black'):         cv.string,     # Custom color of armed away display ###REMOVE###
    # vol.Optional(CONF_ARMED_HOME_Color, default='black'):         cv.string,     # Custom color of armed home display ###REMOVE###
    # vol.Optional(CONF_PERIMETER_Color, default='black'):          cv.string,     # Custom color of perimeter display ###REMOVE###

    #---------------------------OPTIONAL MODES---------------------------
    vol.Optional(CONF_LOG):                                        vol.Any(vol.Schema({vol.Optional(CONF_LOG_SIZE): vol.All(vol.Coerce(int), vol.Range(min=-1))}), None), 
    #---------------------------LOG RELATED------------------------------
    
    vol.Optional(CONF_ENABLE_PERIMETER_MODE, default=False):       cv.boolean,    # Enable perimeter mode?
    vol.Optional(CONF_ENABLE_PERSISTENCE, default=False):          cv.boolean,    # Enables persistence for alarm state
    vol.Optional(CONF_CODE_TO_ARM, default=False):                 cv.boolean,    # Require code to arm alarm?

    #---------------------------PANEL RELATED---------------------------
    # vol.Optional(CONF_CLOCK, default=False):                       cv.boolean,    # Display clock on panel ###REMOVE###
    # vol.Optional(CONF_WEATHER, default=False):                     cv.boolean,    # Display weather on panel ###REMOVE###
    # vol.Optional(CONF_ENABLE_SENSORS_PANEL, default=True):         cv.boolean,    # Enable sensor groups panel? ###REMOVE###
    # vol.Optional(CONF_ENABLE_CUSTOM_PANEL, default=False):         cv.boolean,    # Enable custom panel? ###REMOVE###
    # vol.Optional(CONF_ENABLE_CAMERA_PANEL, default=False):         cv.boolean,    # Enable camera panel? ###REMOVE###
    # vol.Optional(CONF_ENABLE_FLOORPLAN_PANEL, default=False):      cv.boolean,    # Enable floorplan panel? ###REMOVE###
    # vol.Optional(CONF_HIDE_PASSCODE, default=True):                cv.boolean,    # Show passcode entry during disarm? ###REMOVE###
    # vol.Optional(CONF_HIDE_SIDEBAR, default=False):                cv.boolean,    # Show all sensors in group? ###REMOVE###
    # vol.Optional(CONF_LANGUAGE, default='english'):                cv.string,     # GUI Language ###REMOVE###
    # vol.Optional(CONF_FLOORPLAN, default='binary_sensor.floorplan'):  cv.entity_id,  # Floorplan binary_sensor ###REMOVE###
    # vol.Optional(CONF_ROUND_BUTTONS, default=False):               cv.boolean,    # GUI Round Buttons ###REMOVE###
    # vol.Optional(CONF_PANEL_TITLE, default='Home Alarm'):          cv.string,     # GUI Panel Title ###REMOVE###
    # vol.Optional(CONF_ENABLE_SERIF_FONT, default=True):            cv.boolean,    # GUI serif font ###REMOVE###

    #--------------------------PASSWORD ATTEMPTS--------------------------
    vol.Optional(CONF_PASSCODE_ATTEMPTS, default=-1):              vol.All(vol.Coerce(int), vol.Range(min=-1)),
    vol.Optional(CONF_PASSCODE_ATTEMPTS_TIMEOUT, default=-1):      vol.All(vol.Coerce(int), vol.Range(min=-1)),

    #---------------------------MQTT RELATED------------------------------
    # vol.Optional(CONF_MQTT):                                       _mqtt_schema(),
    vol.Optional(CONF_MQTT):                                         vol.Any(MQTT_SCHEMA, None), #cv.boolean, # Allows MQTT functionality
    # vol.Optional(CONF_QOS, default=0):                             vol.All(vol.Coerce(int), vol.Range(min=0)), ###REMOVE###
    # vol.Optional(CONF_STATE_TOPIC, default='home/alarm'):          cv.string, ###REMOVE###
    # vol.Optional(CONF_COMMAND_TOPIC, default='home/alarm/set'):    cv.string, ###REMOVE###
    # vol.Optional(CONF_PAYLOAD_ARM_AWAY, default='ARM_AWAY'):       cv.string, ###REMOVE###
    # vol.Optional(CONF_PAYLOAD_ARM_HOME, default='ARM_HOME'):       cv.string, ###REMOVE###
    # vol.Optional(CONF_PAYLOAD_ARM_NIGHT, default='ARM_NIGHT'):     cv.string, ###REMOVE###
    # vol.Optional(CONF_PAYLOAD_DISARM, default='DISARM'):           cv.string, ###REMOVE###
    # vol.Optional(CONF_OVERRIDE_CODE, default=False):               cv.boolean, ###REMOVE###
    # vol.Optional(CONF_PENDING_ON_WARNING, default=False):          cv.boolean, ###REMOVE###



    #---------------------------CAMERA RELATED----------------------------
    # vol.Optional(CONF_CAMERAS):                                    cv.entity_ids, #List of cameras

    #---------------------------YAML RELATED----------------------------
    # vol.Optional(CONF_ADMIN_PASSWORD, default='HG28!!&dn'):        cv.string, #Admin panel password
    vol.Optional(CONF_YAML_ALLOW_EDIT, default=True):              cv.boolean, #Allow alarm.yaml to be edited
    #-----------------------------END------------------------------------
}, _state_validator))

SERVICE_YAML_SAVE  = 'ALARM_YAML_SAVE'

CONF_CONFIGURATION      = 'configuration'
CONF_VALUE              = 'value'

# YAML_SAVE_SERVICE_SCHEMA = vol.Schema({
#     vol.Required(CONF_CONFIGURATION): cv.string,
#     vol.Required(CONF_VALUE):         cv.string,
# })

_LOGGER = logging.getLogger(__name__)



@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):

    #Setup MQTT if enabled
    mqtt = None
    if (CONF_MQTT in config):
        import homeassistant.components.mqtt as mqtt
    alarm = BWAlarm(hass, config, mqtt)
    hass.bus.async_listen(EVENT_STATE_CHANGED, alarm.state_change_listener)
    hass.bus.async_listen(EVENT_TIME_CHANGED, alarm.time_change_listener)
    hass.bus.async_listen(EVENT_TIME_CHANGED, alarm.passcode_timeout_listener)
    async_add_devices([alarm])

    @callback
    def alarm_yaml_save(service):
        alarm.settings_save(service.data.get(CONF_CONFIGURATION), service.data.get(CONF_VALUE))
     
    hass.services.async_register(DOMAIN, SERVICE_YAML_SAVE, alarm_yaml_save)
  
class BWAlarm(alarm.AlarmControlPanel):

    def __init__(self, hass, config, mqtt):
        #------------------------------Initalize the alarm system----------------------------------
        self._config                 = config
        self._mqtt                   = mqtt
        self._hass                   = hass

        self.init_variables()

        self._updateUI = False

        #---------------------------------------SENSORS--------------------------------------------


        #------------------------------------OPTIONAL MODES---------------------------------------
        # self._code_to_arm            = config[CONF_CODE_TO_ARM]
        # self._enable_log             = config[CONF_LOG]
        
        # self._enable_persistence     = config[CONF_ENABLE_PERSISTENCE]



    #     #-------------------------------------MQTT--------------------------------------------------
    #     self._mqtt                   = config[CONF_MQTT]
    #     # self._qos                    = config[CONF_QOS]
    #     # self._state_topic            = config[CONF_STATE_TOPIC]
    #     # self._command_topic          = config[CONF_COMMAND_TOPIC]
    #     # self._payload_disarm         = config[CONF_PAYLOAD_DISARM]
    #     # self._payload_arm_home       = config[CONF_PAYLOAD_ARM_HOME]
    #     # self._payload_arm_away       = config[CONF_PAYLOAD_ARM_AWAY]
    #     # self._payload_arm_night      = config[CONF_PAYLOAD_ARM_NIGHT]
    #     # self._override_code          = config[CONF_OVERRIDE_CODE]
    #     # self._pending_on_warning     = config[CONF_PENDING_ON_WARNING]
    #         vol.Optional(CONF_STATE_TOPIC, default='home/alarm'):          cv.string,
    # vol.Optional(CONF_COMMAND_TOPIC, default='home/alarm/set'):    cv.string,
    # vol.Optional(CONF_PAYLOAD_ARM_AWAY, default='ARM_AWAY'):       cv.string,
    # vol.Optional(CONF_PAYLOAD_ARM_HOME, default='ARM_HOME'):       cv.string,
    # vol.Optional(CONF_PAYLOAD_ARM_NIGHT, default='ARM_NIGHT'):     cv.string,
    # vol.Optional(CONF_PAYLOAD_DISARM, default='DISARM'):           cv.string,
    # vol.Optional(CONF_OVERRIDE_CODE, default=False):               cv.boolean,
    # vol.Optional(CONF_PENDING_ON_WARNING, default=False):          cv.boolean,







    def init_variables(self):
        #-------------------------------------STATE SPECIFIC--------------------------------------------------
        # self._trigger_time_by_state = {state: self._config[state][CONF_TRIGGER_TIME] for state in SUPPORTED_PENDING_STATES}
        # self._pending_time_by_state = {state: self._config[state][CONF_PENDING_TIME] for state in SUPPORTED_PENDING_STATES}
        # self._warning_time_by_state = {state: self._config[state][CONF_WARNING_TIME] for state in SUPPORTED_PENDING_STATES}

        self._supported_statuses_on  = self._config.get(CONF_CUSTOM_SUPPORTED_STATUSES_ON,  []) + SUPPORTED_STATUSES_ON
        self._supported_statuses_off = self._config.get(CONF_CUSTOM_SUPPORTED_STATUSES_OFF, []) + SUPPORTED_STATUSES_OFF

        self._state                  = STATE_ALARM_DISARMED
        self._returnto               = STATE_ALARM_DISARMED
        self._armstate               = STATE_ALARM_DISARMED

        self._allsensors             = []
        self._states                 = {}
        for state in self._config.get(CONF_STATES, {}):
            self._states[state]      = self._config[CONF_STATES][state]
            self._allsensors = set(self._states[state]['immediate']) | set(self._states[state]['delayed']) | set(self._states[state]['override'])

        #-------------------------------------SENSORS--------------------------------------------------
        # self._immediate_by_state     = {state: self._config[state].get(CONF_IMMEDIATE, []) for state in SUPPORTED_PENDING_STATES}
        # self._delayed_by_state       = {state: self._config[state].get(CONF_DELAYED,   []) for state in SUPPORTED_PENDING_STATES}
        # self._override_by_state      = {state: self._config[state].get(CONF_OVERRIDE,  []) for state in SUPPORTED_PENDING_STATES}
        self.immediate               = None
        self.delayed                 = None
        self.override                = None
        self._opensensors            = None

        # for state in SUPPORTED_PENDING_STATES:
        #     for value in self._immediate_by_state[state]:
        #         if value not in self._allsensors:
        #             self._allsensors.append(value)
        #     for value in self._delayed_by_state[state]:
        #         if value not in self._allsensors:
        #             self._allsensors.append(value)
        #     for value in self._override_by_state[state]:
        #         if value not in self._allsensors:
        #             self._allsensors.append(value)

        #------------------------------------CORE ALARM RELATED------------------------------------- 
        self._enable_perimeter_mode  = self._config[CONF_ENABLE_PERIMETER_MODE]
        self._panic_mode             = 'deactivated'
        self._lasttrigger            = ""
        self._timeoutat              = None
        self._passcode_timeoutat     = None

        #------------------------------------PASSCODE RELATED------------------------------------- 
        self._code                   = self._config.get(CONF_CODE, None)
        self._users                  = self._config.get(CONF_USERS, [])
        self._panic_code             = self._config.get(CONF_PANIC_CODE, None)
        self._panel_locked           = False
        self._passcodeAttemptNo      = 0
        self._passcode_attempt_allowed = self._config[CONF_PASSCODE_ATTEMPTS]
        self._passcode_attempt_timeout = self._config[CONF_PASSCODE_ATTEMPTS_TIMEOUT]

        #------------------------------------PANEL RELATED-------------------------------------
        self.changedbyuser           = None

        #-------------------------------------MQTT--------------------------------------------------
        # IF MQTT Enabled define its configuration
        if (CONF_MQTT in self._config):    
            # If MQTT enabled but is empty then set default values
            if (self._config[CONF_MQTT] == None): self._config[CONF_MQTT] = {}

            self._qos                   = self._config[CONF_MQTT].get(CONF_QOS, 0)
            self._state_topic           = self._config[CONF_MQTT].get(CONF_STATE_TOPIC, 'home/alarm')
            self._command_topic         = self._config[CONF_MQTT].get(CONF_COMMAND_TOPIC, 'home/alarm/set')
            self._payload_disarm        = self._config[CONF_MQTT].get(CONF_PAYLOAD_DISARM, 'DISARM')
            self._payload_arm_home      = self._config[CONF_MQTT].get(CONF_PAYLOAD_ARM_HOME, 'ARM_HOME')
            self._payload_arm_away      = self._config[CONF_MQTT].get(CONF_PAYLOAD_ARM_AWAY, 'ARM_HOME')
            self._payload_arm_night     = self._config[CONF_MQTT].get(CONF_PAYLOAD_ARM_NIGHT, 'ARM_NIGHT')
            self._override_code         = self._config[CONF_MQTT].get(CONF_OVERRIDE_CODE, False)
            self._pending_on_warning    = self._config[CONF_MQTT].get(CONF_PENDING_ON_WARNING, False)

        #------------------------------------LOGGING--------------------------------------------------------
        # IF logging Enabled define its configuration
        if (CONF_LOG in self._config):
            self._config[CONF_LOG]['logs']  = []
            self._log_size = self._config[CONF_LOG].get(CONF_LOG_SIZE, 10) 

            # Get the log file or create one if it doesnt exist
            log_path       = self._hass.config.path()
            if not os.path.isdir(log_path):
               _LOGGER.error("[ALARM] Activity Log path %s does not exist.", log_path)
            else:
               self._log_final_path = os.path.join(log_path, "alarm_log.json")
               self.log_load()

        #------------------------------------PERSISTENCE----------------------------------------------------
        self._persistence_list  = []
        if (self._config[CONF_ENABLE_PERSISTENCE]):
           persistence_path     = self._hass.config.path()

           if not os.path.isdir(persistence_path):
              _LOGGER.error("[ALARM] Persistence path %s does not exist.", persistence_path)
           else:
              self._persistence_final_path = os.path.join(persistence_path, "alarm.json")
              self.persistence_load()

              self._state     = self._persistence_list["state"]
              self._timeoutat = pytz.UTC.localize(datetime.datetime.strptime(self._persistence_list["timeoutat"].split(".")[0].replace("T"," "), '%Y-%m-%d %H:%M:%S')) if self._persistence_list["timeoutat"] != None else None
              self._returnto  = self._persistence_list["returnto"]

              self.save_alarm_state()

        #------------------------------------YAML--------------------------------------------------------
        # self._yaml_allow_edit                = self._config[CONF_YAML_ALLOW_EDIT]         
        # if (self._yaml_allow_edit):
        self._yaml_content = self.yaml_load()  

        # Reset Alarm
        self.clearsignals()

    # Alarm properties
    @property
    def should_poll(self) -> bool: return False
    @property
    def name(self) -> str:         return self._config[CONF_NAME]
    @property
    def changed_by(self) -> str:   return self._lasttrigger
    @property
    def state(self) -> str:        return self._state
    @property
    def device_state_attributes(self):

        results = {

            'immediate':                self.immediate,
            'delayed':                  self.delayed,
            'ignored':                  self.ignored,
            'allsensors':               self._allsensors,

            'code_to_arm':              self._config[CONF_CODE_TO_ARM],

            'panel_locked':             self._panel_locked,
            'passcode_attempts':        self._passcode_attempt_allowed,
            'passcode_attempt_timeout': self._passcode_attempt_timeout,

            'changedbyuser':            self.changedbyuser,
            'panic_mode':               self._panic_mode,

            'arm_state':                self._armstate,

            'enable_perimeter_mode':    self._config[CONF_ENABLE_PERIMETER_MODE],
            'enable_persistence':       self._config[CONF_ENABLE_PERSISTENCE],

            'supported_statuses_on':    self._supported_statuses_on,
            'supported_statuses_off':   self._supported_statuses_off,

            'updateUI':					self._updateUI,

            'bwalarm_version':          VERSION,
            'py_version':               sys.version_info,
        }

        users = []

        for entity in self._users:
            users.append('{"name":"' + entity['name'] + '","enabled":"' + str(entity['enabled']) + '", "picture":"' + entity['picture'] + '"}')
        results['users'] = users

        if (CONF_PANEL in self._config):

            panel = copy.deepcopy(self._config[CONF_PANEL])

            if (CONF_ADMIN_PASSWORD not in panel):
                panel[CONF_ADMIN_PASSWORD] = 'HG28!!&dn'
            panel[CONF_ADMIN_PASSWORD] = hashlib.sha256(str.encode(panel[CONF_ADMIN_PASSWORD])).hexdigest()

            results[CONF_PANEL] = panel

        if (CONF_THEMES in self._config):

            results[CONF_THEMES] = self._config[CONF_THEMES]

        if (CONF_LOG in self._config):
            results[CONF_LOG] = self._config[CONF_LOG]

        if (CONF_MQTT in self._config):
            results[CONF_MQTT] = self._config[CONF_MQTT]

        if ('states' in self._config):
            results['states'] = self._config['states']

        return results;

    def yaml_load(self):
        from ruamel.yaml                   import YAML
        self.yaml = YAML()
        with open(self._hass.config.path() + "/alarm.yaml") as stream:
            try:
                return self.yaml.load(stream)
            except self.yaml.YAMLError as exc:
                print(exc)
        return None

    def settings_save(self, configuration=None, value=None):
        """Push the alarm state to the given value."""

        configuration = configuration.lower();
        configDict = configuration.split('-')

        # TODO REWORK THIS AS ITS SLOPPY
        if ( len(configDict) == 1 ):
            if (configuration == 'log' or configuration == 'mqtt'):
                if (value): 
                    self._config[configuration] = dict()
                    self._yaml_content[configuration] = dict()
                else: 
                    self._config.pop(configuration, None)
                    self._yaml_content.pop(configuration, None)
            else:
                self._config[configuration] = value
                self._yaml_content[configuration] = value
        if ( len(configDict) == 2 ):
            self._config[ configDict[0] ][ configDict[1] ] = value
            self._yaml_content[ configDict[0] ][ configDict[1] ] = value
        if ( len(configDict) == 3 ):
            self._config[ configDict[0] ][ configDict[1] ][ configDict[2] ] = value
            self._yaml_content[ configDict[0] ][ configDict[1] ][ configDict[2] ] = value
        if ( len(configDict) == 4 ):
            self._config[ configDict[0] ][ configDict[1] ][ configDict[2] ][ configDict[3] ] = value
            self._yaml_content[ configDict[0] ][ configDict[1] ][ configDict[2] ][ configDict[3] ] = value
        if ( len(configDict) == 5 ):
            self._config[ configDict[0] ][ configDict[1] ][ configDict[2] ][ configDict[3] ][ configDict[4] ]  = value
            self._yaml_content[ configDict[0] ][ configDict[1] ][ configDict[2] ][ configDict[3] ][ configDict[4] ]  = value



        #Trigger a GUI update
        self._updateUI = not self._updateUI

        # yaml = YAML()

        with open(self._hass.config.path() + "/alarm.yaml", 'w') as fil:
            self.yaml.dump(self._yaml_content, fil)

        _LOGGER.debug("Set the yaml entry %s to %s", configuration, value)

        self.init_variables()

        self.schedule_update_ha_state()

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

    ### LOAD activity log previously saved
    def log_load(self):
        try:
           if os.path.isfile(self._log_final_path):  #Find the persistence JSON file and load. Once found update the alarm_control_panel object
              self._config[CONF_LOG]['logs'] = json.load(open(self._log_final_path, 'r'))
           else: #No persistence file found
              _LOGGER.warning("[ALARM] Activity log file doesnt exist")
              self._config[CONF_LOG]['logs'] = []
              self.log_save()
        except Exception as e:
           _LOGGER.error("[ALARM] Error occured loading: %s", str(e))

    ### UPDATE activity log
    def log_save(self): 
        try:
           if self._config[CONF_LOG]['logs'] is not []: #Check we have genuine log to save if so dump to file
              with open(self._log_final_path, 'w') as fil:
                 fil.write(json.dumps(self._config[CONF_LOG]['logs'], ensure_ascii=False))
           else:
              _LOGGER.error("[ALARM] No log to save!")
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

    # def check_open_sensors(self):
    #     for sensor in self._allsensors:    
    #         if self._hass.states.get(sensor).state != None:
    #             if self._hass.states.get(sensor).state in self._supported_statuses_on:
    #                 _LOGGER.error(self._hass.states.get(sensor)) # do summit

    @property
    def code_format(self):
        """One or more characters."""
        return None if self._code is None else '.+'

    def alarm_disarm(self, code=None):     
        #If the provided code matches the panic alarm then deactivate the alarm but set the state of the panic mode to active.
        if self._validate_panic_code(code):
            self.process_event(Events.Disarm)
            self._panic_mode = "ACTIVE"
            self._update_log('HA', 'Alarm disarmed') #Show a default disarm message incase this is displayed on the interface
            # Let HA know that something changed
            self.schedule_update_ha_state()
            return

        if not self._validate_code(code):
            return
        self.process_event(Events.Disarm)

    def alarm_arm_home(self, code=None):
        if code == "override": #ARM THE ALARM IMMEDIATELY
            self.process_event(Events.ArmHome, True)
            self._update_log('HA', 'Alarm set in Home mode')
            return

        for entity in self._users:
            if entity['code'] == code:
                self._update_log(entity['name'], 'alarm set in Home mode')
                self.process_event(Events.ArmHome)
                return

        if self._config[CONF_CODE_TO_ARM]:
            if code == self._code:
                self._update_log('HA', 'Alarm set in Home mode')
                self.process_event(Events.ArmHome)
        else:
            self._update_log('HA', 'Alarm set in Home mode')
            self.process_event(Events.ArmHome)


    def alarm_arm_away(self, code=None):
        if code == "override": #ARM THE ALARM IMMEDIATELY
            self.process_event(Events.ArmAwat, True)
            self._update_log('HA', 'Alarm set in Away mode')
            return

        for entity in self._users:
            if entity['code'] == code:
                self._update_log(entity['name'], 'alarm set in Away mode')
                self.process_event(Events.ArmAway)
                return

        if self._config[CONF_CODE_TO_ARM]:
            if code == self._code:
                self._update_log('HA', 'Alarm set in Away mode')
                self.process_event(Events.ArmAway)
        else:
            self._update_log('HA', 'Alarm set in Away mode')
            self.process_event(Events.ArmAway)

    def alarm_arm_night(self, code=None):
        if code == "override": #ARM THE ALARM IMMEDIATELY
            self.process_event(Events.ArmPerimeter, True)
            self._update_log('HA', 'Alarm set in Perimeter mode')
            return

        for entity in self._users:
            if entity['code'] == code:
                self._update_log(entity['name'], 'alarm set in Perimeter mode')
                self.process_event(Events.ArmPerimeter)
                return

        if self._config[CONF_CODE_TO_ARM]:
            if code == self._code:
                self._update_log('HA', 'Alarm set in Perimeter mode')
                self.process_event(Events.ArmPerimeter)
        else:
            self._update_log('HA', 'Alarm set in Perimeter mode')
            self.process_event(Events.ArmPerimeter)

    def alarm_trigger(self, code=None):
        self.process_event(Events.Trigger)
        self._update_log('HA', 'Alarm has been triggered')

    ### Internal processing
    def setsignals(self, alarmMode):
        """ Figure out what to sense and how """
        self.immediate = self._states[alarmMode]['immediate'].copy()
        self.delayed   = self._states[alarmMode]['delayed'].copy()
        self.override  = self._states[alarmMode]['override'].copy()
        self.ignored   = set(self._allsensors) - (set(self.immediate) | set(self.delayed))

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
                if (datetime.timedelta(seconds=int(self._states[STATE_ALARM_ARMED_HOME][CONF_PENDING_TIME])) and override_pending_time == False):
                    self._state = STATE_ALARM_PENDING
                else:
                    self._state = STATE_ALARM_ARMED_HOME
                self._armstate = STATE_ALARM_ARMED_HOME
            
            elif event == Events.ArmAway:       
                if (datetime.timedelta(seconds=int(self._states[STATE_ALARM_ARMED_AWAY][CONF_PENDING_TIME])) and override_pending_time == False):
                    self._armstate = STATE_ALARM_ARMED_AWAY
                    self._state = STATE_ALARM_PENDING
                else:
                    self._state = STATE_ALARM_ARMED_AWAY
                self._armstate = STATE_ALARM_ARMED_AWAY

            elif event == Events.ArmPerimeter:  
                if (datetime.timedelta(seconds=int(self._states[STATE_ALARM_ARMED_PERIMETER][CONF_PENDING_TIME])) and override_pending_time == False):
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
                if self._config.get(CONF_WARNING):
                    switch.turn_on(self._hass, self._config.get(CONF_WARNING))
                self._timeoutat = now() +  datetime.timedelta(seconds=int(self._states[self._armstate][CONF_WARNING_TIME]))
                self._update_log('HA', 'Alarm has been tripped by: ' + self._lasttrigger)
            elif new_state == STATE_ALARM_TRIGGERED:
                _LOGGER.debug("[ALARM] Turning on alarm")
                if self._config.get(CONF_ALARM):
                    switch.turn_on(self._hass, self._config.get(CONF_ALARM))
                if (self._states[self._armstate][CONF_TRIGGER_TIME] == -1):
                    self._timeoutat = now() + datetime.timedelta(hours=int(24))
                else:
                    self._timeoutat = now() + datetime.timedelta(seconds=int(self._states[self._armstate][CONF_TRIGGER_TIME]))
                self._update_log('HA', 'Alarm has been triggered by: ' + self._lasttrigger)
            elif new_state == STATE_ALARM_PENDING:
                _LOGGER.debug("[ALARM] Pending user leaving house")
                if self._config.get(CONF_WARNING):
                    switch.turn_on(self._hass, self._config.get(CONF_WARNING))
                self._timeoutat = now() + datetime.timedelta(seconds=int(self._states[self._armstate][CONF_PENDING_TIME]))
                #self._returnto = STATE_ALARM_ARMED_AWAY
                self.setsignals(self._armstate)
            elif new_state == STATE_ALARM_ARMED_HOME:
                self._returnto = new_state
                self.setsignals(STATE_ALARM_ARMED_HOME)
            elif new_state == STATE_ALARM_ARMED_AWAY:
                self._returnto = new_state
                self.setsignals(STATE_ALARM_ARMED_AWAY)
            elif new_state == STATE_ALARM_ARMED_PERIMETER:
                self._returnto = new_state
                self.setsignals(STATE_ALARM_ARMED_PERIMETER)
            elif new_state == STATE_ALARM_DISARMED:
                self._returnto = new_state
                self.clearsignals()
  
            # Things to do on leaving state
            if old_state == STATE_ALARM_WARNING or old_state == STATE_ALARM_PENDING:
                _LOGGER.debug("[ALARM] Turning off warning")
                if self._config.get(CONF_WARNING):
                    switch.turn_off(self._hass, self._config.get(CONF_WARNING))
                
            elif old_state == STATE_ALARM_TRIGGERED:
                _LOGGER.debug("[ALARM] Turning off alarm")
                if self._config.get(CONF_ALARM):
                    switch.turn_off(self._hass, self._config.get(CONF_ALARM))

            # Let HA know that something changed
            if self._config[CONF_ENABLE_PERSISTENCE]:
                self.save_alarm_state()
            self.schedule_update_ha_state()

    def _validate_code(self, code):
        """Validate given code."""
        if ((self._passcode_attempt_allowed == -1) or (self._passcodeAttemptNo <= self._passcode_attempt_allowed)):
            check = self._code is None or code == self._code or self._validate_user_codes(code)
            if code == self._code: 
                self._update_log('HA', "Disarmed the alarm")
            return self._validate_code_attempts(check)
        else:
            _LOGGER.warning("[ALARM] Too many passcode attempts, try again later")
            return False

    def _validate_user_codes(self, code):
        for entity in self._users:
            if entity['code'] == code:
                self._update_log(entity['name'], "disarmed the alarm")
                return True
        return False

    def _validate_code_attempts(self, check):
        if check:
            self._passcodeAttemptNo = 0
        else:
            _LOGGER.debug("[ALARM] Invalid code given")
            self._passcodeAttemptNo += 1   
            if (self._passcode_attempt_allowed != -1 and self._passcodeAttemptNo > self._passcode_attempt_allowed):
                self._panel_locked = True
                self._passcode_timeoutat = now() + datetime.timedelta(seconds=int(self._passcode_attempt_timeout))
                _LOGGER.warning("[ALARM] Panel locked, too many passcode attempts!")
                self._update_log('HA', 'Panel locked')
        self.schedule_update_ha_state()
        return check

    def _validate_panic_code(self, code):
        """Validate given code."""
        check = code == self._panic_code
        if check:
            _LOGGER.warning("[ALARM] PANIC MODE ACTIVATED!!!")
            self._passcodeAttemptNo = 0
        return check

    def _update_log(self, name, message):
        self.changedbyuser = name
        if (CONF_LOG in self._config):
            self._log_size = self._config[CONF_LOG][CONF_LOG_SIZE] if CONF_LOG_SIZE in self._config[CONF_LOG] else 10
            if self._log_size != -1 and len(self._config[CONF_LOG]["logs"]) >= self._log_size:
                self._config[CONF_LOG]["logs"].remove(self._config[CONF_LOG]["logs"][0])
            self._config[CONF_LOG]["logs"].append({"name": name, "message": message, "dayTime": datetime.datetime.strftime(now(), "%H:%M %A")})
            self.log_save()

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
        if (CONF_MQTT in self._config):
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
        if (CONF_MQTT in self._config): 
            return self._mqtt.async_subscribe(
                self.hass, self._command_topic, message_received, self._qos)
        
    @asyncio.coroutine
    def _async_state_changed_listener(self, entity_id, old_state, new_state):
        """Publish state change to MQTT."""
        if (CONF_MQTT in self._config): 
            state = new_state.state
            if (self._pending_on_warning == True and state == STATE_ALARM_WARNING):
                state = STATE_ALARM_PENDING

            self._mqtt.async_publish(self.hass, self._state_topic, state, self._qos, True)
            _LOGGER.debug("[ALARM/MQTT] State changed")