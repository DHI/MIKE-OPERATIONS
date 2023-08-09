import clr
clr.AddReference("System")
from System import *
from System.IO import *
clr.AddReference("DHI.Solutions.Generic")
from DHI.Solutions.Generic import *

def ManageInitialConditions(modelsetupPath, days, types):
    """
    <Script>
    <Author>ANK</Author>
    <Description>This script deletes initial conditions for a model setup
    from the database based upon an age criteria</Description>
    <Parameters>
    <Parameter name="modelsetupPath" type="string">the full path of the model setup</Parameter>
    <Parameter name="days" type="int">the number of days</Parameter>
    <Parameter name="types" type="string">semicolon separated list of the types to consider COLD, WARM, HOT</Parameter>
    </Parameters>
    </Script>
    """
    scmgr = app.Modules.Get("Scenario Manager");

    # calculate the date to compare to
    d = DateTime.Now.AddDays(-days);

    # calculate the date to compare to
    upperTypes = ";" + types.upper();
    
    # get the model setup
    modelsetup = scmgr.ModelSetupList.Fetch(modelsetupPath);
    if (modelsetup != None):
        _log(  "Deleting initial conditions for modelsetup \'%s\' of type(s) \'%s\' older than %d days" %(modelsetupPath, types, days));
        initialConditions = modelsetup.ModelInitialConditionList.GetAll();
        initialConditionsToDelete = [];
        keep = 0
        for ic in initialConditions:
            icType = ic.Type.ToString().upper();
            if (upperTypes.IndexOf(icType)>0):
                if (ic.EndDate < d): 
                    initialConditionsToDelete.Add(ic);
                else:
                    keep = keep + 1;

        _log( "%d initial condition match criteria" %(initialConditionsToDelete.Count));
        if (initialConditionsToDelete.Count>0):
            if keep>0:                
                for ic in initialConditionsToDelete:
                    _log( "\'%s\' : %s - %s : %s" %(ic.Name, ic.StartDate.ToString("yyyy-MM-dd hh:mm:ss"), ic.StartDate.ToString("yyyy-MM-dd hh:mm:ss"), ic.Type.ToString()));
                    ic.UseChangeLog = False;
                    modelsetup.ModelInitialConditionList.Delete(ic);            
            else:
                _log( "Nothing deleted as no initial conditions of searched types will remain. Cannot delete last initial condition.")
        else:
            _log( "Nothing to delete")
    else:
        _log( "   " + modelsetupPath + " does not exist")
    _log( "...Finished")            

