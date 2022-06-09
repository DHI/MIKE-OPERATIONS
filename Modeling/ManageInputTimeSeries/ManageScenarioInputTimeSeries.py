import clr
import System

clr.AddReference('DHI.Solutions.Generic')
clr.AddReference('DHI.Solutions.ScenarioManager.Interfaces')

import DHI.Solutions.Generic
import DHI.Solutions.ScenarioManager.Interfaces

def RunInputTimeSeriesUtilities():
    """
    <Script>
    <Author>admin</Author>
    <Description>Script for creating a spreadsheet in the spreadsheet manager containing all input time series of a model</Description>
    </Script>
    """
  
    #CreateInputTimeSeriesSpreadsheet('/Group of Sava5/Sava5', 'Scenario of Sava5', 'Sava_InputTimeSeries')
    UpdateScenarioInputTimeSeries('/Sava_InputTimeSeries')
    pass


def UpdateScenarioInputTimeSeries(spreadsheetPath):
    """
    <Script>
    <Author>admin</Author>
    <Description>Script for updating mapping on scenario input time series.</Description>
    <Parameters>
    <Parameter name="spreadsheetPath" type="string">Spreadsheet containing mapping information.</Parameter>
    </Parameters>
    </Script>
    """
    
    # Get the spreadsheet and open it
    spreadsheetModule = app.Modules.Get('Spreadsheet Manager')
    scenarioModule = app.Modules.Get('Scenario Manager')
    timeSeriesModule = app.Modules.Get('Time series Manager')

    if (spreadsheetModule == None):
        raise System.ArgumentException('Spreadsheet module is not loaded')

    if (scenarioModule == None):
        raise System.ArgumentException('Scenario module is not loaded')
    
    spreadsheet = spreadsheetModule.SpreadsheetList.Fetch(spreadsheetPath)
    
    if (spreadsheet == None):
        raise System.ArgumentException('Spreadsheet ' + spreadsheetPath + ' was not found')
        
    modelSetup = None
    scenario = None

    # Dictionary containing included input time series
    inputTsDict = System.Collections.Generic.Dictionary[str, str]();

    # Loop the spreadsheet to get input time series mapping information.
    try:
        spreadsheetModule.OpenSpreadsheet(spreadsheet)
        
        # Get model setup path and scenario name from the spreadsheet.
        modelSetupPath = spreadsheetModule.GetCellValue(spreadsheet, 'Sheet1', 0, 1)
        scenarioName = spreadsheetModule.GetCellValue(spreadsheet, 'Sheet1', 1, 1)
        
        modelSetup = scenarioModule.ModelSetupList.Fetch(modelSetupPath)
        
        if (modelSetup == None):
            raise System.ArgumentException('The Model setup ' + modelSetupPath + ' was not found.')
        
        scenarioPath = modelSetupPath.TrimEnd('/') + '/' + scenarioName
        scenario = scenarioModule.ScenarioList.Fetch(scenarioPath);
    
        if (scenario == None):
            raise System.ArgumentException('A scenario with the name ' + scenarioName + ' was not found on the model setup.')
            
        # Make a dictionary of model object names and objects to be able to find the model objects fast.
        modelObjectList = modelSetup.ModelObjectList.FetchAll()
        modelObjectDict = System.Collections.Generic.Dictionary[str, DHI.Solutions.ScenarioManager.Interfaces.IModelObject]()

        for modelObject in modelObjectList:
            modelObjectDict.Add(modelObject.Name, modelObject);
            
        for rowNo in range(4, 10000):
            include = spreadsheetModule.GetCellValue(spreadsheet, 'Sheet1', rowNo, 0)
            modelObjectName = spreadsheetModule.GetCellValue(spreadsheet, 'Sheet1', rowNo, 1)
            inputTsName = spreadsheetModule.GetCellValue(spreadsheet, 'Sheet1', rowNo, 2)
            tsPath = spreadsheetModule.GetCellValue(spreadsheet, 'Sheet1', rowNo, 3)

            # Break when a row where model object name is empty.
            if (modelObjectName == None):
                break;
                
            if (inputTsName == None):
                continue
                
            # Get the input time series and check incude/exclude
            
            if (modelObjectDict.ContainsKey(modelObjectName) == False):
                print 'A model object with the name ' + modelObjectName + ' was not found in the model setup. The configuration row was ignored!'
                continue
                
            if include:
                inputTsKey = modelObjectName + ';' + inputTsName
                inputTsDict.Add(inputTsKey, tsPath)

    finally:
        spreadsheetModule.CloseSpreadsheet(spreadsheet)
        
    # Loop all input time series and include them.
    modelObjectList = modelSetup.ModelObjectList.FetchAll()
    modelObjectDict = System.Collections.Generic.Dictionary[object, DHI.Solutions.ScenarioManager.Interfaces.IModelObject]()

    for modelObject in modelObjectList:
        modelObjectDict.Add(modelObject.Id, modelObject);

    entitiesToInclude = System.Collections.Generic.List[DHI.Solutions.Generic.IEntity]();
    
    for modelInputTs in modelSetup.ModelInputTimeseriesList:
        modelObject = modelObjectDict[modelInputTs.ModelObjectId]
        
        key = modelObject.Name + ';' + modelInputTs.Name
        
        if (inputTsDict.ContainsKey(key)):
            entitiesToInclude.Add(modelInputTs)

    # Include all input time series of the spreadsheet.
    scenario.Include(entitiesToInclude)
    
    # Loop all input time series of the scenario and update the ts path if it has changed or exclude the input time series.
    scenarioInputTsList = scenario.ScenarioInputTimeseriesDefinitionList.FetchAll()

    entitiesToExclude = System.Collections.Generic.List[DHI.Solutions.Generic.IEntity]();
    
    for scenarioInputTs in scenarioInputTsList:
        inpuyTsKey = scenarioInputTs.ModelObjectName + ';' + scenarioInputTs.Name
        
        if (inputTsDict.ContainsKey(inputTsKey)):
            tsPath = inputTsDict[inputTsKey]
            ts = timeSeriesModule.TimeSeriesList.Fetch(tsPath);
            
            if (ts == None):
                print 'A time series with the path ' + tsPath + ' was not found'
                continue
            
            scenarioInputTs.TimeseriesId = ts.Id
            scenario.ScenarioInputTimeseriesDefinitionList.Update(scenarioInputTs)
        else:
            # Exclude the input time series
            entitiesToExclude.Add(scenarioInputTs)
    
    scenario.Exclude(entitiesToExclude)

    return


