 
import clr
clr.AddReference("System")
from System import *
clr.AddReference('mscorlib')

def DeleteInitialCondition(modelsetuppath, id):
    """
    <Script>
    <Author>ANK</Author>
    <Description>This script delete a specific initial condition for a model</Description>
    <Parameters>
    <Parameter name="modelsetuppath" type="string">The full path of the model setup in the database (copy Full Path)</Parameter>
    <Parameter name="id" type="string">guid of the initial condition to delete</Parameter>
    </Parameters>
    </Script>
    """
 
    scm = app.Modules.Get("Scenario Manager")
    ms = scm.ModelSetupList.Fetch(modelsetuppath)
    if ms!=None:
        print "found model setup " + ms.Name;        
        guid = Guid.Parse(id);
        ini = ms.ModelInitialConditionList.Fetch(guid)
        if ini != None:
            # check it is not used in any scenarios
            bOK = True;
            for sc in scm.ScenarioList.FetchAll():
                if (sc.ModelSetupId.Equals(ms.Id) and sc.InitialCondition!=""):
                    pini = scm.ScenarioList.GetModelInitialConditionParser(sc);
                    if pini.GetInitialCondition().Id.Equals(guid):
                        print "Initial condition is used - cannot delete"
                        bOK = False;
            
            if bOK:
                print "deleting " + ini.ToString();
                ms.ModelInitialConditionList.Delete(ini);
            else:
                print "cannot delete";
        else:
            print "not found " + id;
    else:
        print "model setup not found";
        
    print "done";

    """
    <Script>
    <Author>ANK</Author>
    <Description>This script deletes initial conditions for a model setup from the database based upon an age criteria</Description>
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
        print "Deleting initial conditions for modelsetup \'%s\' of type(s) \'%s\' older than %d days" %(modelsetupPath, types, days);
        scmgr.ModelSetupList.Fill(modelsetup);
        initialConditions = modelsetup.ModelInitialConditionList.GetAll();
        initialConditionsToDelete = [];
        for ic in initialConditions:
            icType = ic.Type.ToString().upper();
            if ((ic.EndDate < d) & (upperTypes.IndexOf(icType)>0)):
                initialConditionsToDelete.Add(ic);  
                
        if (initialConditionsToDelete.Count>0):
            for ic in initialConditionsToDelete:
                print "\'%s\' : %s - %s : %s" %(ic.Name, ic.StartDate.ToString("yyyy-MM-dd hh:mm:ss"), ic.StartDate.ToString("yyyy-MM-dd hh:mm:ss"), ic.Type.ToString());
                modelsetup.ModelInitialConditionList.Delete(ic);            
        else:
            print "Nothing to delete"	
