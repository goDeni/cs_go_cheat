from contextlib import contextmanager
from ctypes import *
from ctypes.wintypes import *
from time import sleep
from typing import Callable, Any

import psutil as psutil
import win32api
import win32con
import win32gui
import win32process

CSGO_PROCESS_NAME = 'csgo.exe'
MODULE_NAME = "client_panorama.dll"
ReadProcessMemory: Callable[[int, int, Any, int], bool] = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle

screenX = 1920
screenY = 1080

BRUSH = win32gui.CreateSolidBrush(255)

m_iHealth = 0x100
dwEntityList = 0x4D43AB4
dwViewMatrix = 0x4D353F4
m_iTeamNum = 0xF4
m_vecOrigin = 0x138
m_lifeState = 0x25F
dwLocalPlayer = 0xD2FB84
m_Collision = 0x320


def get_process_id(process_name: str) -> int:
    for process in psutil.process_iter():
        if process.name() == process_name:
            return process.pid


def get_module_address(process_handle: int, module_name: str) -> int:
    modules = win32process.EnumProcessModulesEx(process_handle, win32process.LIST_MODULES_ALL)
    for module in modules:
        m = win32process.GetModuleFileNameEx(process_handle, module)
        if m.endswith(module_name):
            return module


def _rpm(process_handle: int, address: int, size: int) -> c_buffer:
    buffer = create_string_buffer(size)
    buffer_size = sizeof(buffer)
    bytes_read = c_char(0)
    ReadProcessMemory(process_handle, address, buffer, buffer_size, byref(bytes_read))
    return buffer


def rpm(process_handle: int, address: int, c_type) -> Any:
    return c_type.from_buffer(_rpm(process_handle, address, sizeof(c_type)))


class Vector(Structure):
    _fields_ = [
        ("x", FLOAT),
        ("y", FLOAT),
        ("z", FLOAT),
    ]

    def __str__(self):
        return f"x: {self.x} y: {self.y} z: {self.z}"


@contextmanager
def get_process_handle(pid: int):
    try:
        process_handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
        yield process_handle
    finally:
        process_handle.close()


def draw_line(dc: int, start_x: int, start_y: int, end_x: int, end_y: int):
    # print(start_x, start_y, end_x, end_y)
    hpen = win32gui.CreatePen(win32con.PS_SOLID, 4, 255)
    hopen = win32gui.SelectObject(dc, hpen)
    win32gui.MoveToEx(dc, start_x, start_y)
    win32gui.LineTo(dc, end_x, end_y)
    win32gui.DeleteObject(win32gui.SelectObject(dc, hopen))


def world_to_screen(pos, matrix) -> Vector:
    _x = matrix[0][0] * pos.x + matrix[0][1] * pos.y + matrix[0][2] * pos.z + matrix[0][3]
    _y = matrix[1][0] * pos.x + matrix[1][1] * pos.y + matrix[1][2] * pos.z + matrix[1][3]

    w = matrix[3][0] * pos.x + matrix[3][1] * pos.y + matrix[3][2] * pos.z + matrix[3][3]
    inv_w = 1. / w
    _x *= inv_w
    _y *= inv_w
    x = screenX * 0.5
    y = screenY * 0.5

    x += 0.5 * _x * screenX + 0.5
    y -= 0.5 * _y * screenY + 0.5
    return Vector(x, y, w)


def draw_filled_rect(dc, x: int, y: int, w: int, h: int):
    win32gui.FillRect(dc, (x, y, x + w, y + h), BRUSH)


def draw_text(dc, text: str, x, y):
    win32gui.DrawText(dc, text, len(text), (x, y, x + 30, y + 100), win32con.DT_LEFT)


def draw_border_box(dc, x: int, y: int, w: int, h: int, thickness: int):
    draw_filled_rect(dc, x, y, w, thickness)
    draw_filled_rect(dc, x, y, thickness, h)
    draw_filled_rect(dc, x + w, y, thickness, h)
    draw_filled_rect(dc, x, y + h, w + thickness, thickness)


Int4x4Array = c_float * 4 * 4


class Player:
    def __init__(self, handle: int, base_address: int):
        self._handle = handle
        self._base_address = base_address

    def _rpm(self, offset: int, c_type) -> Any:
        return rpm(self._handle, self._base_address + offset, c_type)

    def get_team(self) -> int:
        return self._rpm(m_iTeamNum, INT).value

    def get_health(self) -> int:
        return self._rpm(m_iHealth, INT).value

    def get_vector(self) -> Vector:
        return self._rpm(m_vecOrigin, Vector)


def main():
    pid = get_process_id(CSGO_PROCESS_NAME)
    if pid is None:
        print(f"Процесс {CSGO_PROCESS_NAME} не найден")
        return
    dc = win32gui.GetDC(
        win32gui.FindWindow(None, "Counter-Strike: Global Offensive")
    )

    with get_process_handle(pid) as process_handle:
        base_address = get_module_address(process_handle, MODULE_NAME)

        while True:
            view_matrix = Int4x4Array.from_buffer(_rpm(process_handle.handle, base_address + dwViewMatrix, 64))

            local_player = Player(
                process_handle.handle,
                rpm(process_handle.handle, base_address + dwLocalPlayer, DWORD).value
            )
            local_team = local_player.get_team()
            for i in range(64):
                # break
                player_pointer = DWORD.from_buffer(
                    _rpm(process_handle.handle, base_address + dwEntityList + (i * 0x10), 4))
                other_player = Player(process_handle.handle, player_pointer.value)
                o_health = other_player.get_health()
                if o_health <= 0 or o_health > 100 or other_player.get_team() == local_team:
                    continue
                pos = other_player.get_vector()
                head = Vector(pos.x, pos.y, pos.z + 75)

                screenpos = world_to_screen(pos, view_matrix)
                screenhead = world_to_screen(head, view_matrix)

                height = screenhead.y - screenpos.y
                width = height / 2.4

                if screenpos.z >= 0.01:
                    draw_text(dc, str(other_player.get_health()), int(screenpos.x - width / 2), int(screenpos.y))
                    draw_border_box(dc, int(screenpos.x - width / 2), int(screenpos.y), int(width), int(height), 2)
                    draw_line(dc, int(screenX / 2), int(screenY), int(screenpos.x), int(screenpos.y))
            sleep(0.01)


if __name__ == "__main__":
    main()
