from System import DateTime

def UpdateTOF():

    """
    <Script>
    <Author>ANK</Author>
    <Description>This script modifies scenario dates </Description>
    </Script>
    """

    scenarioFullPath = "/Group of cali/cali/Scenario of cali"
    TOF = DateTime(2014,2,1)
    SOS = TOF.AddDays(-1)
    EOS = TOF.AddDays(1)

    scmgr = app.Modules.Get("Scenario Manager")
 
    scenario = scmgr.ScenarioList.Fetch(scenarioFullPath);

    # first make sure we can set the dates without conflict (must hav SOS<=TOF<=EOS)
    scenario.SimulationStartDate = DateTime.MinValue
    scenario.SimulationTimeOfForecast = DateTime.MinValue
    scenario.SimulationEndDate = DateTime.MinValue

    # then set the dates
    scenario.SimulationEndDate = EOS
    scenario.SimulationTimeOfForecast = TOF
    scenario.SimulationStartDate = SOS

    # write changes to the database
    scmgr.ScenarioList.Update (scenario);
