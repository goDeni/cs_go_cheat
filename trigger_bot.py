import offsets
from player import Player
from process import wpm


def set_shoot_state(handle: int, base_address: int, state: bool):
    wpm(handle, base_address + offsets.dwForceAttack, int.to_bytes(int(state), 1, 'big'))


class TriggerBot:
    def __init__(self, player: Player, handle: int, base_address: int):
        self._player = player
        self._handle = handle
        self._base_address = base_address
        self._enabled = False
        self._attack_state = False

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def shoot(self):
        self._attack_state = not self._attack_state
        set_shoot_state(self._handle, self._base_address, self._attack_state)

    def clear_shoot_state(self):
        if self._attack_state:
            self.shoot()

    def shoot_if_needed(self, target_id: int):
        if not self._enabled:
            return
        if self._player.target_id == target_id:
            self.shoot()
