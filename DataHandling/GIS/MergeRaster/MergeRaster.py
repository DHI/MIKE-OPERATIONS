def MergeRaster(rasterGroupPath):
    """
    <Script>
    <Author>jalu</Author>
    <Description>test script to add rasters within one group. It assumes that each raster has one timestep</Description>
    <Parameters>
    <Parameter name="rasterGroupPath" type="string">path to raster group</Parameter>
    </Parameters>
    </Script>
    """
    # get gis module
    gisMgr = app.Modules.Get("GIS Manager")
    
    # fetch all raster to list and sort by name
    rasterList = gisMgr.RasterList.FetchChildren(rasterGroupPath)
    rasterList = sorted(rasterList, key=lambda x: x.Name)
    
    # create target raster group
    targetGroupPath = rasterGroupPath + "/Processed"
    
    if gisMgr.RasterGroupList.Fetch(targetGroupPath) == None:
        targetGroup = gisMgr.RasterGroupList.CreateNew(targetGroupPath)
        gisMgr.RasterGroupList.Add(targetGroup)
        targetGroupID = targetGroup.Id
    else:
        targetGroup = gisMgr.RasterGroupList.Fetch(targetGroupPath)
        targetGroupID = targetGroup.Id
    
    # create target raster and add it to database (it replaces existing rasters)
    if rasterList.Count > 0:
        raster = rasterList[0]
        targetRaster = raster.Clone()
        targetRaster.Name = "gfs_latest"
        targetRaster.GroupId = targetGroupID
        
        r = gisMgr.RasterList.Fetch(targetGroupPath + "/" + targetRaster.Name)
        if r != None:
            gisMgr.RasterList.Delete(r)
        
        # add raster bands to target raster
        timeStep = rasterList[0].TimeSteps[0]
        for raster in rasterList:
            RasterBand = raster.RasterBands[0]
            RasterBand.FillData()
            # timeStep = raster.TimeSteps[0]
            
            # add raster band to target raster
            BandClone = RasterBand.Clone()
            targetRaster.RasterBands.Add(BandClone, timeStep)
            
            # increase time step by one hour
            timeStep = timeStep.AddHours(1)
         
        # add target raster to database
        gisMgr.RasterList.Add(targetRaster)
    else:
        print("There are no raster in group " + rasterGroupPath)
        return
