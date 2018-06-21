# coding: utf-8
# In[ ]:

## PRAEMAMBLE

import sys
import os
import string
import datetime
import xml.etree.ElementTree as etree

if sys.version_info[0] < 3: 
    from StringIO import StringIO
    import urllib2
else:
    from io import StringIO
    import urllib

import clr
import System
from System import DateTime
#clr.AddReference('System.Data')

# CODE FOR EXTERNAL DEBUGGING
import __builtin__
if not hasattr(__builtin__, "app"):
    sys.path.append(r"C:\Program Files (x86)\DHI\2017\MIKE OPERATIONS 7")
    os.chdir(r"C:\Program Files (x86)\DHI\2017\MIKE OPERATIONS 7")
    clr.AddReference('DHI.Solutions.Application')
    from DHI.Solutions.Application import Application
    __builtin__.app = Application()
    external_app_start = True
else:
    external_app_start = False
    
clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import DataSeriesValueType


# In[ ]:

# CODE FOR EXTERNAL DEBUGGING
if external_app_start:
    connectiondef = 'host=localhost;port=5432;database=Irrimode;dbflavour=PostgreSQL'
    #connectiondef = 'host=auper1-vm01;port=5432;database=FMG_MWOP;dbflavour=PostgreSQL'
    print("connecting to "+connectiondef)
    app.SetConnection(connectiondef)
    app.Login('admin', 'dssadmin', 'workspace1')
    app.StartUp()



