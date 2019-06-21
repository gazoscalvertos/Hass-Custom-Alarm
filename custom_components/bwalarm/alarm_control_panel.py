"""
  CHANGE LOG:
1.1.7_ak74
  - Arm/Disarm with MQTT commands, including codes, code_to_arm and override
  - alarm_arm/alarm_disarm revision
  - debug/info/warning logging added/changed
  - fixed duplicate reaction to state change
  - fixed bug #3 (https://github.com/akasma74/Hass-Custom-Alarm/issues/3)
  - Perimeter -> Night migration
  - change DOMAIN from alarm_control_panel to bwalarm (affects service calls from HA automations)
  - changed_by() returns the original trigger and resets upon DISARM/coming back to ARM_XXX state (after trigger time)
  - persistence file now exists in all but DISARMED states

1.1.6_ak74
  - Alarm is going back to Triggered state if the sensor that caused the alarm is still active
"""

# For legacy installations, this is not used in HA > 0.93
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
import hashlib
import time
import uuid

from collections import OrderedDict

from homeassistant.const         import (
    # SERVICES
    SERVICE_ALARM_ARM_NIGHT, SERVICE_ALARM_ARM_HOME, SERVICE_ALARM_ARM_AWAY, SERVICE_ALARM_DISARM,
    # STATES
    STATE_ALARM_DISARMED, STATE_ALARM_PENDING,
    STATE_ALARM_ARMED_NIGHT, STATE_ALARM_ARMED_HOME, STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_TRIGGERED,
    # CONFIG PARAMETERS
    CONF_PLATFORM, CONF_NAME, CONF_CODE,
    CONF_PENDING_TIME, CONF_DELAY_TIME, CONF_TRIGGER_TIME,
    CONF_DISARM_AFTER_TRIGGER,
    STATE_ON, STATE_OFF,
    ATTR_ENTITY_ID, ATTR_CODE,
    EVENT_STATE_CHANGED, EVENT_TIME_CHANGED
    )

from homeassistant.components.alarm_control_panel         import (
    ALARM_SERVICE_SCHEMA
    )

from operator                    import attrgetter
from homeassistant.core          import callback
#from homeassistant.components    import websocket_api
from homeassistant.util.dt       import utcnow                       as now
from homeassistant.loader        import bind_hass
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.helpers.event import async_track_state_change
from homeassistant.util          import sanitize_filename

import voluptuous                                                    as vol
import homeassistant.components.alarm_control_panel                  as alarm
import homeassistant.components.switch                               as switch
import homeassistant.helpers.config_validation                       as cv

_LOGGER = logging.getLogger(__name__)

VERSION                            = '1.1.7_ak74'
DOMAIN                             = 'bwalarm'

# The type of the message
#WS_STATE_BWALARM_OPENSENSORS = DOMAIN + '/opensensors'
# The schema for the message
#SCHEMA_WEBSOCKET_GET_OPENSENSORS = \
#    websocket_api.BASE_COMMAND_MESSAGE_SCHEMA.extend({
#        'type': WS_STATE_BWALARM_OPENSENSORS,
        # The entity that we want to retrieve the thumbnail for.
#        'state': cv.string
#    })

#//------------ INTERNAL ATTRIBUTES ------------
INT_ATTR_STATE_CHECK_BEFORE_ARM = '_check_before_arm'

#//--------------------SUPPORTED STATES----------------------------
OBSOLETE_STATE_ALARM_ARMED_PERIMETER    = 'armed_perimeter'
STATE_ALARM_WARNING                 = 'warning'
#STATE_ALARM_ARMED_NIGHT             = 'armed_night'

SUPPORTED_PENDING_STATES            = [STATE_ALARM_ARMED_NIGHT, STATE_ALARM_ARMED_HOME, STATE_ALARM_ARMED_AWAY]

SUPPORTED_STATES                    = [STATE_ALARM_DISARMED, STATE_ALARM_PENDING,
                                        STATE_ALARM_WARNING, STATE_ALARM_TRIGGERED] + SUPPORTED_PENDING_STATES


# example from https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/components/manual/alarm_control_panel.py
# SUPPORTED_PRETRIGGER_STATES = [state for state in SUPPORTED_STATES
#                               if state != STATE_ALARM_TRIGGERED]

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
CONF_ID                            = 'id'
CONF_PICTURE                       = 'picture'
CONF_HOME_PERM                     = 'home_permision'
CONF_AWAY_PERM                     = 'away_permission'
CONF_PERI_PERM                     = 'perimiter_permission'
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
OBSOLETE_CONF_ENABLE_PERIMETER_MODE         = 'enable_perimeter_mode'    # OBSOLETE, DELETE
CONF_ENABLE_NIGHT_MODE             = 'enable_night_mode'
CONF_ENABLE_PERSISTENCE            = 'enable_persistence'

#//----------------------PANEL RELATED------------------------------
CONF_GUI                           = 'gui'
CONF_PANEL                         = 'panel'
CONF_ColorS                        = 'colors'
CONF_THEMES                        = 'themes'
CONF_ADMIN_PASSWORD                = 'admin_password'
CONF_DISABLE_ANIMATIONS            = 'disable_animations'

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
CONF_ENABLE_MQTT                   = 'enable_mqtt'
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
CONF_ENABLE_LOG                    = 'enable_log'
CONF_LOG_SIZE                      = 'log_size'
CONF_LOGS                          = 'logs'

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
    ArmNight                 = 8

EATTR_SERVICE   = 'service'
EATTR_STATE     = 'state'

event2name = {
    Events.ArmNight: {
        EATTR_SERVICE   :   SERVICE_ALARM_ARM_NIGHT,
        EATTR_STATE     :   STATE_ALARM_ARMED_NIGHT
        },
    Events.ArmHome: {
        EATTR_SERVICE   :   SERVICE_ALARM_ARM_HOME,
        EATTR_STATE     :   STATE_ALARM_ARMED_HOME
        },
    Events.ArmAway: {
        EATTR_SERVICE   :   SERVICE_ALARM_ARM_AWAY,
        EATTR_STATE     :   STATE_ALARM_ARMED_AWAY
        }
    }
#event2name = {Events.ArmHome: 'armed_home', Events.ArmAway: 'armed_away', Events.ArmNight: 'armed_night'}

class LOG(enum.Enum):
    DISARMED = 0 #'disarmed the alarm'
    DISARM_FAIL = 1 #'Failed to disarm alarm'
    TRIGGERED = 2 #'alarm has been triggered!'
    HOME = 3 #'set the alarm in Home mode'
    AWAY = 4 #'set the alarm in Away mode'
    TRIPPED = 5 #'Alarm has been tripped by: '
    LOCKED = 6 #'Panel Locked
    PERIMETER = 8 #'set the alarm in Perimeter mode'

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

PANEL_SCHEMA = vol.Schema({
	vol.Optional(CONF_CAMERAS):                                   cv.entity_ids,
    vol.Optional(cv.slug):                                        cv.string,
})

USER_SCHEMA = vol.Schema([{
            vol.Required(CONF_ID, default=uuid.uuid4().hex):             cv.string,
            vol.Required(CONF_NAME):                                     cv.string,
            vol.Optional(CONF_PICTURE, default='/local/images/ha.png'):  cv.string,
            vol.Required(CONF_CODE):                                     cv.string,
            vol.Optional(CONF_ENABLED, default=True):                    cv.boolean,
            vol.Optional(CONF_DISABLE_ANIMATIONS, default=False):        cv.boolean
            # vol.Optional(CONF_HOME_PERM, default=True):                  cv.boolean,
            # vol.Optional(CONF_AWAY_PERM, default=True):                  cv.boolean,
            # vol.Optional(CONF_PERI_PERM, default=True):                  cv.boolean
            ##ADD TIME BASED SETTINGS
}])

