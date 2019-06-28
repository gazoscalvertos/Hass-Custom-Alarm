"""Constants for bwalarm"""

CUSTOM_INTEGRATIONS_ROOT    = 'custom_components'
# create [HA config]/OVERRIDE_FOLDER/INTEGRATION_FOLDER/ to take precedence
# over a correspondent file in [HA config]/CUSTOM_INTEGRATIONS_ROOT/INTEGRATION_FOLDER/RESOURCES_FOLDER
OVERRIDE_FOLDER             = 'resources'
PLATFORM                    = 'bwalarm'

# integration folder inside [HA config]/CUSTOM_INTEGRATIONS_ROOT/
INTEGRATION_FOLDER          = PLATFORM
# resides inside INTEGRATION_FOLDER
RESOURCES_FOLDER            = 'resources'

CONFIG_FNAME                = "{}.yaml".format(PLATFORM)
PERSISTENCE_FNAME           = "{}.json".format(PLATFORM)
LOG_FNAME                   = "{}_log.json".format(PLATFORM)
PANEL_FNAME                 = "panel.html"

# resides inside RESOURCES_FOLDER
IMAGES_FOLDER               = 'images'
DEFAULT_ICON_NAME           = 'ha.png'
