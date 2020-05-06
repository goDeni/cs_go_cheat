from ctypes.wintypes import DWORD, INT
from typing import Any

import offsets
from process import rpm, get_module_address

ENGINE_MODULE_NAME = "engine.dll"


class EngineControl:
    def __init__(self, handle: int):
        self._base_addr = get_module_address(handle, ENGINE_MODULE_NAME)
        self._handle = handle

        self._client_state_pointer: DWORD = rpm(handle, self._base_addr + offsets.dwClientState, DWORD)

    @property
    def client_state_pointer(self) -> int:
        return self._client_state_pointer.value

    def _rpm(self, offset: int, c_type) -> Any:
        return rpm(self._handle, self.client_state_pointer + offset, c_type)

    def is_ingame(self) -> bool:
        return self._rpm(offsets.dwClientState_State, INT).value == 6

    def get_max_players(self) -> int:
        return self._rpm(offsets.dwClientState_MaxPlayer, INT).value