THEMES_SCHEMA = vol.Schema([{
    vol.Optional(cv.slug):                                        cv.string,
}])

MQTT_SCHEMA = vol.Schema({
    vol.Required(CONF_ENABLE_MQTT, default=False):                cv.boolean,
    vol.Optional(CONF_QOS, default=0):                            vol.All(vol.Coerce(int), vol.Range(min=0)),
    vol.Optional(CONF_STATE_TOPIC, default='home/alarm'):         cv.string,
    vol.Optional(CONF_COMMAND_TOPIC, default='home/alarm/set'):   cv.string,
    vol.Optional(CONF_PAYLOAD_ARM_AWAY, default='ARM_AWAY'):      cv.string,
    vol.Optional(CONF_PAYLOAD_ARM_HOME, default='ARM_HOME'):      cv.string,
    vol.Optional(CONF_PAYLOAD_ARM_NIGHT, default='ARM_NIGHT'):    cv.string,
    vol.Optional(CONF_PAYLOAD_DISARM, default='DISARM'):          cv.string,
    vol.Optional(CONF_OVERRIDE_CODE, default=False):              cv.boolean,
    vol.Optional(CONF_PENDING_ON_WARNING, default=False):         cv.boolean,
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
    vol.Optional(CONF_USERS):                                      USER_SCHEMA, # Schema to hold the list of names with codes allowed to disarm the alarm
    vol.Optional(CONF_PANIC_CODE):                                 cv.string,

    #------------------------------STATE RELATED-------------------------
    vol.Optional(CONF_STATES):                                     vol.Schema({cv.slug: _state_schema()}),
    vol.Optional(STATE_ALARM_ARMED_AWAY, default={}):              _state_schema(),  #state specific times ###REMOVE###
    vol.Optional(STATE_ALARM_ARMED_HOME, default={}):              _state_schema(),  #state specific times ###REMOVE###
    vol.Optional(STATE_ALARM_ARMED_NIGHT, default={}):         _state_schema(), #state specific times ###REMOVE###
    # vol.Optional(STATE_ALARM_DISARMED, default={}):                _state_schema(STATE_ALARM_DISARMED),    #state specific times ###REMOVE###
    # vol.Optional(STATE_ALARM_TRIGGERED, default={}):               _state_schema(STATE_ALARM_TRIGGERED),   #state specific times ###REMOVE###

    #------------------------------GUI-----------------------------------
    vol.Optional(CONF_PANEL):                                        PANEL_SCHEMA,
    vol.Optional(CONF_THEMES):                                       THEMES_SCHEMA,

    #---------------------------OPTIONAL MODES---------------------------
    vol.Optional(CONF_ENABLE_LOG, default=True):                   cv.boolean,
    vol.Optional(CONF_LOG_SIZE, default=10):                       vol.All(vol.Coerce(int), vol.Range(min=-1)),
    vol.Optional(CONF_LOGS):                                       vol.Schema([cv.string]),
    #---------------------------LOG RELATED------------------------------

    vol.Optional(OBSOLETE_CONF_ENABLE_PERIMETER_MODE, default=False):       cv.boolean,    # Enable perimeter mode?  # OBSOLETE, DELETE!
    vol.Optional(CONF_ENABLE_NIGHT_MODE, default=False):           cv.boolean,    # Enable perimeter mode?
    vol.Optional(CONF_ENABLE_PERSISTENCE, default=False):          cv.boolean,    # Enables persistence for alarm state
    vol.Optional(CONF_CODE_TO_ARM, default=False):                 cv.boolean,    # Require code to arm alarm?

    #---------------------------PANEL RELATED---------------------------
    vol.Optional(CONF_ADMIN_PASSWORD, default='HG28!!&dn'):       cv.string,     # Admin panel password

    #--------------------------PASSWORD ATTEMPTS--------------------------
    vol.Optional(CONF_PASSCODE_ATTEMPTS, default=-1):              vol.All(vol.Coerce(int), vol.Range(min=-1)),
    vol.Optional(CONF_PASSCODE_ATTEMPTS_TIMEOUT, default=900):      vol.All(vol.Coerce(int), vol.Range(min=1)),

    #---------------------------MQTT RELATED------------------------------
    vol.Required(CONF_MQTT, default={CONF_ENABLE_MQTT: False}):                                       MQTT_SCHEMA, #vol.Any(MQTT_SCHEMA, None), #cv.boolean, # Allows MQTT functionality

    #---------------------------YAML RELATED----------------------------
    vol.Optional(CONF_YAML_ALLOW_EDIT, default=True):              cv.boolean, #Allow alarm.yaml to be edited
    #-----------------------------END------------------------------------
}, _state_validator))

ATTR_IGNORE_OPEN_SENSORS        =   'ignore_open_sensors'
CONST_DEF_IGNORE_OPEN_SENSORS   =   False

# TODO: extend it properly using ALARM_SERVICE_SCHEMA
EXTENDED_ALARM_SERVICE_SCHEMA = vol.Schema({
    vol.Optional(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_CODE): cv.string,
    vol.Optional(ATTR_IGNORE_OPEN_SENSORS, default=CONST_DEF_IGNORE_OPEN_SENSORS):          cv.boolean
})


SERVICE_YAML_SAVE  = 'ALARM_YAML_SAVE'
SERVICE_YAML_USER  = 'ALARM_YAML_USER'

CONF_CONFIGURATION      = 'configuration'
CONF_VALUE              = 'value'

CONF_USER               = 'user'
CONF_COMMAND            = 'command'

try:
    from ruamel.yaml                   import YAML
except Exception as e:
    _LOGGER.warning('Import Error: %s. Attempting to download and import', e)

def str2bool(string) -> bool:
    """ Convert True/False string info boolean True/False or returns its input """
    d = {'True': True, 'False': False}
    return d.get(string, string)

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):

    # Set up a static enpoint to serve files
    resources = hass.config.path('custom_components/bwalarm/resources')
    hass.http.register_static_path("/bwalarm", resources)

    # Register the panel
    url = "/api/panel_custom/alarm"
    hass.http.register_static_path(url, "{}/panel.html".format(resources))
    await hass.components.panel_custom.async_register_panel(
        webcomponent_name='alarm',
        frontend_url_path="alarm",
        html_url=url,
        sidebar_title='Alarm',
        sidebar_icon='mdi:shield-home',
        config={"alarmid": "alarm_control_panel.house"},
    )

    #Setup MQTT if enabled
    mqtt = None
    if (config[CONF_MQTT][CONF_ENABLE_MQTT]):
        import homeassistant.components.mqtt as mqtt

    # redefine arm_xxx service calls to accept additional attributes
    @callback
    def async_alarm_arm_home(service):
        alarm.async_alarm_arm_home(service.data.get(ATTR_CODE), service.data.get(ATTR_IGNORE_OPEN_SENSORS))

    @callback
    def async_alarm_arm_away(service):
        # service.endity_id ignored for simplicity, chage?
        alarm.alarm_arm_away(service.data.get(ATTR_CODE), service.data.get(ATTR_IGNORE_OPEN_SENSORS))

    @callback
    def async_alarm_arm_night(service):
        alarm.alarm_arm_night(service.data.get(ATTR_CODE), service.data.get(ATTR_IGNORE_OPEN_SENSORS))

    @callback
    def async_alarm_disarm(service):
        alarm.alarm_disarm(service.data.get(ATTR_CODE))

    @callback
    def alarm_yaml_save(service):
        alarm.settings_save(service.data.get(CONF_CONFIGURATION), service.data.get(CONF_VALUE))

    @callback
    def alarm_yaml_user(service):
        alarm.settings_user(service.data.get(CONF_USER), service.data.get(CONF_COMMAND))

