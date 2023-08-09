import clr
clr.AddReference('DHI.Solutions.GISManager.UI.Tools.ASCIITemporalImportTool')
clr.AddReference('DHI.Solutions.GISManager.UI.Tools.ASCIIGridImportTool')
from DHI.Solutions.GISManager.UI.Tools.ASCIITemporalImportTool import *
import os
# import of Directory to get to files
from System.IO import Directory, File, Path
clr.AddReference('DHI.TimeSeries')
clr.AddReference('DHI.Solutions.TimeseriesManager.Tools.Processing')
import DHI.TimeSeries

clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import EUMWrapper
clr.AddReference('DHI.Solutions.GISManager.Tools.RasterToDatabaseTool')
from DHI.Solutions.GISManager.Tools.RasterToDatabaseTool import *


def ImportAsciiRaster(folder,gisgroup):
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
    <Parameters>
    <Parameter name="folder" type="string">path on disk to the directory of ascii grid -files</Parameter>
    <Parameter name="gisgroup" type="string">target group - will be created if it does not exist</Parameter>
    </Parameters>
    </Script>
    """
            
       
    # Variables
    gisgroup = '/WRIS/Overlays'
    coordinateSystemName = 'GGRS87 / Greek Grid';
    folder = 'C:\Temp\MIKEFLOODCheckedOut01\OUTPUT_DATA\TemporalRasterMaxH'
    itemName = 'Water Level'
    unitName = 'meter'
    gisgrouppath = '/WRIS/Overlays/TemporalRasterMaxH'
    gisgrouppath2 ='/WRIS/Overlays/RasterName'
    
    
    gisManager = app.Modules.Get('GIS Manager')
    existingRaster = gisManager.RasterList.Fetch(gisgrouppath2)

    gisManager.RasterList.Delete(existingRaster)  
    
    if (Directory.Exists(folder) == False):
        raise Exception('Source directory does not exist: ' + folder)
   
    gisManager = app.Modules.Get('GIS Manager');
           
    # Find the coordinate system.
    coordinateSystem = None;
    
    for cSystem in gisManager.CoordinateSystemList.GetAll():
        if (cSystem.Name == coordinateSystemName):
            coordinateSystem = cSystem;
            break;
    
    if (coordinateSystem == None):
        raise Exception('Coordinate system not found: ' + coordinateSystemName)
    
    # Find the raster group to import the raster to (input item).
    rasterGroup = gisManager.RasterGroupList.Fetch(gisgroup);
    
    if (rasterGroup == None):
        raise Exception('Import raster group was not found: ' + rasterGroupPath)
    
    # Find the id of the item and unit number of the item.
    eumItem = clr.StrongBox[int]();
    eumUnit = clr.StrongBox[int]();

    EUMWrapper.GetItemTypeTag(itemName, eumItem);
    EUMWrapper.GetUnitTag(unitName, eumUnit);
           
    existingRaster = gisManager.RasterList.Fetch(gisgrouppath)

 
    if (existingRaster != None):

        gisManager.RasterList.Delete(existingRaster)
        
    tool = app.Tools.CreateNew('Import temporal rasters from ASCII files')
    tool.InputItems.Add(rasterGroup);
    tool.DirectoryPath = folder         
    tool.DateTimeFilenameMask = 'yyyyMMddHHmm'
    tool.CoordinateSystem = coordinateSystem;
    tool.AddToExistingRaster = False 
    tool.Enum_Item = eumItem.Value
    tool.Enum_Unit = eumUnit.Value
#    
    tool.Execute() 
    try:  
    
        rasterPath = gisgroup + '/TemporalRasterMaxH'
        raster=gisManager.RasterList.Fetch(rasterPath)
        
        raster.Name="RasterName"
        raster.DefaultSymbology="<RasterLayerDefinition StyleType=\"Simple\" RasterStyleType=\"ValueRanges\" Name=\"4?�e?? ??????s? �????? ?at????s?? (m)\" IsVisible=\"True\" OwnOverlay=\"False\" ShowInLegend=\"True\" DispalyMapScale=\"1:577,791\"><LayerStyleDefinition Attribute=\"\" BaseColor=\"Color [Black]\" ResetMaxMin=\"True\" NumOfIntervals=\"4\" Color=\"Color [A=255, R=176, G=225, B=255]\" Transparency=\"0\" ColorTransparency=\"0\" OuterLineType=\"Solid\" OuterLineThickness=\"1\"><ValueRangeStyleDefinition MinValue=\"0.5\" MaxValue=\"1\" Color=\"Color [A=255, R=176, G=225, B=255]\" ColorTransparency=\"0\" /><ValueRangeStyleDefinition MinValue=\"1\" MaxValue=\"1.5\" Color=\"Color [A=255, R=0, G=128, B=192]\" ColorTransparency=\"0\" /><ValueRangeStyleDefinition MinValue=\"1.5\" MaxValue=\"2\" Color=\"Color [A=255, R=0, G=64, B=128]\" ColorTransparency=\"0\" /><ValueRangeStyleDefinition MinValue=\"2\" MaxValue=\"20\" Color=\"Color [A=255, R=255, G=0, B=128]\" ColorTransparency=\"0\" /><AllOtherValuesStyleDefinition /></LayerStyleDefinition><LayerScaleRange /></RasterLayerDefinition>"
      
        gisManager.RasterList.Update(raster)
         
    except Exception as e:
        print(str(e))   
        
    
    gisManager.RasterList.Update(raster)    
    return;
    
    