def DeleteScenario(scPath, maxNo):
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
    <Parameters>
    <Parameter name="scPath" type="string">scenario Path</Parameter>
    <Parameter name="maxNo" type="int">max simulations to delete</Parameter>
    </Parameters>
    </Script>
    """

    _log("Starting - " + scPath);
    # Get a reference to the Scenario Manager
    scenarioManager = app.Modules.Get('Scenario Manager')

    # Use it for e.g. reading a Scenario
    scenario = scenarioManager.ScenarioList.Fetch(scPath)
    simlist = sorted(scenarioManager.GetSimulationsForScenario(scenario.Id), key=lambda s: s.Name)

    _log( "%d simulations match criteria" %(simlist.Count));
    if simlist.Count>maxNo :
        _log( "deleting the oldest %d ..." %(maxNo));
        
    i=0
    for sim in simlist:
        if i==maxNo:
            _log("stoping after " + str(maxNo) + " deletes");
            i=-1
            break;
        _log(" deleting " + sim.Name);
        sim.UseChangeLog = False;
        scenarioManager.SimulationList.Delete(sim)
        _log(" ...done");
        i = i + 1

    if i!=-1:
        _log(" deleting " + scenario.Name);
        scenario.UseChangeLog = False;
        scenarioManager.ScenarioList.Delete(scenario)
        _log(" ...done")
    _log(" ...finished");
        
def DeleteSimulations(scPath, days, maxNo):
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
    <Parameters>
    <Parameter name="scPath" type="string">scenario Path</Parameter>
    <Parameter name="days" type="int">delete simulations older than som many days</Parameter>
    <Parameter name="maxNo" type="int">max simulations to delete</Parameter>
    </Parameters>
    </Script>
    """
    d = DateTime.Now.AddDays(-days);
    _log("starting - " + scPath);
    _log("deleting older than - " + d.ToString("yyyy-MM-dd HH:mm:ss"));
    # Get a reference to the Scenario Manager
    scenarioManager = app.Modules.Get('Scenario Manager')

    # Use it for e.g. reading a Scenario
    scenario = scenarioManager.ScenarioList.Fetch(scPath)
    simlist = sorted(filter(lambda ss: ss.TimeOfSimulationRun < d and ss.ModelSetupId.Equals(scenario.ModelSetupId) , scenarioManager.GetSimulationsForScenario(scenario.Id)), key=lambda s: s.Name)

    _log( "%d simulations match criteria" %(simlist.Count));
    if simlist.Count>maxNo :
        _log( "deleting the oldest %d ..." %(maxNo));
        
    i=0
    for sim in simlist:
        if i==maxNo:
            _log( "stopping after " + str(maxNo) + " deletes")
            i=-1
            break;
        _log(" deleting " + sim.Name);
        for s in sim.ChildSimulations:
            s.UseChangeLog = False;
            if (s.IsRunning):
                # force delete -  enable by update status in database 
                _log ("    child simulation " + s.Name + " in status " + s.Status + " - force deleted !")                
                s.Status = "UNDEFINED"
                scenarioManager.SimulationList.Update(s);                         
 
        sim.UseChangeLog = False;
        if (sim.IsRunning):
            # force delete -  enable by update status in database 
            _log ("    in status " + sim.Status + " - force deleted !")
            sim.Status = "UNDEFINED"
            scenarioManager.SimulationList.Update(sim);         
            
        scenarioManager.SimulationList.Delete(sim, True)
        _log(" ...done");
        i = i + 1
    _log(" ...finished");

def DeleteTimeSeriesGroups(rootPath, days, maxNo):
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
    <Parameters>
    <Parameter name="rootPath" type="string">root group Path</Parameter>
    <Parameter name="days" type="int">delete timeseries groups with datename older than this number of days</Parameter>
    <Parameter name="maxNo" type="int">max simulations to delete</Parameter>
    </Parameters>
    </Script>
    """
    # Get a reference to the Time series Manager
    tsMgr = app.Modules.Get('Time series Manager')

    tsMgr.TimeSeriesGroupList.Query(Query())
    
    _log(" start " + rootPath);
    _log("Number of groups : " + str(tsMgr.TimeSeriesGroupList.Count));
    groupDate = DateTime.Now.AddDays(-days);
    groupPath= rootPath; #'/Forecasted/Outputs/FWOS/Mohawk/Hydraulic/NWSForecasts-Rules'
    groupList = sorted(tsMgr.TimeSeriesGroupList.FetchChildren(groupPath), key=lambda g: g.Name)
    i = 0
    for group in groupList:
        if i==maxNo:
            _log("stopping after " + str(maxNo) + " deletes");
            i=-1
            break;

        d = group.Name.Replace(".","-")
        if d.Contains(":") and DateTime.Parse(d)<groupDate:
            _log(" deleting " + group.Name)
            try:
                group.UseChangeLog = False;
                tsMgr.TimeSeriesGroupList.Delete(group, True)
                _log(" ...done ")
                i = i + 1
            except Exception as e:
                _log(DateTime.Now.ToString("HH:mm:ss") + " ...ERROR: " + str(e))
        else:
            _log("skipping " + group.Name)
    
    _log("Number of groups : " + str(tsMgr.TimeSeriesGroupList.Count));
    _log(" ...finished");            


def ExportDocument(docPath, directory):
    """
    <Script>
    <Author>ANK</Author>
    <Description>Export a document to a folder on disk</Description>
    <Parameters>
    <Parameter name="docPath" type="string">Full path to the document</Parameter>
    <Parameter name="directory" type="string">directory path on disk</Parameter>
    </Parameters>
    </Script>
    """
    
    _log( "Getting document " + docPath)

    # Get a reference to the Time series Manager
    docMgr = app.Modules.Get('Document Manager')
    doc = docMgr.DocumentList.Fetch(docPath)
    
    docFile = Path.Combine(directory, doc.Name)
    docMgr.DocumentList.Export(doc, docFile, True);

    _log( "... to " + docFile)
                           
def _log(msg):
    print("%s - %s" %(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"), msg));

clr.AddReference("Ionic.Zip")
from Ionic.Zip import *


def _ExportgetDocument(docPath, tempFolder):

    _log( "Getting document " + docPath)
    docMgr = app.Modules.Get("Document Manager")
    doc = docMgr.DocumentList.Fetch(docPath)
    
    docFile = Path.Combine(tempFolder, doc.Name)
    docMgr.DocumentList.Export(doc, docFile, True);

    if docPath.upper().EndsWith(".ZIP"):
        _unzipfile(docFile, tempFolder);
        try:
            _log( "deleting zip file")
            File.Delete(docFile);
        except:
            _log( "could not delete " + docFile)
    _log("...done")


        
def _unzipfile(zippath, unpackDirectory):

    _log( "unzipping " + zippath)
    with ZipFile.Read(zippath) as zip:
        for e in zip:
            _log( e.FileName)
            e.Extract(unpackDirectory, ExtractExistingFileAction.OverwriteSilently);
    _log( "...done")



clr.AddReference("DHI.Solutions.ScenarioManager.Interfaces")
clr.AddReference('DHI.Solutions.ScenarioManager.Tools.RStatisticsTool')
from DHI.Solutions.ScenarioManager.Interfaces import *
from DHI.Solutions.ScenarioManager.Tools.RStatisticsTool import *

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
    if sim==None:
        Message.ShowWarningDialog("Simulation was not found","Script")
        return
        
    sim.Status = "UNDEFINED"    
    simlist.Update(sim);

    for childsim in sim.ChildSimulations:
        childsim.Status = "UNDEFINED"    
        simlist.Update(childsim);
        
    # delete - if linked it will delete childre
    simlist.Delete(sim);
    
    # warn user if Shell is active
    if app.Shell != None:
        Message.ShowWarningDialog("Remember to refresh the Scenario Explorer","Script")

def MakeDateFromNow(days):
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>Calculate datetime offset from now</Description>
    <Parameters>
    <Parameter name="days" type="int">days</Parameter>
    </Parameters>
    </Script>
    """
    return DateTime.Now.Date.AddDays(-days)    

