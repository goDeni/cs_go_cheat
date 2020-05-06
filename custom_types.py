from ctypes import c_float, Structure
from ctypes.wintypes import FLOAT, DWORD, CHAR, BOOLEAN

Int4x4Array = c_float * 4 * 4


class Vector(Structure):
    _fields_ = [
        ("x", FLOAT),
        ("y", FLOAT),
        ("z", FLOAT),
    ]

    def __str__(self):
        return f"x: {self.x} y: {self.y} z: {self.z}"


class GlowObjectDefinition(Structure):
    _fields_ = [
        ('pEntity', DWORD),
        ('r', FLOAT),
        ('g', FLOAT),
        ('b', FLOAT),
        ('a', FLOAT),
        ('unk1', CHAR * 16),
        ('m_bRenderWhenOccluded', BOOLEAN),
        ('m_bRenderWhenUnoccluded', BOOLEAN),
        ('m_bFullBloom', BOOLEAN),
        ('unk2', CHAR * 14),
    ]

    def __repr__(self):
        return f"GlowObjectDefinition(\n" \
               f"pEntity={self.pEntity}\n" \
               f"r={self.r}\n" \
               f"g={self.g}\n" \
               f"b={self.b}\n" \
               f"a={self.a}\n" \
               f"unk1={self.unk1}\n" \
               f"m_bRenderWhenOccluded={self.m_bRenderWhenOccluded}\n" \
               f"m_bRenderWhenUnoccluded={self.m_bRenderWhenUnoccluded}\n" \
               f"m_bFullBloom={self.m_bFullBloom}\n" \
               f"unk2={self.unk2}\n" \
               f")\n"
