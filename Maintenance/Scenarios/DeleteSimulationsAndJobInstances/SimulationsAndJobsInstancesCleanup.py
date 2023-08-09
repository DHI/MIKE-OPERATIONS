import sys
import clr
import datetime
from datetime import date, timedelta
import System
from System import DateTime
  
def Cleanup(numberOfDays, scenarioFullPath, jobName):
    """
    <Script>
    <Author>SNI</Author>
    <Description>This script will cleanup the simulations and job logs older than specified number of days.</Description>
    <Parameters>
    <Parameter name="numberOfDays" type="int">Number of days.</Parameter>
    <Parameter name="scenarioFullPath" type="string">Full path of the scenario whose old simulations are to be cleaned.</Parameter>
    <Parameter name="jobName" type="string">Name of the job whose old instances are to be cleaned.</Parameter>
    </Parameters>
    <ReturnValue type="IType">Function returns object of type IType</ReturnValue>
    </Script>
    """
    cutoffDT = datetime.datetime.now()-timedelta(days=numberOfDays)
    cutoffDateTime = DateTime(cutoffDT.year, cutoffDT.month, cutoffDT.day, cutoffDT.hour, cutoffDT.minute, cutoffDT.second)
    scmgr = app.Modules.Get("Scenario Manager")
    scenario = scmgr.ScenarioList.Fetch(scenarioFullPath);
    allSimulationList = scmgr.SimulationList.FetchAll()
    simulationList = []
    for simulation in allSimulationList:
        if simulation.ScenarioId == scenario.Id:
            simulationList.append(simulation)
    
    #simulationList = scmgr.SimulationList.Get(scenario)
    #simulationList = scmgr.SimulationList.Fetch(scenarioFullPath)
    simulationsToBeDeleted = []
    for simulation in simulationList:
        if simulation.TimeOfSimulationRun < cutoffDateTime:
            simulationsToBeDeleted.append(simulation)
    
    if len(simulationsToBeDeleted) > 0:
        for simulation in simulationsToBeDeleted:
            print('Deleting Simulation: ' + simulation.Name)
            scmgr.SimulationList.Delete(simulation, True)
    
    # Delete job logs older than 7 days as well.
    jobmgr = app.Modules.Get("Job Manager")
    job = jobmgr.JobList.Fetch(jobName);
    jobInstances = jobmgr.JobInstanceList.FetchJobInstance(job.Id)
    jobInstancesToBeDeleted = []
    for jobInstance in jobInstances:
        if jobInstance.ExecutedAt < cutoffDateTime:
            jobInstancesToBeDeleted.append(jobInstance)
    
    if len(jobInstancesToBeDeleted) > 0:
        for jobInstance in jobInstancesToBeDeleted:
            print('Deleting Job Instance: ' + jobInstace.Name)
            jobmgr.JobInstanceList.Delete(jobInstance)