#    @callback
#    def websocket_handle_get_opensensors(hass, connection, msg):
#        async def send_opensensors():
#            _LOGGER.debug("websocket_handle_get_opensensors: msg: {}".format(msg))
#            connection.send_result(
#                msg['id'], msg['state'] + ': 1st floor - safe'
#                )
#        hass.async_add_job(send_opensensors())

    alarm = BWAlarm(hass, config, mqtt)
    hass.bus.async_listen(EVENT_STATE_CHANGED, alarm.state_change_listener)
    hass.bus.async_listen(EVENT_TIME_CHANGED, alarm.time_change_listener)
    hass.bus.async_listen(EVENT_TIME_CHANGED, alarm.passcode_timeout_listener)
    async_add_devices([alarm])

    hass.services.async_register(DOMAIN, SERVICE_ALARM_ARM_HOME, async_alarm_arm_home, EXTENDED_ALARM_SERVICE_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_ALARM_ARM_AWAY, async_alarm_arm_away, EXTENDED_ALARM_SERVICE_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_ALARM_ARM_NIGHT, async_alarm_arm_night, EXTENDED_ALARM_SERVICE_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_ALARM_DISARM, async_alarm_disarm, ALARM_SERVICE_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_YAML_SAVE, alarm_yaml_save)
    hass.services.async_register(DOMAIN, SERVICE_YAML_USER, alarm_yaml_user)

#    hass.components.websocket_api.async_register_command(
#        WS_STATE_BWALARM_OPENSENSORS, websocket_handle_get_opensensors,
#        SCHEMA_WEBSOCKET_GET_OPENSENSORS)

class BWAlarm(alarm.AlarmControlPanel):

    def __init__(self, hass, config, mqtt):
        #------------------------------Initalize the alarm system----------------------------------
        self._config                 = config   # it holds data imported from yaml on startup and is used to return component's attributes in device_state_attributes
        self._mqtt                   = mqtt
        self._hass                   = hass

        self.init_variables()
        self._updateUI = False

    def init_variables(self):
        # basically transfers data from self._config (i.e yaml) and persistence (alarm.json) into internal current settings (self._states etc)
        FNAME = '[INIT_VARIABLES]'

        _LOGGER.debug("{} begin".format(FNAME))
        #-------------------------------------STATE SPECIFIC--------------------------------------------------
        self._supported_statuses_on  = self._config.get(CONF_CUSTOM_SUPPORTED_STATUSES_ON,  []) + SUPPORTED_STATUSES_ON
        self._supported_statuses_off = self._config.get(CONF_CUSTOM_SUPPORTED_STATUSES_OFF, []) + SUPPORTED_STATUSES_OFF

        self._state                  = STATE_ALARM_DISARMED
        self._returnto               = STATE_ALARM_DISARMED
        self._armstate               = STATE_ALARM_DISARMED

        self._allsensors             = set()
        self._states                 = {}

        for state in self._config.get(CONF_STATES, {}):
            _LOGGER.debug("{} {}: init {}".format(FNAME, CONF_STATES, state))
            self._states[state]      = self._config[CONF_STATES][state]
            self._allsensors |= set(self._states[state][CONF_IMMEDIATE]) | set(self._states[state][CONF_DELAYED]) # no need to include override sensors, they're already there

        #-------------------------------------SENSORS--------------------------------------------------
        self.immediate               = None
        self.delayed                 = None
        self.override                = None
        self._opensensors            = None

        #------------------------------------CORE ALARM RELATED-------------------------------------
        # deal with obsolete enable_perimeter_mode attribute
        # assume it's old yaml and first init (as we delete it then)
        if OBSOLETE_CONF_ENABLE_PERIMETER_MODE in self._config.keys():
            # import value only if it's True (False it will be anyway as default)
            if self._config[OBSOLETE_CONF_ENABLE_PERIMETER_MODE]:
                _LOGGER.debug("{} core: attribute {} is obsolete, set {} to {} and delete the former".format(FNAME, OBSOLETE_CONF_ENABLE_PERIMETER_MODE, CONF_ENABLE_NIGHT_MODE, self._config[OBSOLETE_CONF_ENABLE_PERIMETER_MODE]))
                self._config[CONF_ENABLE_NIGHT_MODE] = copy.deepcopy(self._config[OBSOLETE_CONF_ENABLE_PERIMETER_MODE])
            del self._config[OBSOLETE_CONF_ENABLE_PERIMETER_MODE]

        self._enable_night_mode      = self._config[CONF_ENABLE_NIGHT_MODE]
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
        if (self._config[CONF_MQTT][CONF_ENABLE_MQTT]):
            # # If MQTT enabled but is empty then set default values
            # if (self._config[CONF_MQTT] == None): self._config[CONF_MQTT] = {}

            self._qos                   = self._config[CONF_MQTT].get(CONF_QOS)
            self._state_topic           = self._config[CONF_MQTT].get(CONF_STATE_TOPIC)
            self._command_topic         = self._config[CONF_MQTT].get(CONF_COMMAND_TOPIC)
            self._payload_disarm        = self._config[CONF_MQTT].get(CONF_PAYLOAD_DISARM)
            self._payload_arm_home      = self._config[CONF_MQTT].get(CONF_PAYLOAD_ARM_HOME)
            self._payload_arm_away      = self._config[CONF_MQTT].get(CONF_PAYLOAD_ARM_AWAY)
            self._payload_arm_night     = self._config[CONF_MQTT].get(CONF_PAYLOAD_ARM_NIGHT)
            self._override_code         = self._config[CONF_MQTT].get(CONF_OVERRIDE_CODE)
            self._pending_on_warning    = self._config[CONF_MQTT].get(CONF_PENDING_ON_WARNING)

        #------------------------------------LOGGING--------------------------------------------------------
        # IF logging Enabled define its configuration
        if (CONF_ENABLE_LOG in self._config):
            self._config[CONF_LOGS]  = []
            self._log_size = self._config.get(CONF_LOG_SIZE, 10)

            # Get the log file or create one if it does not exist
            log_path       = self._hass.config.path()
            if not os.path.isdir(log_path):
               _LOGGER.error("{} logging: Activity Log path {} does not exist".format(FNAME, log_path))
            else:
               self._log_final_path = os.path.join(log_path, "alarm_log.json")
               self.log_load()


        #------------------------------------YAML--------------------------------------------------------
        # self._yaml_allow_edit                = self._config[CONF_YAML_ALLOW_EDIT]
        # if (self._yaml_allow_edit):
        self._yaml_content = self.yaml_load()

        # Reset Alarm
        self.clearsignals()

        #------------------------------------PERSISTENCE----------------------------------------------------
        self._persistence_list  = json.loads('{}')
        if (self._config[CONF_ENABLE_PERSISTENCE]):
            persistence_path = self._hass.config.path()
            if os.path.isdir(persistence_path):
                self._persistence_final_path = os.path.join(persistence_path, "alarm.json")
                if (self.persistence_load() and (self._persistence_list["state"] != STATE_ALARM_DISARMED) ):
                    self._state     = self._persistence_list["state"]
                    self._timeoutat = pytz.UTC.localize(datetime.datetime.strptime(self._persistence_list["timeoutat"].split(".")[0].replace("T"," "), '%Y-%m-%d %H:%M:%S')) if self._persistence_list["timeoutat"] != None else None
                    self._returnto  = self._persistence_list["returnto"]
                    self._armstate  = self._persistence_list["armstate"]

                    _LOGGER.debug("{} persistence: state:{}, timeoutat: {}, returnto: {}, armstate: {}".format(FNAME, self._state, self._timeoutat, self._returnto, self._armstate))

                    if (self._armstate == STATE_ALARM_WARNING or self._armstate == STATE_ALARM_TRIGGERED or self._armstate == STATE_ALARM_PENDING):
                        _LOGGER.debug("{} persistence: init states, immediate, delayed and override from {} state".format(FNAME, self._returnto))
                        self._states    = self._persistence_list[CONF_STATES]
                        self.immediate  = self._states[self._returnto][CONF_IMMEDIATE]
                        self.delayed    = self._states[self._returnto][CONF_DELAYED]
                        self.override   = self._states[self._returnto][CONF_OVERRIDE]
                    elif self._armstate in SUPPORTED_PENDING_STATES:
                        self._states    = self._persistence_list[CONF_STATES]
                        self.immediate  = self._states[self._armstate][CONF_IMMEDIATE]
                        self.delayed    = self._states[self._armstate][CONF_DELAYED]
                        self.override   = self._states[self._armstate][CONF_OVERRIDE]
                    else:
                        ## raise exception?
                        _LOGGER.error("{} persistence: Invalid armstate: {}".format(FNAME, self._armstate))
            else:
                _LOGGER.error("{} persistence: path \"{}\" does not exist".format(FNAME, persistence_path))

        # to migrate settings from obsolete armed_perimeter state to armed_night
        if OBSOLETE_STATE_ALARM_ARMED_PERIMETER in self._states.keys():
            _LOGGER.debug("{} init state {} with infomation from obsolete state {} and update appropriate config".format(FNAME, STATE_ALARM_ARMED_NIGHT, OBSOLETE_STATE_ALARM_ARMED_PERIMETER))
            self._states[STATE_ALARM_ARMED_NIGHT] = copy.deepcopy(self._states[OBSOLETE_STATE_ALARM_ARMED_PERIMETER])
            self._config[CONF_STATES][STATE_ALARM_ARMED_NIGHT] = copy.deepcopy(self._config[CONF_STATES][OBSOLETE_STATE_ALARM_ARMED_PERIMETER])

            _LOGGER.debug("{} delete obsolete state {} from imported config and states".format(FNAME, OBSOLETE_STATE_ALARM_ARMED_PERIMETER))
            del self._config[CONF_STATES][OBSOLETE_STATE_ALARM_ARMED_PERIMETER]
            del self._states[OBSOLETE_STATE_ALARM_ARMED_PERIMETER]

        # create lists of sensors to check for every state
        arm_states_dict = self._config[CONF_STATES]
        for state in arm_states_dict.keys():
            state_config = arm_states_dict[state]
            # convert to sets first as it's easier to merge (|) and remove (-)
            state_config[INT_ATTR_STATE_CHECK_BEFORE_ARM] = list( (set(state_config[CONF_IMMEDIATE]) | set(state_config[CONF_DELAYED])) - set(state_config[CONF_OVERRIDE]) )

        _LOGGER.debug("{} end".format(FNAME))


    # Alarm properties
    @property
    def should_poll(self) -> bool: return False

    @property
    def name(self) -> str:         return self._config[CONF_NAME]

    #"""Last change triggered by."""
    @property
    def changed_by(self) -> str:   return self._lasttrigger

    @property
    def state(self) -> str:        return self._state

    @property
    def code_format(self):
        """Regex for code format or None if no code is required."""
        # affects Lovelace keypad presence (None means no keypad)
    #        return None if self._code is None else '.+'
        return None if ((self._code is None) or (self._state == STATE_ALARM_DISARMED)) else alarm.FORMAT_NUMBER

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
            'passcode_attempts_timeout': self._passcode_attempt_timeout,

            'changedbyuser':            self.changedbyuser,
            'panic_mode':               self._panic_mode,

            'arm_state':                self._armstate,

