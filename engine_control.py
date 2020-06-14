from functools import partial
from typing import Any, Callable

from pymem import Pymem

import offsets
from process import get_module_address

ENGINE_MODULE_NAME = "engine.dll"


class EngineControl:
    def __init__(self, process: Pymem):
        self._base_addr = get_module_address(process.process_handle, ENGINE_MODULE_NAME)
        self._process = process

        self._client_state_pointer = self._process.read_int(self._base_addr + offsets.dwClientState)

        self._read_int: Callable[[Any], int] = partial(
            lambda *args: self._process.read_int(sum(args)),
            self._client_state_pointer
        )

    @property
    def client_state_pointer(self) -> int:
        return self._client_state_pointer

    def is_ingame(self) -> bool:
        return self._read_int(offsets.dwClientState_State) == 6

    def get_max_players(self) -> int:
        return self._read_int(offsets.dwClientState_MaxPlayer)
