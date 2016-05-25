"""
Author: Federica Lionetto
Date: May 12th, 2016

Description:
    Define global variables used frequently in the code.

How to run it:
    Include it in other python scripts.
"""

import os

boardList = ['M1','M3','M4']
PAList = ['FanIn','FanUp']
BSList = ['Top','Back','Both']

modeList = ['local','batch']

# Pitch adapter region: fan-in or fan-up.
PADict = {}
PADict['M1'] = ['FanIn','FanUp']
PADict['M3'] = ['FanIn','FanUp']
PADict['M4'] = ['FanIn','FanUp']

# Type of sensor: p-in-n or n-in-p.
typeDict = {}
typeDict['M1'] = 'pn'
typeDict['M3'] = 'pn'
typeDict['M4'] = 'pn'

user = os.environ['USER']
userFirst = user[0]

# MAMBA = '/afs/cern.ch/user/f/flionett/eos/lhcb/testbeam/ut/TemporaryData/May2016/MAMBA/'
MAMBA = '/afs/cern.ch/user/'+userFirst+'/'+user+'/eos/lhcb/testbeam/ut/OfficialData/May2016/MAMBA/'
DQM = '/afs/cern.ch/user/'+userFirst+'/'+user+'/eos/lhcb/testbeam/ut/TemporaryData/May2016/DQM/'
# DQM = '/afs/cern.ch/user/'+userFirst+'/'+user+'/eos/lhcb/testbeam/ut/TemporaryData/May2016/DQMTest/'
