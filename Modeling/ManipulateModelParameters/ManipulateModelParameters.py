import clr
clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import *
from System import *
from System.Reflection import BindingFlags

clr.AddReference('System.Core')
from System.Linq import Enumerable

modelName = "Demo"
simulation = '/Group of Demo/Demo/Scenario of Demo/Simulation of Scenario of Demo at 2018-09-05 16:39:46' 
       
def ListModelObject(t):
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>Script to list  model objects.</Description>
    <Parameters>
    <Parameter name="t" type="int">Define what to list: 
    '1' will list all the parameters visible by the model adaptor 
    '2' will list all the parameters used in the scenarion called
    '3' will list all the parameters used in the simulation</Parameter>
    </Parameters>
    </Script>
    """

    scenario = '/Group of ' + modelName + '/' + modelName + '/Scenario of ' + modelName
    
    # get the manager
    scm = app.Modules.Get('Scenario Manager');

    # get the model setup
    modelsetup = scm.ModelSetupList.Fetch('/Group of ' + modelName+ '/' + modelName);
    # fill details of it - performs queries on all lists
    scm.ModelSetupList.Fill(modelsetup);
    
    if (t==1):    
        # inspect some model object parameters
        for mo in modelsetup.ModelObjectList.GetAll():
            printMO(mo);
    
    if (t==2):
        # getthe sccenario
        sc = scm.ScenarioList.Fetch(scenario);
        scm.ScenarioList.Fill(sc);
        for mo in sc.ScenarioModelObjectList.GetAll():
            printMO(mo);

    if (t==3):
        # getthe sccenario
        sc = scm.ScenarioList.Fetch(scenario);
        scm.ScenarioList.Fill(sc);
        # get the simulation
        
        sim = scm.SimulationList.Fetch(simulation);
        scm.SimulationList.Fill(sim);
        for mo in sim.SimulationModelObjectList.GetAll():
            printMO(mo);
     
def UpdateModelObject():
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>test to update the model object</Description>
    </Script>
    """
    
    scenario = '/Group of ' + modelName + '/' + modelName + '/Scenario of ' + modelName
    
    # get the manager
    scm = app.Modules.Get('Scenario Manager');
    
    # get the scenario
    sc = scm.ScenarioList.Fetch(scenario)
    scm.ScenarioList.Fill(sc);

    # find a model object
    molist = sc.ScenarioModelObjectList.GetAll();
    for mo in molist:
        if (mo.Name == 'R5 (Reservoir 1)'):
            # try to set the Name - this should not reflect back in the database
            # it appears to go, but the XML is not changed.... as expected because
            # the Name property is readonly.
            pmo = mo.GetObject();
            try:
                # Edit InitialWaterLevel paramter
                parampath = '.InitialWaterLevel';
                param = mo.GetParameter(parampath);
                param.Value = param.Value + 2;
                mo.SetParameter(param, parampath); # put it back in the object
                
                # get the paramter
                parampath = '.SedimentDistributionType';
                mo.SetParameterValue('Type2_FloodPlainFoothill', parampath); # change the value directly
    
                # update back to the database
                sc.ScenarioModelObjectList.Update(mo);
            except Exception as e:
                print e;
    pass;    

def UpdateCrossSectionObject():
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>test to update the model object</Description>
    </Script>
    """
    
    scenario = '/Group of ' + modelName + '/' + modelName + '/Scenario of ' + modelName
    
    # get the manager
    scm = app.Modules.Get('Scenario Manager');
    
    # get the scenario
    sc = scm.ScenarioList.Fetch(scenario)
    scm.ScenarioList.Fill(sc);

    # find a model object
    molist = sc.ScenarioModelObjectList.GetAll();
    for mo in molist:
        if (mo.Name == 'CALI - 4402,5 - QPoint'):
            # try to update the CrossSections
            pmo = mo.GetObject();
            if (pmo.GetType().ToString()=='DHI.Solutions.ScenarioManager.ScenarioModelObject.MIKE11CrossSection'):
                try:
                    # get the paramter
                    parampath = '.CrossSection';
                    param = mo.GetParameter(parampath);
                    v = param.Value;
                    
                    # update the parameter value directly in model object
                    pmo.CrossSection.Value = "123" + v;
                    
                    # update the parameter value directly in model object
                    param.Value = "abc" + v;
                    
                    # write it back 
                    mo.SetParameter(param, parampath);
        
                    # reset value to original
                    mo.SetParameterValue(v, parampath);
                    
                    # update back to the database
                    # sc.ScenarioModelObjectList.Update(mo);
                except Exception as e:
                    print e;
            pass;

    pass;    
    
def printMO(mo):
    pmo = mo.GetObject();
    if (pmo!=None):
        # we have model object
        print "\n%s - %s" %(mo.Name, pmo.GetType().ToString());
        dict = mo.GetPathsAndParameters();
        for kv in dict:
            print '   ' + kv.Key + ' = ' + kv.Value.Value.ToString() + '     (readonly='+kv.Value.ReadOnly.ToString()+')';
            print '-- ' + mo.GetParameterPath(kv.Value)+ ' = ' + mo.GetParameter(kv.Key).Value.ToString();
            print '** ' + mo.GetParameterPath(kv.Value)+ ' = ' + mo.GetParameterValue(kv.Key).ToString();
    
