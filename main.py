import time
from functools import partial
from threading import Event
from typing import Callable

from client_control import ClientControl, CLIENT_MODULE_NAME
from engine_control import EngineControl, ENGINE_MODULE_NAME
from glow_object_manager import GlowObjectManager
from in_game_control import InGameControl
from players_cache import PlayersCache
from process import get_process_handle, get_process_id
from wallhack import start_wallhack_thread

CSGO_PROCESS_NAME = 'csgo.exe'


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

        players_cache = PlayersCache(client_control,
                                     engine_control)
        start_wallhack_callback: Callable[[Event], None] = partial(start_wallhack_thread,
                                                                   players_cache,
                                                                   glow_object_manager)
        in_game_control = InGameControl(engine_control,
                                        start_game_callback=[
                                            players_cache.read_all_players,
                                            start_wallhack_callback,
                                        ],
                                        stop_game_callback=[
                                            players_cache.clear,
                                        ])
        in_game_control.start()

        while True:
            time.sleep(10)


if __name__ == "__main__":
    main()
