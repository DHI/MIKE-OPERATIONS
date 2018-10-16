import clr
clr.AddReference('DHI.Solutions.Generic')
clr.AddReference('DHI.Solutions.Generic.Tools')
clr.AddReference('DHI.Solutions.GISManager.Tools.RasterProcessing')
clr.AddReference('DHI.Solutions.GISManager.Tools.RasterToDatabaseTool')
clr.AddReference('DHI.Solutions.GISManager.Tools.RasterQueryTool')

from DHI.Solutions.Generic import *
from DHI.Solutions.Generic.Tools import *
from DHI.Solutions.GISManager.Tools.RasterProcessing import *
from DHI.Solutions.GISManager.Tools.RasterToDatabaseTool import *
from DHI.Solutions.GISManager.Tools.RasterQueryTool import *
from System import DateTime

def GenerateMap():
    """
    <Script>
    <Author>aaug</Author>
    <Description>This script generate map showing level of lakes based on maimum forecast WL</Description>
    </Script>
    """
    scenarioPath = "/MYDRO_ECMWF/MHYDRO_ECMWF_20180910/Scenario of MHYDRO_ECMWF_20180910"
    outputTimeseriesName = "Vierwaldstaettersee - 19186.5 - HPoint-Water level"
    inputRasterPath = "dhm100m_viwa"
    outputRasterName = "OutputMap"
    
#   Get latest simulation
    scmgr = app.Modules.Get("Scenario Manager")
    scenario = scmgr.ScenarioList.Fetch(scenarioPath)
    allSimulationList = scmgr.SimulationList.FetchAll()
    latestSimulation = None
    for simulation in allSimulationList:
        if simulation.ScenarioId == scenario.Id:
            if(latestSimulation == None):
                latestSimulation = simulation
            if (simulation.TimeOfSimulationRun > latestSimulation.TimeOfSimulationRun):
                latestSimulation = simulation
    print "Latest simulation = " +latestSimulation.ToString()
    
#   Get output timeseries 
    simulationOutputTimeseries=None;
    for timeseries in simulation.SimulationOutputTimeseriesList:
        if (timeseries.Name == outputTimeseriesName):
            simulationOutputTimeseries = timeseries;
            break
    if simulationOutputTimeseries != None:
        print "Output timeseries found"
    else :
        print "Output timeseries not found"
        exit()
        
#   Get maximum value in forecast period 
    tsmod = app.Modules.Get("Time series Manager")
    outputTimeseries = tsmod.TimeSeriesList.Fetch(simulationOutputTimeseries.TimeseriesId)
    q = Query()
    q.Add(QueryElement("datetime", DateTime.Now.Date, QueryOperator.Gte))
    timesteps = outputTimeseries.Fetch(q)
    max = -9999
    for t in timesteps:
        if t.YValue > max:
            max = t.YValue
    print "Max value = " + max.ToString()
    
#   Prepare raster processor 
    gismod = app.Modules.Get("GIS Manager")
    inputItems = []
    intputRaster = gismod.RasterList.Fetch("/" + inputRasterPath)
    inputItems.append(intputRaster)
    
    mapping = {inputRasterPath : intputRaster}
    print 'running...'
    
#  Run raster processor and save output
    raster = gismod.RasterList.Fetch("/" + outputRasterName)
    if(raster != None):
        gismod.RasterList.Delete(raster.Id)
    outputRaster = RasterCalculatorTool(inputItems,"IF([value] >  " + max.ToString() + ", [value], 0)",mapping)
    outputRaster.Name = outputRasterName 
    gismod.RasterList.Add(outputRaster)
    
    print 'done'

def RasterCalculatorTool(inputItems, formula, nameMapping):
    """
    This tool performs raster math on input rasters using syntax 
        commonly found in spreadsheet programs.

    @param inputItems @type Array
        Tool input items

    @param formula @type System.String
        The formula to apply for the calculation. 

The syntax should match the one used in the Spreadsheet Manager.
This tool creates a spreadsheet from the Spreadsheet Manager in memory 
        and interprets the formula by substituting raster names by 
        raster values in the formula. 
Any formula that works in the Spreadsheet Manager will work in the 
        Raster Calculator.

This tool can be used in two ways.

Entering raster names will produce one output raster. This requires 
        mapping the input rasters in the Mapping property within square 
        brackets (e.g. “[myraster]”) 
= [raster1] + [raster2]: Calculates the sum of raster1 and raster2. 
= AVERAGE([raster1], [raster2]: [raster3], [raster4]). Calculates the 
        average value of 4 rasters.

Specifying “[value]” mapping will produce one output for each input. 
        "Value" shall not be mapped in the Mapping property.
= SQRT([value]): For each input raster, calculates the square root and 
        returns a corresponding output raster. 
= IF([value] < 1000, 0, [value]): For each input raster, replaces all 
        values in input rasters below 1000 with 0.

Missing or "No Data" values can be represented in the formula with any 
        of the following key words (which must be in brackets): [null], 
        [nothing], [nodata], [novalue], [missing], [missingdata], 
        [missingvalue].
= IF([value] < 1000, [missing], [value])

    @param nameMapping @type 
        System.Collections.Generic.IDictionary`2[[System.String, 
        mscorlib],[DHI.Solutions.GISManager.Interfaces.IRaster, 
        DHI.Solutions.GISManager.Interfaces>
        The mapping of raster names used in the formula to the input 
        rasters. Do not include brackets.
    """
    tool = app.Tools.CreateNew('Raster Calculator')
    if isinstance(inputItems,list):
        for inputItem in inputItems:
            tool.InputItems.Add(inputItem)
    else:
        if inputItems <> None:
            tool.InputItems.Add(inputItems)
    tool.Formula = formula
    tool.NameMapping = nameMapping
    tool.Execute()
    
    return tool.OutputItems[0]
