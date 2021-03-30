import clr
clr.AddReference('DHI.Solutions.GISManager.Tools.ShapeFileExportTool')
from DHI.Solutions.GISManager.Tools.ShapeFileExportTool import *
clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import *

def ExportShapefiles():
    """
    <Script>
    <Author>admin</Author>
    <Description>This script bulk-exports features classes from a group to a local folder.</Description>
    <Parameters>
    </Parameters>
    </Script>
    """
    inputGroup = "/shapes"
    exportFolder = "C:\\DHI\\Test\\"
    
    gismod = app.Modules.Get("GIS Manager")
    fcgroup = gismod.FeatureClassGroupList.Fetch(inputGroup)
    
    # build the query object full of one element with a like query
    q = Query();
    q.Add(QueryElement('GroupId', fcgroup.Id, QueryOperator.Eq));
        
    fcList = gismod.FeatureClassList.Fetch(q)
    for fc in fcList:
        tool = app.Tools.CreateNew('Export to shape file')
        tool.InputItems.Add(fc)
        tool.FilePath = exportFolder  + fc.Name + ".shp"
        tool.ExportMetadata = False
        tool.CoordinateSystemName = ''
        tool.Execute()



