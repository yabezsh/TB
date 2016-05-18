from Gaudi.Configuration import *
from Configurables import Kepler

from Configurables import TbEventBuilder
TbEventBuilder().MinPlanesWithHits = 2
TbEventBuilder().PrintFreq = 100
TbEventBuilder().Monitoring = True
Kepler().EvtMax=5000

Kepler().AlignmentFile = "eos/lhcb/testbeam/velo/timepix3/Dec2014/RootFiles/Run4012/Conditions/Alignment4012.dat"

from Configurables import TbTracking
TbTracking().PrintConfiguration = True
TbTracking().MinNClusters = 3

TbTracking().SearchRadius = 0.5
TbTracking().VolumeAngle = 0.2
TbTracking().TimeWindow = 75
TbTracking().Monitoring = False
TbTracking().SearchPlanes = [2,3]
TbTracking().MaskedPlanes = []

from Configurables import TbTrackPlots
