import clr
import System
clr.AddReference("System.Drawing")
clr.AddReference("DHI.Solutions.RealtimeManager.Business")
clr.AddReference("DHI.Solutions.Shell")
clr.AddReference("DHI.Solutions.RealtimeManager.UI")

from System import *
from System.Drawing import *
from DHI.Solutions.RealtimeManager.Business import RealtimeModule
import DHI.Solutions.RealtimeManager.UI
import DHI.Solutions.Shell

def CreateFeatureTimeSeriesChartAsImage():
    """
    <Script>
    <Author>admin</Author>
    <Description>Sample code for creating a chart of a station and saving it to an image file. This will work with MO 2019.2 and versions after that.</Description>
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
        if (configuration.Name == 'Sava5'):
            realtimeModule.CurrentConfiguration = configuration;
            
            # Load the configuration.Active False means that loading in done in the current thread.
            configuration.LoadConfiguration(False);
            break;
            
    # Find a station of a feature type (here a Water level station from the demo configuration).
    wlFeatureType = realtimeModule.CurrentConfiguration.FeatureTypesSpreadsheet.GetSpreadsheetItem('FT1');
    wlStation = wlFeatureType.Spreadsheet.GetSpreadsheetItem('3080');
    
    # Get the time series of the station
    realtimeTimeSeriesList = wlStation.GetAllTimeSeries(True);
    
    # Create a chart image using the chart component.
    realtimeChart = DHI.Solutions.RealtimeManager.UI.RealtimeChart();
    realtimeChart.Initialize(app);
    
    # Show the legend if required.
    realtimeChart.LegendVisible = True;

    # Set the size of the chart.
    realtimeChart.Width = 640;
    realtimeChart.Height = 480;
    
    # Add the time series of the station to the chart (note that this works only with MO 2019.2 an later when using jobs).
    for realtimeTimeSeries in realtimeTimeSeriesList:
        realtimeChart.AddTimeSeries(realtimeTimeSeries);
        
    # Add threshold annotations for the feature (after adding the time series). False means that there are no threshold lines on the secondary axis.
    realtimeChart.CreateWarningLevelAnnotations(wlStation, False);
    
    # Get the image
    bitmap = System.Drawing.Bitmap(realtimeChart.Width, realtimeChart.Height);
    realtimeChart.DrawToBitmap(bitmap, realtimeChart.ClientRectangle);
    
    # Save the image to a file (for testing).
    bitmap.Save('c:\\temp\\mychart.png', System.Drawing.Imaging.ImageFormat.Png)
    return;
