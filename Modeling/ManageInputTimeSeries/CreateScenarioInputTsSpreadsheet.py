import clr
import System

clr.AddReference('DHI.Solutions.ScenarioManager.Interfaces')
import DHI.Solutions.ScenarioManager.Interfaces

def RunInputTimeSeriesUtilities():
    """
    <Script>
    <Author>admin</Author>
    <Description>Script for creating a spreadsheet in the spreadsheet manager containing all input time series of a model</Description>
    </Script>
    """
  
    CreateInputTimeSeriesSpreadsheet('/Group of Sava5/Sava5', 'Scenario of Sava5', 'Sava_InputTimeSeries')
    pass


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
    

