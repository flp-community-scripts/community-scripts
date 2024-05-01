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
  # in same direction IOT be lit
  lightVector = vec4(-lightVector.x, -lightVector.y, -lightVector.z)
  n = normvec(lightVector)
  lightVector.x /= n
  lightVector.y /= n
  lightVector.z /= n
  # light each vertex on its own based on corresponding normal vector
  for i in range(len(mesh.verts)):
    # amount of lighting (normalize normal vector, could be != 1 due to mesh scaling)
    amt = min(max(dotprod(mesh.normals[i], lightVector) / normvec(mesh.normals[i]), 0), 1)
    # mix material phenotype with light
    mesh.phenos[i] = interpolatePhenotypes([mesh.phenos[i], lightPheno], [1 - amt, amt])
