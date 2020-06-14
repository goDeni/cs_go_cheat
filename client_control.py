from functools import partial
from typing import Any, Callable

from pymem import Pymem

import offsets
from player import Player
from process import get_module_address, wpm

CLIENT_MODULE_NAME = "client.dll"


class ClientControl:
    def __init__(self, process: Pymem):
        self._process = process

        self._base_address = get_module_address(process.process_handle, CLIENT_MODULE_NAME)

        self._read_int: Callable[[Any], int] = partial(
            lambda *args: self._process.read_int(sum(args)),
            self._base_address
        )

    @property
    def address(self) -> int:
        return self._base_address

    def _wpm(self, offset: int, data: bytes) -> bool:
        return wpm(self._process.process_handle, self._base_address + offset, data)

    def get_local_player_pointer(self) -> int:
        return self._read_int(offsets.dwLocalPlayer)

    def get_player_pointer(self, index: int) -> int:
        return self._read_int(offsets.dwEntityList + (index * 0x10))

    def get_local_player(self) -> Player:
        local_player_pointer = self.get_local_player_pointer()
        return Player(self._process, local_player_pointer)

    def get_player_by_index(self, index: int):
        player_pointer = self.get_player_pointer(index)
        return Player(self._process, player_pointer)

    def set_shoot_state(self, state: bool) -> bool:
        return self._wpm(offsets.dwForceAttack, int.to_bytes(int(state), 1, 'big'))
