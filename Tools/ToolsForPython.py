"""
Author: Federica Lionetto
Date: May 12th, 2016

Description:
    Define some tools used frequently in the code.

How to run it:
    Include it in other python scripts.
"""

def GetDUTRun(df,DUTRun) :
    """
    Given a pandas dataframe and a DUT run, select and return the corresponding row in the pandas dataframe.
    """
    rowDUTRun = df.loc[(df['DUT run'] == DUTRun)]
    rowDUTRun_i = rowDUTRun.index.tolist()[0]
    print '=========================='
    print 'Information on physics run'
    print '=========================='
    print rowDUTRun
    print rowDUTRun_i
    print '=========================='

    return rowDUTRun, rowDUTRun_i



def AssociatePed(df,DUTRun) :
    """
    Given a pandas dataframe and a DUT run, associate and return the row in the pandas dataframe corresponding to the right pedestal. 
    """
    rowDUTRun = df.loc[(df['DUT run'] == DUTRun)]
    rowDUTRun_i = rowDUTRun.index.tolist()[0]
    print '=========================='
    print 'Information on physics run'
    print '=========================='
    print rowDUTRun
    print rowDUTRun_i
    
    sector = rowDUTRun.get_value(rowDUTRun_i,'Sector')
    purpose = rowDUTRun.get_value(rowDUTRun_i,'Purpose')
    biasingScheme = rowDUTRun.get_value(rowDUTRun_i,'Biasing scheme')
    x = rowDUTRun.get_value(rowDUTRun_i,'x (mm)')
    y = rowDUTRun.get_value(rowDUTRun_i,'y (mm)')
    rotation = rowDUTRun.get_value(rowDUTRun_i,'Rotation (deg)')
    biasVoltage = rowDUTRun.get_value(rowDUTRun_i,'Bias voltage (V)')
    
    print 'Associate pedestal to DUT run with'
    print 'Sector:', sector
    print 'Purpose:', purpose
    print 'Biasing scheme:', biasingScheme
    print 'x (mm):', x
    print 'y (mm):', y
    print 'Rotation (deg):', rotation
    print 'Bias voltage (V):', biasVoltage
   
    rowPed = df.loc[(df['Biasing scheme'] == biasingScheme) & (df['Bias voltage (V)'] == biasVoltage) & (df['Purpose'] == 'Pedestal')]
    rowPed_i = rowPed.index.tolist()

    # !!! What if there's no corresponding pedestal with same biasing scheme?
    if len(rowPed_i) == 0 :
        print 'WARNING! No pedestal run associated to this physics run, using the pedestal run with the other biasing scheme.'
        rowPed = df.loc[(df['Bias voltage (V)'] == biasVoltage) & (df['Purpose'] == 'Pedestal')]
        rowPed_i = rowPed.index.tolist()
    
    print '==========================='
    print 'Information on pedestal run'
    print '==========================='
    print rowPed
    print rowPed_i 
    print '=========================='

    return rowPed,rowPed_i
