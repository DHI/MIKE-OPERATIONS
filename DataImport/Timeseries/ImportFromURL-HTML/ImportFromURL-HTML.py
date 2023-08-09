import clr

clr.AddReference("System")
from System import *
from System.Globalization import *
from System.IO import *
from System.Net import *
from System.Text import *

clr.AddReference("DHI.Solutions.Generic")
from DHI.Solutions.Generic import *

clr.AddReference("DHI.Solutions.TimeseriesManager.Interfaces")
from DHI.Solutions.TimeseriesManager.Interfaces import *

from HTMLParser import HTMLParser
import string

class MyHTMLParser(HTMLParser):
    def feed(self, data):
        self.listData = []
        HTMLParser.feed(self, data)
        
    def handle_data(self, data):
        d = data.strip()
        if d != '':
            # print("some data  :", d)
            self.listData.append(d)
            
def crawler(spreadsheet,worksheet, days):
    """
    <Script>
    <Author>ANK</Author>
    <Description>Parse napa.onerain.com</Description>
    <Parameters>
    <Parameter name="spreadsheet" type="string">path to configuration spreadsheet</Parameter>
    <Parameter name="worksheet" type="string">worksheet name</Parameter>
    <Parameter name="days" type="int">how many days to look back</Parameter>
    </Parameters>
    </Script>
    """

    # Get a reference to the Time series Manager
    tsMgr = app.Modules.Get('Time series Manager')
    tsDefs = _readspreadsheet(spreadsheet,worksheet)
    toDate = DateTime.Now
    fromDate = toDate.AddDays(-days)
    
    for tsDef in tsDefs:
        tsPath = tsDef['tsPath']
        tsVariable = tsDef['tsVariable']
        tsUnit = tsDef['tsUnit']
        tsURL = tsDef['tsURL']
        tsTargetUnit = tsDef['tsTargetUnit']
        tsOffset = tsDef['tsOffset']
        print(tsPath)
        valuepairs = _crawl4data(tsURL, fromDate, toDate)
        if valuepairs.Count>0:
            tsTemp = tsMgr.TimeSeriesList.CreateNew(tsPath)
            tsTemp.YAxisVariable = tsVariable            
            tsTemp.SetYAxisUnit(tsUnit,False)
            if tsVariable == 'Rainfall':
                tsTemp.ValueType = DataSeriesValueType.Step_Accumulated
#            tsTemp.Name = DssPath.GetEntityName(tsPath)

            vpList = []
            for tv in valuepairs:
                vp = tsTemp.CreateNew()
                vp.XValue = DateTime.Parse(tv[0])
                vp.YValue = Convert.ToSingle(tv[1],CultureInfo.InvariantCulture) + tsOffset
                
                vpList.append(vp)
        
            print("{} timesteps".format(vpList.Count))
            
            tsTemp.SetData(sorted(vpList,key=lambda vp:vp.XValue))
            tsTemp.SetYAxisUnit(tsTargetUnit,True)
                        
            tsGroupPath = DssPath.RemoveEntityName(tsPath)
            tsMgr.CopyTimeSeries(tsTemp,tsGroupPath, TimeSeriesCopyAction.CopyDataInPeriod)
        else:
            print("no value found for interval")
            
    print("done")
    
def _readspreadsheet(sPath,worksheet):
    
    tsDef = []
    # Get a reference to the Spreadsheet Manager
    sprMgr = app.Modules.Get('Spreadsheet Manager')

    # Use it for e.g. reading a Spreadsheet
    spreadsheet = sprMgr.OpenSpreadsheet(sPath)
    usedRange = sprMgr.GetUsedRangeValue(spreadsheet, worksheet)
    
    endRow = usedRange.GetLength(0);
    endCol = usedRange.GetLength(1);
    for r in range(1,endRow):
        tsDef.append({'tsPath': usedRange[r,0] ,
                      'tsVariable': usedRange[r,1] ,
                      'tsUnit': usedRange[r,2] ,
                      'tsOffset': usedRange[r,3] ,
                      'tsTargetUnit':usedRange[r,4] ,
                      'tsURL': usedRange[r,5]} )
    
    sprMgr.CloseSpreadsheet(spreadsheet)
    
    return tsDef



def _crawl4data(url, fromDate, toDate):
    valuepairs = []
    try:
        request = WebRequest.Create (url+"&data_start=" + fromDate.Date.ToString("yyyy-MM-dd")+"&data_end="+toDate.Date.ToString("yyyy-MM-dd 23:59:59"));
        request.CookieContainer = CookieContainer();
        # If required by the server, set the credentials.
        # request.Credentials = CredentialCache.DefaultCredentials;
        # Get the response.
        with request.GetResponse () as response:
            # Display the status.
            print("Web : " + response.StatusDescription);
            # Get the stream containing content returned by the server.
            with response.GetResponseStream () as dataStream :
                # Open the stream using a StreamReader for easy access.
                reader = StreamReader (dataStream);
                # Read the content.
                responseFromServer = reader.ReadToEnd ();
                #print(responseFromServer)
                #print("***************************************************")
                
                # find all h4tags and extract time and value
                parser = MyHTMLParser()
                h4tags = _getTextBetweenTags(responseFromServer, "h4")
                t = ""
                v = ""
                for tag in h4tags:
                    if '<span class="text-nowrap">' in tag:
                        # the date and time
                        parser.feed(tag)
                        
                        if parser.listData.Count>0:
                            t = parser.listData[0]
                        else:
                            v = ""
                    elif not '<span' in tag:
                        # value
                        parser.feed(tag)
                        if parser.listData.Count>0:
                            v = parser.listData[0]
                        else:
                            t = ""
                    else:
                        t = ""
                        v = ""                    

                    if t != "" and v != "":
                        valuepairs.append([t,v])
                        t = ""
                        v = ""                    

    except Exeption as e:
        print("Error parsing " + str(e))
    
    return valuepairs    
    
import re
def _getTextBetweenTags(html, tagname):
    starttag = '<'+tagname
    endtag = '</'+tagname+'>'
    startpos = [m.start() for m in re.finditer(starttag, html)]
    endpos = [m.start() for m in re.finditer(endtag, html)]
    result = []
    for i in range(startpos.Count):
        result.append(html[startpos[i] : endpos[i]+len(endtag)])
    return result        
    
