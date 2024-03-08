# these are used as primitive data types, hence the lower case naming

# math primitives (vectors, matrices) are always suffixed with their size

class vec2:
  """vector (x, y)
  """
  __slots__ = ['x', 'y']

  def __init__(self, x: float = 0.0, y: float = 0.0):
    self.x = x
    self.y = y

# TODO: vec3

class mat3:
  """maxtrix 3x3
  """
  __slots__ = ['a11', 'a12', 'a13', 'a21', 'a22', 'a23', 'a31', 'a32', 'a33']

  def __init__(self,
      a11: float = 0.0, a12: float = 0.0, a13: float = 0.0,
      a21: float = 0.0, a22: float = 0.0, a23: float = 0.0,
      a31: float = 0.0, a32: float = 0.0, a33: float = 0.0):
    self.a11 = a11
    self.a12 = a12
    self.a13 = a13
    self.a21 = a21
    self.a22 = a22
    self.a23 = a23
    self.a31 = a31
    self.a32 = a32
    self.a33 = a33

# TODO: mat4

# geometry primitives (box, figures, meshes etc) are only suffixed when using 3d

class box:
  """Class for 2D boxes
  """
  __slots__ = ['x0', 'y0', 'x1', 'y1']

  def __init__(self, x0: float, y0: float, x1: float, y1: float):
    self.x0 = x0
    self.y0 = y0
    self.x1 = x1
    self.y1 = y1

type figure = list[list[vec2]]
"Type alias for a list of list of points (each interpreted as polygon)"

class phenotype:
  """Class representing the property vector for all the note properties.
  """
  __slots__ = ['vel', 'pan', 'rel', 'pof', 'cut', 'res', 'col']

  def __init__(self, vel=0.78, pan=0.5, rel=0.5, pof=0, cut=0.5, res=0.5, col=0):
    self.vel = vel
    self.pan = pan
    self.rel = rel
    self.pof = pof
    self.cut = cut
    self.res = res
    self.col = col

  vel: float
  "velocity, also treated as opacity, 0.0 to 1.0, default 0.78"
  pan: float
  "panning, 0.0 to 1.0, default 0.5"
  rel: float
  "release, 0.0 to 1.0, default 0.5"
  pof: int
  "pitch offset, -120 to 120, default 0"
  cut: float
  "fcut/modx, 0.0 to 1.0, default 0.5"
  res: float
  "fres/mody, 0.0 to 1.0, default 0.5"
  col: int
  "note color/MIDI channel, 0 to 15, default 0"