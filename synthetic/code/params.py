"""Measurement and scenario parameters.

Measurement parameters (T, tau, Delta) are the proposed initial values (tau for UAM follows ICAO GANP
KPI14, variant 1). Scenario parameters are illustrative author assumptions and are varied in the
experiments. Times in seconds.
"""
from dataclasses import dataclass, field, replace

MIN = 60.0


@dataclass(frozen=True)
class MeasurementParameters:          # mirrors attribute def MeasurementParameters
    periodSeconds: float
    toleranceSeconds: float           # tau
    shiftWindowSeconds: float         # Delta


UTM_MEAS = MeasurementParameters(periodSeconds=3600, toleranceSeconds=60, shiftWindowSeconds=5 * MIN)
AAM_MEAS = MeasurementParameters(periodSeconds=3600, toleranceSeconds=5 * MIN, shiftWindowSeconds=10 * MIN)


@dataclass(frozen=True)
class UTMScenario:                    # mirrors UTM_Selected::SyntheticScenario (+ operational levers)
    demandPerHour: float = 120
    ussCount: int = 3
    constraintActive: bool = True
    messageFailureProbability: float = 0.02
    startDeviationSigmaSeconds: float = 30
    params: MeasurementParameters = UTM_MEAS
    # generator assumptions
    cells: int = 256                  # elementary airspace volumes in the study area
    cellsPerRoute: tuple = (2, 5)     # volumes crossed in sequence; each occupied for a fraction of the duration
    durationRange: tuple = (8 * MIN, 20 * MIN)
    leadTimeRange: tuple = (5 * MIN, 30 * MIN)   # submission lead time
    invalidFraction: float = 0.05
    withdrawProbability: float = 0.03
    searchWindowSeconds: float = 20 * MIN        # how far the USS may shift the start
    shiftStepSeconds: float = 60
    separationBufferSeconds: float = 60          # required buffer between intents in the same volume (E4 lever)
    constraintCells: int = 3
    constraintDurationSeconds: float = 30 * MIN
    lateReadinessProbability: float = 0.10
    lateReadinessMeanSeconds: float = 3 * MIN
    tacticalBufferSeconds: float = 30


@dataclass(frozen=True)
class AAMScenario:                    # mirrors AAM_Selected::SyntheticScenario (+ operational levers)
    vertiportCount: int = 4
    padsPerVertiport: int = 2
    chargersPerVertiport: int = 4
    fleetSize: int = 32
    peakDemandPerHour: float = 40
    turnaroundSeconds: float = 5 * MIN
    chargingSeconds: float = 15 * MIN
    corridorClosureProbability: float = 0.2      # per corridor, within the period
    params: MeasurementParameters = AAM_MEAS
    # generator assumptions
    flightTimeRange: tuple = (8 * MIN, 20 * MIN)
    invalidFraction: float = 0.03
    searchWindowSeconds: float = 20 * MIN
    shiftStepSeconds: float = 60
    scheduleBufferSeconds: float = 2 * MIN       # planned buffer before the next departure (E4 lever)
    corridorClosureSeconds: float = 15 * MIN
    boardingDelayProbability: float = 0.25
    boardingDelayMeanSeconds: float = 3 * MIN
    flightTimeCV: float = 0.10
    chargingSigmaSeconds: float = 4 * MIN
    turnaroundSigmaSeconds: float = 1 * MIN
    networkSeed: int = 7                         # keeps the network geometry fixed across replications


def with_(s, **kw):
    return replace(s, **kw)
