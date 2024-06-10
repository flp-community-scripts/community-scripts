"""
Title: Tempo transition utility class
Author: BinaryBorn

Changelog:
v1.0 (2024-06-10)
  - initial version (copied from "Multiply with tempo transition" script)
  - CHANGED rates now given in pulse length (in ticks)
  - FIXED division by zero error when duration is too short
"""

import math

def Tension(value: float, rate: float, knob=True):
  """Applies the FL Studio Tension function to a value.

  Args:
    value (float): value to skew
    rate (float): tension rate
    knob (bool): if True, function behaves like the one behind knobs (e.g. scale levels), if False, it behaves like the one in Formula Controller
  """
  if rate == 0: return value
  # rate mapping
  R = rate
  if not knob and rate > 0:
    R = math.log2(rate + 1) / 10
  elif not knob and rate < 0:
    R = -math.log2(-rate + 1) / 10
  # f(x,R) = (2^(-10*R*x)-1)/(2^(-10*R)-1)
  return (pow(2, -10 * R * value) - 1) / (pow(2, -10 * R) - 1)

class TempoTransition:
  "Represents a tempo transition"

  def __init__(self, l0: float, l1: float, dt: int, p0: int = 0, p1: int = 0, subdiv: int = 1, sweepMode: int = 0, tension: float = 0, phaseMode: int = 0, phaseTension: float = 0):
    """Create a sequence of pulses with a tempo transition.

    Args:
      l0 (float): start pulse length (in ticks)
      l1 (float): end pulse length (in ticks)
      dt (int): duration of transition (in ticks)
      p0 (int): pulses before transition
      p1 (int): pulses after transition
      subdiv (int): pulse subdivision, multiplies the number of generated pulses
      sweepMode (int): tempo sweep mode, 0: sweep frequency, 1: sweep pulse length
      tension (float): tempo application tension
      phaseMode (int): phase correction mode, 0: none, 1: stretch, 2: squash
      phaseTension (float): phase correction application tension
    """
    self.pulses: list[int] = []
    "List of pulses (in ticks)"
    self.t0: int
    "Transition start time (in ticks)"
    self.t1: int
    "Transition end time (in ticks)"

    # apply subdivision to initial pulse definition
    l0 /= subdiv
    l1 /= subdiv
    p0 *= subdiv
    p1 *= subdiv

    # pulse rate (pulse per tick)
    r0 = 1 / l0
    r1 = 1 / l1

    # before transition
    for p in range(p0):
      t = round(p * l0)
      self.pulses.append(t)
    self.t0 = round(p0 * l0)

    # transition
    tpulses: list[int] = []
    dp = 0
    p_next = 0
    for t in range(dt + 1): # dt must be included here (for spot-on-phase transitions, otherwise they'd be stretched/squashed)
      t_star = t / dt
      if sweepMode == 0:
        dp += (r1 - r0) * Tension(t_star, tension) + r0
      else:
        dp += 1 / ((l1 - l0) * Tension(t_star, tension) + l0)
      if dp >= p_next:
        tpulses.append(t)
        p_next += 1

    ttrans = tpulses[-1]
    corrRequired = ttrans != dt or (subdiv > 1 and len(tpulses) % subdiv != 1)

    # if there's no complete set of pulses, phase correction is always squash
    if phaseMode and dp < subdiv: phaseMode = 2

    # if phase correction is set to squash and required, find one additional pulse
    if phaseMode == 2 and corrRequired:
      t = dt
      while True:
        t += 1
        dp += r1
        if dp >= p_next:
          tpulses.append(t)
          p_next += 1
          if subdiv == 1:
            break
          elif len(tpulses) % subdiv == 1:
            break
      ttrans = tpulses[-1]
    # if phase correction is set to stretch and required, drop incomplete set of pulses
    elif phaseMode == 1 and corrRequired and subdiv > 1:
      while len(tpulses) % subdiv != 1:
        del tpulses[-1]
        dp -= 1
      ttrans = tpulses[-1]
    # if no phase correction is set, make it complete at least one whole pulse
    elif phaseMode == 0 and dp < subdiv:
      p1 += (subdiv - math.floor(dp))

    dp = math.floor(dp)

    # no phase correction required
    if phaseMode == 0 or not corrRequired:
      ttransEff = ttrans
    # apply phase correction
    else:
      ttransEff = dt
      for p in range(dp + 1):
        t = tpulses[p]
        s = ttransEff / ttrans
        sf0 = Tension(t / ttrans, phaseTension)
        t = t * (1 + sf0 * (s - 1))
        tpulses[p] = round(t)

    # drop the last pulse - will be appended later on
    del tpulses[-1]

    self.pulses.extend([t + self.t0 for t in tpulses])

    # after transition
    self.t1 = self.t0 + ttransEff
    for p in range(p1):
      t = round(p * l1)
      self.pulses.append(t + self.t1)
    
    # final pulse
    tend = round(p1 * l1)
    self.pulses.append(tend + self.t1)
