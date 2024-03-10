# Refactor
Refactor is a Linux distro for Recore based on Armbian.

[![Build](https://github.com/intelligent-agent/Refactor/actions/workflows/main.yml/badge.svg)](https://github.com/intelligent-agent/Refactor/actions/workflows/main.yml)

The starting point for Refactor is the Armbian console image, details are in the wiki here:
https://wiki.iagent.no/wiki/Refactor

This build system will install Klipper and the choice of OctoPrint or Mainsail and Moonraker.
A touch screen interface is also installed, either Toggle for OctoPrint or KlipperScreen for Mainsail.
In addition, there are some other programs such as mjpg-streamer to add webcam functionality and the setting up the
right folders and config files so the software is ready to use out of the box.

The hostname for Recore is `recore`.

During installation using Reflash, the user can choose to leave the SSH access for user `debian` open or closed. If you choose to have it open, you should log in as user `debian` which will force a change of password. The USB C connector also presents the a serial port which will always allow anyone with physical access to the board to log in. Default passwords are:
Username/password: `root`/`kamikaze`  
Username/password: `debian`/`temppwd`  

## Running the image generation on the command line
The images generated are focused on being a boot-strapped firmware for Thing-Printer control boards, such as Replicape and Recore. PRs to make Refactor better are welcome. To support multiple platforms, the build script usage has been modified:
```
cd <path to Refactor git clone>
sudo ./build-image-in-chroot-end-to-end.sh <platform> [OPTIONAL: system setup script]
```
If not specified, the _ansible-playbook_ that is used is ___SYSTEM_klipper_octoprint-DEFAULT.yml___

The script then exports the `platform` ansible variable, and sources the `BaseLinux/$platform/Linux` file for a number of items:
* a URL for which base linux image to build from (pine64 armbian for `pi64` and `recore`, RCN-built console debian 10.3 for `replicape`, raspbian for `pi`)
* the `decompress()` function, to allow the script to properly decompress the downloaded file and export the image file to where it can be mounted
* additional ansible parameters specific to the platform requirements. For the moment this is where the `platform` gets passed through, as well as the `firmware` variable.

**IMPORTANT NOTE**: Only the `SYSTEM-[...].yml` playbook files can work with the `build-image-in-chroot-end-to-end.sh` script. The `INSTALL-[...].yml` playbooks are provided as means for end-users to customize their running images. It is inadvisable to run a `SYSTEM-[...].yml` playbook on an already running system. And especially not during a print. That would cause a division by zero and make the printer disappear into its own micro black hole. Or release the magic smoke. Either way, not a good thing. You have been warned.

# Contributing
Any contribution you make should be in the form of a PR in a separate branch and mull against master.
It's nice to add a descriptive prefix like `chore/clean-up-unused-code`
If you are trying to fix a bug, please prefix the `PR` with `[bug]`, and mention the Github Issue # in the PR description.

In case you need help building an image to test your changes and do not have a build environment available, please submit your PR against `goeland86/ReFactor`, with a title prefixed with `[Dev]` to clearly identify that the features are still under active development.

# Latest images
Latest images for testing are uploaded to github: https://github.com/intelligent-agent/Refactor/releases
