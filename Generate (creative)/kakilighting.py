"""
Copyright 2024 Olivier Stuker a.k.a. BinaryBorn
"""

from kakigeometryutils import getPointsPlane
from kakiprimitives import vec4, phenotype, mesh
from kakiutils import normvec, dotprod, interpolatePhenotypes

def lightMesh(mesh: mesh, lightVector: vec4, lightPheno: phenotype):
  """Lights a mesh in place.
  """
  # invert the light vector, because face normals need to be aligned
  # in same directio IOT be lit
  lightVector = vec4(-lightVector.x, -lightVector.y, -lightVector.z)
  n = normvec(lightVector)
  lightVector.x /= n
  lightVector.y /= n
  lightVector.z /= n
  # keep the original phenotypes until done,
  # IOT always work on material and not light vertices multiple times
  phenos: list[phenotype] = [None] * len(mesh.phenos)
  for tri in mesh.tris:
    v0 = mesh.verts[tri[0]]
    v1 = mesh.verts[tri[1]]
    v2 = mesh.verts[tri[2]]
    norm = getPointsPlane([v0, v1, v2])
    amt = min(max(dotprod(norm, lightVector), 0), 1)
    for i in range(3):
      phenos[tri[i]] = interpolatePhenotypes([mesh.phenos[tri[i]], lightPheno], [1 - amt, amt])
  # only now replace/discard original material phenotypes
  mesh.phenos = phenos
