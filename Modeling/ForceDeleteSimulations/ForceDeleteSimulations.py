import clr
clr.AddReference("DHI.Solutions.ScenarioManager.Interfaces")
from DHI.Solutions.ScenarioManager.Interfaces import *
clr.AddReference("DHI.Solutions.Generic")
from DHI.Solutions.Generic import Message 

def ForceDeleteSimulation(simpath):
    """
    <Script>
    <Author>ANK</Author>
    <Description>Force delete a simulation which cannot be deleted from UI</Description>
    <Parameters>
    <Parameter name="simpath" type="string">Path to simulation</Parameter>
    </Parameters>
    </Script>
    """

    # Get a reference to the Scenario Manager
    scenarioManager = app.Modules.Get('Scenario Manager')    

    # use a local list to avoid interferrence with UI and threading issues
    # as it may change behaviour of the explorer
    simlist = scenarioManager.CreateNewList[ISimulation](); 

    # featch the simulation - and switch STATUS
    sim = simlist.Fetch(simpath);
    sim.Status = "UNDEFINED"            

    # update status in database and delete
    simlist.Update(sim);
    simlist.Delete(sim);    

    # warn user if Shell is active
    if app.Shell != None:
        Message.ShowWarningDialog("Remember to refresh the Scenario Explorer","Script")
