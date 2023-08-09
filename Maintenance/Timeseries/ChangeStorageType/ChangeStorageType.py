import clr
clr.AddReference("DHI.Solutions.Generic")
from DHI.Solutions.Generic import *

clr.AddReference("DHI.Solutions.TimeseriesManager.Interfaces")
from DHI.Solutions.TimeseriesManager.Interfaces import *

def TestStorageTypeChange(newStorageType):
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
    <Parameters>
    <Parameter name="newStorageType" type="string">new storage type - RAW/BLOB</Parameter>
    </Parameters>
    </Script>
    """
    
    if newStorageType == "RAW":
        newStorageType = DataSeriesStorageType.Raw
    elif newStorageType == "BLOB":
        newStorageType = DataSeriesStorageType.Blob
    else: 
        raise Exception("specify only BLOB or RAW")
    
    # Get a reference to the Time series Manager
    tsMgr = app.Modules.Get('Time series Manager')

    # Read the time series
    for ts in tsMgr.TimeSeriesList.FetchAll():
        tsPath = tsMgr.TimeSeriesList.GetEntityDescriptor(ts)
        print(ts.Id, tsPath, ts.StorageType)
        
        if ts.StorageType != newStorageType:
            tsId = ts.Id
            
            # this will fill all the values
            tsClone= ts.Clone()
            
            # remove all time steps from database
            ts.DeleteAll()
            # reset the ID (to allow change fo Storage Type)
            ts.Id = None
            # change storage type
            ts.StorageType = newStorageType
            # fill back the timestepsand the ID
            ts.SetData(tsClone.GetAll())
            ts.Id = tsId
            # update -  it will change the storage type and wqrite the timesteps as blobs
            tsMgr.TimeSeriesList.Update(ts,True)
        
            # get it again to check
            ts = tsMgr.TimeSeriesList.Fetch(tsPath)
            print(ts.Id, ts.StorageType)
        else:
            print("is already " + str(newStorageType))
