import clr
clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import *

def GISScript():
    """
    <Script>
    <Author>DHI</Author>
    <Description>stub to call UpdateFeatureAttribute</Description>
    </Script>
    """
    
    # get the manager
    gmgr = app.Modules.Get('GIS Manager');
    
    # get a featureclass
    fc = gmgr.FeatureClassList.Fetch('/Shapes/Einzugsgebiete_20180125');
    
    # find the index of the field called CatchmentN
    fa  = None
    i=0
    while ( i < fc.AttributeList.Count):
        if (fc.AttributeList.Item[i].Name == 'area'):
            fa = fc.AttributeList.Item[i];
        i=i+1;
    
    if (fa == None):
        print('field ' + fieldname + 'not found');
        return;
        
    # find a feature in the feature class
    q = Query();
    q.Add(QueryElement('perimeter', 64424.0, QueryOperator.Gte));
    q.Add(QueryElement('teil_eg', 'ZEG*', QueryOperator.Like));
    features = fc.Fetch(q);
    if (features.Count==0):
        print('Not feautre found with value ' + oldvalue);
        return
    
    fc.Delete(features)
