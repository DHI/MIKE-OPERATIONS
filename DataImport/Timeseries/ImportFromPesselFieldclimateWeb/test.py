
# coding: utf-8

# # REST-API for Pessl Instruments Weather Station
# 
# See API documentation http://www.fieldclimate.com/api/intro.html 

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

import sys
import urllib2  # python 2.7, use urllib for Python 3
import json


# In[ ]:

# REMOVE THIS WHEN TRANSFERRING IN SCRIPT MANAGER   
if external_app_start:
    connectiondef = 'host=localhost;port=5432;database=Irrimode;dbflavour=PostgreSQL'
    #connectiondef = 'host=auper1-vm01;port=5432;database=FMG_MWOP;dbflavour=PostgreSQL'
    print("connecting to "+connectiondef)
    app.SetConnection(connectiondef)
    app.Login('admin', 'dssadmin', 'workspace1')
    app.StartUp()


# In[ ]:

def ImportFromPesslFieldclimate(spreadsheetpath):
    """
    <Script>
    <Author>ARE</Author>
    <Description>This will import measurements of Pessl weather station from
    the vendors online platform (www.fieldclimate.com). All Settings and 
    further description are provided through the configuration spreadsheet.
    </Description>
    <Parameters>
    <Parameter name="spreadsheetpath" type="String">path to config spreadsheet</Parameter>
    </Parameters>
    <ReturnValue type="IType">None</ReturnValue>
    </Script>
    """

    
    
    # SCRIPT PARAMETER
    #spreadsheetpath = "/DataImport/Timeseries/ImportFromPesslFieldclimateWeb/Configuration"
    
    
    # In[ ]:
    
    # get Settings from Spreadsheet
    print("reading settings from {}:".format(spreadsheetpath))
    sheetName = "Configuration"
    sheetMgr = app.Modules.Get("Spreadsheet Manager")
    importSheetConfig = sheetMgr.OpenSpreadsheet(spreadsheetpath)
    
    # read settings
    
    auth_user = sheetMgr.GetCellValue(importSheetConfig, sheetName, 2, 1)
    if auth_user is None:
        print("\tuser name:\tNOT SET!")
    else:
        print("\tuser name:\t{}".format(auth_user))
    
    auth_passw = sheetMgr.GetCellValue(importSheetConfig, sheetName, 3, 1)
    if auth_passw is None:
        print("\tpassword: NOT SET!")
    else:
        print("\tpassword:\t"+"*"*len(auth_passw))
    
    basepath = sheetMgr.GetCellValue(importSheetConfig, sheetName, 4, 1)
    print("\troot folder:\t "+basepath)
    
    relative_to_now = sheetMgr.GetCellValue(importSheetConfig, sheetName, 5, 1)
    print("\timport interval relative to current time: {}".format(relative_to_now))
    
    from_time_d = sheetMgr.GetCellValue(importSheetConfig, sheetName, 6, 1)
    from_time = DateTime(1899,12,30).AddDays(from_time_d)
    print("\tabsolute import period starts {} ".format(from_time))
    
    to_time_d = sheetMgr.GetCellValue(importSheetConfig, sheetName, 7, 1)
    to_time = DateTime(1899,12,30).AddDays(to_time_d)
    print("\tabsolute import period ends   {}".format(to_time))
    
    relative_interval = sheetMgr.GetCellValue(importSheetConfig, sheetName, 8, 1)
    print("\trelative import period {} h".format(relative_interval))
    
    max_rows = int(sheetMgr.GetCellValue(importSheetConfig, sheetName, 9, 1))
    print("\tmax rows to read: {}".format(max_rows))
    
    if relative_to_now:
        from_time = System.DateTime.Now.AddHours(-relative_interval)
        to_time = System.DateTime.Now.AddDays(1)
        print("Importing data for last {} h + 1 day lead time ({} to {}).".format(relative_interval, from_time, to_time))
    else:
        print("Importing all available data between {} and {}".format(from_time, to_time))
    
    
    # In[ ]:
    
    def api_request(command, parameters=None):
        url_base = "http://www.fieldclimate.com/api/"
        str_auth = "user_name={}&user_passw={}".format(auth_user, auth_passw)
        str_request = url_base+command+"?"+str_auth
        if parameters is not None:
            str_request += "&"+"&".join(parameters)
        
        print("reading " + str_request)
        try:
            json_str = urllib2.urlopen(str_request).read()
            json_dict = json.loads(json_str)
            return json_dict
        except urllib2.HTTPError as e:
            print("HTTPError reading "+str_request)
            raise e
    
    
    # In[ ]:
    
    def api_request2(command, parameters=[]):
        url_base = "http://www.fieldclimate.com/api/index.php?"
        parameters.append("action="+command)
        parameters.append("user_name="+auth_user)
        parameters.append("user_passw="+auth_passw)
        str_request = url_base + "&".join(parameters)
        print(str_request)    
    
        try:
            json_str = urllib2.urlopen(str_request).read()
            json_dict = json.loads(json_str)
            return json_dict
        except urllib2.HTTPError as e:
            print("HTTPError reading "+str_request)
            raise e  
    
    
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
    
    def to_datetime(DT):
        return datetime.datetime(from_time.Year, 
                  from_time.Month, 
                  from_time.Day, 
                  from_time.Hour, 
                  from_time.Minute, 
                  from_time.Second)
        
    to_datetime(from_time)
    
    
    # ## Dev Script
    
    # In[ ]:
    
    # iterate over list of weather stations
    weather_stations = api_request("CIDIStationList/GetStations")['ReturnDataSet']
    print("found {} weather stations:".format(len(weather_stations)))
    for station_id in weather_stations:
    
        # get information on station and its sensors
        station_name = weather_stations[station_id]["custom_name"]
        print("\t{} ({})".format(station_id, station_name))
        
        station_sensors = api_request("CIDIStationSensors/Get",["station_name="+station_id])['ReturnDataSet']  # station name: f_name / serial number
        print("\tfound {} sensors:".format(len(station_sensors)))
        print("\ttchannel\tcode\tunit\tdescription")
        for sensor_id in range(len(station_sensors)):
            sensor_info = station_sensors[sensor_id]
            
            sensor_channel = sensor_info["f_sensor_ch"]
            sensor_code = sensor_info["f_sensor_code"]
            sensor_name = sensor_info["f_name"]
            sensor_name_user = sensor_info["f_sensor_user_name"]
            sensor_unit = sensor_info["f_unit"]
    
            print(u"\t{}\t{}\t[{}]\t{} ('{}')".format(sensor_channel, sensor_code, sensor_unit, sensor_name, sensor_name_user))
    
            sensor_by_code = { s["f_sensor_code"] : s for s in station_sensors}
    
        # read out stations measurment data
        response = api_request2("CIDIStationData3_GetFromDate",["station_name="+station_id, 
                                                                "row_count="+str(max_rows),
                                                                "dt_from="+to_datetime(from_time).strftime("%Y-%m-%dT%H:%M:%S")]) 
        
                                                                
        for reading in response["ReturnDataSet"]:
    
    
            reading_time = reading["f_date"]
            sys.stdout.write("\nReading Measurements for {}:".format(reading_time))
            # parse string to DateTime (via datetime)
            dt = datetime.datetime.strptime(reading_time, "%Y-%m-%d %H:%M:%S") 
            DT = DateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    
            for sensor in reading.keys():
    
                # skip if not a sensor:
                if not sensor.split("_")[0] == "sens":
                    continue
    
                _, sensor_type, sensor_channel, sensor_code = sensor.split("_")
                sensor_reading = reading[sensor]
    
                # skip min/max values or if no reading was taken
                if sensor_type in ["min","max"]:
                    continue
                if sensor_reading is None:
                    continue
    
                # sensor logics        
                sensor_variable = None
                sensor_unit = None
                sensor_factor = 1.
                sensor_comment = ""
                value_type = None
    
    
                if sensor_code=="0": # air temperature
                    sensor_variable = "Temperature"
                    sensor_unit = "deg C"
                    if sensor_type == "last":
                        value_type = "Instantaneous"
                    if sensor_type == "aver":
                        value_type = "Reverse Mean Step Accumulated"  # TODO: check if this makes sense in EUM
                      
                    
                if sensor_code=="5": # Wind Speed
                    sensor_variable = "Wind speed"
                    sensor_unit = "m/s"
                    if sensor_type == "last":
                        value_type = "Instantaneous"
                    if sensor_type == "aver":
                        value_type = "Reverse Mean Step Accumulated"  # TODO: check if this makes sense in EUM
                    
    
                if sensor_code=="6": # precipitation
                    sensor_variable = "Rainfall"
                    sensor_unit = "mm"
                    if sensor_type == "sum":
                        value_type = "Reverse Mean Step Accumulated"  # TODO: check if this makes sense in EUM
                     
                if sensor_code=="7": # Battery Voltage
                    sensor_variable = "Voltage"
                    sensor_unit = "V"
                    sensor_factor = 1/1000.
                    if sensor_type == "last":
                        value_type = "Instantaneous"
                    if sensor_type == "aver":
                        value_type = "Reverse Mean Step Accumulated"  # TODO: check if this makes sense in EUM
                        
                if sensor_code=="21": # Dew Point
                    sensor_variable = "Temperature"
                    sensor_unit = "deg C"
                    if sensor_type == "last":
                        value_type = "Instantaneous"
                    if sensor_type == "aver":
                        value_type = "Reverse Mean Step Accumulated"  # TODO: check if this makes sense in EUM
                        
                if sensor_code=="1201": # ET_0
                    sensor_variable = "Evaporation"
                    sensor_unit = "mm"
                    if sensor_type == "aver":
                        value_type = "Reverse Mean Step Accumulated"  # TODO: check if this makes sense in EUM
                
                
                
      
                # TODO:
                #f_sensor_code  f_name  f_sensor_user_name  f_unit
                #4  Leaf Wetness    Leaf Wetness    Min
                #16 Soil temperature    Bodentemperatur C
                #25 VPD VPD kPa
                #30 Solar Panel Solarpanel  mV
                #43 Water meter 1L - Differential   Water Meter 1L - Differential   L
                #506    HC Air temperature  HC Lufttemperatur   C
                #506    HC Air temperature  HC Air temperature  C
                #507    HC Relative humidity    HC Luftfeuchte  %
                #507    HC Relative humidity    HC Relative humidity    %
                #508    HC Serial Number    HC Serial Number     
                #600    Solar radiation Solar radiation Dgt W/mm
                
                # set path of time series
                ts_path = basepath + "/{} ({})/ch{:04d} {}".format(station_id, 
                                                               station_name,
                                                               int(sensor_by_code[sensor_code]["f_sensor_ch"]),
                                                               sensor_by_code[sensor_code]["f_name"])
    
                desc = "ch{:04d} {}".format(int(sensor_by_code[sensor_code]["f_sensor_ch"]),
                                                               sensor_by_code[sensor_code]["f_name"])
                
                if sensor_variable is None or sensor_unit is None or value_type is None:
                    #print("\t\t\t\tskipping {}".format(desc))
                    continue
    
                 # check if TS exists and create if necessary
                if not timeseries_exists(ts_path):
                    print("\nCreating Time Series "+str(ts_path))
                    _ = CreateTimeSeries(ts_path, sensor_variable, sensor_unit, value_type)
    
                sys.stdout.write(" ch{:04d}".format(int(sensor_by_code[sensor_code]["f_sensor_ch"])))   
                #print("\t\t\t\tAdding   {}".format(desc))
                add_steps_to_ts([(DT, float(sensor_reading)*sensor_factor)], ts_path)    
    
    
    # In[ ]:
    
    

