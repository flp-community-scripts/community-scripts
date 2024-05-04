"""
Copyright 2024 Olivier Stuker a.k.a. BinaryBorn
"""

from kakiprimitives import vec4, phenotype, mesh
from kakiutils import vecnorm, normalize, dotprod, interpolatePhenotypes

def lightMesh(mesh: mesh, lightVector: vec4, lightPheno: phenotype, shininess: float = 0.0):
  """Lights a mesh in place.
  """
  # invert the light vector, because face normals need to be aligned
  # in same direction IOT be lit
  lightVector = normalize(vec4(-lightVector.x, -lightVector.y, -lightVector.z))
  # light each vertex on its own based on corresponding normal vector
  for i in range(len(mesh.verts)):
    # amount of lighting (normalize normal vector, could be != 1 due to mesh scaling)
    norm = vecnorm(mesh.normals[i])
    amt = 0 if norm == 0 else dotprod(mesh.normals[i], lightVector) / norm
    amt = min(max(amt, -1), 1)
    if shininess > 0:
      sign = 1 if amt >= 0 else -1
      amt = abs(amt)
      amt = sign * (pow(2, 10 * shininess * amt) - 1) / (pow(2, 10 * shininess) - 1)
    if amt > 0:
      # mix material phenotype with light, keep original opacity (for logical reasons)
      matPheno = mesh.phenos[i]
      mesh.phenos[i] = interpolatePhenotypes([matPheno, lightPheno], [1 - amt, amt])
      mesh.phenos[i].opa = matPheno.opa
    elif amt < 0:
      # or shade
      mesh.phenos[i].vel *= (amt + 1)
