from threading import Lock
from typing import Generator, Dict

from client_control import ClientControl
from engine_control import EngineControl
from player import Player


class PlayersCache:
    def __init__(self,
                 client_control: ClientControl,
                 engine_control: EngineControl):
        self._client_control = client_control
        self._engine_control = engine_control

        self._local_player = client_control.get_local_player()
        self._players: Dict[int, Player] = {}
        self._create_player_lock = Lock()

    def get_local_player(self, read_variables: bool = False) -> Player:
        p = self._local_player
        p.change_pointer_if_needed(
            self._client_control.get_local_player_pointer()
        )
        if read_variables:
            p.read_all_variables()
        return p

    def create_player_if_doesnt_exist(self, index: int):
        if index in self._players:
            return
        with self._create_player_lock:
            # Во время лока возможно кто то уже создал нужного нам пользователя
            # По этому тут проверка
            if index not in self._players:
                self._players[index] = self._client_control.get_player_by_index(index)

    def get_player_by_index(self, i: int, read_variables: bool = False) -> Player:
        self.create_player_if_doesnt_exist(i)
        p = self._players[i]
        p.change_pointer_if_needed(
            self._client_control.get_player_pointer(i)
        )
        if read_variables:
            p.read_all_variables()
        return p

    def clear(self):
        self._players.clear()
        print("Players cache clear")

    @property
    def players(self) -> Generator[Player, None, None]:
        max_players_count = self._engine_control.get_max_players()
        for i in range(max_players_count):
            yield self.get_player_by_index(i, read_variables=True)

    def read_all_players(self, *args):
        for _ in self.players:
            continue
        print(f"{len(self._players)} игроков было прочитано")
