import clr
clr.AddReference("System")
from System import DateTime, Convert
clr.AddReference("System.Globalization")
from System.Globalization import *
clr.AddReference("System.Xml")
from System.Xml import *
clr.AddReference("DHI.Solutions.Generic")
from DHI.Solutions.Generic import DssPath
clr.AddReference("DHI.Solutions.TimeseriesManager.Interfaces ")
from DHI.Solutions.TimeseriesManager.Interfaces import TimeSeriesCopyAction

import urllib

tsMgr = app.Modules.Get('Time series Manager')
spreadsheetMgr = app.Modules.Get('Spreadsheet Manager')

debug = False

def _logprint(m):
    print(DateTime.Now.ToString("HH:mm:ss") + " - ", m);

def DownloadYr(spreadsheetPath, worksheetName,hours):
    """
    <Script>
    <Author>ANK</Author>
    <Description>Download precipitation forecast from Yr.no based on mapping in a spreadsheet</Description>
    <Parameters>
    <Parameter name="spreadsheetPath" type="string">Path to spreadsheet containing mapping to website</Parameter>
    <Parameter name="worksheetName" type="string">workshseet name</Parameter>
    <Parameter name="hours" type="int">number of hours to convert from UTC to local time</Parameter>
    </Parameters>
    </Script>
    """
    
    try: 
        # spreadsheetPath = '/DataCalculation/YR'        
        if (spreadsheetPath[0] != '/'):
            spreadsheetPath = '/' + spreadsheetPath
        spreadsheet = spreadsheetMgr.OpenSpreadsheet(spreadsheetPath)
        
        rowNo = 1;
        # worksheetName = 'sheet1'
        while True:
            # There is one station on each row..
            StationName = spreadsheetMgr.GetCellValue(spreadsheet, worksheetName, rowNo, 0);
    
            # Stop reading the spreadsheet when a row contains no station name.
            if (StationName == None or StationName == ''):
                break;
            
            StationName = StationName.Trim();
            url = spreadsheetMgr.GetCellValue(spreadsheet, worksheetName, rowNo, 1).Trim();
            path = spreadsheetMgr.GetCellValue(spreadsheet, worksheetName, rowNo, 2);
            types = spreadsheetMgr.GetCellValue(spreadsheet, worksheetName, rowNo, 3).split(";");

            if url[-12:] != 'forecast.xml':
                if url[-1] != '/':
                    url = url + '/'
                url = url + 'forecast.xml'
            
            _logprint('fetching data from Yr.no for station ' + StationName)
            _logprint(url)
            
            response = urllib.urlopen(url)
            xml = response.read()
            _logprint("loading xml...")
            doc = XmlDocument();
            doc.LoadXml(xml);
            
            for typ in types:
                targetts = tsMgr.TimeSeriesList.Fetch(path)
                if targetts == None:
                    targetts = tsMgr.TimeSeriesList.CreateNew(path)
                    if typ == "precipitation":
                        targetts.YAxisVariable = "Rainfall"
                    elif typ == "pressure":
                        targetts.YAxisVariable = "Pressure"
                        targetts.SetYAxisUnit("hPa",False)
                    elif typ == "windSpeed":
                        targetts.YAxisVariable = "Wind speed"
                    elif typ == "windDirection":
                        targetts.YAxisVariable = "Wind Direction"
                    elif typ == "temperature":
                        targetts.YAxisVariable = "Temperature"
                else:
                    targetts = targetts.Clone()
                
                vplist=[]
                t="";
                forecast = doc.GetElementsByTagName("forecast")[0]
                table = forecast.GetElementsByTagName("tabular")[0]
                for t in table.GetElementsByTagName("time"):
                    tim = t.Attributes["to"].Value
                    p = t.GetElementsByTagName(typ)[0]
                    precip = p.Attributes["value"].Value
                    
                    vp = targetts.CreateNew()
                    vp.XValue = DateTime.Parse(tim).AddHours(hours) # convert to local time GMT +2
                    vp.YValue = Convert.ToDouble(precip, CultureInfo.InvariantCulture)
        
                    _logprint("   " + vp.XValue.ToString('yyyy-MM-dd HH:mm:ss') + "; " + vp.YValue.ToString())
                    vplist.append(vp)
        
                targetts.SetData(vplist)
                TargetGroupPath = '/'.join(path.split('/')[0:-1])
                targetts.Name = targetts.Name + "_" + typ
                _logprint("Copy " + targetts.Name + " to " + TargetGroupPath + " with " + str(targetts.Count) + " timesteps")
                tsMgr.CopyTimeSeries(targetts, TargetGroupPath, TimeSeriesCopyAction.CopyDataInPeriod)
            
            rowNo = rowNo + 1;
            
        _logprint("Done");
    except Exception as e:
        _logprint("ERROR: %s" %(str(e)));
        

