from kakiprimitives import vec2, mat3, box, figure
from kakiutils import getBoundingBox, transform

def getFigureBoundingBox(figure: figure, round: bool = False):
  """Returns the bounding box of a whole figure.
  """
  points = []
  for pts in figure:
    points.extend(pts)
  return getBoundingBox(points, round)

def transformPoints(points: list[vec2], t: mat3):
  """Transforms all points in list in-place.
  """
  for i in range(len(points)):
    points[i] = transform(points[i], t)

def transformFigure(figure: figure, t: mat3):
  """Transforms a figure in-place.
  """
  for pts in figure:
    transformPoints(pts, t)

def clonePoints(points: list[vec2]):
  """Returns a clone of a list of points, all points cloned.
  """
  clone = []
  for p in points:
    clone.append(vec2(p.x, p.y))
  return clone

def cloneFigure(figure: figure):
  """Returns a clone of given figure.
  """
  clone = []
  for pts in figure:
    clone.append(clonePoints(pts))
  return clone