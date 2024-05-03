"""
Copyright 2024 Olivier Stuker a.k.a. BinaryBorn
"""

# these are used as primitive data types, hence the lower case naming

# math primitives (vectors, matrices) are always suffixed with their size

class vec4:
  """vector (x, y, z, w)
  """
  __slots__ = ['x', 'y', 'z', 'w']

  def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0):
    self.x = x
    self.y = y
    self.z = z
    self.w = w

class mat4:
  """maxtrix 4x4
  """
  __slots__ = ['a11', 'a12', 'a13', 'a14', 'a21', 'a22', 'a23', 'a24', 'a31', 'a32', 'a33', 'a34', 'a41', 'a42', 'a43', 'a44']

  def __init__(self,
      a11: float = 0.0, a12: float = 0.0, a13: float = 0.0, a14: float = 0.0,
      a21: float = 0.0, a22: float = 0.0, a23: float = 0.0, a24: float = 0.0,
      a31: float = 0.0, a32: float = 0.0, a33: float = 0.0, a34: float = 0.0,
      a41: float = 0.0, a42: float = 0.0, a43: float = 0.0, a44: float = 0.0):
    self.a11 = a11
    self.a12 = a12
    self.a13 = a13
    self.a14 = a14
    self.a21 = a21
    self.a22 = a22
    self.a23 = a23
    self.a24 = a24
    self.a31 = a31
    self.a32 = a32
    self.a33 = a33
    self.a34 = a34
    self.a41 = a41
    self.a42 = a42
    self.a43 = a43
    self.a44 = a44

class box:
  """Class for 2D boxes
  """
  __slots__ = ['x0', 'y0', 'x1', 'y1']

  def __init__(self, x0: float, y0: float, x1: float, y1: float):
    self.x0 = x0
    self.y0 = y0
    self.x1 = x1
    self.y1 = y1

type figure = list[list[vec4]]
"Type alias for a list of list of points (each interpreted as polygon)"

class phenotype:
  """Class representing the property vector for all the note properties.
  """
  __slots__ = ['vel', 'pan', 'rel', 'pof', 'cut', 'res', 'col']

  def __init__(self, vel=100/128, pan=0.5, rel=0.5, pof=0, cut=128/255, res=128/255, col=0):
    self.vel = vel
    "velocity, also treated as opacity, 0.0 to 1.0, default 0.78"
    self.pan = pan
    "panning, 0.0 to 1.0, default 0.5"
    self.rel = rel
    "release, 0.0 to 1.0, default 0.5"
    self.pof = pof
    "pitch offset, -120 to 120, default 0"
    self.cut = cut
    "fcut/modx, 0.0 to 1.0, default 0.5"
    self.res = res
    "fres/mody, 0.0 to 1.0, default 0.5"
    self.col = col
    "note color/MIDI channel, 0 to 15, default 0"

type tri = tuple[int, int, int]

class mesh:
  __slots__ = ['verts', 'normals', 'phenos', 'tris']

  def __init__(self, verts: list[vec4], phenos: list[phenotype], tris: list[tri]):
    self.verts = verts
    self.normals = [vec4()] * len(verts)
    self.phenos = phenos
    self.tris = tris