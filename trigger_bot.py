import time
from datetime import datetime
from threading import Event, Thread

import offsets
from client_control import ClientControl
from players_cache import PlayersCache
from process import wpm


def set_shoot_state(handle: int, base_address: int, state: bool):
    wpm(handle, base_address + offsets.dwForceAttack, int.to_bytes(int(state), 1, 'big'))


def start_trigger_bot(client_control: ClientControl,
                      players_cache: PlayersCache,
                      is_in_game: Event):
    def shoot():
        client_control.set_shoot_state(True)
        time.sleep(0.1)
        client_control.set_shoot_state(False)

    print(datetime.now().isoformat(), "Trigger bot enabled")

    while is_in_game.is_set():
        local_player = players_cache.get_local_player()
        if 0 < local_player.target_id <= players_cache.max_players_count:
            enemy_player = players_cache.get_player_by_index(local_player.target_id)
            if enemy_player.team != local_player.team:
                shoot()
                time.sleep(0.2)
        time.sleep(0.01)
    print(datetime.now().isoformat(), "Trigger bot disabled")


def start_trigger_bot_thread(client_control: ClientControl,
                             players_cache: PlayersCache,
                             is_in_game: Event):
    Thread(target=start_trigger_bot,
           name="trigger bot",
           args=(client_control, players_cache, is_in_game)).start()
