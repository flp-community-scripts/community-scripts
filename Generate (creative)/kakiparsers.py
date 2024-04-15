"""
Copyright 2024 Olivier Stuker a.k.a. BinaryBorn
"""

import math

from kakiprimitives import vec2, figure, phenotype
from kakiutils import anglevec2

def parsePhenotypeFromStyle(style: str):
  """Parses a CSS-like style string for note phenotypes and returns the interpreted phenotype.

  Example string: `velocity: 0.8; pan: 0.5; release: 0.5; pitchofs: 0; fcut: 1; fres: 0.5; color: 4`

  Args:
    style (str): style string

  Returns:
    phenotype: interpreted phenotype
  """
  # grab the defaults from the phenotype initializer
  vel = phenotype.__init__.__defaults__[0]
  pan = phenotype.__init__.__defaults__[1]
  rel = phenotype.__init__.__defaults__[2]
  pof = phenotype.__init__.__defaults__[3]
  cut = phenotype.__init__.__defaults__[4]
  res = phenotype.__init__.__defaults__[5]
  col = phenotype.__init__.__defaults__[6]
  # properties are separated by ;
  propStrs = style.split(';')
  for propStr in propStrs:
    try:
      # key: value pairs are separated by :
      prop = propStr.split(':')
      key = prop[0].strip()
      val = prop[1].strip()
      # all known keys
      if key == 'velocity':
        vel = float(val)
      elif key == 'pan':
        pan = float(val)
      elif key == 'release':
        rel = float(val)
      elif key == 'pitchofs':
        pof = int(val)
      elif key == 'fcut':
        cut = float(val)
      elif key == 'fres':
        res = float(val)
      elif key == 'color':
        col = int(val)
    except Exception:
      pass
  return phenotype(vel, pan, rel, pof, cut, res, col)

