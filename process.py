from contextlib import contextmanager
from ctypes import create_string_buffer, sizeof, c_char, c_buffer, byref, windll
from typing import Any, Callable, Generator, TypeVar, Type

import psutil
import pymem

T = TypeVar('T')

ReadProcessMemory: Callable[[int, int, Any, int], bool] = windll.kernel32.ReadProcessMemory
WriteProcessMemory: Callable[[int, int, Any, int], bool] = windll.kernel32.WriteProcessMemory


def _rpm(process_handle: int, address: int, size: int) -> c_buffer:
    buffer = create_string_buffer(size)
    buffer_size = sizeof(buffer)
    bytes_read = c_char(0)
    ReadProcessMemory(process_handle, address, buffer, buffer_size, byref(bytes_read))
    return buffer


def wpm(process_handle: int, address: int, c_data: bytes):
    bytes_write = c_char(0)
    WriteProcessMemory(process_handle, address, c_data, len(c_data), byref(bytes_write))


def rpm(process_handle: int, address: int, c_type: Type[T]) -> T:
    return c_type.from_buffer(_rpm(process_handle, address, sizeof(c_type)))


def get_process_id(process_name: str) -> int:
    for process in psutil.process_iter():
        if process.name() == process_name:
            return process.pid


@contextmanager
def get_process_handle(pid: int) -> Generator[pymem.Pymem, None, None]:
    pm = pymem.Pymem()
    pm.open_process_from_id(pid)
    try:
        yield pm
    finally:
        pm.close_process()


def get_module_address(process_handle: int, module_name: str) -> int:
    return pymem.process.module_from_name(process_handle, module_name).lpBaseOfDll
