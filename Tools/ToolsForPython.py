"""
Author: Federica Lionetto
Date: May 12th, 2016

Description:
    Define some tools used frequently in the code.

How to run it:
    Include it in other python scripts.
"""

import pandas as pd

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



def GetInfoFromLogbook(logbook) :    
    """
    Given the location of the logbook, create the corresponding pandas dataframe and sanitise it.
    """
    # Create pandas dataframe.
    logbook_df = pd.read_csv(logbook,sep=',',header=0,names=['Sector','Purpose','Biasing scheme','DUT run','Telescope run','x (mm)','y (mm)','Rotation (deg)','Bias voltage (V)','Current (uA)','Temperature (C)','RH (%)','Online flag','Offline flag','Comments'],skiprows=1,na_values=['\n'],usecols=['Sector','Purpose','Biasing scheme','DUT run','Telescope run','x (mm)','y (mm)','Rotation (deg)','Bias voltage (V)','Current (uA)','Temperature (C)','RH (%)','Online flag','Offline flag','Comments'],skip_blank_lines=True)

    print '================'
    print 'Original logbook'
    print '================'
    print logbook_df.head()
    print logbook_df.shape
    print '================'

    # Drop NaN rows (empty rows).
    logbook_df_clean = logbook_df.dropna(axis=0,how='all')

    print '================================='
    print 'Logbook after dropping empty rows'
    print '================================='
    print logbook_df_clean.head()
    print logbook_df_clean.shape
    print '================'

    # Sanitise input.
    # bad,good -> Bad,Good
    # empty -> -
    # AngleScan -> Angle scan
    # Angle Scan -> Angle scan
    # BiasScan -> Bias scan
    # Bias Scan -> Bias scan
    logbook_df_san = logbook_df_clean.fillna('-')
    logbook_df_san = logbook_df_san.replace('bad','Bad')
    logbook_df_san = logbook_df_san.replace('good','Good')
    logbook_df_san = logbook_df_san.replace('BiasScan','Bias scan')
    logbook_df_san = logbook_df_san.replace('Bias Scan','Bias scan')
    logbook_df_san = logbook_df_san.replace('AngleScan','Angle scan')
    logbook_df_san = logbook_df_san.replace('Angle Scan','Angle scan')
    # Delete rows without DUT run.
    logbook_df_san = logbook_df_san.drop(logbook_df_san[logbook_df_san['DUT run'].astype(str) == '-'].index)
    # Delete rows with bad online or offline flag. 
    logbook_df_san = logbook_df_san.drop(logbook_df_san[logbook_df_san['Online flag'] == 'Bad'].index)
    logbook_df_san = logbook_df_san.drop(logbook_df_san[logbook_df_san['Offline flag'] == 'Bad'].index)

    print '=============================='
    print 'Logbook after sanitising input'
    print '=============================='
    print logbook_df_san.head()
    print logbook_df_san.shape
    print '================'

    return logbook_df_san
