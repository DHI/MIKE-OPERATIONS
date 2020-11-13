import clr
import System
clr.AddReference("DHI.Solutions.RealtimeManager.Business")
from System import *
from DHI.Solutions.RealtimeManager.Business import RealtimeModule

def UpdateThresholdCache(simulationPath):
    """
    <Script>
    <Author>jalu</Author>
    <Description>updates the threshold cache for MO web and Desktop</Description>
    <Parameters>
    <Parameter name="simulationPath" type="string">path to simulation</Parameter>
    </Parameters>
    </Script>
    """
    
    _log("load simulation: " + simulationPath)
    sceMgr = app.Modules.Get("Scenario Manager")
    sim = sceMgr.SimulationList.Fetch(simulationPath)
    
    if sim != None:
        _log("load real-time configurations...")
        realtimeModule = app.Modules.Get("RealtimeModule")
    
        # Load the real-time configurations spreadsheet to get all the configurations available.
        realtimeModule.LoadRealtimeConfigurations();
        
        # Loop over all configurations  
        for configuration in realtimeModule.RealtimeConfigurations:
            _log("load configuration: " + configuration.Name)
            realtimeModule.CurrentConfiguration = configuration;
            configuration.LoadConfiguration(False);
        
            obsPeriods = realtimeModule.CurrentConfiguration.ObservationPeriodSpreadsheet.SpreadsheetItems
            themes = realtimeModule.CurrentConfiguration.ThemesSpreadsheet.SpreadsheetItems

            # Loop over all obs periods
            for obsPeriod in realtimeModule.CurrentConfiguration.ObservationPeriodSpreadsheet.SpreadsheetItems:
                _log("update cache on observation period: " + obsPeriod.Name)
                obsPeriod.UpdateThresholdCache(None, sim.Id, True)

                # Loop over all themes
                for theme in realtimeModule.CurrentConfiguration.ThemesSpreadsheet.SpreadsheetItems:
                    _log("update cache on theme: " + theme.Name)
                    obsPeriod.UpdateThresholdCache(theme.Id, sim.Id, True)
        
    _log("...done.")

def _log(msg):
    print "%s - %s" %(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"), msg);