def CreateInputTimeSeriesSpreadsheet(modelSetupPath, scenarioName, spreadsheetName):
    """
    <Script>
    <Author>admin</Author>
    <Description>Script for creating a spreadsheet in the spreadsheet manager containing all input time series of a model</Description>
    <Parameters>
    <Parameter name="modelSetupPath" type="string">Model setup containing input time series to add to the spreadsheet.</Parameter>
    <Parameter name="scenarioName" type="string">Optional name of a scenario containing input time series mapping to add to the spreadsheet (the scenario should be on the model setup above).</Parameter>
    <Parameter name="spreadsheetName" type="string">Name of the spreadsheet to create. The spreadsheet will be created in the spreadsheet explorer root.</Parameter>
    </Parameters>
    </Script>
    """
    
    scenarioModule = app.Modules.Get('Scenario Manager')
    spreadsheetModule = app.Modules.Get('Spreadsheet Manager')
    timeSeriesModule = app.Modules.Get('Time series Manager')
    
    if (scenarioModule == None):
        raise System.ArgumentException('Scenario module is not loaded')
        
    if (spreadsheetModule == None):
        raise System.ArgumentException('Spreadsheet module is not loaded')
        
    modelSetup = scenarioModule.ModelSetupList.Fetch(modelSetupPath)
    
    if (modelSetup == None):
        raise System.ArgumentException('The Model setup ' + modelSetupPath + ' was not found.')

    scenario = None
    
    if (modelSetup == None):
        raise System.ArgumentException('ModelSetup ' + modelSetupPath + ' was not found')
        
    if (scenarioName <> None):
        scenarioPath = modelSetupPath.TrimEnd('/') + '/' + scenarioName
        scenario = scenarioModule.ScenarioList.Fetch(scenarioPath);
        
        if (scenario == None):
            raise System.ArgumentException('A scenario with the name ' + scenarioName + ' was not found on the model setup.')
    
    spreadsheet = spreadsheetModule.SpreadsheetList.Fetch('/' + spreadsheetName)
    
    if (spreadsheet <> None):
        raise System.ArgumentException('Spreadsheet ' + spreadsheetName + ' already exists.')
        
    # Create, add and open the spreadsheet.
    spreadsheet = spreadsheetModule.SpreadsheetList.CreateNew()
    spreadsheet.Name = spreadsheetName
    spreadsheetModule.SpreadsheetList.Add(spreadsheet)
    spreadsheetModule.OpenSpreadsheet(spreadsheet)
    
    # Write column headers
    rowNo = 0
    spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 0, 'Model Setup Path')
    spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 1, modelSetupPath)
    
    rowNo = rowNo + 1
    spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 0, 'Scenario name')
    spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 1, scenarioName)

    rowNo = rowNo + 2
    spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 0, 'Include')
    spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 1, 'Model Object Name')
    spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 2, 'Input Ts Name')
    spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 3, 'Time series path')
    
    rowDict = System.Collections.Generic.Dictionary[str, int]();

    # Get all input time series of the model setup
    for inputTs in modelSetup.ModelInputTimeseriesList:
        rowNo = rowNo + 1
        modelObjectName = inputTs.ModelObjectName
        inputTsName = inputTs.Name
        
        # Update the row dictionary, so that a row can be found quickly.
        rowKey = modelObjectName + ';' + inputTsName
        rowDict.Add(rowKey, rowNo)
        
        # Set row values for the input time series.
        spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 0, False)
        spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 1, modelObjectName)
        spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 2, inputTsName)

    # Set the ts path if mapped ts has been mapped.
    if (scenario <> None):
        modelObjectList = modelSetup.ModelObjectList.FetchAll()
        modelObjectDict = System.Collections.Generic.Dictionary[object, DHI.Solutions.ScenarioManager.Interfaces.IModelObject]()

        for modelObject in modelObjectList:
            modelObjectDict.Add(modelObject.Id, modelObject);

        inputTsList = scenario.ScenarioInputTimeseriesDefinitionList.FetchAll()

        for inputTs in inputTsList:
            if (inputTs.TimeseriesId <> None):
                modelObjectId = inputTs.ModelSetupInputTimeseriesDefinition.ModelObjectId
                moName = modelObjectDict[modelObjectId].Name
                rowKey = moName + ';' + inputTs.Name
                
                if (rowDict.ContainsKey(rowKey)):
                    ts = timeSeriesModule.TimeSeriesList.Fetch(inputTs.TimeseriesId)
                    tsPath = timeSeriesModule.TimeSeriesList.GetEntityDescriptor(ts)
                    rowNo = rowDict[rowKey]
                    spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 0, True)
                    spreadsheetModule.SetCellValue(spreadsheet, 'Sheet1', rowNo, 3, tsPath)
                else:
                    raise System.ArgumentException('Spreadsheet does not model obejct in input ts ' + rowKey)

    # Save and close the spreadsheet.
    spreadsheetModule.SaveSpreadsheet(spreadsheet)
    spreadsheetModule.CloseSpreadsheet(spreadsheet)
    

