"""
Copyright 2024 Olivier Stuker a.k.a. BinaryBorn
"""

from kakiprimitives import vec4, mat4, box, figure
from kakiutils import getBoundingBox, transform

def getFigureBoundingBox(figure: figure, round: bool = False) -> box:
  """Returns the bounding box of a whole figure.
  """
  points = []
  for pts in figure:
    points.extend(pts)
  return getBoundingBox(points, round)

def transformPoints(points: list[vec4], t: mat4) -> None:
  """Transforms all points in list in-place.
  """
  for i in range(len(points)):
    points[i] = transform(points[i], t)

def transformFigure(figure: figure, t: mat4) -> None:
  """Transforms a figure in-place.
  """
  for pts in figure:
    transformPoints(pts, t)

def clonePoints(points: list[vec4]) -> list[vec4]:
  """Returns a clone of a list of points, all points cloned.
  """
  clone = []
  for p in points:
    clone.append(vec4(p.x, p.y, p.z, p.w))
  return clone

def cloneFigure(figure: figure) -> figure:
  """Returns a clone of given figure.
  """
  clone = []
  for pts in figure:
    clone.append(clonePoints(pts))
  return clone

def applyPerspectivePoints(points: list[vec4]) -> None:
  """Applies the perspective projection to a list of points.
  """
  for p in points:
    w = p.w
    # undocumented safety feature: prevent division by 0
    if w <= 1e-10:
      w = 1e-10
    p.x /= w
    p.y /= w

def applyPerspectiveFigure(figure: figure) -> None:
  """Applies the perspective projection to a figure.
  """
  for pts in figure:
    applyPerspectivePoints(pts)