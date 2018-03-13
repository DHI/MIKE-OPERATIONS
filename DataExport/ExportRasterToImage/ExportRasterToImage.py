import os,subprocess

def ExportRasters():
    """
    <Script>
    <Author>RASK</Author>
    <Description>This script exports the flood raster to to tif ın order to be displayed in GeoServer</Description>
    <Parameters>
    </Parameters>
    </Script>
    """
    # write your code here
    
    # Get a reference to the GIS Manager
    gisMgr = app.Modules.Get('GIS Manager')

    # Use it for e.g. reading a Feature class
    rl = gisMgr.RasterList.FetchChildren('/Publish/FloodExtent')

    
    for r in rl:
        subprocess.Popen("C:\\Program Files\\GDAL\\gdal_translate.exe -of GTIFF \"PG:host=localhost dbname='BlackSea' user='postgres' password='Aaa123456' schema='workspace1' table='fc_" + str(r.Id).replace('-','') + "' mode=2\" C:\\DHI\\GeoServerData\\data\\Rasters\\" + r.Name + ".tif")
        
     
