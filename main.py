import datetime
import time
from functools import partial
from threading import Event
from typing import Callable, List

from client_control import ClientControl, CLIENT_MODULE_NAME
from engine_control import EngineControl, ENGINE_MODULE_NAME
from glow_object_manager import GlowObjectManager
from in_game_control import InGameControl
from player import Player
from process import get_process_handle, get_process_id

CSGO_PROCESS_NAME = 'csgo.exe'


def start_wallhack(engine_control: EngineControl,
                   client_control: ClientControl,
                   glow_object_manager: GlowObjectManager,
                   is_in_game_event: Event):
    print(datetime.datetime.now().isoformat(), 'Wallhack enabled')
    local_player = client_control.get_local_player()

    while is_in_game_event.is_set():
        max_players_count = engine_control.get_max_players()
        if not max_players_count:
            break

        local_player.change_pointer_if_needed(
            client_control.get_local_player_pointer()
        )
        local_player.read_all_variables()

        for i in range(max_players_count):
            other_player = client_control.get_player_by_index(i)

            if not other_player.is_alive() or other_player.get_team() == local_player.team:
                continue

            other_player.read_all_variables()
            glow_object_manager.draw_player(other_player.glow_index, other_player.health)

        time.sleep(0.01)
    print(datetime.datetime.now().isoformat(), 'Wallhack disabled')


def main():
    pid = get_process_id(CSGO_PROCESS_NAME)
    if pid is None:
        print(f"Процесс {CSGO_PROCESS_NAME} не найден")
        return

    with get_process_handle(pid) as process_handle:
        client_control = ClientControl(process_handle.handle)
        engine_control = EngineControl(process_handle.handle)

        glow_object_manager = GlowObjectManager(client_control.address, process_handle.handle)

        print(
            f"{CSGO_PROCESS_NAME} pid: {pid}\n"
            f"handle: {process_handle.handle}\n"
            f"engine_address ({ENGINE_MODULE_NAME}): {engine_control.client_state_pointer}\n"
            f"client_address ({CLIENT_MODULE_NAME}): {client_control.address}\n"
            f"client_state: {engine_control.client_state_pointer}"
        )
        start_wallhack_callback: Callable[[Event], None] = partial(start_wallhack,
                                                                   engine_control,
                                                                   client_control,
                                                                   glow_object_manager)
        in_game_control = InGameControl(engine_control, start_wallhack_callback)
        in_game_control.start()

        while True:
            time.sleep(10)


if __name__ == "__main__":
    main()
