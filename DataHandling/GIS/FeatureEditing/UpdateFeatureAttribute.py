import clr
clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import *

def GISScript():
    """
    <Script>
    <Author>ANK</Author>
    <Description>stub to call UpdateFeatureAttribute</Description>
    </Script>
    """
    
    # change the name of CatchmentN atttribute from Catchment5 to NewCatchment5
    UpdateFeatureAttribute('/DHI_Catchments','CatchmentN','Catchment5','NewCatchment5');
    pass;
    
def UpdateFeatureAttribute(fcpath, fieldname, oldvalue, newvalue):
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>modify the value of a particular feature in a feature class</Description>
    <Parameters>
    <Parameter name="fcpath" type="string">path for the featuree class</Parameter>
    <Parameter name="fieldname" type="string">name fo the field to change</Parameter>
    <Parameter name="oldvalue" type="string">old value to change</Parameter>
    <Parameter name="newvalue" type="string">new value of the feature</Parameter>
    </Parameters>
    </Script>
    """    

    # get the manager
    gmgr = app.Modules.Get('GIS Manager');
    
    # get a featureclass
    fc = gmgr.FeatureClassList.Fetch(fcpath);
    
    # find the index of the field called CatchmentN
    fa  = None
    i=0
    while ( i < fc.AttributeList.Count):
        if (fc.AttributeList.Item[i].Name == fieldname):
            fa = fc.AttributeList.Item[i];
        i=i+1;
    
    if (fa == None):
        print('field ' + fieldname + 'not found');
        return;
        
    # find a feature in the feature class
    q = Query();
    q.Add(QueryElement(fieldname, oldvalue, QueryOperator.Like));
    fc.Query(q);
    features = fc.GetAll();
    if (features.Count==0):
        print('Not feautre found with value ' + oldvalue);
        return

    # get the first
    feat = features[0];

    # change the name
    feat.Item[fa] = newvalue;

    # update the featureclass
    fc.Update(feat); 

    # update the featureclass to database
    gmgr.FeatureClassList.Update(fc)

    # reset the query - just in case the feature class is in UI
    fc.Query(Query())
    pass;
