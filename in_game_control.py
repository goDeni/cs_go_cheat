import time
from threading import Thread, Event
from typing import Optional, Callable

from engine_control import EngineControl


class InGameControl(Thread):
    def __init__(self,
                 engine_control: EngineControl,
                 start_game_callback: Callable[[Event], None] = lambda *args: None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._engine_control = engine_control
        self._thread_stop_event = Event()
        self._start_game_callback = start_game_callback

        self._is_in_game = Event()

    def run(self) -> None:
        while not self._thread_stop_event.is_set():
            if self._is_in_game.is_set() and not self._engine_control.is_ingame():
                self._is_in_game.clear()
            elif not self._is_in_game.is_set() and self._engine_control.is_ingame():
                self._is_in_game.set()
                self._start_game_callback(self._is_in_game)
            time.sleep(1)

    def join(self, timeout: Optional[float] = 0) -> None:
        self._thread_stop_event.set()
        super().join(timeout)
