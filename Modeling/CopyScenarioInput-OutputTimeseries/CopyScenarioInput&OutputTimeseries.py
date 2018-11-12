def copyScenarioInOut():
    """
    <Script>
    <Author>RASK</Author>
    <Description>This script copies </Description>
    </Script>
    """
    # write your code here
    # Get a reference to the Scenario Manager
    sceMgr = app.Modules.Get('Scenario Manager')
    originalScenario = '/Group of Model_Real_Time/MyModel/MyScenario1'
    destinationScenario = '/Group of Model_Real_Time/MyModel/MyScenario2'
	
    # Use it to  read a Scenario
    sce1 = sceMgr.ScenarioList.Fetch(originalScenario)
    sce2 = sceMgr.ScenarioList.Fetch(destinationScenario)

    copyScenarioInputimeseries(sce1,sce2)
    copyScenarioOutputimeseries(sce1,sce2)
	
def copyScenarioInputimeseries(source, target):
    """
    <Script>
    <Author>admin</Author>
    <Description>copy output time series definitions betweensource and target</Description>
    <Parameters>
    <Parameter name="source" type="IScenario">input scenario</Parameter>
    <Parameter name="target" type="IScenario">output scenario</Parameter>
    </Parameters>
    </Script>
    """
    sourceMS = source.ModelSetup
    sourceMOList = sourceMS.ModelObjectList.GetAll()
    sourceMOTSList = sourceMS.ModelInputTimeseriesList
    
    targetMS = target.ModelSetup
    targetMOList = targetMS.ModelObjectList.GetAll()
    targetMOTSList = targetMS.ModelInputTimeseriesList 
    
    notfound = 0
    mitsList = []
    for sits in source.ScenarioInputTimeseriesDefinitionList.GetAll():
        msg = sits.Name
        # check if we have this in target                                        
        mits = filter(lambda x: x.Name.startswith(sits.Name), targetMOTSList)
        if len(mits) >= 1:
            msg = msg + "  / " + mits[0].Name
            mitsList.append(mits[0]);
        else:
            arrsits = sits.Name.split(" - ")                    
            if len(arrsits) == 1 or len(arrsits) == 3 :
                mits = filter(lambda x: x.Name.startswith(arrsits[0]), targetMOTSList)
                if len(mits) == 1:
                    msg = msg + "  / " + mits[0].Name
                    mitsList.append(mits[0]);
                else:
                    notfound =  notfound + 1
                    msg = msg + "  - ***** NOT INCLUDED *****"
            else:
                notfound =  notfound + 1
                msg = msg + "  - ***** NOT INCLUDED *****"

        print msg
        
    print notfound, "not found"        
    if len(mitsList) >0:
        print "inserting ", len(mitsList)
        target.Include(mitsList);
        

def copyScenarioOutputimeseries(source, target):
    """
    <Script>
    <Author>admin</Author>
    <Description>copy output time series definitions between source and target</Description>
    <Parameters>
    <Parameter name="source" type="IScenario">input scenario</Parameter>
    <Parameter name="target" type="IScenario">output scenario</Parameter>
    </Parameters>
    </Script>
    """
    sourceMS = source.ModelSetup
    sourceMOList = sourceMS.ModelObjectList.GetAll()
    sourceMOTSList = sourceMS.ModelOutputTimeseriesList
    
    targetMS = target.ModelSetup
    targetMOList = targetMS.ModelObjectList.GetAll()
    targetMOTSList = targetMS.ModelOutputTimeseriesList 
    
    nameFilter = ''
    targetMOTSdict = {}
    for item in filter(lambda x: x.Name.startswith(nameFilter), targetMOTSList):        
        k = item.Name.split(" - ")[0]
        if k in targetMOTSdict.keys():
            targetMOTSdict[k].append(item)
        else:
            targetMOTSdict[k] = [item]
            
    notfound = 0
    motsList = []
    for sots in filter(lambda x: x.Name.startswith(nameFilter), source.ScenarioOutputTimeseriesDefinitionList.GetAll()):
        msg = sots.Name
        # check if we have this in target                                        
        arrsots = sots.Name.split(" - ")
        if arrsots[0] in targetMOTSdict.keys():
            mots = targetMOTSdict[arrsots[0]]
            if len(mots) == 1 :
                msg = msg + "  / " + mots[0].Name
                motsList.append(mots[0]);
            else:
                mots = filter(lambda x: x.Name == sots.Name, mots)
                if len(mots) == 1:
                    msg = msg + "  / " + mots[0].Name
                    motsList.append(mots[0]);
                else:
                    notfound = notfound + 1
                    msg = msg + "  - ***** NOT INCLUDED *****"
        else:
            notfound = notfound + 1
            msg = msg + "  - ***** NOT INCLUDED *****"

        print msg

    print notfound, "not found"        
    if len(motsList) >0:
        print "inserting ", len(motsList)
        target.Include(motsList);
