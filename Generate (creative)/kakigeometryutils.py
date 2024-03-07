from kakiprimitives import vec2, mat3, box, cluster, figure
from kakiutils import getBoundingBox, transform

def getFigureBoundingBox(figure: figure, round: bool = False):
  """Returns the bounding box of a whole figure.
  """
  points = []
  for cluster in figure:
    points.extend(cluster)
  return getBoundingBox(points, round)

def transformCluster(cluster: cluster, t: mat3):
  """Transforms a cluster in-place.
  """
  for i in range(len(cluster)):
    cluster[i] = transform(cluster[i], t)

def transformFigure(figure: figure, t: mat3):
  """Transforms a figure in-place.
  """
  for cluster in figure:
    transformCluster(cluster, t)

def cloneCluster(cluster: cluster):
  """Returns a clone of given cluster.
  """
  clone = []
  for p in cluster:
    clone.append(vec2(p.x, p.y))
  return clone

def cloneFigure(figure: figure):
  """Returns a clone of given figure.
  """
  clone = []
  for c in figure:
    clone.append(cloneCluster(c))
  return clone