from System import DateTime
import clr
clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import *

def ForecastPeriod():
    """
    <Script>
    <Author>AUG</Author>
    <Description>This script gets the forecast period (as string) of the latest simulation of the input scenario</Description>
    <ReturnValue type="string">String representing the forecast period (TimeOfForecast to EndDate)</ReturnValue>
    </Script>
    """
    scmgr = app.Modules.Get("Scenario Manager")
    scenario = scmgr.ScenarioList.Fetch("/Group of doktis/doktis/RealTime");
    date = DateTime.Min
    
    q = Query();
    q.Add(QueryElement('scenario_id', scenario.Id, QueryOperator.Like));
    
    list = scmgr.SimulationList.Fetch(q)
    output = ""
    for scenarion in list:
        if scenarion.TimeOfForecast > date:
            output = ConvertDate(scenarion.TimeOfForecast) + " - " + ConvertDate(scenarion.SimulationEndDate)
            date = scenarion.TimeOfForecast
    return output
