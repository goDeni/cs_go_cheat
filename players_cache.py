import time
from datetime import datetime
from threading import Lock, Event, Thread
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
        self._max_players_count = 0

    @property
    def max_players_count(self) -> int:
        return self._max_players_count

    def get_local_player(self,
                         read_variables: bool = False,
                         change_pointer_if_needed: bool = False) -> Player:
        p = self._local_player
        if change_pointer_if_needed:
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

    def get_player_by_index(self, i: int,
                            read_variables: bool = False,
                            change_pointer_if_needed: bool = False) -> Player:
        self.create_player_if_doesnt_exist(i)
        p = self._players[i]
        if change_pointer_if_needed:
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
        for i in range(self._max_players_count):
            yield self.get_player_by_index(i)

    def read_all_players(self, *args):
        self._max_players_count = self._engine_control.get_max_players()
        self.get_local_player(read_variables=True,
                              change_pointer_if_needed=True)
        for i in range(self._max_players_count):
            self.get_player_by_index(i,
                                     read_variables=True,
                                     change_pointer_if_needed=True)

    def follow_players(self, is_in_game: Event):
        print(datetime.now().isoformat(), "Players following started")
        while is_in_game.is_set():
            self._max_players_count = self._engine_control.get_max_players()
            self.get_local_player(read_variables=True,
                                  change_pointer_if_needed=True)
            for i in range(self._max_players_count):
                self.get_player_by_index(i,
                                         read_variables=True,
                                         change_pointer_if_needed=True)
            time.sleep(0.01)
        print(datetime.now().isoformat(), "Players following stopped")


def start_players_follow_thread(players_cache: PlayersCache, is_in_game: Event):
    Thread(target=players_cache.follow_players,
           name='follow players thread',
           args=(is_in_game,)).start()
