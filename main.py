import time
from ctypes.wintypes import *
from typing import Tuple

import win32gui

import offsets
from engine_control import EngineControl, ENGINE_MODULE_NAME
from glow_object_manager import GlowObjectManager
from player import Player
from process import rpm, get_process_handle, get_process_id, get_module_address
from trigger_bot import TriggerBot

CSGO_PROCESS_NAME = 'csgo.exe'
CLIENT_MODULE_NAME = "client_panorama.dll"


def get_window_size(hwnd: int) -> Tuple[int, int]:
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    return w, h


def main():
    pid = get_process_id(CSGO_PROCESS_NAME)
    if pid is None:
        print(f"Процесс {CSGO_PROCESS_NAME} не найден")
        return

    with get_process_handle(pid) as process_handle:
        client_address = get_module_address(process_handle, CLIENT_MODULE_NAME)
        engine_control = EngineControl(process_handle.handle)

        glow_object_manager = GlowObjectManager(client_address, process_handle.handle)

        print(
            f"{CSGO_PROCESS_NAME} pid: {pid}\n"
            f"handle: {process_handle.handle}\n"
            f"engine_address ({ENGINE_MODULE_NAME}): {engine_control.client_state_pointer}\n"
            f"client_address ({CLIENT_MODULE_NAME}): {client_address}\n"
            f"client_state: {engine_control.client_state_pointer}"
        )

        local_player = Player(process_handle.handle, 0)
        trigger_bot = TriggerBot(local_player, process_handle.handle, client_address)
        # trigger_bot.enable()
        while True:
            max_players_count = engine_control.get_max_players()

            local_player_pointer = rpm(process_handle.handle, client_address + offsets.dwLocalPlayer, DWORD)
            local_player.change_pointer_if_needed(local_player_pointer)
            local_player.read_all_variables()

            for i in range(max_players_count):
                player_pointer = rpm(process_handle.handle, client_address + offsets.dwEntityList + (i * 0x10), DWORD)
                other_player = Player(process_handle.handle, player_pointer.value)
                if not other_player.is_alive() or other_player.get_team() == local_player.team:
                    continue

                trigger_bot.shoot_if_needed(i)
                other_player.read_all_variables()
                glow_object_manager.draw_player(other_player.glow_index, other_player.health)

            trigger_bot.clear_shoot_state()
            time.sleep(0.01)


if __name__ == "__main__":
    main()
