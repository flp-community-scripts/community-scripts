"""
Copyright 2024 Olivier Stuker a.k.a. BinaryBorn
"""

import math
import flpianoroll

from kakiprimitives import vec4, mat4, phenotype, box

def getBoundingBox(points: list[vec4], round: bool = False) -> box:
  """Returns the smallest box that completely includes all points in a given list of points.

  Args:
    points (list[vec4]): list of points

  Returns:
    box: bounding box
  """
  if len(points) == 0: return None
  xmin = points[0].x
  xmax = points[0].x
  ymin = points[0].y
  ymax = points[0].y
  for p in points:
    if p.x < xmin: xmin = p.x
    if p.x > xmax: xmax = p.x
    if p.y < ymin: ymin = p.y
    if p.y > ymax: ymax = p.y
  if round:
    xmin = math.floor(xmin)
    ymin = math.floor(ymin)
    xmax = math.ceil(xmax)
    ymax = math.ceil(ymax)
  return box(xmin, ymin, xmax, ymax)

def limitBox(box: box, limit: box) -> None:
  """Limits a box's edges to the ones of another box.
  """
  box.x0 = min(max(box.x0, limit.x0), limit.x1)
  box.x1 = min(max(box.x1, limit.x0), limit.x1)
  box.y0 = min(max(box.y0, limit.y0), limit.y1)
  box.y1 = min(max(box.y1, limit.y0), limit.y1)

def copyPhenotype(pheno: phenotype):
  """Returns a copy of a given phenotype.
  """
  return phenotype(pheno.vel, pheno.pan, pheno.rel, pheno.pof, pheno.cut, pheno.res, pheno.col, pheno.opa)

def mixPhenotypes(pheno1: phenotype, pheno2: phenotype):
  """Mixes two phenotypes. Takes their respective opacity into account.
  """
  # special cases: both or one of them fully absent
  if pheno1 is None and pheno2 is None: return None
  if pheno1 is None:
    pheno1 = phenotype(opa=0.0)
  if pheno2 is None:
    pheno2 = phenotype(opa=0.0)
  # weigh by opacity
  wgt1 = pheno1.opa
  wgt2 = pheno2.opa
  wgtTot = wgt1 + wgt2
  if wgtTot == 0:
    wgtTot = 1
  # interpolate
  vel = (pheno1.vel * wgt1 + pheno2.vel * wgt2) / wgtTot
  pan = (pheno1.pan * wgt1 + pheno2.pan * wgt2) / wgtTot
  rel = (pheno1.rel * wgt1 + pheno2.rel * wgt2) / wgtTot
  pof = (pheno1.pof * wgt1 + pheno2.pof * wgt2) / wgtTot
  cut = (pheno1.cut * wgt1 + pheno2.cut * wgt2) / wgtTot
  res = (pheno1.res * wgt1 + pheno2.res * wgt2) / wgtTot
  col = (pheno1.col * wgt1 + pheno2.col * wgt2) / wgtTot
  opa = (pheno1.opa + pheno2.opa) / 2
  return phenotype(vel, pan, rel, pof, cut, res, col, opa)
  
def interpolatePhenotypes(phenos: list[phenotype], weights: list[float] = None):
  """Interpolates multiple phenotypes. Does not take their respective opacity into account for weighing.
  """
  # if no weights are given, fallback to all-1
  if weights is None:
    weights = [1.0 for pheno in phenos]
  # special case: total weight is zero
  wgtTot = sum(weights)
  if wgtTot == 0: return None
  # normalize weights
  for i in range(len(phenos)):
    try:
      weights[i] /= wgtTot
    except Exception:
      # happens if there are too few weights, appending 0 won't affect total weight
      weights.append(0.0)
  # replace Nones with transparent phenotypes
  for i in range(len(phenos)):
    if phenos[i] is None:
      phenos[i] = phenotype(vel=0.0)
  # interpolate
  vel = 0
  pan = 0
  rel = 0
  pof = 0
  cut = 0
  res = 0
  col = 0
  opa = 0
  for i in range(len(phenos)):
    pheno = phenos[i]
    wgt = weights[i]
    vel += pheno.vel * wgt
    pan += pheno.pan * wgt
    rel += pheno.rel * wgt
    pof += pheno.pof * wgt
    cut += pheno.cut * wgt
    res += pheno.res * wgt
    col += pheno.col * wgt
    opa += pheno.opa * wgt
  return phenotype(vel, pan, rel, pof, cut, res, col, opa)

