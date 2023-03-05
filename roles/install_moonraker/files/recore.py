# Machine manipulation request handlers
#
# Copyright (C) 2020 Eric Callahan <arksine.code@gmail.com>
# Copyright (C) 2022 Elias Bakken <elias@iagent.no>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

from __future__ import annotations
import logging
import asyncio

# Annotation imports
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional
)

if TYPE_CHECKING:
    from confighelper import ConfigHelper
    from websockets import WebRequest
    from .shell_command import ShellCommandFactory as SCMDComp

class Recore:
    def __init__(self, config: ConfigHelper) -> None:
        self.server = config.get_server()

        self.server.register_endpoint(
            "/recore/enable_ssh", ['POST'], self._handle_enable_ssh_request)
        self.server.register_endpoint(
            "/recore/set_boot_media", ['POST'], self._handle_boot_media_request)
        self.server.register_endpoint(
            "/recore/state", ['GET'], self._handle_recore_state_request)

        shell_cmd: SCMDComp = self.server.load_component(
            config, 'shell_command')
        get_boot_media_bin = "/usr/local/bin/get-boot-media"
        self.get_boot_media_cmd = shell_cmd.build_shell_command(
            get_boot_media_bin)
        is_ssh_enabled_bin = "/usr/local/bin/is-ssh-enabled"
        self.is_ssh_enabled_cmd = shell_cmd.build_shell_command(
            is_ssh_enabled_bin)
        self.init_evt = asyncio.Event()

    async def wait_for_init(
        self, timeout: Optional[float] = None
    ) -> None:
        try:
            await asyncio.wait_for(self.init_evt.wait(), timeout)
        except asyncio.TimeoutError:
            pass

    async def component_init(self) -> None:
        self.init_evt.set()

    async def _exec_sudo_command(self, command: str):
        machine: Machine = self.server.lookup_component("machine")
        return await machine.exec_sudo_command(command, timeout=5)

    async def _handle_enable_ssh_request(self, web_request: WebRequest) -> str:
        enabled = web_request.get("value")
        await self._exec_sudo_command(
            f"/usr/local/bin/set-ssh-access {enabled}")
        return "ok"

    async def _handle_boot_media_request(self, web_request: WebRequest) -> str:
        media = web_request.get("value")
        await self._exec_sudo_command(f"/usr/local/bin/set-boot-media {media}")
        return "ok"

    async def _handle_recore_state_request(self, web_request: WebRequest
                                           ) -> Dict[str, Any]:
        boot_media = await self._get_boot_media()
        ssh_enabled = await self._get_ssh_enabled()
        recore_state = {
            "ssh_enabled": ssh_enabled,
            "boot_media": boot_media
        }
        return {"recore_state": recore_state}

    async def _get_boot_media(self) -> str:
        shell_cmd: SCMDComp = self.server.lookup_component('shell_command')
        try:
            resp = await self.get_boot_media_cmd.run_with_response(
                log_complete=False)
        except shell_cmd.error:
            return "Error: setting boot media failed"
        if resp:
            return resp.strip()
        return "unknown"

    async def _get_ssh_enabled(self) -> str:
        shell_cmd: SCMDComp = self.server.lookup_component('shell_command')
        try:
            resp = await self.is_ssh_enabled_cmd.run_with_response(
                log_complete=False)
        except shell_cmd.error:
            return "Error: setting SSH access failed"
        if resp:
            return resp.strip()
        return "unknown"

def load_component(config: ConfigHelper) -> Recore:
    return Recore(config)