#            'enable_perimeter_mode':    self._config[CONF_ENABLE_NIGHT_MODE],   # OBSOLETE, CAN WE REMOVE IT?
            'enable_night_mode':        self._config[CONF_ENABLE_NIGHT_MODE],
            'enable_persistence':       self._config[CONF_ENABLE_PERSISTENCE],

            'enable_log':               self._config[CONF_ENABLE_LOG],
            'log_size':                 self._config[CONF_LOG_SIZE],

            'supported_statuses_on':    self._supported_statuses_on,
            'supported_statuses_off':   self._supported_statuses_off,

            'updateUI':					self._updateUI,

            'admin_password':           hashlib.sha256(str.encode(self._config[CONF_ADMIN_PASSWORD])).hexdigest(),

            'bwalarm_version':          VERSION,
            'py_version':               sys.version_info,
        }

        if (CONF_USERS in self._config):
            users = copy.deepcopy(self._config[CONF_USERS])
            for user in users:
                user['code'] = '****'
            results[CONF_USERS] = users

        if (CONF_PANEL in self._config):
            results[CONF_PANEL] = self._config[CONF_PANEL]

        if (CONF_THEMES in self._config):
            results[CONF_THEMES] = self._config[CONF_THEMES]

        if (CONF_LOGS in self._config):
            results[CONF_LOGS] = self._config[CONF_LOGS][-10:]

        if (CONF_MQTT in self._config):
            results[CONF_MQTT] = self._config[CONF_MQTT]

        if (CONF_STATES in self._config):
            results[CONF_STATES] = self._config[CONF_STATES]

        return results;

    def yaml_load(self):
        FNAME = '[LOAD_YAML]'
        try:
            self.yaml = YAML()
            filename = self._hass.config.path() + "/alarm.yaml"
            with open(filename) as stream:
                try:
                    _LOGGER.debug("{} File \"{}\" loaded successfully".format(FNAME, filename))
                    return self.yaml.load(stream)
                except self.yaml.YAMLError as exc:
                    print(exc)
            return None
        except Exception as e:
            _LOGGER.warning("{} Error loading file \"{}\": {}".format(FNAME, filename, str(e)));

    def settings_save(self, key=None, value=None):
        """Push the alarm state to the given value."""
        # it is called on change of every entry

        FNAME = '[SAVE_SETTINGS]'
        _LOGGER.debug("{} key: \"{}\", value: \"{}\"".format(FNAME, key if key else '', value if value else ''))

        key = key.lower()

        # update runtime config
        self._config[key] = value
        # load WHOLE config from yaml into loaded config
        self._yaml_content = self.yaml_load()
        if self._yaml_content:
            # and update it as well (as it is different to runtime config!!!)
            if key == CONF_STATES:
                _LOGGER.debug("{} {} value received, clean it up".format(FNAME, key))
                self._yaml_content[key] = self._clean_states_info(value)
            else:
                self._yaml_content[key] = value
        else:
            _LOGGER.error("{} yaml_load failed!".format(FNAME))
        # and now save the whole loaded config (not runtime one!!!)
        self.settings_yaml_save()

    def settings_user(self, user=None, command=None):
        """Push the alarm state to the given value."""
        self._yaml_content = self.yaml_load()

        x = 0

        if (command == 'add'):
            if user['id'] == None:
                user['id'] = uuid.uuid4().hex
            if ('users' not in self._config):
                self._config['users'] = [user]
                self._yaml_content['users'] = [user]
            else:
                _LOGGER.warning(user)
                self._config['users'].append(user)
                self._yaml_content['users'].append(user)
        elif (command == 'update'):
            for _user in self._config['users']:
                if _user['id'] == user['id']:
                    self._config['users'][x] = user
                    self._yaml_content['users'][x] = user
                x = x + 1
        elif (command == 'delete'):
            for _user in self._config['users']:
                if _user['id'] == user:
                    self._config['users'].pop(x)
                    self._yaml_content['users'].pop(x)
                x = x + 1
        elif (command == True or command == False):
            for _user in self._config['users']:
                if _user['id'] == user:
                    self._config['users'][x]['enabled'] = command
                    self._yaml_content['users'][x]['enabled'] = command
                x = x + 1

        self.settings_yaml_save()

    def settings_yaml_save(self):
        """ Save the whole loaded config and trigger a GUI update """

        FNAME = '[SAVE_SETTINGS_YAML]'
        _LOGGER.debug("{} begin".format(FNAME))
        self._updateUI = not self._updateUI

        # as it saves loaded config, make sure it is consistent with runtime config
        self._replace_obsolete_settings(self._config, self._yaml_content)
        # this magic required to get a proper representation of OrderedDict in generated yaml
        self.yaml.Representer.add_representer(OrderedDict, self.yaml.Representer.represent_dict)

        filename = self._hass.config.path() + "/alarm.yaml"
        with open(filename, 'w') as fil:
            self.yaml.dump(self._yaml_content, fil)

        _LOGGER.debug("{} settings saved to file \"{}\"".format(FNAME, filename))

        self.init_variables()
        self.schedule_update_ha_state()
        _LOGGER.debug("{} end".format(FNAME))

    def _replace_obsolete_settings(self, current_settings, loaded_settings):
        # it is required to get clear loaded config from obsolete stuff
        # and make sure new stuff is there as well

        FNAME = '[REPLACE_OBSOLETE_SETTINGS]'

        # if CONF_ENABLE_NIGHT_MODE attibute is not in yaml, add it
        if CONF_ENABLE_NIGHT_MODE in current_settings.keys() and CONF_ENABLE_NIGHT_MODE not in loaded_settings.keys():
            _LOGGER.debug("{} add core attribute {}: {}".format(FNAME, CONF_ENABLE_NIGHT_MODE, current_settings[CONF_ENABLE_NIGHT_MODE]))
            loaded_settings[CONF_ENABLE_NIGHT_MODE] = copy.deepcopy(current_settings[CONF_ENABLE_NIGHT_MODE])

        # if STATE_ALARM_ARMED_NIGHT state is not in yaml, add it
        if STATE_ALARM_ARMED_NIGHT in current_settings[CONF_STATES].keys() and STATE_ALARM_ARMED_NIGHT not in loaded_settings[CONF_STATES].keys():
            _LOGGER.debug("{} add state {}".format(FNAME, STATE_ALARM_ARMED_NIGHT))
            loaded_settings[CONF_STATES][STATE_ALARM_ARMED_NIGHT] = copy.deepcopy(current_settings[CONF_STATES][STATE_ALARM_ARMED_NIGHT])

        # delete obsolete records
        if OBSOLETE_CONF_ENABLE_PERIMETER_MODE in loaded_settings.keys():
            _LOGGER.debug("{} deleting obsolete core attribute {}: {}".format(FNAME, OBSOLETE_CONF_ENABLE_PERIMETER_MODE, loaded_settings[OBSOLETE_CONF_ENABLE_PERIMETER_MODE]))
            del loaded_settings[OBSOLETE_CONF_ENABLE_PERIMETER_MODE]

        if OBSOLETE_STATE_ALARM_ARMED_PERIMETER in loaded_settings[CONF_STATES].keys():
            _LOGGER.debug("{} delete obsolete state {}".format(FNAME, OBSOLETE_STATE_ALARM_ARMED_PERIMETER))
            del loaded_settings[CONF_STATES][OBSOLETE_STATE_ALARM_ARMED_PERIMETER]


    def persistence_load(self):
        """ LOAD persistence from file """
        FNAME = '[LOAD_PERSISTENCE]'

        filename = self._persistence_final_path
        if os.path.exists(filename):
            try:
                if os.path.isfile(filename):
                    # avoid empty files as they cause JSON error
                    if os.path.getsize(filename):
                        self._persistence_list = json.load(open(filename, 'r'))
                        _LOGGER.debug("{} File \"{}\" loaded successfully".format(FNAME, filename))
                        return True
                    else:
                        _LOGGER.warning("{} Ignored empty file \"{}\"".format(FNAME, filename))
                        return False
                else:
                    _LOGGER.warning("{} Cannot use file \"{}\": not a regular file".format(FNAME, filename))
                    return False
            except Exception as e:
                _LOGGER.error("{} Error occured while loading file \"{}\": {}".format(FNAME, filename, str(e)))
        else:
            # no worries, it only exists in pending modes
            #_LOGGER.info("{} File \"{}\" does not exist".format(FNAME, filename))
            return False

    def _clean_states_info(self, arm_states_dict):
        FNAME = '[CLEAN_STATES_INFO]'
        _LOGGER.debug("{} remove {} from states".format(FNAME, INT_ATTR_STATE_CHECK_BEFORE_ARM))

        states_dict = copy.deepcopy(arm_states_dict)
        # remove check_before_arm lists from each state
        for state in states_dict:
            # it deletes an entry
            states_dict[state].pop(INT_ATTR_STATE_CHECK_BEFORE_ARM, None)
            #_LOGGER.debug("{} state {}: {} removed".format(FNAME, state, INT_ATTR_STATE_CHECK_BEFORE_ARM))

        return states_dict

    def persistence_save(self, persistence):
        """ SAVE persistence to file """
        FNAME = '[SAVE_PERSISTENCE]'

        if persistence: #Check we have something to save [TODO] validate this is a persistence object
            self._persistence_list = persistence
            filename = self._persistence_final_path
            try:
                if self._persistence_list: #Check we have genuine persistence to save if so dump to file
                    with open(filename, 'w') as fil:
                        fil.write(json.dumps(self._persistence_list, ensure_ascii=False))
                        _LOGGER.debug("{} File \"{}\" saved successfully".format(FNAME, filename))
                else:
                    _LOGGER.error("{} No data to save".format(FNAME))
            except Exception as e:
               _LOGGER.error("{} Error occured while saving file \"{}\": {}".format(FNAME, filename, str(e)))

    def persistence_remove(self):
        """ REMOVE persistence file """
        FNAME = '[REMOVE_PERSISTENCE]'

        filename = self._persistence_final_path
        try:
            if os.path.exists(filename):
                os.remove(filename)
                _LOGGER.debug("{} File {} removed".format(FNAME, filename))
            else:
                _LOGGER.info("{} File {} does not exist".format(FNAME, filename))
        except Exception as e:
           _LOGGER.error("{} Error occured while removing file \"{}\": {}".format(FNAME, filename, str(e)))

    def save_alarm_state(self):
        """ Save alarm state """
        FNAME = '[SAVE_ALARM_STATE]'

        _LOGGER.debug("{} ({}) begin".format(FNAME, self._state))
        self._persistence_list["state"]     = self._state
        self._persistence_list["timeoutat"] = self._timeoutat.isoformat() if self._timeoutat else None
        self._persistence_list["returnto"]  = self._returnto
        self._persistence_list[CONF_STATES]  = self._clean_states_info(self._states)
        self._persistence_list["armstate"]  = self._armstate
        self.persistence_save(self._persistence_list)
        _LOGGER.debug("{} ({}) end".format(FNAME, self._state))

    def log_load(self):
        """ LOAD activity log previously saved """
        FNAME = '[LOAD_LOG]'

        try:
           if os.path.isfile(self._log_final_path):  #Find the log file and load.
              self._config[CONF_LOGS] = json.load(open(self._log_final_path, 'r'))
           else: #No log file found
              _LOGGER.warning("[ALARM] Activity log file does not exist")
              self._config[CONF_LOGS] = []
              self.log_save()
        except Exception as e:
           _LOGGER.error("[ALARM] Error occured loading: %s", str(e))

    def log_save(self):
        """ UPDATE activity log """
        FNAME = '[SAVE_LOG]'

        try:
           if self._config[CONF_LOGS] is not []: #Check we have genuine log to save if so dump to file
              with open(self._log_final_path, 'w') as fil:
                 fil.write(json.dumps(self._config[CONF_LOGS], ensure_ascii=False))
           else:
              _LOGGER.error("{} No log to save".format(FNAME))
        except Exception as e:
           _LOGGER.error("{} Error occured saving file \"{}\": {}".format(FNAME, self._log_final_path, str(e)))

    def has_open_sensors(self, arm_state):
        """ Returns True if there are open sensors for that mode and they are not in override section"""
        FNAME = '[HAS_OPEN_SENSORS]'

        # iterate over all but override registered sensors of that state (ready-made list)
        for entity_id in self._config[CONF_STATES][arm_state][INT_ATTR_STATE_CHECK_BEFORE_ARM]:
            state = self._hass.states.get(entity_id)
            if state and state.state.lower() in self._supported_statuses_on:
                _LOGGER.debug("{}({}) {} is {}".format(FNAME, arm_state, entity_id, state.state))
                return True

        _LOGGER.debug("{}({}) all clear".format(FNAME, arm_state))
        return False

    def alarm_arm(self, event, code, ignore_open_sensors):
        FNAME = "[ALARM_ARM]"
        einfo = event2name[event]
        service = einfo[EATTR_SERVICE]
        state = einfo[EATTR_STATE]

        _LOGGER.debug("{} (service: {}, passcode: \"{}\", ignore_open_sensors: {}) begin".format(FNAME, service, code, ignore_open_sensors))
        if not isinstance(ignore_open_sensors, bool):
            _LOGGER.error("{} ignore_open_sensors must be bool, got {}".format(FNAME, type(ignore_open_sensors)))
            return False

        # for MQTT or service calls as Control Panel always sends ignore_open_sensors = True (it checks them itself atm)
        if not ignore_open_sensors and self.has_open_sensors(state):
            _LOGGER.info("{} Failed to {}: opens sensors detected".format(FNAME, service))
            return False

        admin_id = 'HA'
        user_id = ''
        arm_immediately = False    # makes sense only for non-GUI calls (MQTT message/service call)

        # if code provided, try to match it with user
        if code:
            if code == self._code:
                user_id = admin_id
                _LOGGER.info("{} {} the alarm as {}".format(FNAME, service, user_id))
            elif code == "override":
                arm_immediately = True
                user_id = admin_id
                _LOGGER.info("{} {} the alarm immediately as {}".format(FNAME, service, user_id))
            else:
                # is it one of the users?
                for entity in self._users:
                    if entity['enabled'] and entity['code'] == code:
                        user_id = entity['id']
                        _LOGGER.info("{} {} the alarm as {}".format(FNAME, service, entity['name']))

                # code does not match any known code
                # arm as HA
                if not user_id:
                    user_id = admin_id
                    _LOGGER.warning("{} Ignored invalid passcode \"{}\", {} the alarm as {}".format(FNAME, code, service, user_id))
        else:
            user_id = admin_id
            _LOGGER.info("{} no passcode supplied, {} the alarm as {}".format(FNAME, service, user_id))

        self.process_event(event, arm_immediately)
        self._update_log(user_id, event)
        _LOGGER.debug("{} (service: {}, passcode: \"{}\", ignore_open_sensors: {}) end".format(FNAME, service, code, ignore_open_sensors))
        return True

    def alarm_arm_home(self, code, ignore_open_sensors):
        return self.alarm_arm(Events.ArmHome, code, ignore_open_sensors)

    def alarm_arm_away(self, code, ignore_open_sensors):
        return self.alarm_arm(Events.ArmAway, code, ignore_open_sensors)

    def alarm_arm_night(self, code, ignore_open_sensors):
        return self.alarm_arm(Events.ArmNight, code, ignore_open_sensors)

    # required for MQTT commands
    def async_alarm_arm_home(self, code, ignore_open_sensors):
        return self._hass.async_add_executor_job(self.alarm_arm_home, code, ignore_open_sensors)

    # required for MQTT commands
    def async_alarm_arm_away(self, code, ignore_open_sensors):
        return self._hass.async_add_executor_job(self.alarm_arm_away, code, ignore_open_sensors)

    # required for MQTT commands
    def async_alarm_arm_night(self, code, ignore_open_sensors):
        return self._hass.async_add_executor_job(self.alarm_arm_night, code, ignore_open_sensors)

    def alarm_trigger(self, code=None):
        self.process_event(Events.Trigger)
        self._update_log(None, LOG.TRIGGERED)

    def alarm_disarm(self, code):
        FNAME = "[ALARM_DISARM]"

        _LOGGER.debug("{} (passcode: \"{}\") begin".format(FNAME, code))

        #If the provided code matches the panic alarm then deactivate the alarm but set the state of the panic mode to active.
        if self._validate_panic_code(code):
            _LOGGER.warning("{} passcode matches the panic code, disarm but activate panic mode!".format(FNAME))
            self.process_event(Events.Disarm)
            self._panic_mode = "ACTIVE"
            self._update_log(None, LOG.DISARMED) #Show a default disarm message incase this is displayed on the interface
            # Let HA know that something changed
            self.schedule_update_ha_state()
            _LOGGER.debug("{} (passcode: \"{}\") end (return True)".format(FNAME, code))
            return True

        if not self._validate_code(code):
            _LOGGER.error("{} Failed to disarm: invalid passcode \"{}\"".format(FNAME, code))
            self._update_log(None, LOG.DISARM_FAIL)
            _LOGGER.debug("{} (passcode: \"{}\") end (return False)".format(FNAME, code))
            return False

        self.process_event(Events.Disarm)
        _LOGGER.debug("{} (passcode: \"{}\") end (return True)".format(FNAME, code))
        return True

    ### Internal processing
    def setsignals(self, state):
        """ Figure out what to sense and how """
        FNAME = '[SETSIGNALS]'
        _LOGGER.debug("{} {}".format(FNAME, state))

        self.immediate = self._states[state][CONF_IMMEDIATE].copy()
        self.delayed   = self._states[state][CONF_DELAYED].copy()
        self.override  = self._states[state][CONF_OVERRIDE].copy()
        # TODO?
        self.ignored   = set(self._allsensors) - (set(self.immediate) | set(self.delayed))
        # make room for a trigger
        self._lasttrigger = ''

    def clearsignals(self):
        """ Clear all our signals, we aren't listening anymore """
        FNAME = '[CLEARSIGNALS]'
        _LOGGER.debug("{}".format(FNAME))

        self._panic_mode = "deactivated"
        self._armstate = STATE_ALARM_DISARMED
        self.immediate = set()
        self.delayed = set()
        self.ignored = self._allsensors.copy()
        self._timeoutat = None
        # makes no sense when DISARMED?
        self._lasttrigger = ''

    def process_event(self, event, override_pending_time=False):
        FNAME = '[PROCESS_EVENT]'
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

            elif event == Events.ArmNight:
                if (datetime.timedelta(seconds=int(self._states[STATE_ALARM_ARMED_NIGHT][CONF_PENDING_TIME])) and override_pending_time == False):
                    self._armstate = STATE_ALARM_ARMED_NIGHT
                    self._state = STATE_ALARM_PENDING
                else:
                    self._state = STATE_ALARM_ARMED_NIGHT
                self._armstate = STATE_ALARM_ARMED_NIGHT

        elif old_state == STATE_ALARM_PENDING:
            if   event == Events.Timeout:       self._state = self._armstate

        elif old_state == STATE_ALARM_ARMED_HOME or \
             old_state == STATE_ALARM_ARMED_AWAY or \
             old_state == STATE_ALARM_ARMED_NIGHT:
            if   event == Events.ImmediateTrip: self._state = STATE_ALARM_TRIGGERED
            elif event == Events.DelayedTrip:   self._state = STATE_ALARM_WARNING

        elif old_state == STATE_ALARM_WARNING:
            if   event == Events.Timeout:       self._state = STATE_ALARM_TRIGGERED

        elif old_state == STATE_ALARM_TRIGGERED:
            if   event == Events.Timeout:       self._state = self._returnto

        new_state = self._state
        if old_state != new_state:
            _LOGGER.debug("{} state changes from {} to {}".format(FNAME, old_state, new_state))
            # Things to do on entering state
            if new_state == STATE_ALARM_WARNING:
                _LOGGER.debug("{} Turning on warning".format(FNAME))
                if self._config.get(CONF_WARNING):
                    self._hass.services.call(self._config.get(CONF_WARNING).split('.')[0], 'turn_on', {'entity_id':self._config.get(CONF_WARNING)})
                self._timeoutat = now() +  datetime.timedelta(seconds=int(self._states[self._armstate][CONF_WARNING_TIME]))
                self._update_log(None, LOG.TRIPPED, self._lasttrigger)
            elif new_state == STATE_ALARM_TRIGGERED:
                _LOGGER.debug("{} Turning on alarm".format(FNAME))
                if self._config.get(CONF_ALARM):
                    self._hass.services.call(self._config.get(CONF_ALARM).split('.')[0], 'turn_on', {'entity_id':self._config.get(CONF_ALARM)})
                if (self._states[self._armstate][CONF_TRIGGER_TIME] == -1):
                    self._timeoutat = now() + datetime.timedelta(hours=int(24))
                else:
                    self._timeoutat = now() + datetime.timedelta(seconds=int(self._states[self._armstate][CONF_TRIGGER_TIME]))
                self._update_log(None, LOG.TRIPPED, self._lasttrigger)
            elif new_state == STATE_ALARM_PENDING:
                _LOGGER.debug("{} Pending user leaving house".format(FNAME))
                if self._config.get(CONF_WARNING):
                    self._hass.services.call(self._config.get(CONF_WARNING).split('.')[0], 'turn_on', {'entity_id':self._config.get(CONF_WARNING)})
                self._timeoutat = now() + datetime.timedelta(seconds=int(self._states[self._armstate][CONF_PENDING_TIME]))
                #self._returnto = STATE_ALARM_ARMED_AWAY
                self.setsignals(self._armstate)
            elif new_state == STATE_ALARM_ARMED_HOME:
                self._returnto = new_state
                self.setsignals(STATE_ALARM_ARMED_HOME)
            elif new_state == STATE_ALARM_ARMED_AWAY:
                self._returnto = new_state
                self.setsignals(STATE_ALARM_ARMED_AWAY)
            elif new_state == STATE_ALARM_ARMED_NIGHT:
                self._returnto = new_state
                self.setsignals(STATE_ALARM_ARMED_NIGHT)
            elif new_state == STATE_ALARM_DISARMED:
                self._returnto = new_state
                self.clearsignals()

            # Things to do on leaving state
            if old_state == STATE_ALARM_WARNING or old_state == STATE_ALARM_PENDING:
                _LOGGER.debug("{} Turning off warning".format(FNAME))
                if self._config.get(CONF_WARNING):
                    self._hass.services.call(self._config.get(CONF_WARNING).split('.')[0], 'turn_off', {'entity_id':self._config.get(CONF_WARNING)})

            elif old_state == STATE_ALARM_TRIGGERED:
                _LOGGER.debug("{} Turning off alarm".format(FNAME))
                if self._config.get(CONF_ALARM):
                    self._hass.services.call(self._config.get(CONF_ALARM).split('.')[0], 'turn_off', {'entity_id':self._config.get(CONF_ALARM)})

            # if persistence enabled
            if self._config[CONF_ENABLE_PERSISTENCE]:
                # remove persistence file as it makes no sense when disarmed
                if new_state == STATE_ALARM_DISARMED:
                    self.persistence_remove()
                else:
                    self.save_alarm_state()
            # Let HA know that something changed
            self.schedule_update_ha_state()

            # check if the sensor that triggered the alarm is still in alarm state
            if old_state == STATE_ALARM_TRIGGERED and new_state != STATE_ALARM_DISARMED and self._lasttrigger:
                _LOGGER.debug("{} Checking state of {}..".format(FNAME, self._lasttrigger))
                lasttrigger_state = self._hass.states.get(self._lasttrigger)
                if (lasttrigger_state != None):
                    _state = lasttrigger_state.state.lower()
                    _LOGGER.debug("{} {} is {}".format(FNAME, self._lasttrigger, _state))
                    if _state in self._supported_statuses_on:
                        _LOGGER.info("{} {} is still in alarm state, trigger the alarm immediately".format(FNAME, self._lasttrigger))
                        self.process_event(Events.ImmediateTrip)
                    else:
                        _LOGGER.debug("{} {} is in normal state, nothing to do".format(FNAME, self._lasttrigger))
                else:
                    _LOGGER.info("{} sensor {} is not found!".format(FNAME, self._lasttrigger))

    def _validate_code(self, code):
        """Validate given code."""
        FNAME = '[VALIDATE_CODE]'

        if ((int(self._passcode_attempt_allowed) == -1) or (self._passcodeAttemptNo <= int(self._passcode_attempt_allowed))):
            check = self._code is None or code == self._code or self._validate_user_codes(code)
            if code == self._code:
                self._update_log(None, LOG.DISARMED)
            return self._validate_code_attempts(check)
        else:
            _LOGGER.info("{} Too many passcode attempts, try again later".format(FNAME))
            return False

    def _validate_user_codes(self, code):
        FNAME = '[VALIDATE_USER_CODES]'

        for entity in self._users:
            if entity['enabled'] and entity['code'] == code:
                self._update_log(entity['id'], LOG.DISARMED)
                return True
        return False

    def _validate_code_attempts(self, check):
        FNAME = '[VALIDATE_CODE_ATTEMPTS]'

        if check:
            self._passcodeAttemptNo = 0
        else:
            _LOGGER.info("{} Invalid passcode".format(FNAME))
            self._passcodeAttemptNo += 1
            if (int(self._passcode_attempt_allowed) != -1 and self._passcodeAttemptNo > int(self._passcode_attempt_allowed)):
                self._panel_locked = True
                self._passcode_timeoutat = now() + datetime.timedelta(seconds=int(self._passcode_attempt_timeout))
                _LOGGER.info("{} Panel locked, too many passcode attempts!".format(FNAME))
                self._update_log(None, LOG.LOCKED)

        self.schedule_update_ha_state()
        return check

    def _validate_panic_code(self, code):
        """Validate given code."""
        FNAME = '[VALIDATE_PANIC_CODE]'

        check = code == self._panic_code
        if check:
            _LOGGER.info("{} PANIC MODE ACTIVATED!".format(FNAME))
            self._passcodeAttemptNo = 0
        return check

    def _update_log(self, user_id, event, entity_id=None):
        FNAME = '[UODATE_LOG]'

        # entity_id is an active sensor's id
        if not user_id:
            user_id = 'HA'
        self.changedbyuser = user_id
        if (CONF_ENABLE_LOG in self._config):
            self._log_size = int(self._config[CONF_LOG_SIZE]) if CONF_LOG_SIZE in self._config else 10
            if self._log_size != -1 and len(self._config[CONF_LOGS]) >= self._log_size:
                self._config[CONF_LOGS].remove(self._config[CONF_LOGS][0])
            self._config[CONF_LOGS].append([time.time(), user_id, event.value, entity_id])
            self.log_save()

    #### Listeners ####
    def state_change_listener(self, event):
        """ Something changed, we only care about things turning on at this point """
        FNAME = '[STATE_CHANGE_LISTENER]'

