
def ChangeLogExample():
    """
    <Script>
    <Author>ANK</Author>
    <Description>How to add a change log record</Description>
    </Script>
    """
    # get the changelog module and time series manager
    cmgr = app.Modules.Get('ChangeLog Manager');
    tsmgr = app.Modules.Get('Time series Manager');

	path = '/Misc/'
    oldName = 'OldTimeseries';
    newName = 'New name';
    
    # Get the Time Series
    fullpath = path + oldName
    ts = tsmgr.TimeSeriesList.Fetch(fullpath);
    
    # rename the series
    ts.Name = newName;
    
    # make a changelog record
    # public IChangeLogEntry AddChangeLogEntry(
    # IEntity entity,
    # string source,
    # string description,
    # Object data
    # )
    cmgr.AddChangeLogEntry(ts, 
                           'ChangeLogExample script', 
                           "Changing the name from %s to %s" %(oldName, newName), 
                           None);
    
    ## update the series - the changelog will follow automatically
    tsmgr.TimeSeriesList.Update(ts);
    
