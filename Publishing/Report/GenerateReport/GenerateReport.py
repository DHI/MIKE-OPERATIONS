def GenerateReports(simulation):
    """
    <Script>
    <Author>AUG</Author>
    <Description>This script generates the report 'MyReport' and imports it into the document manager</Description>
     <Parameters>
    <Parameter name="simulation" type="string">Simulation used to define folder name</Parameter>
    </Parameters>
    </Script>
    """
  
    scenarioModule = app.Modules.Get("Scenario Manager")
    simu = scenarioModule.SimulationList.Fetch(simulation);Simulation
    tof = simu.TimeOfForecast;
    end = simu.SimulationEndDate;
    path = "/Publish/From " + tof.ToString("yyyy MM-dd HH:mm") + " to " + end.ToString("MM-dd HH:mm") ;
    reportModule = app.Modules.Get("Report Manager")
    
    report = reportModule.ReportList.Fetch("/MyReport"); 
    generationSettings = reportModule.CreateReportGenerationSettings(report);
    generationSettings.DocumentManagerPath = path + "//Report.docx";
    generationSettings.ReportWriterSettings.OutputFolder = "c:\\ReportsFolder";
    reportModule.GenerateReport(report, generationSettings)

    