def parseFigureFromSvgPath(path: str) -> figure:
  """Parses SVG path data (the `d` attribute) and turns it into a figure.

  Args:
    path (str): any valid SVG path data

  Returns:
    figure: the interpreted figure
  """

  cursor = 0
  cend = len(path)

  polygons = []
  curPoly = None
  cmd = None
  x = 0
  y = 0
  cpx = None
  cpy = None

  def getWsp():
    nonlocal path, cursor, cend
    c0 = cursor
    while cursor < cend and ord(path[cursor]) in [0x09, 0x20, 0x0A, 0x0C, 0x0D]:
      cursor += 1
    if c0 == cursor: return None
    return path[c0:cursor]
  
  def getCommaWsp():
    nonlocal path, cursor, cend
    c0 = cursor
    getWsp()
    if cursor < cend and path[cursor] == ',': cursor += 1
    getWsp()
    if c0 == cursor: return None
    return path[c0:cursor]
  
  def getCommand():
    nonlocal path, cursor, cend
    c0 = cursor
    if cursor < cend and path[cursor].upper() in ['M', 'Z', 'L', 'H', 'V', 'C', 'S', 'Q','T', 'A']: cursor += 1
    if c0 == cursor: return None
    return path[c0:cursor]
  
  def getNumber():
    nonlocal path, cursor, cend
    c0 = cursor
    digits = range(48,58)
    # sign
    if cursor < cend and path[cursor] in ['+', '-']: cursor += 1
    # integer part
    while cursor < cend and ord(path[cursor]) in digits: cursor += 1
    # optional decimal point
    if cursor < cend and path[cursor] == '.': cursor += 1
    # fractional part
    while cursor < cend and ord(path[cursor]) in digits: cursor += 1
    if c0 == cursor: return None
    return float(path[c0:cursor])
  
  def getFlag():
    nonlocal path, cursor
    c0 = cursor
    if cursor < cend and path[cursor] in ['0', '1']: cursor += 1
    if c0 == cursor: return None
    return int(path[c0:cursor])
  
  def drawQuadraticBezier(x1, y1, cx, cy, x2, y2):
    nonlocal curPoly
    # draw arc in pieces of straight lines
    # TODO: dynamic pcs count dep. on curve length etc
    pcs = 24
    for i in range(pcs):
      t = (i + 1) / pcs
      tinv = 1 - t
      # https://en.wikipedia.org/wiki/Bézier_curve
      x = tinv ** 2 * x1 + 2 * tinv * t * cx + t ** 2 * x2
      y = tinv ** 2 * y1 + 2 * tinv * t * cy + t ** 2 * y2
      curPoly.append(vec2(x,y))
  
  def drawCubicBezier(x1, y1, cx1, cy1, cx2, cy2, x2, y2):
    nonlocal curPoly
    # draw arc in pieces of straight lines
    # TODO: dynamic pcs count dep. on curve length etc
    pcs = 24
    for i in range(pcs):
      t = (i + 1) / pcs
      tinv = 1 - t
      # https://en.wikipedia.org/wiki/Bézier_curve
      x = tinv ** 3 * x1 + 3 * tinv ** 2 * t * cx1 + 3 * tinv * t ** 2 * cx2 + t ** 3 * x2
      y = tinv ** 3 * y1 + 3 * tinv ** 2 * t * cy1 + 3 * tinv * t ** 2 * cy2 + t ** 3 * y2
      curPoly.append(vec2(x,y))
  
  def drawArc(x1, y1, rx, ry, phi, fA, fS, x2, y2):
    nonlocal curPoly
    # https://www.w3.org/TR/SVG2/implnote.html#ArcCorrectionOutOfRangeRadii

    # B.2.5: ensure radii are non-zero (otherwise draw a straight line)
    if rx == 0 or ry == 0:
      curPoly.append(vec2(x2,y2))
      return

    # B.2.5: ensure radii are positive
    rx = abs(rx)
    ry = abs(ry)

    # B.2.4: prime x1 and y1
    phi = rotation / 180 * math.pi
    cosphi = math.cos(phi)
    sinphi = math.sin(phi)
    dxmid = (x1 - x2) / 2
    dymid = (y1 - y2) / 2
    x1primed = cosphi * dxmid + sinphi * dymid
    y1primed = -sinphi * dxmid + cosphi * dymid

    # B.2.5: ensure radii are large enough
    Lambda = x1primed ** 2 / rx ** 2 + y1primed ** 2 / ry ** 2
    if (Lambda > 1):
      sqrLambda = math.sqrt(Lambda)
      rx = sqrLambda * rx
      ry = sqrLambda * ry

    # B.2.4: compute primed center coordinates
    thatradicand = (rx ** 2 * ry ** 2 - rx ** 2 * y1primed ** 2 - ry ** 2 * x1primed ** 2) / (rx ** 2 * y1primed ** 2 + ry ** 2 * x1primed ** 2)
    # should never be negative, but epsilon...
    thatroot = 0 if thatradicand < 0 else math.sqrt(thatradicand)
    thatsign = 1 if fA != fS else -1
    cxprimed = thatsign * thatroot * (rx / ry * y1primed)
    cyprimed = thatsign * thatroot * (-ry / rx * x1primed)

    # B.2.4: compute center coordinates
    cx = cosphi * cxprimed - sinphi * cyprimed + (x1 + x2) / 2
    cy = sinphi * cxprimed + cosphi * cyprimed + (y1 + y2) / 2

    # B.2.4: compute theta1 and dtheta
    vstart = vec2((x1primed - cxprimed) / rx, (y1primed - cyprimed) / ry)
    vend = vec2((-x1primed - cxprimed) / rx, (-y1primed - cyprimed) / ry)
    theta1 = anglevec2(vec2(1,0), vstart)
    dtheta = anglevec2(vstart, vend)

    if fS == 0 and dtheta > 0:
      dtheta -= 2 * math.pi
    if fS == 1 and dtheta < 0:
      dtheta += 2 * math.pi

    # draw arc in pieces of straight lines
    # TODO: dynamic pcs count dep. on arc length etc
    pcs = 24
    for i in range(pcs):
      f = (i + 1) / pcs
      theta = theta1 + dtheta * f
      _x = rx * math.cos(theta)
      _y = ry * math.sin(theta)
      x = cosphi * _x - sinphi * _y + cx
      y = sinphi * _x + cosphi * _y + cy
      curPoly.append(vec2(x,y))


  live = 100000
  while cursor < len(path) and live:
    # always keep track of currect cursor coordinate
    x1 = x
    y1 = y
    try:
      getWsp()
      _cmd = getCommand()
      getWsp()
      if _cmd is not None: cmd = _cmd
      cmdUC = cmd.upper()
      rel = cmd.islower()
      if cmdUC == 'M':
        curPoly = []
        polygons.append(curPoly)
        x = x + getNumber() if rel else getNumber()
        getCommaWsp()
        y = y + getNumber() if rel else getNumber()
        if x is not None and y is not None:
          curPoly.append(vec2(x,y))
        # subsequent pairs are treated as implicit lineto commands
        cmd = 'l' if rel else 'L'
      elif cmdUC == 'Z':
        p0 = curPoly[0]
        x = p0.x
        y = p0.y
        curPoly.append(vec2(x, y))
      elif cmdUC == 'L':
        x = x + getNumber() if rel else getNumber()
        getCommaWsp()
        y = y + getNumber() if rel else getNumber()
        if x is not None and y is not None:
          curPoly.append(vec2(x,y))
      elif cmdUC == 'H':
        x = x + getNumber() if rel else getNumber()
        if x is not None and y is not None:
          curPoly.append(vec2(x,y))
      elif cmdUC == 'V':
        y = y + getNumber() if rel else getNumber()
        if x is not None and y is not None:
          curPoly.append(vec2(x,y))
      elif cmdUC == 'C':
        u1 = x + getNumber() if rel else getNumber()
        getCommaWsp()
        v1 = y + getNumber() if rel else getNumber()
        getCommaWsp()
        u2 = x + getNumber() if rel else getNumber()
        getCommaWsp()
        v2 = y + getNumber() if rel else getNumber()
        getCommaWsp()
        x = x + getNumber() if rel else getNumber()
        getCommaWsp()
        y = y + getNumber() if rel else getNumber()
        if x is not None and y is not None:
          cpx = u2
          cpy = v2
          drawCubicBezier(x1, y1, u1, v1, u2, v2, x, y)
      elif cmdUC == 'S':
        u2 = x + getNumber() if rel else getNumber()
        getCommaWsp()
        v2 = y + getNumber() if rel else getNumber()
        getCommaWsp()
        x = x + getNumber() if rel else getNumber()
        getCommaWsp()
        y = y + getNumber() if rel else getNumber()
        if x is not None and y is not None:
          # reflect control points
          if cpx is not None:
            u1 = 2 * x1 - cpx
            v1 = 2 * y1 - cpy
          else:
            u1 = x1
            v1 = y1
          cpx = u2
          cpy = v2
          drawCubicBezier(x1, y1, u1, v1, u2, v2, x, y)
      elif cmdUC == 'Q':
        u1 = x + getNumber() if rel else getNumber()
        getCommaWsp()
        v1 = y + getNumber() if rel else getNumber()
        getCommaWsp()
        x = x + getNumber() if rel else getNumber()
        getCommaWsp()
        y = y + getNumber() if rel else getNumber()
        if x is not None and y is not None:
          cpx = u1
          cpy = v1
          drawQuadraticBezier(x1, y1, u1, v1, x, y)
      elif cmdUC == 'T':
        x = x + getNumber() if rel else getNumber()
        getCommaWsp()
        y = y + getNumber() if rel else getNumber()
        if x is not None and y is not None:
          # reflect control points
          if cpx is not None:
            u1 = 2 * x1 - cpx
            v1 = 2 * y1 - cpy
          else:
            u1 = x1
            v1 = y1
          cpx = u1
          cpy = v1
          drawQuadraticBezier(x1, y1, u1, v1, x, y)
      elif cmdUC == 'A':
        rx = getNumber()
        getCommaWsp()
        ry = getNumber()
        getCommaWsp()
        rotation = getNumber()
        getCommaWsp()
        large = getFlag()
        getCommaWsp()
        sweep = getFlag()
        getCommaWsp()
        x = x + getNumber() if rel else getNumber()
        getCommaWsp()
        y = y + getNumber() if rel else getNumber()
        if x is not None and y is not None:
          drawArc(x1, y1, rx, ry, rotation / 180 * math.pi, large, sweep, x, y)

      # drop control point memory except in curve commands
      if not cmdUC in ['C', 'S', 'Q', 'T']:
        cpx = None
        cpy = None

      live -= 1
      getWsp()
    except Exception:
      break
  
  return polygons