import sys
import clr
import System
from System import DateTime
from System import Array
import datetime
from array import array
from System.Globalization import CultureInfo
from System.Collections.Generic import List, Dictionary

#clr.AddReference('DHI.Solutions.Generic')
#from DHI.Solutions.Generic import IDataSeries, Query, QueryElement, QueryOperator, DataSeriesValueType, IDataSeriesValuePair 

clr.AddReference('DHI.Solutions.TimeseriesManager.Interfaces')
clr.AddReference('DHI.Solutions.TimeseriesManager.Business')
clr.AddReference('DHI.Solutions.TimeseriesManager.Tools.Processing')
from DHI.Solutions.TimeseriesManager.Tools.Processing import *

worksheetName = 'Sheet1' # Name of the first worksheet.
        
def executeConvertToEnsenble(ensembleSpreadsheetPath):
    """
    <Script>
    <Author>KTH</Author>
    <Description>Executes the time series validation according to the validation spreadsheet specified.</Description> 
    <Parameters>
    <Parameter name="ensembleSpreadsheetPath" type="string">Path to the spreadsheet</Parameter>
    </Parameters>
    </Script>
    """
        
    ensembleInfoList = LoadEnsembleSpreadsheet(ensembleSpreadsheetPath);
    
    ts = [];
    tsMoy = [];
    tsMin = [];
    tsMax = [];
    
            
    timeSeriesManager = app.Modules.Get('Time series Manager')
    if timeSeriesManager == None:
        raise Exception('Can''t obtain a reference to Time series Manager.')
        
    for ensembleInfo in ensembleInfoList: 
        tsMoy = timeSeriesManager.TimeSeriesList.Fetch(ensembleInfo.TsPathMoy)
        tsMin = timeSeriesManager.TimeSeriesList.Fetch(ensembleInfo.TsPathMin)
        tsMax = timeSeriesManager.TimeSeriesList.Fetch(ensembleInfo.TsPathMax)
        
       
        ts=[tsMoy,tsMin,tsMax];
               
        if (ensembleInfo.TsPathMoy <> None):
                    ensembleName = ensembleInfo.TsOutput ;
                    targetGroup = ensembleInfo.GroupName;
                    tsOutputPath = targetGroup + '/' + ensembleName
                    duplicateNameOption = DuplicateNameOption.CreateAndReplace;
                    outputItems = ConvertToEnsembleTool(ts, ensembleName, targetGroup, duplicateNameOption);
                    outputTimeSeries = outputItems

    return;
        
		
#LoadExportSpreadsheet charge les données du spreadsheet Export
def LoadEnsembleSpreadsheet(ensembleSpreadsheetPath):
    """
    <Script>
    <Author>GKE from KTH script</Author>
    <Description>Load a station ensemble information spreadsheet.</Description> 
    <Parameters>
    <Parameter name="ensembleSpreadsheetPath" type="string">Path to the spreadsheet</Parameter>
    </Parameters>
    <ReturnValue type="List[EnsembleInfo]" >time series </ReturnValue>
    </Script>
    """  

    ssmgr = app.Modules.Get('Spreadsheet Manager');
    if ssmgr == None:
        raise Exception('Can''t obtain a reference to Spreadsheet Manager.')        

    stationEnsembleList = List[EnsembleInfo]();

    # Fetch and open the station import spreadsheet.
    stationEnsembleSpreadsheet = ssmgr.SpreadsheetList.Fetch(ensembleSpreadsheetPath)
    if (stationEnsembleSpreadsheet == None):
        raise Exception('Can''t locate ' + ensembleSpreadsheetPath + ' station ensemble spreadsheet.')
        
    # Open the station import spreadsheet.
    ssmgr.OpenSpreadsheet(stationEnsembleSpreadsheet);
    
    # Read all rows in the station map spreadsheet and add the maps to the 3 map dictinaries.
    rowNo = 1; # Start in the second row.

    while True:
        objectTsPathMoy = ssmgr.GetCellValue(stationEnsembleSpreadsheet, worksheetName, rowNo, 0);
        
        # Stop when the value of the first column is empty.
        if objectTsPathMoy == None:
            break;
        
        objectTsPathMin = ssmgr.GetCellValue(stationEnsembleSpreadsheet, worksheetName, rowNo, 1)
        objectTsPathMax = ssmgr.GetCellValue(stationEnsembleSpreadsheet, worksheetName, rowNo, 2)
        objectTsOutput = ssmgr.GetCellValue(stationEnsembleSpreadsheet, worksheetName, rowNo, 3)
        objectGroupName = ssmgr.GetCellValue(stationEnsembleSpreadsheet, worksheetName, rowNo, 4)
            
        tsPathMoy = objectTsPathMoy.ToString().Trim();
        tsPathMin = objectTsPathMin.ToString().Trim();
        tsPathMax = objectTsPathMax.ToString().Trim();
        tsOutput = objectTsOutput.ToString().Trim();
        groupName= objectGroupName.ToString().Trim();
                      
        ensembleInfo = EnsembleInfo(tsPathMoy, tsPathMin, tsPathMax, tsOutput, groupName);
        stationEnsembleList.Add(ensembleInfo);
                    
        rowNo = rowNo + 1;
        
    ssmgr.CloseSpreadsheet(stationEnsembleSpreadsheet);
    
    return stationEnsembleList;   

def ConvertToEnsembleTool(inputItems, ensembleName, targetGroup, 
        duplicateNameOption):
    """
    

    @param inputItems @type Array
        Tool input items

    @param ensembleName @type System.String
        The name of the output ensemble

    @param targetGroup @type System.String
        The output ensemble will be stored in this group.

    @param duplicateNameOption @type 
        DHI.Solutions.TimeseriesManager.Tools.Processing.DuplicateNameOption
        Use this option to specify what should happen if the destination 
        group already contains a time series with the same name as the 
        time series being created.
        @values DuplicateNameOption.CreateAndReplace, 
        DuplicateNameOption.DontCreate, 
        DuplicateNameOption.CreateButRename
    """
    tool = app.Tools.CreateNew('Convert to ensemble')
    if isinstance(inputItems,list):
        for inputItem in inputItems:
            tool.InputItems.Add(inputItem)
    else:
        if inputItems <> None:
            tool.InputItems.Add(inputItems)

        
    tool.EnsembleName = ensembleName
    tool.TargetGroup = targetGroup
    tool.DuplicateNameOption = duplicateNameOption
    tool.Execute()
    return tool.OutputItems

# Class for holding validation information for a station.
class EnsembleInfo(object):
    def __init__(self, tsPathMoy, tsPathMin, tsPathMax,tsOutput, groupName):
        self.TsPathMoy = tsPathMoy
        self.TsPathMin = tsPathMin
        self.TsPathMax = tsPathMax
        self.TsOutput = tsOutput
        self.GroupName = groupName
