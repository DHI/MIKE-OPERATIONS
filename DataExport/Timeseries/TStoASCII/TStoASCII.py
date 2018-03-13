import clr
clr.AddReference('DHI.Solutions.TimeseriesManager.Tools.TimeseriesExportTool')
from DHI.Solutions.TimeseriesManager.Tools.TimeseriesExportTool import * 

def ExportSimulationOutput(simPath):

    """
    <Script>
    <Author>ANK</Author>
    <Description>Export all simulation output time series</Description>
    <Parameters>
    <Parameter name="simPath" type="string">the full path to the simulation in MC</Parameter>
    </Parameters>
    </Script>
    """
    # Get a reference to the Scenario Manager
    sceMgr = app.Modules.Get('Scenario Manager')

    # Get a reference to the Time series Manager
    tsMgr = app.Modules.Get('Time series Manager')

    # Use it to  read a Simulation
    print "Starting export of output for " + simPath
    sim = sceMgr.SimulationList.Fetch(simPath)

    # collect the output timeseries
    tslist = []
    for sots in sim.SimulationOutputTimeseriesList.GetAll():  
        print sots.Name
        ts = tsMgr.TimeSeriesList.Fetch(sots.TimeseriesId)
        tslist.append(ts);

    if tslist.Count > 0 :
        # do the export using the tool:
        exportDirectory = r'c:\temp\exportPierre';
        TimeseriesExportTool(tslist, ExportFormatOptions.Ascii, exportDirectory, False, DirectoryStructureOptions.NoSubfolders);

    else:
        print "No time series to export";

    print "...done"    

def TimeseriesExportTool(inputItems, exportFormat, exportDirectory, exportMetadata, directoryStructure):
    """
    Timeseries export tool
    @param inputItems @type Array
        Tool input items
    @param exportFormat @type 
        DHI.Solutions.TimeseriesManager.Tools.TimeseriesExportTool.ExportFormatOptions
        Supported export files.
        @values ExportFormatOptions.Ascii, ExportFormatOptions.Excel, 
        ExportFormatOptions.dfs0
    @param exportDirectory @type System.String
        Click the button to pick the export folder.
    @param exportMetadata @type System.Boolean
        Export the metadata of the  timeseries if any. The metadata is 
        placed in a file with the extension ".dssmet".
    @param directoryStructure @type 
        DHI.Solutions.TimeseriesManager.Tools.TimeseriesExportTool.DirectoryStructureOptions
        If the "Replicate sub-groups" option is selected, only the 
        sub-groups to the group on which the tool is executed are 
        replicated as folders on the disk.
    If the "Replicate full path" option is selected, a directory structure 
        corresponding to the full group path, starting at the database 
        root shall be replicated as folders on the disk. The root shall 
        be in the Export directory.
    If "No sub-folders" is selected all selected time series shall be added 
        to the Export directory, regardless of what groups they come from.
    @values DirectoryStructureOptions.ReplicateSubgroups, 
        DirectoryStructureOptions.ReplicateFullPath, 
        DirectoryStructureOptions.NoSubfolders
    """
    tool = app.Tools.CreateNew('To file')
    if isinstance(inputItems,list):
        for inputItem in inputItems:
            tool.InputItems.Add(inputItem)
    else:
        if inputItems <> None:
            tool.InputItems.Add(inputItems)
    tool.ExportFormat = exportFormat
    tool.ExportDirectory = exportDirectory
    tool.ExportMetadata = exportMetadata
    tool.DirectoryStructure = directoryStructure
    tool.Execute()
    return tool.OutputItems
