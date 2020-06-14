from typing import Optional, TypeVar, Type

from _ctypes import sizeof
from pymem import Pymem

import offsets
from custom_types import GlowObjectDefinition
from process import rpm, wpm

T = TypeVar('T')


class GlowObjectManager:
    def __init__(self, client_address: int, process: Pymem):
        self._process = process

        self._pointer: int = process.read_int(client_address + offsets.dwGlowObjectManager)

    def _rpm(self, offset: int, c_type: Type[T]) -> T:
        return rpm(self._process.process_handle, self._pointer + offset, c_type)

    def _wpm(self, offset: int, data: bytes):
        return wpm(self._process.process_handle, self._pointer + offset, data)

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
