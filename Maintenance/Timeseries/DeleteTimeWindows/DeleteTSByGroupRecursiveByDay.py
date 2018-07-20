import clr
from System import DateTime

clr.AddReference("DHI.Solutions.Generic")

from DHI.Solutions.Generic import *

def DeleteTSByGroupRecursiveByDay(groupPath, nDay):
    """
    <Script>
    <Author>jalu</Author>
    <Description>This script cleans time steps older than date in all ts in groupPath recursively</Description>
    <Parameters>
    <Parameter name="groupPath" type="string">group Path</Parameter>
    <Parameter name="nDay" type="int">integer for number of months to keep in database</Parameter>
    </Parameters>
    </Script>
    """
    try:
        # Set date older than which time steps should be deleted
        date = DateTime.Now.AddDays(-nDay)
        
        # Delete time steps in TS in groupPath recursively
        _DeleteTSByGroupRecursiveByDate(groupPath, date)
    except Exception, e:
        _log("ERROR: %s" %(str(e)));
    pass;


def _DeleteTSByGroupRecursiveByDate(groupPath, date):
    # get ts Module
    tsMgr = app.Modules.Get("Time series Manager")
    
    # Delete time steps in ts in groupPath
    _DeleteTSByGroupByDate(groupPath, date)
    
    # Get sorted list of groups
    tsGroups = sorted(tsMgr.TimeSeriesGroupList.FetchChildren(groupPath), key=lambda x: x.Name)
    for tsg in tsGroups:
        tsgPath = DssPath.Combine(groupPath, tsg.Name)
        
        # Delete time steps in ts in the sub-groups
        _DeleteTSByGroupRecursiveByDate(tsgPath, date)
    pass;

def _DeleteTSByGroupByDate(groupPath, date):
    # get ts Module
    tsMgr = app.Modules.Get("Time series Manager")
    
    # Fetch ts in group
    tsList = tsMgr.TimeSeriesList.FetchChildren(groupPath)
    
    # Remove time steps in ts older than "date"
    _log(groupPath)
    for ts in tsList:
            _log("Delete time steps from " + ts.Name + " older than " + date.ToString())
            ts.Delete(DateTime.MinValue, True, date, True)
       
    pass;


def _log(msg):

    print "%s - %s" %(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"), msg);
