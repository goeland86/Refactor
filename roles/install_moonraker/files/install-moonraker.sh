#!/bin/bash

cd /home/debian
git clone https://github.com/Arksine/moonraker.git --depth 1
chown -R debian:debian moonraker
cd moonraker
su - debian -c "/home/debian/moonraker/scripts/install-moonraker.sh"

cp docs/moonraker.conf /home/debian
chown debian:debian /home/debian/moonraker.conf
sed -i 's/enabled: True//' /home/debian/moonraker.conf

mkdir -p /home/debian/printer_config
chown debian:debian /home/debian/printer_config

sed -i 's:klippy\.log:klippy\.log -a /tmp/klippy_uds:' /etc/systemd/system/klipper.service
systemctl daemon-reload
systemctl restart klipper
