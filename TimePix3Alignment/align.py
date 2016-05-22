from Gaudi.Configuration import *

from Configurables import Kepler
Kepler().Alignment = True

from Configurables import TbAlignment
from Configurables import TbMillepede, TbAlignmentMinuit2, TbAlignmentMinuit1

Kepler().addAlignment(TbAlignmentMinuit1(DOFs=[1,1,0,0,0,1],MaxChi2=9999999999999999999,ReferencePlane=3))
Kepler().addAlignment(TbMillepede(DOFs=[1,1,0,1,1,1],MaxChi2=200,ResCutInit=0.5,ResCut=0.1))
Kepler().addAlignment(TbMillepede(DOFs=[1,1,1,1,1,1],MaxChi2=50,ResCutInit=1.0,ResCut=0.2))
Kepler().addAlignment(TbMillepede(Monitoring=True,DOFs=[1,1,1,1,1,1],MaxChi2=15,ResCutInit=1.0,ResCut=0.2))

TbAlignment().PrintConfiguration = True
TbAlignment().NTracks = 8000

from Configurables import TbEventBuilder
TbEventBuilder().MinPlanesWithHits = 8
#TbEventBuilder().Monitoring = True 

from Configurables import TbSimpleTracking
Kepler().UseSimpleTracking = True

TbSimpleTracking().MinPlanes = 8
TbSimpleTracking().TimeWindow = 35
# TbSimpleTracking().MaskedPlanes = [4]
TbSimpleTracking().MaxDistance = 1.2

from Configurables import TbTriggerMonitor
TbTriggerMonitor().OutputLevel = ERROR
