from ctypes.wintypes import DWORD
from typing import Any, Optional

from _ctypes import sizeof

import offsets
from custom_types import GlowObjectDefinition
from process import rpm, wpm


class GlowObjectManager:
    def __init__(self, client_address: int, handle: int):
        self._handle = handle

        self._pointer: int = rpm(handle, client_address + offsets.dwGlowObjectManager, DWORD).value

    def _rpm(self, offset: int, c_type) -> Any:
        return rpm(self._handle, self._pointer + offset, c_type)

    def _wpm(self, offset: int, data: bytes):
        return wpm(self._handle, self._pointer + offset, data)

    def draw_player(self, glow_index: int, health: Optional[int] = 0):
        glow_offset = glow_index * sizeof(GlowObjectDefinition)
        glow_object_definition = self._rpm(glow_offset, GlowObjectDefinition)
        if health == 100:
            glow_object_definition.r = 17
            glow_object_definition.g = 0
            glow_object_definition.b = 255
            glow_object_definition.a = 1
        elif health >= 50:
            glow_object_definition.r = 72
            glow_object_definition.g = 255
            glow_object_definition.b = 0
            glow_object_definition.a = 1
        else:
            glow_object_definition.r = 255
            glow_object_definition.g = 0
            glow_object_definition.b = 0
            glow_object_definition.a = 1

        glow_object_definition.m_bRenderWhenOccluded = 1
        glow_object_definition.m_bRenderWhenUnoccluded = 0

        self._wpm(glow_offset, bytes(glow_object_definition))


