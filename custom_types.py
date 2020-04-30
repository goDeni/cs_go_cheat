from ctypes import c_float, Structure
from ctypes.wintypes import FLOAT

Int4x4Array = c_float * 4 * 4


class Vector(Structure):
    _fields_ = [
        ("x", FLOAT),
        ("y", FLOAT),
        ("z", FLOAT),
    ]

    def __str__(self):
        return f"x: {self.x} y: {self.y} z: {self.z}"
