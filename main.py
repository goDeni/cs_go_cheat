import time
from ctypes.wintypes import *
from typing import Tuple

import win32gui
import win32process

import offsets
from custom_types import Int4x4Array
from player import Player
from player_drawer import PlayerDrawer
from process import rpm, get_process_handle, get_process_id, wpm
from trigger_bot import TriggerBot

CSGO_PROCESS_NAME = 'csgo.exe'
CLIENT_MODULE_NAME = "client_panorama.dll"
ENGINE_MODULE_NAME = "engine.dll"


def get_module_address(process_handle: int, module_name: str) -> int:
    modules = win32process.EnumProcessModulesEx(process_handle, win32process.LIST_MODULES_ALL)
    for module in modules:
        m = win32process.GetModuleFileNameEx(process_handle, module)
        if m.endswith(module_name):
            return module


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
    hwnd = win32gui.FindWindow(None, "Counter-Strike: Global Offensive")
    screen_x, screen_y = 1920, 1080

    dc = win32gui.GetDC(hwnd)

    with get_process_handle(pid) as process_handle:
        client_address = get_module_address(process_handle, CLIENT_MODULE_NAME)
        engine_address = get_module_address(process_handle, ENGINE_MODULE_NAME)

        client_state_pointer: DWORD = rpm(process_handle.handle, engine_address + offsets.dwClientState, DWORD)

        print(
            f"{CSGO_PROCESS_NAME} pid: {pid}\n"
            f"handle: {process_handle.handle}\n"
            f"engine_address ({ENGINE_MODULE_NAME}): {engine_address}\n"
            f"client_address ({CLIENT_MODULE_NAME}): {client_address}\n"
            f"client_state: {client_state_pointer.value}"
        )

        local_player = Player(process_handle.handle, 0)
        trigger_bot = TriggerBot(local_player, process_handle.handle, client_address)
        # trigger_bot.enable()
        while True:
            max_players: INT = rpm(process_handle.handle, client_state_pointer.value + offsets.dwClientState_MaxPlayer, INT)

            view_matrix = rpm(process_handle.handle, client_address + offsets.dwViewMatrix, Int4x4Array)
            local_player_pointer = rpm(process_handle.handle, client_address + offsets.dwLocalPlayer, DWORD)
            local_player.change_pointer_if_needed(local_player_pointer)
            local_player.read_all_variables()

            for i in range(max_players.value):
                player_pointer = rpm(process_handle.handle, client_address + offsets.dwEntityList + (i * 0x10), DWORD)
                other_player = Player(process_handle.handle, player_pointer.value)
                if not other_player.is_alive() or other_player.get_team() == local_player.team:
                    continue
                p_drawer = PlayerDrawer(other_player, view_matrix, dc, screen_x, screen_y)

                trigger_bot.shoot_if_needed(i)

                other_player.read_all_variables()
                p_drawer.calc_position()

                if p_drawer.screen_position.z >= 0.01:
                    p_drawer.draw_border_box()
                    p_drawer.draw_health()
                    p_drawer.draw_line_to_player()

            trigger_bot.clear_shoot_state()
            time.sleep(0.01)


if __name__ == "__main__":
    main()