def getPhenotypeFromNote(note: flpianoroll.Note) -> phenotype:
  """Returns the phenotype of a given note.
  """
  return phenotype(note.velocity, note.pan, note.release, note.pitchofs, note.fcut, note.fres, note.color)

def copyVec(a: vec4) -> vec4:
  """Returns a copy of a given vector.
  """
  return vec4(a.x, a.y, a.z, a.w)

def vecadd(a: vec4, b: vec4) -> vec4:
  """Returns the sum of two vectors.
  The homogeneous component (w) is ignored.
  """
  return vec4(a.x + b.x, a.y + b.y, a.z + b.z)

def vecnorm(a: vec4):
  """Returns the norm of a given vector.
  The homogeneous component (w) is ignored.
  """
  return math.sqrt(a.x ** 2 + a.y ** 2 + a.z ** 2)

def normalize(a: vec4):
  """Returns the normalized form of a given vector.
  The homogeneous component (w) is ignored.
  """
  norm = vecnorm(a)
  return vec4(
    a.x / norm,
    a.y / norm,
    a.z / norm
  )

def dotprod(a: vec4, b: vec4):
  """Returns the dot product of two given vectors.
  The homogeneous component (w) is ignored.
  """
  return a.x * b.x + a.y * b.y + a.z * b.z

def crossprod(a: vec4, b: vec4) -> vec4:
  """Returns the cross product of two given vectors.
  The homogeneous component (w) is ignored.
  """
  return vec4(
    x = a.y * b.z - a.z * b.y,
    y = a.z * b.x - a.x * b.z,
    z = a.x * b.y - a.y * b.x
  )

def vecangle(a: vec4, b: vec4):
  """Returns the angle between two given vectors.
  The homogeneous component (w) is ignored.
  """
  # TODO: find out what to do with the z component
  sign = 1 if a.x * b.y - a.y * b.x > 0 else -1
  p = dotprod(a,b) / (vecnorm(a) * vecnorm(b))
  # should never be outside [-1, +1], but epsilon...
  if p < -1:
    p = -1
  elif p > 1:
    p = 1
  return sign * math.acos(p)

def matmul4(a: mat4, b: mat4):
  """Multiplies two 4x4 matrices.
  """
  res = mat4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

  res.a11 = a.a11 * b.a11 + a.a12 * b.a21 + a.a13 * b.a31 + a.a14 * b.a41
  res.a12 = a.a11 * b.a12 + a.a12 * b.a22 + a.a13 * b.a32 + a.a14 * b.a42
  res.a13 = a.a11 * b.a13 + a.a12 * b.a23 + a.a13 * b.a33 + a.a14 * b.a43
  res.a14 = a.a11 * b.a14 + a.a12 * b.a24 + a.a13 * b.a34 + a.a14 * b.a44

  res.a21 = a.a21 * b.a11 + a.a22 * b.a21 + a.a23 * b.a31 + a.a24 * b.a41
  res.a22 = a.a21 * b.a12 + a.a22 * b.a22 + a.a23 * b.a32 + a.a24 * b.a42
  res.a23 = a.a21 * b.a13 + a.a22 * b.a23 + a.a23 * b.a33 + a.a24 * b.a43
  res.a24 = a.a21 * b.a14 + a.a22 * b.a24 + a.a23 * b.a34 + a.a24 * b.a44

  res.a31 = a.a31 * b.a11 + a.a32 * b.a21 + a.a33 * b.a31 + a.a34 * b.a41
  res.a32 = a.a31 * b.a12 + a.a32 * b.a22 + a.a33 * b.a32 + a.a34 * b.a42
  res.a33 = a.a31 * b.a13 + a.a32 * b.a23 + a.a33 * b.a33 + a.a34 * b.a43
  res.a34 = a.a31 * b.a14 + a.a32 * b.a24 + a.a33 * b.a34 + a.a34 * b.a44

  res.a41 = a.a41 * b.a11 + a.a42 * b.a21 + a.a43 * b.a31 + a.a44 * b.a41
  res.a42 = a.a41 * b.a12 + a.a42 * b.a22 + a.a43 * b.a32 + a.a44 * b.a42
  res.a43 = a.a41 * b.a13 + a.a42 * b.a23 + a.a43 * b.a33 + a.a44 * b.a43
  res.a44 = a.a41 * b.a14 + a.a42 * b.a24 + a.a43 * b.a34 + a.a44 * b.a44

  return res

