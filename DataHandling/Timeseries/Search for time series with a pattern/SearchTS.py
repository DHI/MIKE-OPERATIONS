import clr
clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import *

def SearchTS(pattern):
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>Example on how to search for time series by name</Description>
    <Parameters>
    <Parameter name="pattern" type="string">What to search for</Parameter>
    </Parameters>
    </Script>
    """

    tmgr = app.Modules.Get('Time series Manager');

    # build the query object full of one element with a like query
    q = Query();
    q.Add(QueryElement('Name', '*' + pattern + '*', QueryOperator.Like));

    # execute the query
    tslist = tmgr.TimeSeriesList.Fetch(q);

    # do your stuff - show the found time name
    i=0;
    while i<tslist.Count:
        print tslist[i].Name;
        i = i + 1;
    pass;
