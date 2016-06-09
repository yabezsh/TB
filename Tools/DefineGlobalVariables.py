"""
Author: Federica Lionetto
Date: May 12th, 2016

Description:
    Define global variables used frequently in the code.

How to run it:
    Include it in other python scripts.
"""

import os

testbeam = 'May2016'
# testbeam = 'LateMay2016'
testbeamList = ['May2016','LateMay2016']

boardListDict = {}
boardListDict['May2016'] = ['M1','M3','M4']
boardListDict['LateMay2016'] = ['F1','F3']

boardList = boardListDict[testbeam]
PAList = ['FanIn','FanUp']
BSList = ['Top','Back','Both']

modeList = ['local','batch']

# Pitch adapter region: fan-in or fan-up.
PADict = {}
PADict['M1'] = ['FanIn','FanUp']
PADict['M3'] = ['FanIn','FanUp']
PADict['M4'] = ['FanIn','FanUp']
PADict['F1'] = ['FanUp']
PADict['F3'] = ['FanUp']

# Type of sensor: p-in-n or n-in-p.
typeDict = {}
typeDict['M1'] = 'pn'
typeDict['M3'] = 'pn'
typeDict['M4'] = 'pn'
typeDict['F1'] = 'pn'
typeDict['F3'] = 'np'

user = os.environ['USER']
userFirst = user[0]

MAMBA = '/afs/cern.ch/user/'+userFirst+'/'+user+'/eos/lhcb/testbeam/ut/OfficialData/'+testbeam+'/MAMBA/'
DQM = '/afs/cern.ch/user/'+userFirst+'/'+user+'/eos/lhcb/testbeam/ut/TemporaryData/'+testbeam+'/DQM/'
# DQM = '/afs/cern.ch/user/'+userFirst+'/'+user+'/eos/lhcb/testbeam/ut/TemporaryData/'+testbeam+'/DQMTest/'
