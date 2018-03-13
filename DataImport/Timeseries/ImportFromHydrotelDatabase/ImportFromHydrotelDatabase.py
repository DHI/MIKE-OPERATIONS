import clr
clr.AddReference("System.Core")
from System import DateTime, TimeSpan
from datetime import datetime, timedelta
clr.AddReference('System.Data')
from System.Data import *
from System.Text import StringBuilder

strObservedDB = "server=192.122.180.243;database=HydroTel;uid=HydTSM;password=hydtsm"
strForecastDB = "server=192.122.180.243;database=HydroTel;uid=HydTSM;password=hydtsm"
iDeleteValue = -9999
pyDTFormat = "%Y-%m-%d %H:%M:%S"
netDTFormat = "yyyy-MM-dd HH:mm:ss"

def ImportTelemetryData(timeOfForecast, hindcast, forecast, spreadsheetPath, worksheetName, outputPath):
    """
    <Script>
    <Author>SNI</Author>
    <Description>This script will import data from hydrotel onto the disk.</Description>
    <Parameters>
    <Parameter name="timeOfForecast" type="string">Time of forecast for simulation.</Parameter>
    <Parameter name="hindcast" type="int">Hindcast period of simulation. Unit: hours.</Parameter>
    <Parameter name="forecast" type="int">Forecast period of simulation. Unit: hours.</Parameter>
    <Parameter name="spreadsheetPath" type="string">Spreadsheet path to be read. This will hold the sensor ids for the observed and forecast time series.</Parameter>
    <Parameter name="worksheetName" type="string">Name of the sheet in spreadsheet, from where the sensor ids should be read.</Parameter>
    <Parameter name="outputPath" type="string">Path to which time series data will be written to.</Parameter>
    </Parameters>
    </Script>
    """
    
    print "Time of forecast: " + timeOfForecast
    print "Hindcast: " + str(hindcast)
    print "Forecast: " + str(forecast)
    tof = None;
    
    if timeOfForecast.upper() == "NOW":
        tof  = datetime.now()
    else:
        tof = datetime.strptime(timeOfForecast, pyDTFormat)
    
    startDate = tof - timedelta(hours=hindcast)
    endDate  = tof + timedelta(hours=forecast)
    
    ssmgr = app.Modules.Get('Spreadsheet Manager');
    if ssmgr == None:
            raise Exception('Can''t obtain a reference to Spreadsheet Manager.')
            
    # open an existing spreadsheet
    ssObj = ssmgr.SpreadsheetList.Fetch(spreadsheetPath)
    if ssObj == None:
        raise Exception('Can''t locate ' + spreadsheetPath + ' spreadsheet.')
        
    ss = ssmgr.OpenSpreadsheet(ssObj);
    if ss == None:
        raise Exception('Unable to open ' + spreadsheetPath + ' spreadsheet.')
        
    # get a reference to workbook
    workbook = ss.Workbook
    sensorSheet = workbook.Worksheets[worksheetName]
    if sensorSheet == None:
        raise Exception('Sheet ' + worksheetName + ' not found in ' + spreadsheetPath + ' spreadsheet.')
        
    # get list of sensor ids and names
    lstRows = _GetRows(sensorSheet)
    
    if len(lstRows) == 0:
        raise Exception('No data found in Sheet: ' + worksheetName + ' in ' + spreadsheetPath + ' spreadsheet.')
        
    dictObsSensors = {}
    dictForeSensors = {}
    
    for row in lstRows:
        isInt = False
        length = len(row)
        try:
            int(row[0])
            isInt = True
        except:
            pass
            
        if row[0] != None and isInt and (row[0] not in dictObsSensors):
            dictObsSensors[row[0]] = row[1]
            
        if(length > 2):
            try:
                int(row[2])
                isInt = True
            except:
                pass
                
            if row[2] != None and isInt and (row[2] not in dictForeSensors):
                dictForeSensors[row[2]] = row[3]
    
    logName = tof.strftime("%Y%m%d");
    log = open(outputPath + "\\logs\\" + logName + ".txt", 'a')
    log.write("\n*************************************\n")
    log.write("Starting to get telemetry data for TOF: " + tof.strftime(pyDTFormat))
    log.write("\n*************************************\n")
    GetObservedTimeseries(dictObsSensors, startDate, endDate, outputPath, log)
    GetForecastTimeseries(dictForeSensors, tof, endDate, outputPath, log)
    log.close()
    

def _GetRows(worksheet):
    # determine start and end of severities table
    startCellWData = worksheet.Cells['A2']
    endCellWData = worksheet.UsedRange.Cells[worksheet.UsedRange.RowCount-1, worksheet.UsedRange.ColumnCount-1]
    cells = worksheet.Cells[startCellWData.Address + ':' + endCellWData.Address]
    
    return GetRangeContent(worksheet = worksheet, range = startCellWData.Address + ':' + endCellWData.Address, ignoreEmptyCells = False) #lambda(cell): _GetCellValue(cell))
    
    
