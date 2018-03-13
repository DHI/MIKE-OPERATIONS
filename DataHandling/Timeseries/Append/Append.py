import clr
clr.AddReference('DHI.Solutions.Generic')
clr.AddReference('DHI.Solutions.Generic.Tools')
clr.AddReference('DHI.Solutions.GISManager.Tools.ToDatabaseTool')
from DHI.Solutions.Generic.Tools import *
from DHI.Solutions.Generic import Query, QueryElement, QueryOperator 
from DHI.Solutions.GISManager.Tools.ToDatabaseTool import *

def AppendForecast(TsName1, TsName2):
    """
    <Script>
    <Author>DHI</Author>
    <Description>Append two time series. It adds the timesteps of TsName2 at the end of TsName1.</Description>
    <Parameters>
        <Parameter name="TsName1" type="string">Master time series</Parameter>
        <Parameter name="TsName2" type="string">Append time series</Parameter>
    </Parameters>
    </Script>
    """
    inputItems = []

    tsmod = app.Modules.Get("Time Series Manager")
    ts1 = tsmod.TimeSeriesList.Fetch(TsName1)
    ts2 = tsmod.TimeSeriesList.Fetch(TsName2)

    q = Query()
    q.Add(QueryElement("datetime", ts1.End, QueryOperator.Gt))
    vpList = ts2.Fetch(q)    
    ts1.Add(vpList)

    print 'done'
