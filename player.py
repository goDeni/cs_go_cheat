from typing import Optional, Any

from pymem import Pymem
from pymem.exception import MemoryReadError

import offsets
from custom_types import Vector
from process import rpm


class Player:
    def __init__(self, process: Pymem, player_pointer: int):
        self._process = process
        self._player_pointer = player_pointer

        self._team: Optional[int] = None
        self._health: Optional[int] = None
        self._alive: Optional[bool] = None
        self._vector: Optional[Vector] = None
        self._head_vector: Optional[Vector] = None
        self._target_id: Optional[int] = None
        self._glow_index: Optional[int] = None

    def _read_int(self, address: int) -> int:
        try:
            return self._process.read_int(self._player_pointer + address)
        except MemoryReadError:
            return 0

    def read_all_variables(self):
        self._team = self.get_team()
        self._health = self.get_health()
        self._alive = self.is_alive(self._health)
        self._vector = self.get_vector()
        self._head_vector = self.get_head_vector(self._vector)
        self._target_id = self.get_target_id()
        self._glow_index = self.get_glow_index()

    def change_pointer_if_needed(self, pointer: int):
        if self._player_pointer != pointer:
            self._player_pointer = pointer

    @property
    def team(self) -> int:
        return self._team

    @property
    def health(self) -> int:
        return self._health

    @property
    def alive(self) -> bool:
        return self._alive

    @property
    def vector(self) -> Vector:
        return self._vector

    @property
    def head_vector(self) -> Vector:
        return self._head_vector

    @property
    def target_id(self) -> int:
        return self._target_id

    @property
    def glow_index(self) -> int:
        return self._glow_index

    def _rpm(self, offset: int, c_type) -> Any:
        return rpm(self._process.process_handle, self._player_pointer + offset, c_type)

    def get_target_id(self) -> int:
        return self._read_int(offsets.m_iCrosshairId)

    def get_team(self) -> int:
        return self._read_int(offsets.m_iTeamNum)

    def get_health(self) -> int:
        return self._read_int(offsets.m_iHealth)

    def is_alive(self, health: Optional[int] = None) -> bool:
        if health is None:
            health = self.get_health()
        return 0 < health <= 100

    def get_glow_index(self) -> int:
        return self._read_int(offsets.m_iGlowIndex)

    def get_vector(self) -> Vector:
        return self._rpm(offsets.m_vecOrigin, Vector)

    def get_head_vector(self, vector: Optional[Vector] = None) -> Vector:
        if vector is None:
            vector = self.get_vector()
        return Vector(vector.x, vector.y, vector.z + 75)

    def get_life_state(self) -> int:
        return self._read_int(offsets.m_lifeState)