def transform(p: vec4, t: mat4):
  """Returns a new vector that is the given vector transformed by a transformation matrix.
  """
  res = vec4()

  res.x = t.a11 * p.x + t.a12 * p.y + t.a13 * p.z + t.a14 * p.w
  res.y = t.a21 * p.x + t.a22 * p.y + t.a23 * p.z + t.a24 * p.w
  res.z = t.a31 * p.x + t.a32 * p.y + t.a33 * p.z + t.a34 * p.w
  res.w = t.a41 * p.x + t.a42 * p.y + t.a43 * p.z + t.a44 * p.w

  return res

def identity4() -> mat4:
  """Returns a 4x4 identity matrix.
  """
  return mat4(
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1
  )

# common matrix transformations

def translate(mat: mat4, x: float, y: float, z: float = 0.0) -> mat4:
  """Returns a copy of a 3d transformation matrix translated by x, y, z.
  """
  tr = mat4(
    1, 0, 0, x,
    0, 1, 0, y,
    0, 0, 1, z,
    0, 0, 0, 1
  )
  return matmul4(tr, mat)

def scale(mat: mat4, sx: float, sy: float, sz: float = 1.0) -> mat4:
  """Returns a copy of a 3d transformation matrix scaled by sx, sy, sz.
  """
  tr = mat4(
    sx, 0, 0, 0,
    0, sy, 0, 0,
    0, 0, sz, 0,
    0, 0, 0, 1
  )
  return matmul4(tr, mat)

def rotateX(mat: mat4, phi: float) -> mat4:
  """Returns a copy of a 3d transformation matrix rotated around x by phi.
  """
  cosphi = math.cos(phi)
  sinphi = math.sin(phi)
  tr = mat4(
    1, 0, 0, 0,
    0, cosphi, -sinphi, 0,
    0, sinphi, cosphi, 0,
    0, 0, 0, 1
  )
  return matmul4(tr, mat)

def rotateY(mat: mat4, phi: float) -> mat4:
  """Returns a copy of a 3d transformation matrix rotated around y by phi.
  """
  cosphi = math.cos(phi)
  sinphi = math.sin(phi)
  tr = mat4(
    cosphi, 0, sinphi, 0,
    0, 1, 0, 0,
    -sinphi, 0, cosphi, 0,
    0, 0, 0, 1
  )
  return matmul4(tr, mat)

def rotateZ(mat: mat4, phi: float) -> mat4:
  """Returns a copy of a 3d transformation matrix rotated around z by phi.
  """
  cosphi = math.cos(phi)
  sinphi = math.sin(phi)
  tr = mat4(
    cosphi, -sinphi, 0, 0,
    sinphi, cosphi, 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1
  )
  return matmul4(tr, mat)

rotate = rotateZ

def perspectiveTransform(mat: mat4, pinch: float) -> mat4:
  """Returns a copy of a 3d transformation matrix with it's homogeneous component increased, causing a perspective projection like transformation.

  Remember to apply perspective division before rendering!
  """
  tr = mat4(
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, 0, -pinch, 1
  )
  # the -pinch is because -Z is into screen
  # the w=1 part is because the projection plane is at 0, thus @z=0 w has to be 1 for a /1 division
  return matmul4(tr, mat)
