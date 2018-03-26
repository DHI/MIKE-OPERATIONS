import clr
import os
clr.AddReference('DHI.Solutions.Generic')
clr.AddReference('mscorlib')
from System import DateTime
import datetime
import sys
import System
from System.Globalization import CultureInfo
from System.Collections.Generic import List, Dictionary
from System import IO
from System.Globalization import *
from System.Globalization import CultureInfo
from System.Collections.Generic import List, Dictionary
from DHI.Solutions.Generic import IDataSeries, Query, QueryElement, QueryOperator, DataSeriesValueType, IDataSeriesValuePair 

clr.AddReference('DHI.Solutions.TimeseriesManager.Interfaces')
clr.AddReference('DHI.Solutions.TimeseriesManager.Business')
clr.AddReference('DHI.Solutions.TimeseriesManager.Tools.Processing')
clr.AddReference('DHI.Solutions.SystemManager.Tools.DataExportImportTool')
clr.AddReference('DHI.Solutions.TimeseriesManager.Tools.ImportTools')
from DHI.Solutions.TimeseriesManager.Tools.Processing import *
from DHI.Solutions.SystemManager.Tools.DataExportImportTool import *
from DHI.Solutions.TimeseriesManager.Tools.ImportTools import *

worksheetName = 'Sheet1' # Name of the first worksheet.


#Class for holding import information for a station.
class ExportInfo(object):
    def __init__(self, stationCode, type, tsToExport, outputPath, outputNameFile):
        self.StationCode = stationCode
        self.Type = type
        self.TsToExport = tsToExport
        self.OutputPath = outputPath
        self.OutputNameFile = outputNameFile


def LoadExportSpreadsheet(exportSpreadsheetPath):
    """
    <Script>
    <Author>GKE from KTH script</Author>
    <Description>Load a station export information spreadsheet.</Description> 
    <Parameters>
    <Parameter name="exportSpreadsheetPath" type="string">Path to the spreadsheet</Parameter>
    </Parameters>
    <ReturnValue type="List[ExportInfo]" >time series </ReturnValue>
    </Script>
    """  

    ssmgr = app.Modules.Get('Spreadsheet Manager');
    if ssmgr == None:
        raise Exception('Can''t obtain a reference to Spreadsheet Manager.')        

    stationExportList = List[ExportInfo]();

       

    # Fetch and open the station import spreadsheet.
    stationExportSpreadsheet = ssmgr.SpreadsheetList.Fetch(exportSpreadsheetPath)
    if (stationExportSpreadsheet == None):
        raise Exception('Can''t locate ' + exportSpreadsheetPath + ' station validation spreadsheet.')
        
    # Open the station import spreadsheet.
    ssmgr.OpenSpreadsheet(stationExportSpreadsheet);
    
    # Read all rows in the station map spreadsheet and add the maps to the 3 map dictinaries.
    rowNo = 1; # Start in the second row.

    while True:
        objectStationCode = ssmgr.GetCellValue(stationExportSpreadsheet, worksheetName, rowNo, 0);
        
        # Stop when the value of the first column is empty.
        if objectStationCode == None:
            break;
        
        objectTsToExport = ssmgr.GetCellValue(stationExportSpreadsheet, worksheetName, rowNo, 1)
        objectType = ssmgr.GetCellValue(stationExportSpreadsheet, worksheetName, rowNo, 2)
        objectOutputPath = ssmgr.GetCellValue(stationExportSpreadsheet, worksheetName, rowNo, 3)
        objectOutputNameFile = ssmgr.GetCellValue(stationExportSpreadsheet, worksheetName, rowNo, 4)     
        
              
        stationCode = objectStationCode.ToString().Trim();
        type = objectType.ToString();
        tsToExport = objectTsToExport.ToString();
        outputPath = objectOutputPath.ToString().Trim();
        outputNameFile = objectOutputNameFile.ToString().Trim();
                      
        exportInfo = ExportInfo( stationCode, type, tsToExport, outputPath, outputNameFile);
        stationExportList.Add(exportInfo);
         
        rowNo = rowNo + 1;
        
    ssmgr.CloseSpreadsheet(stationExportSpreadsheet);
    
    return stationExportList;
    
    
def Get_TStoExport(exportSpreadsheetPath, startExportDate, endExportDate):
    """
    <Script>
    <Author>admin</Author>
    <Description>Paradis perdu</Description>
    <Parameters>
    <Parameter name="exportSpreadsheetPath" type="string">spreadsheet_full_path</Parameter>
    <Parameter name="startExportDate" type="string">Time of the start export</Parameter>
    <Parameter name="endExportDate" type="string">Time of the end export.</Parameter>
    </Parameters>
    <ReturnValue type="Dictionary[string, List[data]]" >time series to export </ReturnValue>
    </Script>
    """
    exportInfoList = LoadExportSpreadsheet(exportSpreadsheetPath);
    
    
    exportData = {}
    
    timeSeriesManager = app.Modules.Get('Time series Manager');
    if timeSeriesManager == None:
        raise Exception('Can''t obtain a reference to Time series Manager.');
        
    for exportInfo in exportInfoList:
        print 'fichier exporté =', exportInfo.TsToExport;
        print 'dossier MIKE Opération =',exportInfo.OutputPath;

    start = DateTime.ParseExact(startExportDate, 'MM/dd/yyyy HH:mm:ss', CultureInfo.InvariantCulture); 
    end = DateTime.ParseExact(endExportDate, 'MM/dd/yyyy HH:mm:ss', CultureInfo.InvariantCulture);
  
    count = 1;
    
    for exportInfo in exportInfoList:
        
        ts = timeSeriesManager.TimeSeriesList.Fetch(exportInfo.TsToExport);
        exportData = ts.GetAll();
        if (ts == None):
            message = 'Time series ' + exportInfo.TsPath + ' must be created before import.';
            WriteError(message);
               
                                    
            tsMgr = app.Modules.Get('Time series Manager')
            
        outputPath =exportInfo.OutputPath;
        stationId = exportInfo.StationCode;
        type=exportInfo.Type;
        timeOfSimulationRun = start;
        firstTimeStep = startExportDate;
        lastTimeStep = endExportDate;
        
        if count <2:
            WriteExportTs(ts, outputPath, stationId, type, timeOfSimulationRun,firstTimeStep, lastTimeStep);
            count += 1;
            
        WriteExportTs_2(ts, outputPath, stationId, type, timeOfSimulationRun,firstTimeStep, lastTimeStep,startExportDate, endExportDate);        
                