#        _LOGGER.debug("state_change_listener: event {}".format(event))
        # makes sense only in pending states
        # do not modify _lasttrigger if it's not empty to preserve the original trigger
        if self._state in SUPPORTED_PENDING_STATES and not self._lasttrigger:
            new_state = event.data.get('new_state', None)
            if new_state and new_state.state:
                if new_state.state.lower() in self._supported_statuses_on:
                    eid = event.data['entity_id']
                    if eid in self.immediate:
                        _LOGGER.debug("{} immediate: {} is {}".format(FNAME, event.data['entity_id'], new_state.state))
                        self._lasttrigger = eid
                        self.process_event(Events.ImmediateTrip)
                    elif eid in self.delayed:
                        _LOGGER.debug("{} delayed: {} is {}".format(FNAME, event.data['entity_id'], new_state.state))
                        self._lasttrigger = eid
                        self.process_event(Events.DelayedTrip)

    ### Actions from the outside world that affect us, turn into enum events for internal processing
    def time_change_listener(self, eventignored):
        """ I just treat the time events as a periodic check, its simpler then (re-/un-)registration """
        FNAME = '[TIME_CHANGE_LISTENER]'

        if self._timeoutat is not None:
            if now() > self._timeoutat:
                self._timeoutat = None
                self.process_event(Events.Timeout)

    ### Actions from the outside world that affect us, turn into enum events for internal processing
    def passcode_timeout_listener(self, eventignored):
        FNAME = '[PASSCODE_TIME_LISTENER]'

        if self._passcode_timeoutat is not None:
            if now() > self._passcode_timeoutat:
                self._panel_locked = False
                self._passcode_timeoutat = None
                self._passcodeAttemptNo = 0
                self.schedule_update_ha_state()

    async def _async_state_changed_listener(self, entity_id, old_state, new_state):
        """Publish state change to MQTT."""

        # publish only if MQTT enabled
        if (self._config[CONF_MQTT][CONF_ENABLE_MQTT]):
            FNAME = '[ASYNC_STATE_CHANGE_LISTENER]'

            # empty name means HA just started
            old_state_name = old_state.state if old_state else ''
            new_state_name = new_state.state if new_state else ''
