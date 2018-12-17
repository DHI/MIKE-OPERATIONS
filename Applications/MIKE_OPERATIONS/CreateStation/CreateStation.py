def CreateStation(id, name):
    """
    <Script>
    <Author>admin</Author>
    <Description>Script for creating a station on a feature type in a MIKE OPERATIONS Configuration.</Description>
    <Parameters>
    <Parameter name="id" type="string">The id of the station to create.</Parameter>
    <Parameter name="name" type="string">The name of the station to create.</Parameter>
    </Parameters>
    </Script>
    """
    
    # The coordinates (lat, long) of a station is separated by a comma
    coordinates = '15.5300480615163,45.7834322644349'
    
    # Get the real time module (make sure that the realtime module has been loaded in the runtime.config.
    realtimeModule = app.Modules.Get('RealtimeModule');

    if realtimeModule == None:
        raise Exception('Can not obtain a reference to the Real-time Module.')
        
    # Load the realtime configurations
    realtimeModule.LoadRealtimeConfigurations();
    
    # Set and load the current configuration.
    for configuration in realtimeModule.RealtimeConfigurations:
        # Set the configuration named Sava5 as the current configuration.
        if configuration.Name == 'Sava5':
            configuration.LoadConfiguration(False);
            realtimeModule.CurrentConfiguration = configuration;
            break;
    
    if realtimeModule.CurrentConfiguration == None:
        raise Exception('Configuration was not found.')
    
    # Get the water level feature type from it's id of the feature type.
    featureType = realtimeModule.CurrentConfiguration.FeatureTypesSpreadsheet.GetSpreadsheetItem('FT1');
    
    # The spreadsheet containing stations can be found in the 'Spreadsheet' propety of the feature type.
    waterLevelStation = featureType.Spreadsheet.CreateSpreadsheetItem();
    waterLevelStation.Id = id;
    waterLevelStation.Name = name;
   
    # Set the coordinates.
    coordianateArray = coordinates.split(',');
    waterLevelStation.XCoordinate = float(coordianateArray[0])
    waterLevelStation.YCoordinate = float(coordianateArray[1])
    
    # Set thresholds (warning levels) of the station for every time series definition defined on the feature type.
    for tsDefinition in featureType.Items:
        warningLevelValues = waterLevelStation.WarningLevelValueDictionary[tsDefinition.Id]
        warningLevelValues[0].Value = None
        warningLevelValues[1].Value = 147.03
        warningLevelValues[2].Value = 147.98
        warningLevelValues[3].Value = 149.02
        warningLevelValues[4].Value = 149.64
        warningLevelValues[5].Value = 150.14
    
    # Add the station to the spreadsheet and save the spreadsheet.
    featureType.Spreadsheet.SpreadsheetItems.Add(waterLevelStation);
    featureType.Spreadsheet.SaveSpreadsheet();
        
    pass;
