# Refactor
Refactor is a set of Ansible roles to build a working Recore embedded image.

[![Build](https://github.com/intelligent-agent/Refactor/actions/workflows/main.yml/badge.svg)](https://github.com/intelligent-agent/Refactor/actions/workflows/main.yml)

The starting point for Refactor is a Rebuild image, which builds a fresh Armbian-clone for Recore, but pulls in a number of configurations and variables for building from the Refactor ansible roles.
https://wiki.iagent.no/wiki/Refactor

This build system will install Klipper and the choice of OctoPrint or Mainsail and Moonraker, with ustreamer and a few other helpful utilities for Recore.
A touch screen interface is also installed, either Toggle for OctoPrint or KlipperScreen for Mainsail.

The default hostname for Recore is `recore.local`.

During installation using Reflash, the user can choose to leave the SSH access for user `debian` open or closed. If you choose to have it open, you should log in as user `debian` which will force a change of password. The USB C connector also presents as a serial port which will always allow anyone with physical access to the board to log in. 
The default login on a freshly flashed image is:
Username/password: `debian`/`temppwd`  

## Default playbooks
The provided images are generated using Ansible playbook files, which you can find at the root of this repository, starting with the name `SYSTEM-`.
Additional playbooks are added in a subfolder called `addons`, and will optionally install new features (such as a CIFS-based network drive access, various Klipper plugins, etc.)

# Contributing
Any contribution you make should be in the form of a PR in a separate branch and mull against master.
It's nice to add a descriptive prefix like `chore/clean-up-unused-code`
If you are trying to fix a bug, please prefix the `PR` with `[bug]`, and mention the Github Issue # in the PR description.

# Latest images
Latest images for testing are uploaded to github: https://github.com/intelligent-agent/Rebuild/releases
