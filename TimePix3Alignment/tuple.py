from Gaudi.Configuration import *

from Configurables import Kepler

Kepler().WriteTuples = True

from Configurables import TbTupleWriter
TbTupleWriter().WriteTriggers = True
TbTupleWriter().WriteHits = False
TbTupleWriter().WriteClusters = False
TbTupleWriter().WriteTracks = True
TbTupleWriter().StrippedNTuple = True

from Configurables import TbEventBuilder
TbEventBuilder().MinPlanesWithHits = 8
TbEventBuilder().PrintFreq = 100

Kepler().UseSimpleTracking = True
from Configurables import TbSimpleTracking
TbSimpleTracking().MinPlanes = 8
