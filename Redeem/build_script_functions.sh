for f in `ls version.d/*`
  do
    source $f
  done

install_redeem() {
  echo "**install_redeem**"
  if [ ! -d $REDEEM_HOME ]; then
    git clone $REDEEM_REPOSITORY --single-branch --branch $REDEEM_BRANCH $REDEEM_HOME
  fi
  cd $REDEEM_HOME
  git pull
  git checkout $REDEEM_BRANCH
  make install

  # Make profiles uploadable via Octoprint
  cp -r configs /etc/redeem
  cp -r data /etc/redeem
  touch /etc/redeem/local.cfg
  chown -R octo:octo /etc/redeem/
  chown -R octo:octo /usr/local/src/redeem/

  cd $WD

  # Install rules
  cp Redeem/stepper_device.rules /etc/udev/rules.d/

  # Install Umikaze specific systemd script
  cp Redeem/redeem.service /lib/systemd/system
  systemctl enable redeem
  # systemctl start redeem
}
