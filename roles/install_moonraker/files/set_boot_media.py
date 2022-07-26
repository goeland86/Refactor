# Set the boot media of a distribution (emmc or usb)
#
# Copyright (C) 2022  Elias Bakken <elias@iagent.no>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import os
import logging

class SetBootMedia:
    def __init__(self, config):
        self.server = config.get_server()
        self.server.register_remote_method(
            "set_boot_media", self.set_boot_media)

    def set_boot_media(self, boot_media: str) -> None:
        if boot_media in ["usb", "emmc"]:
            logging.info(f"Setting boot media to {boot_media}")
            os.system(f"sudo set-boot-media {boot_media}")
        else:
            logging.error("boot_media not 'usb' or 'emmc'")

def load_component(config):
    return SetBootMedia(config)
