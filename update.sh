#!/bin/bash

function get_file {
  DOWNLOAD_PATH=${2}?raw=true
  FILE_NAME=$1
  if [ "${FILE_NAME:0:1}" = "/" ]; then
    SAVE_PATH=$FILE_NAME
  else
    SAVE_PATH=$3$FILE_NAME
  fi
  TMP_NAME=${1}.tmp
  echo "Getting $1"
  # wget $DOWNLOAD_PATH -q -O $TMP_NAME
  curl -s -q -L -o $TMP_NAME $DOWNLOAD_PATH
  rv=$?
  if [ $rv != 0 ]; then
    rm $TMP_NAME
    echo "Download failed with error $rv"
    exit
  fi
  diff ${SAVE_PATH} $TMP_NAME &>/dev/null
  if [ $? == 0 ]; then
    echo "File up to date."
    rm $TMP_NAME
    return 0
  else
    mv $TMP_NAME ${SAVE_PATH}
    if [ $1 == $0 ]; then
      chmod u+x $0
      echo "Restarting"
      $0
      exit $?
    else
      return 1
    fi
  fi
}

function check_dir {
  if [ ! -d $1 ]; then
    read -p "$1 dir not found. Create? (y/n): [n] " r
    r=${r:-n}
    if [[ $r == 'y' || $r == 'Y' ]]; then
      mkdir -p $1
    else
      exit
    fi
  fi
}

if [ ! -f configuration.yaml ]; then
  echo "There is no configuration.yaml in current dir. 'update.sh' should run from Homeassistant config dir"
  read -p "Are you sure you want to continue? (y/n): [n] " r
  r=${r:-n}
  if [[ $r == 'n' || $r == 'N' ]]; then
    exit
  fi
fi

get_file $0 https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/update.sh ./

check_dir "custom_components/alarm_control_panel"

get_file bwalarm.py https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/custom_components/alarm_control_panel/bwalarm.py custom_components/alarm_control_panel/

check_dir "panels/"

get_file alarm.html https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/panels/alarm.html panels/

check_dir "www/lib/"

get_file countdown360.js https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/www/lib/countdown360.js www/lib/
get_file jquery-3.2.1.min.js https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/www/lib/jquery-3.2.1.min.js www/lib/

check_dir "www/alarm/"

get_file alarm.css https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/www/alarm/alarm.css www/alarm/


get_file alarm.yaml.sample https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/alarm.yaml ./
get_file automation.yaml.sample https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/automation.yaml ./
get_file panel_custom.yaml https://github.com/gazoscalvertos/Hass-Custom-Alarm/blob/master/panel_custom.yaml ./


#
echo ""
echo "Add in configuration.yaml : "
echo ""
echo "alarm_control_panel: !include alarm.yaml"
echo "panel_custom: !include panel_custom.yaml"
