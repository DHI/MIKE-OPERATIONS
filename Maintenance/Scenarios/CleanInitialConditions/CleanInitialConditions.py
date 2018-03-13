 
import clr
clr.AddReference("System")
from System import *
clr.AddReference('mscorlib')


def ManageInitialConditions(modelsetupPath, days, types):
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