#            _LOGGER.debug("{} Got old_state: \"{}\", new_state: \"{}\"".format(FNAME, old_state_name, new_state_name))

            # publish only if the state changed (not on start)
            if old_state_name and new_state_name and new_state_name != old_state_name:
                _LOGGER.debug("{} old_state: \"{}\", new_state: \"{}\"".format(FNAME, old_state_name, new_state_name))
                state_name = STATE_ALARM_PENDING if (new_state_name == STATE_ALARM_WARNING and self._pending_on_warning) else new_state_name
                _LOGGER.debug("{} mqtt.publish(topic={}, state={}, qos={}, retain={})".format(FNAME, self._state_topic, state_name, self._qos, True))
                self._mqtt.async_publish(self._hass, self._state_topic, state_name, self._qos, True)

    #### MQTT support####
    @asyncio.coroutine
    def async_added_to_hass(self):
        """Subscribe mqtt events.
        This method must be run in the event loop and returns a coroutine.
        """

        @callback
        def message_received(msg):
            """Run when new MQTT message has been received."""
            FNAME = '[MESSAGE_RECEIVED]'
            _LOGGER.debug("{} payload: \"{}\"".format(FNAME, msg.payload))

            # assume the message is always like
            # command _JSON_dict_
            # where _JSON_dict_ is optional
            command, sep, params = msg.payload.partition(" ")
            code = None
            ignore_open_sensors = CONST_DEF_IGNORE_OPEN_SENSORS

            if params:
                _LOGGER.debug("{} atributes to import: \"{}\"".format(FNAME, params))
                try:
                    data = json.loads(params)
                    if isinstance(data, dict):
                        _LOGGER.debug("{} valid JSON received".format(FNAME))
                        # extract data from json
                        # TODO: if ATTR_ENTITY_ID in data.keys():
                        if ATTR_CODE in data.keys():
                            _LOGGER.debug("{} {}: \"{}\"".format(FNAME, ATTR_CODE, data[ATTR_CODE]))
                            code = str(data[ATTR_CODE])
                        if ATTR_IGNORE_OPEN_SENSORS in data.keys():
                            _LOGGER.debug("{} {}: {}".format(FNAME, ATTR_IGNORE_OPEN_SENSORS, data[ATTR_IGNORE_OPEN_SENSORS]))
                            ignore_open_sensors = str2bool(data[ATTR_IGNORE_OPEN_SENSORS])
                    else:
                        _LOGGER.warning("{} Only JSON attributess supported, ignore: \"{}\"".format(FNAME, params))
                except Exception as e:
                   _LOGGER.error("{} Exception: {}".format(FNAME, e))

                #_LOGGER.debug("{} extracting attributes: end".format(FNAME))

            #_LOGGER.debug("{} command: \"{}\", code: \"{}\", ignore_open_sensors: {}".format(FNAME, command, code, ignore_open_sensors))

            if command == self._payload_arm_home:
                self.async_alarm_arm_home(code, ignore_open_sensors)
            elif command == self._payload_arm_away:
                self.async_alarm_arm_away(code, ignore_open_sensors)
            elif command == self._payload_arm_night:
                if self._enable_night_mode:
                    self.async_alarm_arm_night(code, ignore_open_sensors)
                else:
                    _LOGGER.error("{} {} disabled".format(FNAME, command))
                    return
            elif command == self._payload_disarm:
                # True if master/user code required to disarm the alarm
                code_to_disarm = not self._override_code
                _LOGGER.debug("{} require passcode to disarm option: {}".format(FNAME, 'Enabled' if code_to_disarm else 'Disabled'))

                # if code required but there is no code, that's not allowed
                if code_to_disarm and not code:
                    _LOGGER.error("{} Failed to {}: passcode required".format(FNAME, command))
                    return
                elif not code_to_disarm:
                    if code:
                        _LOGGER.warning("{} Ignore unexpected passcode \"{}\"".format(FNAME, code))
                    code = self._code
                # safe to disarm with a code or admin code (override mode, no need to supply one externally)
                _LOGGER.info("{} {} with{}".format(FNAME, command, " passcode \"" + code + "\"" if code_to_disarm else "out passcode (override mode)"))
                self.async_alarm_disarm(code)
            else:
                _LOGGER.error("{} Ignoring unsupported command \"{}\"".format(FNAME, command))
                return

        if (self._config[CONF_MQTT][CONF_ENABLE_MQTT]):
            async_track_state_change(
                self._hass, self.entity_id, self._async_state_changed_listener
            )

            return self._mqtt.async_subscribe(
                self._hass, self._command_topic, message_received, self._qos)
