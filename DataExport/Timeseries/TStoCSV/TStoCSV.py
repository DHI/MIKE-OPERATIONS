import System

import clr
clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import IDataSeries, Query, QueryElement, QueryOperator, IDataSeriesValuePair 

def ExportTsGroup2Csv(tsGroupPath, csvDestinationDirectory, realtimeConfigurationName):
    """
    <Script>
    <Author>admin</Author>
    <Description>Saves all time series in a time series group to CSV files.</Description>
    <Parameters>
    <Parameter name="tsGroupPath" type="string">Time series group path to export.</Parameter>    
    <Parameter name="csvDestinationDirectory" type="string">CSV destination path.</Parameter>    
    <Parameter name="realtimeConfigurationName" type="string">The name of the real-time configuration containing the time series map to the model.</Parameter>
    </Parameters>       
    </Script>
    """
    
    # Get the real-time module.
    realtimeModule = app.Modules.Get('RealtimeModule');
    if realtimeModule == None:
            raise Exception('Can''t obtain a reference to realtimeModule.')
            
    realtimeModule.LoadRealtimeConfigurations();
    
    realtimeConfiguration = None;
    
    for configuration in realtimeModule.RealtimeConfigurations:
        if (configuration.Name == realtimeConfigurationName):
            configuration.LoadConfiguration(False);
            realtimeConfiguration = configuration;
            break;

    if (realtimeConfiguration == None):
        raise Exception('No real-time configuration found.')        
            
    if (realtimeConfiguration.ForecastLocationSpreadsheet == None):
        raise Exception('No forecast locations in the real-time configuration.')        
        
    # get the data series
    # get TS Manager
    tmgr = app.Modules.Get('Time series Manager');
    if tmgr == None:
            raise Exception('Can''t obtain a reference to Time series Manager.')        
    
    # get data series
    tsg = tmgr.TimeSeriesGroupList.Fetch(tsGroupPath);
    if tsg == None:
        raise Exception('Time series group not found at ' + tsGroupPath + '.')
    
    query = Query();
    query.Add(QueryElement('groupid', tsg.Id, QueryOperator.Eq));
    timeSeriesList = tmgr.TimeSeriesList.Fetch(query);
    
    simulationDateTime = realtimeConfiguration.LatestSimulation.TimeOfForecast;
        
    forecatLocation = None;
    for ts in timeSeriesList:
        stationId = None;
        stationName = None;
        
        for fl in realtimeConfiguration.ForecastLocationSpreadsheet.SpreadsheetItems:
            if (ts.YAxisVariable == 'Water Level'):
                if (fl.HModelObjectVariable == ts.Name):
                    stationId = fl.Id;
                    stationName = fl.Name;
                    break;
            elif (ts.YAxisVariable == 'Discharge'):
                if (fl.QModelObjectVariable == ts.Name):
                    stationId = fl.Id;
                    stationName = fl.Name;
                    break;
    
        if (stationId != None):
            ExportTs2Csv(ts, csvDestinationDirectory, stationId, stationName, simulationDateTime);
    
    return;

def RemoveInvalidCharsFromFilePath(filePath):
    
    # construct a string containing all invalid characters
    invalidChars = ''.join(System.IO.Path.GetInvalidFileNameChars())
    
    # replace them in the filename
    return filePath.translate(None, invalidChars)

def ExportTs2Csv(ts, csvFilePath, stationId, stationName, timeOfSimulationRun):
    """
    <Script>
    <Author>admin</Author>
    <Description>Saves a time series to a CSV file.</Description>
    <Parameters>
    <Parameter name="ts" type="IDataSeries">Time series to export.</Parameter>    
    <Parameter name="csvFilePath" type="string">The full path to the CSV file.</Parameter>    
    <Parameter name="stationId" type="string">The id of the forecast station.</Parameter>    
    <Parameter name="stationName" type="string">The name of the forecast station.</Parameter>    
    <Parameter name="timeOfSimulationRun" type="datetime">The datetime of the simulation run.</Parameter>    
    </Parameters>       
    </Script>
    """
    
    # Create new file and overwrite if it already exists.
    strBuilder = System.Text.StringBuilder();       
    
    currentDateTimeString = timeOfSimulationRun.ToString('yyyyMMddHHmm');
    ExportDateTimeString = System.DateTime.Now. ToString('yyyyMMddHHmm');
    
    # Write header
    h1 = 'R�sultats MIKE ALLIER;;;';
    h3 = System.String.Format('export g�n�r� le ;;{0};', ExportDateTimeString);
    h4 = ';;;'

    h2 = 'D�bit;;;';
    h5 = 'TYP;CODE;DATE(TU);DEBIT(m3/s)';
    fileName = 'PREQ_' + stationId + '_' + stationName + '_' + currentDateTimeString + '_' + ExportDateTimeString + '.txt';
    
    if (ts.YAxisVariable == 'Water Level'):
        h2 = 'Hauteur;;;';
        h5 = 'TYP;CODE;DATE(TU);HAUTEUR (m)';
        fileName = 'PREH_' + stationId + '_' + stationName + '_' + currentDateTimeString + '_' + ExportDateTimeString +'.txt';
    
    strBuilder.AppendLine(h1);
    strBuilder.AppendLine(h2);
    strBuilder.AppendLine(h3);
    strBuilder.AppendLine(h4);
    strBuilder.AppendLine(h5);
    
    #Write each time step.
    timeSteps = ts.GetAll();
    
    for timeStep in timeSteps:
        valueString = None;
        if (timeStep.YValue != None):
            valueString = timeStep.YValue.ToString(System.Globalization.CultureInfo.InvariantCulture)    
        timeStepString = System.String.Format('{0};{1};{2};{3}', 'PRV', stationId, timeStep.XValue.ToString('yyyyMMddHHmm'), valueString);
        strBuilder.AppendLine(timeStepString);
    
    csvFileName = System.IO.Path.Combine(csvFilePath, fileName);
    System.IO.File.WriteAllText(csvFileName, strBuilder.ToString());
    return;
