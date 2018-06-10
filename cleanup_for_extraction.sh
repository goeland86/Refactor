#!/bin/bash

for f in `ls version.d/*`
  do
    source $f
  done

echo "*** Stopping Octoprint ***"
systemctl stop octoprint

echo "*** Stopping Redeem ***"
systemctl stop redeem

echo "*** Stopping Toggle ***"
systemctl stop toggle

echo "*** Removing log files ***"
rm ${OCTOPRINT_HOME}/.octoprint/logs/*
touch ${OCTOPRINT_HOME}/.octoprint/logs/plugin_redeem.log
chown -R octo:octo ${OCTOPRINT_HOME}

echo "*** Removing bash history for root ***"
rm /root/.bash_history

echo "*** Removing bash history for ubuntu ***"
rm /home/ubuntu/.bash_history

echo "*** Removing bash history for octo ***"
rm ${OCTOPRINT_HOME}/.bash_history

poweroff
