from custom_types import Int4x4Array, Vector


class WorldView:
    def __init__(self, view_matrix: Int4x4Array, screen_width: int, screen_height: int):
        self._view_matrix = view_matrix
        self._screen_width = screen_width
        self._screen_height = screen_height

    def to_screen(self, pos: Vector) -> Vector:
        _x = self._view_matrix[0][0] * pos.x + self._view_matrix[0][1] * pos.y + \
             self._view_matrix[0][2] * pos.z + self._view_matrix[0][3]

        _y = self._view_matrix[1][0] * pos.x + self._view_matrix[1][1] * pos.y + \
             self._view_matrix[1][2] * pos.z + self._view_matrix[1][3]

        w = self._view_matrix[3][0] * pos.x + self._view_matrix[3][1] * pos.y \
            + self._view_matrix[3][2] * pos.z + self._view_matrix[3][3]

        inv_w = 1. / w
        _x *= inv_w
        _y *= inv_w
        x = self._screen_width * 0.5
        y = self._screen_height * 0.5

        x += 0.5 * _x * self._screen_width + 0.5
        y -= 0.5 * _y * self._screen_height + 0.5
        return Vector(x, y, w)
