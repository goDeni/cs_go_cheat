import time
from threading import Thread, Event
from typing import Optional, Callable, Union, List

from engine_control import EngineControl
from sound_utils import play_signal


class InGameControl(Thread):
    def __init__(self,
                 engine_control: EngineControl,
                 start_game_callback: Union[Callable[[Event], None], List[Callable[[Event], None]]] = lambda *args: None,
                 stop_game_callback: Union[Callable[[Event], None], List[Callable[[Event], None]]] = lambda *args: None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._engine_control = engine_control
        self._thread_stop_event = Event()
        if not isinstance(start_game_callback, list):
            self._start_game_callbacks = [start_game_callback]
        else:
            self._start_game_callbacks = start_game_callback

        if not isinstance(stop_game_callback, list):
            self._stop_game_callbacks = [stop_game_callback]
        else:
            self._stop_game_callbacks = stop_game_callback

        self._is_in_game = Event()

    def run(self) -> None:
        while not self._thread_stop_event.is_set():
            if self._is_in_game.is_set() and not self._engine_control.is_ingame():
                self._is_in_game.clear()
                for callback in self._stop_game_callbacks:
                    callback()

                play_signal(0.2, 400)
            elif not self._is_in_game.is_set() and self._engine_control.is_ingame():
                self._is_in_game.set()
                for callback in self._start_game_callbacks:
                    callback(self._is_in_game)

                play_signal(0.2, 550)
            time.sleep(1)

    def join(self, timeout: Optional[float] = 0) -> None:
        self._thread_stop_event.set()
        self._is_in_game.clear()

        for th in self._threads:
            th.join(5)
        super().join(timeout)
