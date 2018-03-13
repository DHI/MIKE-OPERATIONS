import clr
clr.AddReference('Blobfixer')
from Blobfixer import *

clr.AddReferenceToFileAndPath('C:\\Program Files (x86)\\DHI\\2017\\MIKE OPERATIONS 7\\Blobfixer.dll')
from DHI.Solutions.LeakageMonitor.Engine import *

clr.AddReference("System")
clr.AddReference("System.Data")
from System.Data.OleDb import OleDbDataReader, OleDbConnection, OleDbCommand


clr.AddReference('DHI.Solutions.TimeseriesManager.UI')
clr.AddReference('DHI.Solutions.TimeseriesManager.Interfaces')
from DHI.Solutions.TimeseriesManager.Interfaces import *
from DHI.Solutions.TimeseriesManager.UI import *


import logging
import os, sys


def TSBlobToRaw():
    """
    <Script>
    <Author>Kaku&FIK</Author>
    <Description>Changes source type of all time series from Blob to Raw. DLL needed.</Description>
    </Script>
    """
    BlobFix.Fix(app)   
     
    pass;
   
    


