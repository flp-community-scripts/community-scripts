"""
Copyright 2024 Olivier Stuker a.k.a. BinaryBorn
"""

import math

from kakigeometryutils import transformPoints
from kakiprimitives import vec4, phenotype, tri, mesh
from kakiutils import identity4, translate, rotateX, rotateY, transform, copyPhenotype, copyVec

def createCube(pheno: phenotype) -> mesh:
  """Creates a cube with side length 1.
  """
  verts: list[vec4] = []
  tris: list[tri] = []
  for i in range(6):
    vs = []
    ts = []

    vs.extend([
      vec4(0.5, 0.5, 0.5),
      vec4(-0.5, 0.5, 0.5),
      vec4(-0.5, -0.5, 0.5),
      vec4(0.5, -0.5, 0.5)
    ])
    tr = identity4()
    if i < 4:
      tr = rotateX(tr, i * math.pi / 2)
    elif i == 4:
      tr = rotateY(tr, -math.pi / 2)
    elif i == 5:
      tr = rotateY(tr, math.pi / 2)
    transformPoints(vs, tr)

    ts.extend([
      [0, 1, 2],
      [0, 2, 3],
    ])

    i0 = len(verts)
    ts = [[i+i0 for i in t] for t in ts]

    verts.extend(vs)
    tris.extend(ts)

  phenos = [copyPhenotype(pheno)] * len(verts)
  
  return mesh(verts, phenos, tris)

def createPrism(pheno: phenotype, sides: int, rtop: float = 1.0) -> mesh:
  """Creates a prism with outer diameter 1.
  """
  if sides < 3: sides = 3
  if sides > 24: sides = 24
  if rtop < 0: rtop = 0

  verts: list[vec4] = []
  tris: list[tri] = []

  for n in range(sides):
    # helper coordinates
    a0 = n * 2 * math.pi / sides
    a1 = (n + 1) * 2 * math.pi / sides
    v0 = vec4(math.cos(a1) * 0.5, 0, math.sin(a1) * 0.5)
    v1 = vec4(math.cos(a0) * 0.5, 0, math.sin(a0) * 0.5)
    v2 = vec4(math.cos(a0) * 0.5 * rtop, 0, math.sin(a0) * 0.5 * rtop)
    v3 = vec4(math.cos(a1) * 0.5 * rtop, 0, math.sin(a1) * 0.5 * rtop)

    vs = []
    ts = []
    vs.extend([
      vec4(v0.x, -0.5, v0.z),  # mantle
      vec4(v1.x, -0.5, v1.z),
      vec4(v2.x, 0.5, v2.z),
      vec4(0, -0.5, 0),        # bottom face
      vec4(v0.x, -0.5, v0.z),
      vec4(v1.x, -0.5, v1.z),
    ])
    ts.extend([
      [0, 1, 2],    # mantle
      [3, 4, 5],    # bottom face
    ])
    if rtop > 0:
      vs.extend([
        vec4(v3.x, 0.5, v3.z),   # additional mantle vertex
        vec4(0, 0.5, 0),         # top face
        vec4(v2.x, 0.5, v2.z),
        vec4(v3.x, 0.5, v3.z),
      ])
      ts.extend([
        [0, 2, 6],  # additional mantle triangle
        [7, 9, 8],  # top face
      ])

    i0 = len(verts)
    ts = [[i+i0 for i in t] for t in ts]
    
    verts.extend(vs)
    tris.extend(ts)
  
  phenos = [copyPhenotype(pheno)] * len(verts)

  return mesh(verts, phenos, tris)

