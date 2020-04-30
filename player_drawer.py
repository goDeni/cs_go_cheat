from typing import Optional

from custom_types import Int4x4Array, Vector
from draw_utils import draw_text, draw_line, draw_border_box
from player import Player
from world_view import WorldView


class PlayerDrawer:
    def __init__(self, player: Player, view_matrix: Int4x4Array, dc: int, screen_width: int, screen_height: int):
        self._player = player
        self._dc = dc
        self._world_view = WorldView(view_matrix, screen_width, screen_height)
        self._screen_width = screen_width
        self._screen_height = screen_height

        self._screen_pos: Optional[Vector] = None
        self._screen_head_pos: Optional[Vector] = None
        self._height: Optional[int] = None
        self._width: Optional[int] = None

    @property
    def screen_position(self) -> Vector:
        return self._screen_pos

    def calc_position(self):
        player_pos = self._player.vector
        player_head_pos = self._player.head_vector

        self._screen_pos = self._world_view.to_screen(player_pos)
        self._screen_head_pos = self._world_view.to_screen(player_head_pos)

        self._height = self._screen_head_pos.y - self._screen_pos.y
        self._width = self._height / 2.4

    def draw_border_box(self):
        draw_border_box(
            self._dc,
            int(self._screen_pos.x - self._width / 2),
            int(self._screen_pos.y),
            int(self._width),
            int(self._height),
            2
        )

    def draw_health(self):
        draw_text(
            self._dc,
            str(self._player.health),
            int(self._screen_pos.x - self._width / 2),
            int(self._screen_pos.y),
            30, 100
        )

    def draw_line_to_player(self):
        draw_line(
            self._dc,
            int(self._screen_width / 2),
            int(self._screen_height),
            int(self._screen_pos.x),
            int(self._screen_pos.y),
        )