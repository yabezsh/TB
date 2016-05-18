#!/usr/bin/python

import argparse
import subprocess

def Install() :
    """
    Setup the environment.
    """
    print '---------------------'
    print 'Setup the environment'

    command = 'make -j4'
    print '>', command
    subprocess.call(command,shell=True,cwd='../')
        
    command = 'make install'
    print '>', command
    subprocess.call(command,shell=True,cwd='../')

    command = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select -b fuse mount ~/eos'
    print '>', command
    subprocess.call(command,shell=True)

    command = 'chmod +x run.sh'
    print '>', command
    subprocess.call(command,shell=True,cwd='../')

    command = './run.sh bash'
    print '>', command
    # subprocess.Popen(command,shell=True,cwd='./KeplerDev_v3r0/')
    subprocess.call([command,'bash'],shell=True,cwd='../')

    print '---------------------'

    return



###############
#
# Main function
#

if __name__ == "__main__" :

    Install()