def createSphere(pheno: phenotype, sides: int) -> mesh:
  """Creates a sphere with diameter 1.
  """
  verts: list[vec4] = []
  tris: list[tri] = []

  discs = int(max(sides / 2, 3))

  i0 = 2            # offset for mantle vertices
  Ips = discs - 1   # vertices per slice

  # caps
  verts.append(vec4(0, 0.5, 0))
  verts.append(vec4(0, -0.5, 0))

  # mantle
  for n in range(sides):
    # helper coordinates
    a0 = n * 2 * math.pi / sides
    tr = identity4()
    tr = rotateY(tr, -a0)

    in0 = i0 + n * Ips
    in1 = i0 + ((n + 1) % sides) * Ips 

    vs = []
    ts = []
    for m in range(1, discs):
      b = math.pi / 2 - m * math.pi / discs
      v = vec4(math.cos(b) * 0.5, math.sin(b) * 0.5, 0)
      v = transform(v, tr)
      vs.append(v)
      if m < (discs - 1):
        ts.extend([
          [in0+m-1, in1+m-1, in0+m],    # mantle
          [in0+m, in1+m-1, in1+m],
        ])
    ts.extend([
      [0, in1, in0],    # cap
      [1, in0+discs-2, in1+discs-2]
    ])
    
    verts.extend(vs)
    tris.extend(ts)

  phenos = [copyPhenotype(pheno)] * len(verts)
  
  return mesh(verts, phenos, tris)

def createCylinder(pheno: phenotype, sides: int, rtop: float = 1.0) -> mesh:
  """Creates a cylinder with diameter 1.
  """
  if sides < 3: sides = 3
  if sides > 24: sides = 24
  if rtop < 0: rtop = 0

  verts: list[vec4] = []
  tris: list[tri] = []

  i0 = 1      # offset for mantle vertices
  Ips = 3     # vertices per slice

  # caps
  verts.append(vec4(0, -0.5, 0))
  if rtop > 0:
    verts.append(vec4(0, 0.5, 0))
    i0 = 2
    Ips = 4

  # mantle
  for n in range(sides):
    # helper coordinates
    a0 = n * 2 * math.pi / sides
    v0 = vec4(math.cos(a0) * 0.5, -0.5, math.sin(a0) * 0.5)
    v1 = vec4(math.cos(a0) * 0.5 * rtop, 0.5, math.sin(a0) * 0.5 * rtop)

    in0 = i0 + n * Ips
    in1 = i0 + ((n + 1) % sides) * Ips

    vs = []
    ts = []
    vs.extend([
      copyVec(v0),       # mantle
      copyVec(v1),
      copyVec(v0),       # cap
    ])
    ts.extend([
      [in0, in0+1, in1],      # mantle
      [0, in0+2, in1+2],      # bottom cap
    ])
    if rtop > 0:
      vs.extend([
        copyVec(v1),     # cap
      ])
      ts.extend([
        [in0+1, in1+1, in1],  # additional mantle triangle
        [1, in1+3, in0+3],    # top cap
      ])
    
    verts.extend(vs)
    tris.extend(ts)
  
  phenos = [copyPhenotype(pheno)] * len(verts)

  return mesh(verts, phenos, tris)

def createTorus(pheno: phenotype, sides: int, ratio: float = 1.0) -> mesh:
  """Creates a torus with big diameter 1.
  """
  if sides < 3: sides = 3
  if sides > 24: sides = 24

  verts: list[vec4] = []
  tris: list[tri] = []

  Ips = sides     # vertices per slice
  for n in range(sides):
    # helper coordinates
    a0 = n * 2 * math.pi / sides
    tr = identity4()
    tr = translate(tr, 0.5, 0, 0)
    tr = rotateY(tr, -a0)

    in0 = n * Ips
    in1 = ((n + 1) % sides) * Ips 

    vs = []
    ts = []
    for m in range(sides):
      b = m * 2 * math.pi / sides
      v = vec4(math.cos(b) * 0.5 * ratio, math.sin(b) * 0.5 * ratio, 0)
      v = transform(v, tr)
      vs.append(v)
      im0 = m
      im1 = (m + 1) % sides
      ts.extend([
        [in0+im0, in0+im1, in1+im0],
        [in0+im1, in1+im1, in1+im0],
      ])

    verts.extend(vs)
    tris.extend(ts)
  
  phenos = [copyPhenotype(pheno)] * len(verts)

  return mesh(verts, phenos, tris)