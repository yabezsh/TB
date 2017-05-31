"""
Author: Federica Lionetto
Date: May 12th, 2016

Description:
    Define global variables used frequently in the code.

How to run it:
    Include it in other python scripts.
"""

import os

# testbeam = 'May2016'
#testbeam = 'LateMay2016'
testbeam = 'October2016'
#testbeam = 'June2017'
testbeamList = ['May2016','LateMay2016','October2016','June2017']

boardListDict = {}
boardListDict['May2016'] = ['M1','M3','M4']
boardListDict['LateMay2016'] = ['F1','F3']
boardListDict['October2016'] = ['A10_FanIn','A13_FanIn','A12_FanIn','A6_Lower','A3_Lower','A5_Lower','13_HM1','13_HM2','14_HM1','17_HM2','18_HM1','18_HM2']
boardListDict['June2017'] = ['FUP1', 'FUP2', 'FUM1_0', 'FUM1_25', 'FUM2_25', 'FUM2_100', 'FUM3_100', 'FUM3_0', 'FIM1_0', 'FIM1_25', 'FIM2_25', 'FIM2_100', 'FIM3_100', 'FIM3_0',]

boardList = boardListDict[testbeam]
PAList = ['FanIn','FanUp','TTV2_01','TTV2_02','TTV2_03','TTV2_06','TTV2_07','TTV2_08']
BSList = ['Top','Back','Both']

modeList = ['local','batch']

# Pitch adapter region: fan-in or fan-up.
PADict = {}
PADict['M1'] = ['FanIn','FanUp']
PADict['M3'] = ['FanIn','FanUp']
PADict['M4'] = ['FanIn','FanUp']
PADict['F1'] = ['FanUp']
PADict['F3'] = ['FanUp']
PADict['A10_FanIn'] = ['TTV2_02']
PADict['A13_FanIn'] = ['TTV2_03']
PADict['A12_FanIn'] = ['TTV2_02']
PADict['A6_Lower'] = ['TTV2_03']
PADict['A3_Lower'] = ['TTV2_01']
PADict['A5_Lower'] = ['TTV2_01']
PADict['13_HM1'] = ['TTV2_06']
PADict['13_HM2'] = ['TTV2_07']
PADict['14_HM1'] = ['TTV2_06']
PADict['17_HM2'] = ['TTV2_08']
PADict['18_HM1'] = ['TTV2_07']
PADict['18_HM2'] = ['TTV2_08']
PADict['FUP1'] = ['TTV2_01']
PADict['FUP2'] = ['TTV2_01']
PADict['FUM1_0'] = ['TTV2_01']
PADict['FUM1_25'] = ['TTV2_01']
PADict['FUM2_25'] = ['TTV2_01']
PADict['FUM2_100'] = ['TTV2_01']
PADict['FUM3_100'] = ['TTV2_01']
PADict['FUM3_0'] = ['TTV2_01']
PADict['FIM1_0'] = ['TTV2_01']
PADict['FIM1_25'] = ['TTV2_01']
PADict['FIM2_25'] = ['TTV2_01']
PADict['FIM2_100'] = ['TTV2_01']
PADict['FIM3_100'] = ['TTV2_01']
PADict['FIM3_0'] = ['TTV2_01']

# Type of sensor: p-in-n or n-in-p.
typeDict = {}
typeDict['M1'] = 'pn'
typeDict['M3'] = 'pn'
typeDict['M4'] = 'pn'
typeDict['F1'] = 'pn'
typeDict['F3'] = 'np'
typeDict['A10_FanIn'] = 'pn'
typeDict['A13_FanIn'] = 'pn'
typeDict['A12_FanIn'] = 'pn'
typeDict['A6_Lower'] = 'pn'
typeDict['A3_Lower'] = 'pn'
typeDict['A5_Lower'] = 'pn'
typeDict['13_HM1'] = 'np'
typeDict['13_HM2'] = 'np'
typeDict['14_HM1'] = 'np'
typeDict['17_HM2'] = 'np'
typeDict['18_HM1'] = 'np'
typeDict['18_HM2'] = 'np'
typeDict['FUP1'] = 'pn'
typeDict['FUP2'] = 'pn'
typeDict['FUM1_0'] = 'pn'
typeDict['FUM1_25'] = 'pn'
typeDict['FUM2_25'] = 'pn'
typeDict['FUM2_100'] = 'pn'
typeDict['FUM3_100'] = 'pn'
typeDict['FUM3_0'] = 'pn'
typeDict['FIM1_0'] = 'pn'
typeDict['FIM1_25'] = 'pn'
typeDict['FIM2_25'] = 'pn'
typeDict['FIM2_100'] = 'pn'
typeDict['FIM3_100'] = 'pn'
typeDict['FIM3_0'] = 'pn'


user = os.environ['USER']
userFirst = user[0]

MAMBA = '/eos/lhcb/testbeam/ut/TemporaryData/'+testbeam+'/MAMBA/'
#MAMBA = '/afs/cern.ch/user/'+userFirst+'/'+user+'/eos/lhcb/testbeam/ut/OfficialData/'+testbeam+'/MAMBA/'
DQM = '/eos/lhcb/testbeam/ut/TemporaryData/'+testbeam+'/DQM/'
# DQM = '/afs/cern.ch/user/'+userFirst+'/'+user+'/eos/lhcb/testbeam/ut/TemporaryData/'+testbeam+'/DQMTest/'
