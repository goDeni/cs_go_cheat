from ctypes.wintypes import DWORD, BOOLEAN
from typing import Any

import offsets
from player import Player
from process import get_module_address, rpm, wpm

CLIENT_MODULE_NAME = "client_panorama.dll"


class ClientControl:
    def __init__(self, handle: int):
        self._handle = handle

        self._base_address = get_module_address(handle, CLIENT_MODULE_NAME)

    @property
    def address(self) -> int:
        return self._base_address

    def _rpm(self, offset: int, c_type) -> Any:
        return rpm(self._handle, self._base_address + offset, c_type)

    def _wpm(self, offset: int, data: bytes) -> bool:
        return wpm(self._handle, self._base_address + offset, data)

    def get_local_player_pointer(self) -> int:
        return self._rpm(offsets.dwLocalPlayer, DWORD).value

    def get_player_pointer(self, index: int) -> int:
        return self._rpm(offsets.dwEntityList + (index * 0x10), DWORD).value

    def get_local_player(self) -> Player:
        local_player_pointer = self.get_local_player_pointer()
        return Player(self._handle, local_player_pointer)

    def get_player_by_index(self, index: int):
        player_pointer = self.get_player_pointer(index)
        return Player(self._handle, player_pointer)

    def set_shoot_state(self, state: bool) -> bool:
        return self._wpm(offsets.dwForceAttack, int.to_bytes(int(state), 1, 'big'))
