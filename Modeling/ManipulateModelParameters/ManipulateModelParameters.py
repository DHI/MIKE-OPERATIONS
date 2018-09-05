import clr
clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import *
from System import *
from System.Reflection import BindingFlags

clr.AddReference('System.Core')
from System.Linq import Enumerable

def ListModelObject(t, m):
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>Script to list  model objects.</Description>
    <Parameters>
    <Parameter name="t" type="int">Define what to  consider. 
    '1' will list all the parameters visible by the model 
    '2' will list all the parameters used in the scenarion called ""
    '3' will simulation) </Parameter>
    <Parameter name="m" type="string">model name (not the path)</Parameter>
    </Parameters>
    </Script>
    """
    # get the manager
    scm = app.Modules.Get('Scenario Manager');

    # get the model setup
    modelsetup = scm.ModelSetupList.Fetch('/Group of ' + m+ '/' + m);
    # fill details of it - performs queries on all lists
    scm.ModelSetupList.Fill(modelsetup);
    
    if (t==1):    
        # inspect some model object parameters
        for mo in modelsetup.ModelObjectList.GetAll():
            printMO(mo);
    
    if (t==2):
        # getthe sccenario
        sc = scm.ScenarioList.Fetch('/Group of ' + m + '/' + m + '/Scenario of ' + m);
        scm.ScenarioList.Fill(sc);
        for mo in sc.ScenarioModelObjectList.GetAll():
            printMO(mo);

    if (t==3):
        # getthe sccenario
        sc = scm.ScenarioList.Fetch('/Group of ' + m + '/' + m + '/Scenario of ' + m);
        scm.ScenarioList.Fill(sc);
        # get the simulation
        sim = scm.SimulationList.Fetch('/Group of ' + m + '/' + m + '/Scenario of ' + m  + '/Simulation of Scenario of ' + m);
        scm.SimulationList.Fill(sim);
        for mo in sim.SimulationModelObjectList.GetAll():
            printMO(mo);


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
            
            

def TestUpdateModelObject():
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>test to update the model object</Description>
    </Script>
    """

    # get the manager
    scm = app.Modules.Get('Scenario Manager');

    # get the scenario
    sc = scm.ScenarioList.Fetch('/Group of m11/m11/Scenario of m11')
    scm.ScenarioList.Fill(sc);

    # find a model object
    molist = sc.ScenarioModelObjectList.GetAll();
    for mo in molist:
        if (mo.Name == 'CALI - 4402,5 - QPoint'):
            # try to set the Name - this should not reflect back in the database
            # it appears to go, but the XML is not changed.... as expected because
            # the Name property is readonly.
            pmo = mo.GetObject();
            try:
                # get the paramter
                parampath = '.Name';
                param = mo.GetParameter(parampath);
    
                # give it a new value
                param.Value = '123';
                # put it back in the object
                mo.SetParameter(param, parampath);
                # change the value directly
                mo.SetParameterValue('yyy', parampath);
    
                # update back to the database
                # sc.ScenarioModelObjectList.Update(mo);
            except Exception as e:
                print e;

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
    
def Test2(t, m):
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>Script to test model objects</Description>
    <Parameters>
    <Parameter name="t" type="int">test 1=model, 2=scenario, 3=simulation</Parameter>
    <Parameter name="m" type="string">model name - m11 / mb</Parameter>
    </Parameters>
    </Script>
    """
    # get the manager
    scm = app.Modules.Get('Scenario Manager');

    # get the model setup
    modelsetup = scm.ModelSetupList.Fetch('/Group of ' + m+ '/' + m);
    # fill details of it - performs queries on all lists
    scm.ModelSetupList.Fill(modelsetup);
    print 'has scenarios = ' + modelsetup.HasScenario.ToString();
    # getthe sccenario
    sc = scm.ScenarioList.Fetch('/Group of ' + m + '/' + m + '/Scenario of ' + m);
    scm.ScenarioList.Fill(sc);
    print 'has simulations = ' + sc.HasSimulations.ToString();
    # get the simulation
    sim = scm.SimulationList.Fetch('/Group of ' + m + '/' + m + '/Scenario of ' + m  + '/Simulation of Scenario of ' + m);
    scm.SimulationList.Fill(sim);
    
