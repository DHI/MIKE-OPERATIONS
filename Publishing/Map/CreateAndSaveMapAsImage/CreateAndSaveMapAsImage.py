import clr
import System
clr.AddReference("System.Drawing")
clr.AddReference("DHI.Solutions.RealtimeManager.Interfaces")
clr.AddReference("DHI.Solutions.RealtimeManager.Business")
clr.AddReference("DHI.Solutions.Shell")
clr.AddReference("DHI.Solutions.RealtimeManager.UI")

from System import *
from System.Drawing import *
from DHI.Solutions.RealtimeManager.Business import RealtimeModule
import DHI.Solutions.RealtimeManager.Interfaces
import DHI.Solutions.RealtimeManager.UI
import DHI.Solutions.Shell

def CreateAndSaveMapAsImage(configurationName, filePath):
    """
    <Script>
    <Author>admin</Author>
    <Description>Sample code for creating a map containing a range of feature layers. and saving it to a PNG file. 
    The script will work in both MIKE WORKBENCH and when running the script from a job.
    NOTE: This script will work with MO 2019.2 and later versions.</Description>
    <Parameters>
    <Parameter name="configurationName" type="string">The name of the configuration to make a map for.</Parameter>
    <Parameter name="filePath" type="string">Full name of the png to save.</Parameter>
    </Parameters>
    </Script>
    """
    
    realtimeModule = app.Modules.Get('RealtimeModule');
    
    # If the real-time module was not loaded in the runtime.config, load at run-time.
    if (realtimeModule == None):
        
        moduleType = clr.GetClrType(RealtimeModule);
        realtimeModule = System.Activator.CreateInstance(moduleType);
        
        if realtimeModule == None:
            raise Exception('Can not obtain a reference to the Real-time Module.')

        # Start up the real-time module.
        realtimeModule.StartUp(app);
        app.Modules.Add(realtimeModule);
    
    # Load the real-time configurations spreadsheet to get all the configurations available.
    realtimeModule.LoadRealtimeConfigurations();
    
    # Loop all the configurations and load the setup of the configuration name in question.  
    for configuration in realtimeModule.RealtimeConfigurations:
        if (configuration.Name == configurationName):
            realtimeModule.CurrentConfiguration = configuration;
            
            # Load the configuration.Active False means that loading in done in the current thread.
            configuration.LoadConfiguration(False);
            break;

    # Set the time of the realtime configuration
    currentDateTime = realtimeModule.CurrentConfiguration.LatestSimulation.TimeOfForecast;
    realtimeModule.CurrentConfiguration.CurrentDateTime = currentDateTime;

    # Create the map.
    mapUserControl = DHI.Solutions.RealtimeManager.UI.MapUserControl(app, None);
    
    # Set the size of the map.
    mapUserControl.Size = System.Drawing.Size(800, 600);
    
    #mapUserControl.SetCurrentDateTime(currentDateTime);
    
    # Set the background map. 'None' refers to the theme used.
    mapUserControl.SetBackgroundMap(None);
    
    # Set the filtergroups (a semicolon separated list where _NoGroup_ is a stations not belonging to a group).
    filterGroups = '_NoGroup_'; 

    # Add all the groups to the list, so that every station is shown.
    for group in realtimeModule.CurrentConfiguration.GroupSpreadsheet.SpreadsheetItems:
        filterGroups = filterGroups + ';' + group.Id
        
    # Add all dynamic feature types to the map.
    for featureType in realtimeModule.CurrentConfiguration.FeatureTypesSpreadsheet.SpreadsheetItems:
        if (featureType.LayerType == DHI.Solutions.RealtimeManager.Interfaces.LayerType.DynamicFeatureLayer):
            mapUserControl.MapControl.CreateFeatureClass(featureType, filterGroups);
    
    # Refresh the map and Zoom to full extent.
    mapUserControl.Refresh();
    mapUserControl.MapControl.RefreshLayers(True);
    mapUserControl.ZoomToFullExtent();
    
    # Create the image from the map control.
    bitmap = System.Drawing.Bitmap(mapUserControl.Width, mapUserControl.Height);
    mapUserControl.DrawToBitmap(bitmap, mapUserControl.ClientRectangle);
    
    # Save the image to a file.
    bitmap.Save(filePath, System.Drawing.Imaging.ImageFormat.Png)
    return;