def WriteExportTs(ts, outputPath, stationId, type, timeOfSimulationRun, firstTimeStep, lastTimeStep):
    """
    <Script>
    <Author>admin</Author>
    <Description>Saves a time series to a txt file.</Description>
    <Parameters>
    <Parameter name="ts" type="IDataSeries">Time series to export.</Parameter>    
    <Parameter name="outputPath" type="string">The full path to the CSV file.</Parameter>    
    <Parameter name="stationId" type="string">The id of the forecast station.</Parameter>    
    <Parameter name="type" type="string">The name of the forecast station.</Parameter>    
    <Parameter name="timeOfSimulationRun" type="datetime">The datetime of the simulation run.</Parameter> 
    <Parameter name="firstTimeStep" type="datetime">DateTime of the start export.</Parameter>
    <Parameter name="lastTimeStep" type="datetime">DateTime of the end export.</Parameter>
    </Parameters>       
    </Script>
    """
    fileName = 'Export'+ '.txt';
       
       
    # Create new file and overwrite if it already exists.
    strBuilder = System.Text.StringBuilder();       
    
    currentDateTimeString = timeOfSimulationRun.ToString('yyyyMMddHHmm');
    ExportDateTimeString = System.DateTime.Now. ToString('yyyyMMddHHmm');
    
    # Write header
    
    h1 = 'DEB;PRE;Seine-Yonne-Loing;Seine Yonne Loing simulation;' + currentDateTimeString + ';MIKE;' + firstTimeStep + ';' + lastTimeStep
    strBuilder.AppendLine(h1);
    
    FileName = System.IO.Path.Combine(outputPath, fileName);
    System.IO.File.WriteAllText(FileName, strBuilder.ToString());
    #Write each time step.
      
        
    return;
    
def WriteExportTs_2(ts, outputPath, stationId, type, timeOfSimulationRun,firstTimeStep, lastTimeStep, startExportDate, endExportDate):
    """
    <Script>
    <Author>admin</Author>
    <Description>Saves a time series to a txt file.</Description>
    <Parameters>
    <Parameter name="ts" type="IDataSeries">Time series to export.</Parameter>    
    <Parameter name="outputPath" type="string">The full path to the CSV file.</Parameter>    
    <Parameter name="stationId" type="string">The id of the forecast station.</Parameter>    
    <Parameter name="type" type="string">The name of the forecast station.</Parameter>    
    <Parameter name="timeOfSimulationRun" type="datetime">The datetime of the simulation run.</Parameter>
    <Parameter name="firstTimeStep" type="datetime">DateTime of the start export.</Parameter>
    <Parameter name="lastTimeStep" type="datetime">DateTime of the end export.</Parameter>
    <Parameter name="startExportDate" type="string">Time of the start export</Parameter>
    <Parameter name="endExportDate" type="string">Time of the end export.</Parameter>
    </Parameters>       
    </Script>
    """
    fileName = 'Export'+ '.txt';
       
       
    # Create new file and overwrite if it already exists.
    strBuilder = System.Text.StringBuilder();       
    
    currentDateTimeString = timeOfSimulationRun.ToString('yyyyMMddHHmm');
    ExportDateTimeString = System.DateTime.Now. ToString('yyyyMMddHHmm');
    
    start = DateTime.ParseExact(startExportDate, 'MM/dd/yyyy HH:mm:ss', CultureInfo.InvariantCulture); 
    end = DateTime.ParseExact(endExportDate, 'MM/dd/yyyy HH:mm:ss', CultureInfo.InvariantCulture);

    
    #Write each time step.
   
    timeSteps = ts.GetAll();
    
    for timeStep in timeSteps:
        if timeStep.XValue > start and timeStep.XValue < end:
            valueString = None;
            if (timeStep.YValue <> None):
                valueString = timeStep.YValue.ToString(System.Globalization.CultureInfo.InvariantCulture);
                if type == 'debit':
                   timeStepString = System.String.Format('{0};{1};{2};{3};{4};{5};{6}', 'CQT', stationId, timeStep.XValue.ToString('yyyyMMdd'),timeStep.XValue.ToString('HHmm'), valueString, '2', '9');
                   strBuilder.AppendLine(timeStepString);
                    
                else: 
                    timeStepString = System.String.Format('{0};{1};{2};{3};{4};{5};{6}', 'NGF', stationId, timeStep.XValue.ToString('yyyyMMdd'),timeStep.XValue.ToString('HHmm'), valueString, '2', '9');
                    strBuilder.AppendLine(timeStepString);
    FileName = System.IO.Path.Combine(outputPath, fileName);
    System.IO.File.AppendAllText(FileName, strBuilder.ToString());
    return;
