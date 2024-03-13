from kakiprimitives import vec2, vec3, mat3, mat4, box, figure, figure3d
from kakiutils import getBoundingBox, transform, transform3d

def getFigureBoundingBox(figure: figure, round: bool = False) -> box:
  """Returns the bounding box of a whole figure.
  """
  points = []
  for pts in figure:
    points.extend(pts)
  return getBoundingBox(points, round)

def transformPoints(points: list[vec2], t: mat3) -> None:
  """Transforms all points in list in-place.
  """
  for i in range(len(points)):
    points[i] = transform(points[i], t)

def transformFigure(figure: figure, t: mat3) -> None:
  """Transforms a figure in-place.
  """
  for pts in figure:
    transformPoints(pts, t)

def clonePoints(points: list[vec2]) -> list[vec2]:
  """Returns a clone of a list of points, all points cloned.
  """
  clone = []
  for p in points:
    clone.append(vec2(p.x, p.y))
  return clone

def cloneFigure(figure: figure) -> figure:
  """Returns a clone of given figure.
  """
  clone = []
  for pts in figure:
    clone.append(clonePoints(pts))
  return clone

# 3d pendants

def transformPoints3d(points: list[vec3], t: mat4) -> None:
  """Transforms all 3d points in list in-place.
  """
  for i in range(len(points)):
    points[i] = transform3d(points[i], t)

def transformFigure3d(figure: figure3d, t: mat4) -> None:
  """Transforms a 3d figure in-place.
  """
  for pts in figure:
    transformPoints3d(pts, t)

def clonePoints3d(points: list[vec3]) -> list[vec3]:
  """Returns a clone of a list of 3d points, all points cloned.
  """
  clone = []
  for p in points:
    clone.append(vec3(p.x, p.y, p.z))
  return clone

def cloneFigure3d(figure: figure3d) -> figure3d:
  """Returns a clone of given 3d figure.
  """
  clone = []
  for pts in figure:
    clone.append(clonePoints3d(pts))
  return clone

# 2d-3d conversion

def extrudePoints(points: list[vec2]) -> list[vec3]:
  """Returns a clone of a list of points, all points cloned, converted to 3d.
  """
  clone = []
  for p in points:
    clone.append(vec3(p.x, p.y, 0))
  return clone

def extrudeFigure(figure: figure) -> figure3d:
  """Returns a clone of given figure, converted to 3d.
  """
  clone = []
  for pts in figure:
    clone.append(extrudePoints(pts))
  return clone

def projectPoints(points: list[vec3], pinch: float = 0.001) -> list[vec2]:
  """Returns a clone of a list of 3d points, all points cloned, converted to 2d by perspective projection onto a plane at 1 / pinch with a zoom of 1 / pinch.
  """
  clone = []
  for p in points:
    w = 1 - p.z * pinch
    # undocumented safety feature: prevent division by 0
    if w <= 1e-10:
      w = 1e-10
    clone.append(vec2(p.x / w, p.y / w))
  return clone

def projectFigure(figure: figure3d, pinch: float = 0.001) -> figure:
  """Returns a clone of given figure, converted to 2d by perspective projection onto a plane at 1 / pinch with a zoom of 1 / pinch.
  """
  clone = []
  for pts in figure:
    clone.append(projectPoints(pts, pinch))
  return clone