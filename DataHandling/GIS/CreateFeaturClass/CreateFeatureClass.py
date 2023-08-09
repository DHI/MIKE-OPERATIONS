import clr
clr.AddReference("DHI.Solutions.GISManager.Interfaces")
from DHI.Solutions.GISManager.Interfaces import *
import System

def CreateFeatureClass():
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
    </Script>
    """
    # write your code here
    pass;

    _gisModule = app.Modules.Get("GIS Manager");
    cs = _gisModule.CoordinateSystemList.Get(4326);
    geoType = GeometryType.Point;
    fcname = "myfc"
    
    oldfc = _gisModule.FeatureClassList.Fetch("/" + fcname)
    if oldfc != None:
        _gisModule.FeatureClassList.Delete(oldfc)
        
    featureClass = _gisModule.FeatureClassList.CreateNew();
    featureLookup = []
    
    featureClass.Name = fcname;
    featureClass.IsReadOnly = False;
    featureClass.CoordinateSystem = cs;
    featureClass.GeometryType = geoType;

    nameAttribute = featureClass.AttributeList.CreateNew();
    nameAttribute.Name = "Name";
    nameAttribute.Type = nameAttribute.Name.GetType();
    nameAttribute.MaxLength = 40;
    featureClass.AttributeList.Add(nameAttribute);
    featureClass.DisplayAttribute = "Name";

    attribute = featureClass.AttributeList.CreateNew();
    attribute.Name = "ModelObjectName";
    attribute.Type = attribute.Name.GetType();
    attribute.MaxLength = 255;
    featureClass.AttributeList.Add(attribute);
    
    for i in range(0,100000):
        feature = featureClass.CreateNew();
        geometry = "POINT[ 1 1]";
        feature.Geometry.FromWKT(geometry);
        n= geoType.ToString() + " " + str(i);
        #print(n)
        feature["name"] = n;
        feature["modelobjectname"] = n;
        featureClass.Add(feature);

        # keep a reference to feature
        featureLookup.append(feature);
        
    _gisModule.FeatureClassList.Add(featureClass);        
    
    print(i)
