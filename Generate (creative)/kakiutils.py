import math
import flpianoroll

from kakiprimitives import vec2, vec4, mat3, mat4, phenotype, box

def getBoundingBox(points: list[vec2], round: bool = False) -> box:
  """Returns the smallest box that completely includes all points in a given list of points.

  Args:
    points (list[vec2]): list of points

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

def mixPhenotypes(pheno1: phenotype, pheno2: phenotype):
  """Mixes two phenotypes. Takes their respective opacity into account.
  """
  # special cases: both or one of them fully absent
  if pheno1 is None and pheno2 is None: return None
  if pheno1 is None:
    pheno1 = phenotype(vel=0.0)
  if pheno2 is None:
    pheno2 = phenotype(vel=0.0)
  # weigh by velocity
  wgt1 = pheno1.vel
  wgt2 = pheno2.vel
  wgtTot = wgt1 + wgt2
  if wgtTot == 0: return None
  # interpolate
  vel = (pheno1.vel + pheno2.vel) / 2
  pan = (pheno1.pan * wgt1 + pheno2.pan * wgt2) / wgtTot
  rel = (pheno1.rel * wgt1 + pheno2.rel * wgt2) / wgtTot
  pof = (pheno1.pof * wgt1 + pheno2.pof * wgt2) / wgtTot
  cut = (pheno1.cut * wgt1 + pheno2.cut * wgt2) / wgtTot
  res = (pheno1.res * wgt1 + pheno2.res * wgt2) / wgtTot
  col = (pheno1.col * wgt1 + pheno2.col * wgt2) / wgtTot
  return phenotype(vel, pan, rel, pof, cut, res, col)
  
def interpolatePhenotypes(phenos: list[phenotype], weights: list[float] = None):
  """Interpolates multiple phenotypes. Does not take their respective opacity into account.
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
  return phenotype(vel, pan, rel, pof, cut, res, col)

def getPhenotypeFromNote(note: flpianoroll.Note) -> phenotype:
  """Returns the phenotype of a given note.
  """
  return phenotype(note.velocity, note.pan, note.release, note.pitchofs, note.fcut, note.fres, note.color)

def normvec2(a: vec2):
  """Returns the norm of a given vector.
  """
  return math.sqrt(a.x ** 2 + a.y ** 2)

def dotprod2(a: vec2, b: vec2):
  """Returns the dot product of two given vectors.
  """
  return a.x * b.x + a.y * b.y

def anglevec2(a: vec2, b: vec2):
  """Returns the angle between two given vectors.
  """
  sign = 1 if a.x * b.y - a.y * b.x > 0 else -1
  p = dotprod2(a,b) / (normvec2(a) * normvec2(b))
  # should never be outside [-1, +1], but epsilon...
  if p < -1:
    p = -1
  elif p > 1:
    p = 1
  return sign * math.acos(p)

def matmul3(a: mat3, b: mat3):
  """Multiplies two 3x3 matrices.
  """
  res = mat3(0, 0, 0, 0, 0, 0, 0, 0, 0)

  res.a11 = a.a11 * b.a11 + a.a12 * b.a21 + a.a13 * b.a31
  res.a12 = a.a11 * b.a12 + a.a12 * b.a22 + a.a13 * b.a32
  res.a13 = a.a11 * b.a13 + a.a12 * b.a23 + a.a13 * b.a33

  res.a21 = a.a21 * b.a11 + a.a22 * b.a21 + a.a23 * b.a31
  res.a22 = a.a21 * b.a12 + a.a22 * b.a22 + a.a23 * b.a32
  res.a23 = a.a21 * b.a13 + a.a22 * b.a23 + a.a23 * b.a33

  res.a31 = a.a31 * b.a11 + a.a32 * b.a21 + a.a33 * b.a31
  res.a32 = a.a31 * b.a12 + a.a32 * b.a22 + a.a33 * b.a32
  res.a33 = a.a31 * b.a13 + a.a32 * b.a23 + a.a33 * b.a33

  return res

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

def transform(p: vec2, t: mat3):
  """Returns a new vector that is the given vector transformed by a transformation matrix.
  """
  res = vec2(0,0)

  res.x = t.a11 * p.x + t.a12 * p.y + t.a13 * 1
  res.y = t.a21 * p.x + t.a22 * p.y + t.a23 * 1

  return res

def transform3d(p: vec4, t: mat4):
  """Returns a new vector that is the given vector transformed by a transformation matrix.
  """
  res = vec4()

  res.x = t.a11 * p.x + t.a12 * p.y + t.a13 * p.z + t.a14 * p.w
  res.y = t.a21 * p.x + t.a22 * p.y + t.a23 * p.z + t.a24 * p.w
  res.z = t.a31 * p.x + t.a32 * p.y + t.a33 * p.z + t.a34 * p.w
  res.w = t.a41 * p.x + t.a42 * p.y + t.a43 * p.z + t.a44 * p.w

  return res

def identity3() -> mat3:
  """Returns a 3x3 identity matrix.
  """
  return mat3(
    1, 0, 0,
    0, 1, 0,
    0, 0, 1
  )

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

def translate(mat: mat3, x: float, y: float) -> mat3:
  """Returns a copy of a transformation matrix translated by x, y.
  """
  tr = mat3(
    1, 0, x,
    0, 1, y,
    0, 0, 1
  )
  return matmul3(tr, mat)

def scale(mat: mat3, sx: float, sy: float) -> mat3:
  """Returns a copy of a transformation matrix scaled by sx, sy.
  """
  tr = mat3(
    sx, 0, 0,
    0, sy, 0,
    0, 0, 1
  )
  return matmul3(tr, mat)

def rotate(mat: mat3, phi: float) -> mat3:
  """Returns a copy of a transformation matrix rotated by phi.
  """
  cosphi = math.cos(phi)
  sinphi = math.sin(phi)
  tr = mat3(
    cosphi, -sinphi, 0,
    sinphi, cosphi, 0,
    0, 0, 1
  )
  return matmul3(tr, mat)

def translate3d(mat: mat4, x: float, y: float, z: float) -> mat4:
  """Returns a copy of a 3d transformation matrix translated by x, y, z.
  """
  tr = mat4(
    1, 0, 0, x,
    0, 1, 0, y,
    0, 0, 1, z,
    0, 0, 0, 1
  )
  return matmul4(tr, mat)

def scale3d(mat: mat4, sx: float, sy: float, sz: float) -> mat4:
  """Returns a copy of a 3d transformation matrix scaled by sx, sy, sz.
  """
  tr = mat4(
    sx, 0, 0, 0,
    0, sy, 0, 0,
    0, 0, sz, 0,
    0, 0, 0, 1
  )
  return matmul4(tr, mat)

def rotateX3d(mat: mat4, phi: float) -> mat4:
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

def rotateY3d(mat: mat4, phi: float) -> mat4:
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

def rotateZ3d(mat: mat4, phi: float) -> mat4:
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

def perspective3d(mat: mat4, pinch: float) -> mat4:
  """Returns a copy of a 3d transformation matrix with it's homogeneous component increased, causing the projection to pinch like in perspective projection.
  """
  tr = mat4(
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, 0, -pinch, 1
  )
  return matmul4(tr, mat)
