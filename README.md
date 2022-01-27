# Refactor
Simplified Recore and Replicape board image generation toolset, based on Armbian for Recore or Debian images from RCN for beaglebone.

[![Build](https://github.com/intelligent-agent/Refactor/actions/workflows/main.yml/badge.svg)](https://github.com/intelligent-agent/Refactor/actions/workflows/main.yml)

The starting point for Refactor is the Armbian/Debian console image, details are in the wiki here:
https://wiki.iagent.no/wiki/Refactor

Refactor is a build-tool to install a printer's Firmware (at the moment Klipper), a printer control interface (OctoPrint), a touch-screen interface (Toggle w/ OctoPrint) and a few miscellaneous items (webcam streamer, network file share for gcode file uploads, etc.).

The hostname for Recore is `recore`. The hostname for replicape is `replicape`.

It sets a default password for access as root on new images, but leaves the root account alone otherwise:
SSH is meant to be active and allow root login. The `debian` user is normally also setup and runs OctoPrint and Klipper. Both root and debian passwords will need to be changed upon first login.  
Username/password: `root`/`kamikaze`  
Username/password: `debian`/`temppwd`  

## Usage
The images generated are focused on being a boot-strapped firmware for Thing-Printer control boards, such as Replicape and Recore. However PRs to make ReFactor an image generation tool for a wider range of single-board controllers is completely welcome. To support multiple platforms, the build script usage has been modified:
```
cd <path to Refactor git clone>
sudo ./build-image-in-chroot-end-to-end.sh <platform> [OPTIONAL: system setup script]
```
If not specified, the _ansible-playbook_ that is used is ___SYSTEM_klipper_octoprint-DEFAULT.yml___

The platform (required parameter) is one of:
 * replicape
 * recore
 * (pi)
 * (pi64)

The script then exports the `platform` ansible variable, and sources the `BaseLinux/$platform/Linux` file for a number of items:
* a URL for which base linux image to build from (pine64 armbian for `pi64` and `recore`, RCN-built console debian 10.3 for `replicape`, raspbian for `pi`)
* the `decompress()` function, to allow the script to properly decompress the downloaded file and export the image file to where it can be mounted
* additional ansible parameters specific to the platform requirements. For the moment this is where the `platform` gets passed through, as well as the `firmware` variable.

**IMPORTANT NOTE**: Only the `SYSTEM-[...].yml` playbook files can work with the `build-image-in-chroot-end-to-end.sh` script. The `INSTALL-[...].yml` playbooks are provided as means for end-users to customize their running images. It is inadvisable to run a `SYSTEM-[...].yml` playbook on an already running system. And especially not during a print. That would cause a division by zero and make the printer disappear into its own micro black hole. Or release the magic smoke. Either way, not a good thing. You have been warned.

## Example of running a task locally
Creating a complete image can take a long time. During development it's better to run a single task.
Here is an example of re-installing Toggle on a platform on a running Recore board.
`ansible-playbook INSTALL-toggle.yml --extra-vars '{platform: recore}'`

# Contributing
Any contribution you make should be in the form of a PR in a separate branch and mull against master.
It's nice to add a descriptive prefix like `chore/clean-up-unused-code`
If you are trying to fix a bug, please prefix the `PR` with `[bug]`, and mention the Github Issue # in the PR description.

In case you need help building an image to test your changes and do not have a build environment available, please submit your PR against `goeland86/ReFactor`, with a title prefixed with `[Dev]` to clearly identify that the features are still under active development.

# Latest images
Latest images for testing are uploaded to github: https://github.com/intelligent-agent/Refactor/releases