clr.AddReference("Npgsql")
from Npgsql import *

def WipeChangelogs(days):
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>remove changelogs older the specified number of days</Description>
    <Parameters>
    <Parameter name="days" type="int">days</Parameter>
    </Parameters>
    </Script>
    """

    d = DateTime.Now.Date.AddDays(-days)    
    _log( "removing changes before " + d.ToString("yyyy-MM-dd HH:mm:ss") )
    
    conn = app.WorkspaceConnection.Connection
    cmd = conn.CreateCommand()
    cmd.CommandText="DELETE FROM " + app.WorkspaceConnection.DefaultSchema + ".change_log WHERE datetime < '" + d.ToString("yyyy-MM-dd HH:mm:ss") + "'"
    cmd.ExecuteNonQuery()    
    
    _log( "done")

def ClearChangeLogsForJob(jobname):
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>Clear changelogs for a job and its job instances</Description>
    <Parameters>
    <Parameter name="jobname" type="string">Name of Job</Parameter>
    </Parameters>
    </Script>
    """
    jmgr = app.Modules.Get("Job Manager");
    chmgr = app.Modules.Get("ChangeLog Manager");
    
    job = jmgr.JobList.Fetch(jobname);
    jobinstances = jmgr.JobInstanceList.FetchJobInstance(job.Id);
    
    chmgr.Delete(job);
    for ji in jobinstances:
        chmgr.Delete(ji);
        
    pass;