def ImportFromSentekIrrimaxWeb(spreadsheetpath):
    """
    <Script>
    <Author>ARE</Author>
    <Description>This will import measurements of Sentek agricultural probes 
    from vendors online platform (www.irrimaxlive.com). All Settings and 
    further description are provided through the configuration spreadsheet
    </Description>
    <Parameters>
    <Parameter name="spreadsheetpath" type="String">path to config spreadsheet</Parameter>
    </Parameters>
    <ReturnValue type="IType">None</ReturnValue>
    </Script>
    """
    # write your code here
        
    # In[ ]:
    
    # get Settings from Spreadsheet
    print("reading settings from {}:".format(spreadsheetpath))
    sheetName = "Configuration"
    sheetMgr = app.Modules.Get("Spreadsheet Manager")
    importSheetConfig = sheetMgr.OpenSpreadsheet(spreadsheetpath)
    api_key = sheetMgr.GetCellValue(importSheetConfig, sheetName, 2, 1)
    print("\tusing API Key: "+api_key)
    
    from_time_d = sheetMgr.GetCellValue(importSheetConfig, sheetName, 3, 1)
    from_time = DateTime(1899,12,30).AddDays(from_time_d)
    print("\tabsolute import period starts {} ".format(from_time))
    
    to_time_d = sheetMgr.GetCellValue(importSheetConfig, sheetName, 4, 1)
    to_time = DateTime(1899,12,30).AddDays(to_time_d)
    print("\tabsolute import period ends   {}".format(to_time))
    
    basepath = sheetMgr.GetCellValue(importSheetConfig, sheetName, 5, 1)
    print("\troot folder for import "+basepath)
    
    relative_to_now = sheetMgr.GetCellValue(importSheetConfig, sheetName, 6, 1)
    print("\timport interval relative to current time: {}".format(relative_to_now))
    
    relative_interval = sheetMgr.GetCellValue(importSheetConfig, sheetName, 7, 1)
    print("\trelative import period {} h".format(relative_interval))
    
    
    if relative_to_now:
        from_time = System.DateTime.Now.AddHours(-relative_interval)
        to_time = System.DateTime.Now.AddDays(1)
        print("Importing data for last {} h + 1 day lead time ({} to {}).".format(relative_interval, from_time, to_time))
    else:
        print("Importing all available data between {} and {}".format(from_time, to_time))
    
    
    # In[ ]:
    
    # get list of loggers from API
    url_getloggers = "http://www.irrimaxlive.com/api/?cmd=getloggers&key="+api_key
    print("reading " + url_getloggers)
    xml_string = urllib2.urlopen(url_getloggers).read()
    
    # remove encoded characters
    printable = set(string.printable)
    xml_string = filter(lambda x: x in printable, xml_string)
    
    # parse string to XML object
    xml_tree = etree.ElementTree(etree.fromstring(xml_string))
    
    
    # In[ ]:
    
    # print all loggers
    for logger in xml_tree.iter("Logger"):
        print("found logger {} (id={})".format(logger.attrib["name"], logger.attrib["id"]))
    
    
    # In[ ]:
    
    datetimeformat = "{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}"
    from_str = datetimeformat.format(from_time.Year, 
                                     from_time.Month, 
                                     from_time.Day, 
                                     from_time.Hour,
                                     from_time.Minute, 
                                     from_time.Second)
    to_str = datetimeformat.format(to_time.Year, 
                                   to_time.Month, 
                                   to_time.Day,
                                   to_time.Hour,
                                   to_time.Minute, 
                                   to_time.Second)
    
    url_getreadings_byid = "http://www.irrimaxlive.com/api/?cmd=getreadings&key={}&id={}&from={}&to={}"
    
    
    # In[ ]:
    
    def timeseries_exists(path):
        tsmgr = app.Modules.Get('Time series Manager')
        if tsmgr is None:
            raise NameError('Could not load time series manager')
    
        if tsmgr.TimeSeriesList.Fetch(path) is None:
            return False
        else:
            return True
    
    
    # In[ ]:
    
    print(System.Double(1.))
    
    
    # In[ ]:
    
    def CreateTimeSeries(timeSeries, unitType, unitVariable, valueType):
        """
        <Script>
        <Author>jga/are</Author>
        <Description>Create time series</Description>
        <Parameters>
        <Parameter name="timeSeries" type="string">destination time series name</Parameter>
        <Parameter name="unitType" type="string">unit type</Parameter>
        <Parameter name="unitVariable" type="string">Variable type</Parameter>
        <Parameter name="valueType" type="string">"Instantaneous", "Accumulated", "Step Accumulated" or "Reverse Mean Step Accumulated"</Parameter>
        </Parameters>
        </Script>
        """
    
        timeSeriesManager = app.Modules.Get('Time series Manager')
        if timeSeriesManager is None:
            raise NameError('Could not load time series manager')
        dataSeries = GetDataSeries(timeSeries)
    
        if dataSeries is None:
            dataSeries = timeSeriesManager.TimeSeriesList.CreateNew(timeSeries)
            dataSeries.YAxisVariable = unitType
    
            # for Rainfall Depth time series, create as Accumulated, Rainfall Step Accumulated others default to Instantaneous
            if valueType == "Instantaneous":
                dataSeries.ValueType = DataSeriesValueType.Instantaneous
            elif valueType == "Accumulated":
                dataSeries.ValueType = DataSeriesValueType.Accumulated
            elif valueType == "Step Accumulated":
                dataSeries.ValueType = DataSeriesValueType.Step_Accumulated
            elif valueType == "Reverse Mean Step Accumulated":
                dataSeries.ValueType = DataSeriesValueType.Reverse_Mean_Step_Accumulated
            elif type(valueType) == DataSeriesValueType:  # if dataseries value type has been provided, assign it
                dataSeries.ValueType = valueType
            try:
                dataSeries.SetYAxisUnit(unitVariable, False)
            # robustness againast unit name change between MIKE 2014 -> 2016
            except System.Exception as e:
                if unitVariable == "m^3/day":  # 2014 unit
                    unitVariable = "m^3/d"  # 2016 unit
                    dataSeries.SetYAxisUnit(unitVariable, False)
                elif unitVariable == "m^3/d":  # 2016 unit
                    unitVariable = "m^3/day"  # 2014 unit
                    dataSeries.SetYAxisUnit(unitVariable, False)
                else:
                    raise e  # something else is wrong
            timeSeriesManager.TimeSeriesList.Add(dataSeries)
        else:
            dataSeries.DeleteAll()
    
        dataSeries.ClearData()
        del dataSeries
    
        
    
    
    # In[ ]:
    
    def timeseries_exists(path):
        tsmgr = app.Modules.Get('Time series Manager')
        if tsmgr is None:
            raise NameError('Could not load time series manager')
    
        if tsmgr.TimeSeriesList.Fetch(path) is None:
            return False
        else:
            return True
        
    
    
    # In[ ]:
    
    def GetDataSeries(timeSeries):
        """
        <Script>
        <Author>admin</Author>
        <Description>write python list to time series</Description>
        <Parameters>
        <Parameter name="timeSeries" type="string">destination time series path</Parameter>
        </Parameters>
        </Script>
        """
    
        timeSeriesManager = app.Modules.Get('Time series Manager')
        if timeSeriesManager is None:
            raise NameError('Could not load time series manager')
    
        dataSeries = timeSeriesManager.TimeSeriesList.Fetch(timeSeries)
        return dataSeries
    
    
    # In[ ]:
    
    def add_steps_to_ts(plist, ts_path):
        tmgr = app.Modules.Get('Time series Manager')
        ts = tmgr.TimeSeriesList.Fetch(ts_path)
        timestepts = ts.FetchAll()
        if(timestepts.Count > 0):
            lastTimestep = timestepts[timestepts.Count - 1].XValue
        else:
            lastTimestep = DateTime.MinValue
        count = 0
        for x, y in plist:
            date = x
            if date > lastTimestep:
                value = System.Double(y)
                step = ts.CreateNew()
                step.XValue = date
                step.YValue = value
                ts.Add(step)
        count+=1
        tmgr.TimeSeriesList.Update(ts)
        
    
    
    # In[ ]:
    
    # iterate all loggers:
    for logger in xml_tree.iter("Logger"):
        print("logger {} (id={})".format(logger.attrib["name"], logger.attrib["id"]))
        
        # download logger data
        logger_id = logger.attrib["id"]
        url_request = url_getreadings_byid.format(api_key, logger_id , from_str, to_str)
        print("reading data from "+url_request)
        csv_string = urllib2.urlopen(url_request).read()
        
        # create dictionary {header name: column number}
        headers = StringIO(csv_string).readline().split(",")
        header_of = {headers[i].split("(")[0]:i for i in range(len(headers))}
        
        # iterate over sites > probes > sensors
        for site in logger.iter("Site"):
            print("\tsite {}".format(site.attrib["name"]))
            for probe in site.iter("Probe"):
                print("\t\tprobe {}".format(probe.attrib["name"]))
                for sensor in probe.iter("Sensor"):
                    print("\t\t\tsensor {}: {} ({})".format(sensor.attrib["name"], 
                                                            sensor.attrib["type"], 
                                                            sensor.attrib["unit"]))     
                    column = header_of[sensor.attrib["name"]]
                
                    # sensor logics   
                    sensor_variable = None
                    sensor_unit = None
                    sensor_factor = 1.
                    sensor_comment = ""
    
                    if sensor.attrib["type"] == "Voltage":
                        sensor_variable = "Voltage"
                        sensor_comment = sensor.attrib["description"]
                        if sensor.attrib["unit"] == "V":
                            sensor_unit = "V"
    
                    if sensor.attrib["type"] == "Soil Water Content":
                        sensor_variable = "Volumetric Water Content"
                        sensor_comment = "{} cm".format(sensor.attrib["depth_cm"])
                        if sensor.attrib["unit"] == "mm":
                            sensor_unit = "%"
    
                    if sensor.attrib["type"] == "V.I.C.":
                        sensor_variable = "Undefined"
                        sensor_comment = "{} cm".format(sensor.attrib["depth_cm"])
                        if sensor.attrib["unit"] == "VIC":
                            sensor_unit = "-"
    
                    if sensor.attrib["type"] == "Temperature":
                        sensor_variable = "Temperature"
                        sensor_comment = "{} cm".format(sensor.attrib["depth_cm"])
                        if sensor.attrib["unit"] == "C":
                            sensor_unit = "deg C"
                    
                    if sensor_variable is None:
                        print("unknown sensor type "+sensor.attrib["type"])
                    if sensor_unit is None:
                        print("unknow sensor unit "+sensor.attrib["unit"])
    
                    if sensor_variable is None or sensor_unit is None:
                        print("skipped.")
                        continue
    
                    # set path of time series
                    ts_path = basepath+"/{}/{}/{}/{}({})".format(logger.attrib["name"],
                                                site.attrib["name"],
                                                probe.attrib["name"],
                                                sensor.attrib["name"],
                                                sensor_comment)
                   
    
                    # check if TS exists and create if necessary
                    if not timeseries_exists(ts_path):
                        print("\t\t\t\tCreating Time Series "+str(ts_path))
                        CreateTimeSeries(ts_path, sensor_variable, sensor_unit, "Instantaneous")
                    
                    # Add new measurements to time series
                    
                    # create data list [(DateTime, float)] from column in csv
                    ts = []
                    csv = StringIO(csv_string)
                    csv.readline()  # discard headers
                    while True:
                        line = csv.readline()
                        if line == "":
                            break
                        words = line.split(',')
    
                        # parse string to DateTime (via datetime)
                        dt = datetime.datetime.strptime(words[0], "%Y/%m/%d %H:%M:%S") 
                        DT = DateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    
                        # parse string to float
                        ts.append((DT, float(words[column])))
                    
                    if len(ts) == 0:
                        print("\t\t\t\tNo new measurements found.")
                    else:
                        print("\t\t\t\tAdding {} measurments to {} ".format(len(ts), ts_path))
                        add_steps_to_ts(ts, ts_path)    
    
    
    
    
    