def GetRangeContent(worksheet, range, ignoreEmptyCells = False, getValueCallback = None):
    content = []        
    cells = worksheet.Cells[range]
        
    for row in cells.Rows:
        if not ignoreEmptyCells and row.Value == None:
            return rowContent

        rowContent = []
        for cell in row.Cells:
            if getValueCallback <> None:
                cellValue = getValueCallback(cell)
            else:
                cellValue = cell.Value
            if not ignoreEmptyCells and cellValue == None:
                break
            rowContent.append(cellValue)            
        if len(rowContent) > 0:
            content.append(rowContent)
        
    return content
    
    
def GetObservedTimeseries(dictObsSensors, startDate, endDate, outputPath, log):
    try:
		key = 0
        connection = SqlClient.SqlConnection(strObservedDB)
        connection.Open()
            
        for key, value in dictObsSensors.iteritems():
            strSQL = 'SELECT SAMPLES.DT, SAMPLES.SAMPLEVALUE, SAMPLES.POINT '
            strSQL = strSQL + '  FROM HydroTel.dbo.SAMPLES SAMPLES '
            strSQL = strSQL + ' WHERE (SAMPLES.DT>=CONVERT(DATETIME,\'' + startDate.strftime(pyDTFormat) + '\',102)) '
            strSQL = strSQL + '   AND (SAMPLES.DT<=CONVERT(DATETIME,\'' + endDate.strftime(pyDTFormat) + '\',102)) '
            strSQL = strSQL + '   AND (SAMPLES.POINT=' + key.ToString() + ') ORDER BY SAMPLES.DT'
            cmd = SqlClient.SqlCommand(strSQL, connection)
            reader = cmd.ExecuteReader()
            strData = StringBuilder()
            
            while (reader.Read()):
                theTime = reader[0]
                theValue = reader[1]
                strData.Append(theTime.ToString(netDTFormat) + ',')
                if theValue == iDeleteValue:
                    strData.Append('-1E-30\n')
                else:
                    strData.Append(str(theValue) + '\n')

            reader.Close()

            if strData.Length > 0:
                # Write to file
                f = open(outputPath + "\\Observed\\" + value + ".txt", 'w')
                f.write("Time," + value + "\n")
                f.write(strData.ToString())
                f.close()
                log.write("Data import success for sensor id: " + str(int(key)) + " " + value + "\n")
            else:
                log.write("No data for sensor id: " + str(int(key)) + " " + value + "!!!!\n")
                
        connection.Close()
    except:
	if key == 0:
		exceptionMessage = "Failed to connect to database. Connecton string: " + strObservedDB + "\n"
	else:
		exceptionMessage = "Data import failed for sensor id: " + str(int(key)) + " " + value + "!!!!\n"
	
	log.write(exceptionMessage)
	raise
        
        
def GetForecastTimeseries(dictForeSensors, startDate, endDate, outputPath, log):
    try:
		key = 0
        connection = SqlClient.SqlConnection(strObservedDB)
        connection.Open()
            
        for key, value in dictForeSensors.iteritems():
            strSQL = 'SELECT SAMPLES.DT, SAMPLES.SAMPLEVALUE, SAMPLES.POINT '
            strSQL = strSQL + '  FROM HydroTel.dbo.SAMPLES SAMPLES '
            strSQL = strSQL + ' WHERE (SAMPLES.DT>=CONVERT(DATETIME,\'' + startDate.strftime(pyDTFormat) + '\',102)) '
            strSQL = strSQL + '   AND (SAMPLES.DT<=CONVERT(DATETIME,\'' + endDate.strftime(pyDTFormat) + '\',102)) '
            strSQL = strSQL + '   AND (SAMPLES.POINT=' + key.ToString() + ') ORDER BY SAMPLES.DT'
            cmd = SqlClient.SqlCommand(strSQL, connection)
            reader = cmd.ExecuteReader()
            strData = StringBuilder()
            
            while (reader.Read()):
                theTime = reader[0]
                theValue = reader[1]
                strData.Append(theTime.ToString(netDTFormat) + ',')
                if theValue == iDeleteValue:
                    strData.Append('-1E-30\n')
                else:
                    strData.Append(str(theValue) + '\n')

            reader.Close()

            if strData.Length > 0:
                # Write to file
                f = open(outputPath + "\\Forecast\\" + value + ".txt", 'w')
                f.write("Time," + value + "\n")
                f.write(strData.ToString())
                f.close()
                log.write("Data import success for sensor id: " + str(int(key)) + " " + value + "\n")
            else:
                log.write("No data for sensor id: " + str(int(key)) + " " + value + "!!!!\n")
                
        connection.Close()
	except:
	if key == 0:
		exceptionMessage = "Failed to connect to database. Connecton string: " + strObservedDB + "\n"
	else:
		exceptionMessage = "Data import failed for sensor id: " + str(int(key)) + " " + value + "!!!!\n"
	
	log.write(exceptionMessage)
	raise