def StackNetCDFfiles(scriptName, DirPath, SavePath, workingDir,docGroup):
    """
    <Script>
    <Author>JERR</Author>
    <Description>Runs an R script which stacks netcdf files </Description>
    <Parameters>
    <Parameter name="scriptName" type="string">Parameter of type int</Parameter>
    <Parameter name="DirPath" type="string">Location of t he netcdf file</Parameter>
    <Parameter name="SavePath" type="string">Output netCDF file path</Parameter>
    <Parameter name="workingDir" type="string">Temporary working directory</Parameter>
    <Parameter name="docGroup" type="string">Path to the R script in document manager</Parameter>
    </Parameters>
    </Script>
    """
    _log('Starting to stack GPM netcdf files')
    
    argumentString = '" "'.join([scriptName, DirPath, SavePath, workingDir]);
    argumentString = '"{0}"'.format(argumentString);
    
    try:
        # Get a reference to the Time series Manager
        docMgr = app.Modules.Get('Document Manager')
    
        docList = docMgr.DocumentList.FetchChildren(docGroup)
        Directory.CreateDirectory(workingDir)

        for doc in docList:
            ExportgetDocument(docGroup +'/'+ doc.Name,workingDir)
        
        print(argumentString)
        print(workingDir)
        
        RStatisticsTool(argumentString, workingDir)
        # Check if log file exists
        logFile = Path.Combine(workingDir,'Rlog.txt')
        if File.Exists(logFile):
            lines = File.ReadAllText(logFile)
            _log(lines)
            if 'Error' in lines:
                print('GPM netcdf stack failed')
                raise Exception('GPM Data download failed')
        else:
            print('Rlog.txt is missing')
            raise Exception('Rlog.txt is missing')
    finally:
        try:
            Directory.Delete(workingDir, True)
        except Exception as e:
            print(str(e))


def RStatisticsTool(argumentString, workingDir):
    """
    This tool calculates statistics by running R-Statistics.

    @param inputItems @type Array
        Tool input items

    @param argumentString @type System.String
        Argument string containing all arguments used for the execution 
        of R.

    @param workingFolder @type System.String
        Gets or sets the working folder for the script execution.

    @param use64Bit @type System.Boolean
        Indicate that the 64 bit version of R should be used for 
        execution.
    """
    tool = app.Tools.CreateNew('R-Statistics')
    tool.ArgumentString = argumentString
    tool.WorkingFolder = workingDir
    tool.Use64Bit = True
    tool.Execute()
    return tool.OutputItems

import os, shutil

def MoveFilesEUMETSAT(source, destination):
    """
    <Script>
    <Author>JERR</Author>
    <Description>Moves files from one directory to another</Description>
    <Parameters>
    <Parameter name="source" type="string">Parameter of type int</Parameter>
    </Parameters>
    <ReturnValue type="IType">Function returns object of type IType</ReturnValue>
    </Script>
    """
    # write your code here
    files = os.listdir(source)
    # files.sort()
    for f in files[0:-96]:
        _log('Moving file ' + f + ' to directory ' + source)
        src = Path.Combine(source, f)
        dst = Path.Combine(destination, f)
        shutil.move(src,dst)
        _log('Moving ' + f + 'done ')
        
import os
import datetime

def DeleteFilesBasedAge(path, days, fileExt):
    """
    <Script>
    <Author>JERR</Author>
    <Description>Delete specific files older than some days</Description>
    <Parameters>
    <Parameter name="path" type="string">Path to files which should be deleted</Parameter>
    <Parameter name="days" type="int">number of days back </Parameter>
    <Parameter name="fileExt" type="string">extension of files to be deleted </Parameter>
    </Parameters>
    </Script>
    """
    for file in os.listdir(path):
        if file.endswith(fileExt): # delete only files of particular extension
            fullpath   = os.path.join(path,file) 
            # get timestamp of file
            timestamp  = os.stat(fullpath).st_ctime 
            createtime = datetime.datetime.fromtimestamp(timestamp)
            now        = datetime.datetime.now()
            delta      = now - createtime
            # Delete files which were created specified days ago not the netdcf folder 
            if delta.days > days: 
#                print(fullpath, delta.days)
                try:
                    os.remove(fullpath)
                    _log('deleted %s'%file)
                except Exception as e:
                    _log('could not delete %s - ' %(file, str(e)))

def TempDirPath():
    """
    <Script>
    <Author>admin</Author>
    <Description>Creates temp folder</Description>
    </Script>
    """
    # write your code here
    try:
        tempFolder = Path.Combine(DssPath.GetTemporaryDirectory(), Path.GetRandomFileName())
        return tempFolder
    
    except Exception as e:
        _logprint("Problem creating tempDir : " + str(e))
        




