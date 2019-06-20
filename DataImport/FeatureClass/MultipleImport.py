import clr
clr.AddReference('DHI.Solutions.GISManager.UI.Tools.ShapeFileImportTool')
from DHI.Solutions.GISManager.UI.Tools.ShapeFileImportTool import *

gisMgr = app.Modules.Get('GIS Manager')

from System.IO import Directory, Path

def RunShapeFileImportTool():
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
    </Script>
    """
    # Get all the files in the directory
    directory = r"C:\temp\Del_Shape"    #directory with shape files
    FileList = Directory.GetFiles(directory)
    DB_folder = '/xx'   #folder to import shape files to

    for file in FileList:
        fullPath = Path.Combine(directory, file)
        if Path.GetExtension(fullPath) =='.shp':            
            featureClassName = '/' +Path.GetFileNameWithoutExtension(fullPath)   #filenameWithoutExtension
        
            inputItems = gisMgr.FeatureClassGroupList.Get(DB_folder)
            if inputItems == None:
                inputItems = gisMgr.FeatureClassGroupList.CreateNew(DB_folder)
            
            coordinateSystem = gisMgr.DefaultCoordinateSystem
            ShapeFileImportTool(inputItems, coordinateSystem, featureClassName, 
                fullPath)



def ShapeFileImportTool(inputItems, coordinateSystem, featureClassName, 
        filePath):
    """
    This tool imports data in shape files. Shape files can only be 
        imported if the projection is already defined in the DSS. 
        Otherwise, add the projection mapping to ESRIProjections.txt 
        file in the application folder.

    @param inputItems @type Array
        Tool input items

    @param coordinateSystem @type 
        DHI.Solutions.GISManager.Interfaces.ICoordinateSystem
        The coordinate system of the data to be imported. This is 
        automatically filled in case shape file contains a corresponding 
        prj file.

    @param featureClassName @type System.String
        The full path of the feature class name to import the data to.

    @param filePath @type System.String
        The path of the file to import
    """
    tool = app.Tools.CreateNew('Import from shape file')
    if isinstance(inputItems,list):
        for inputItem in inputItems:
            tool.InputItems.Add(inputItem)
    else:
        if inputItems <> None:
            tool.InputItems.Add(inputItems)
    tool.CoordinateSystem = coordinateSystem
    tool.FeatureClassName = featureClassName
    tool.FilePath = filePath
    tool.Execute()
    #return tool.OutputItems
