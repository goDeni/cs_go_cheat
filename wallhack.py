import datetime
import time
from threading import Event, Thread

from glow_object_manager import GlowObjectManager
from players_cache import PlayersCache


def _start_wallhack(players_cache: PlayersCache,
                    glow_object_manager: GlowObjectManager,
                    is_in_game_event: Event):
    print(datetime.datetime.now().isoformat(), 'Wallhack enabled')

    while is_in_game_event.is_set():
        local_player = players_cache.get_local_player(read_variables=True)

        for player in players_cache.players:
            if not player.alive or player.team == local_player.team:
                continue
            glow_object_manager.draw_player(player.glow_index, player.health)

        time.sleep(0.01)
    print(datetime.datetime.now().isoformat(), 'Wallhack disabled')


def start_wallhack_thread(players_cache: PlayersCache,
                          glow_object_manager: GlowObjectManager,
                          is_in_game_event: Event):
    Thread(target=_start_wallhack,
           name='cs_go_wallhack',
           args=(players_cache, glow_object_manager, is_in_game_event)).start()
