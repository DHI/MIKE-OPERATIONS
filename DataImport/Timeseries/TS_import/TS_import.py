import time
import csv
import System
from System import DateTime
import sys
import os.path
import clr
clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import (QueryOperator, Query, QueryElement)
clr.AddReference("SpreadsheetGear2012.Core")
from SpreadsheetGear import *

def ImportTS(spreadSheetPath, forecastTime, hindcastPeriod, forecastPeriod):
    """
    <Script>
    <Author>VS</Author>
    <Description>Import time series to MC</Description>
    <Parameters>
    <Parameter name="spreadSheetPath" type="string">Path to the spreadsheet configuration.</Parameter>
    <Parameter name="forecastTime" type="string">Time of forecast (date and time when we will begin to import forecast data).</Parameter>
    <Parameter name="hindcastPeriod" type="int">Hindcast period in hour.</Parameter>
    <Parameter name="forecastPeriod" type="int">Forecast period in hour.</Parameter>
    </Parameters>
    </Script>
    """
#    excel = None
    success = True
#    default = Excel.XlRangeValueDataType.xlRangeValueDefault
    logString = "Spreadsheet: {0}.".format(spreadSheetPath)
    
    
     #Convert dates from String format to DateTime format
    forecastTime = DateTime.ParseExact(forecastTime, 'MM/dd/yyyy HH:mm:ss', System.Globalization.CultureInfo.InvariantCulture, System.Globalization.DateTimeStyles.None)
    print "TOF" , forecastTime 

    try:
        timeShift = 4
        forecastTimeUtc = forecastTime.AddHours(timeShift)
        hindcastTime = forecastTime.AddHours(-hindcastPeriod)
        forecastEndTime = forecastTime.AddHours(forecastPeriod)
        print "TOF" , forecastTime 
        print forecastEndTime
        print hindcastTime 
        
        logString = logString + "\nTime of forecast: {0} UTC: {1}.".format(forecastTime,forecastTimeUtc)
        logString = logString + "\nFrom time: {0}. Hindcast period: {1} hours.".format(hindcastTime,hindcastPeriod)
        logString = logString + "\n  To time: {0}. Forecast period: {1} hours.".format(forecastEndTime,forecastPeriod)
    
        # ts manager
        tsMgr = app.Modules.Get("Time series Manager")
        q = Query()
        q.Add(QueryElement('datetime', hindcastTime, QueryOperator.Gte))
        q.Add(QueryElement('datetime', forecastEndTime, QueryOperator.Lte))
        # spreadsheet
        sheetName = "Sheet1"
        sheetMgr = app.Modules.Get("Spreadsheet Manager")
        importSheetConfig = sheetMgr.OpenSpreadsheet(spreadSheetPath)
        i = 1
    
        # by rows in spreadsheet
        while sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 1):
            tsFullName = sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 1)
            fileExtension = sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 5)
            a = sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 2)
            b = sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 3)
            fileFullName = a + "\\" + b
            dateTimeSuffixFileFormat = sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 4)
            if (dateTimeSuffixFileFormat != None):
                fileFullName = fileFullName + forecastTimeUtc.ToString(sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 4))
            fileFullName = fileFullName + fileExtension
            logString = logString + "\n\nFile: {0}\nTo TS: {1}.".format(fileFullName, tsFullName)
            
            if os.path.isfile(fileFullName):
                # get ts
                ts = tsMgr.TimeSeriesList.Fetch(tsFullName)
                ts.Query(q)
                #itemsQuery = ts.Fetch(q)
                numberOfHeaderLines = sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 7)
                timeZone = sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 10)
                curTimeShift = timeShift
                if (timeZone != None):
                    if (timeZone.upper() == "GUADELOUPE"):
                        curTimeShift = 0
                    else:
                        logString = logString + "\n Unknown time zone: '{0}'. UTC is used.".format(timeZone)
                        success = False
                if (fileExtension == ".csv") or (fileExtension == ".tsv"):
                    with open(fileFullName, 'rb') as csvfile:
                        delimit = sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 6)
                        if (delimit.upper() == 'TAB'):
                            delimit = '\t'
                        
                        spamreader = csv.reader(csvfile, delimiter=delimit)
                        r = 0
                        newItems = []
                        updateItems = []
                        totalUpdate = 0
                        for row in spamreader:
                            r = r + 1
                            if (r <= numberOfHeaderLines) or (row.Count < 2):
                                continue
                            rowDate = DateTime.ParseExact(row[0], sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 8), None).AddHours(-curTimeShift)
                            if hindcastTime <= rowDate and rowDate <= forecastEndTime:
                                rowValue = float(row[1].replace(sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 9), '.'))
                                # add/update steps in TS
                                curStep = ts.CreateNew()
                                curStep.XValue = rowDate
                                curStep.YValue = rowValue
                                if ts.Contains(rowDate):
                                    updateItems.append(curStep)
                                else:
                                    newItems.append(curStep)
                        ts.Query(Query())
                        ts.Add(newItems)
                        ts.Update(updateItems)
                        tsMgr.TimeSeriesList.Update(ts, True)
                        if newItems.Count==0 and updateItems.Count==0:
                            logString = logString + "\n!!! No Data."
                            success = False
                        else:
                            logString = logString + "\n Inserted: {0}. Updated: {1}.".format(newItems.Count, updateItems.Count)
                            logString = logString + "\n Last imported time step: {0}.".format(curStep.XValue)
                elif (fileExtension == ".xls"):
                    xmlSheetName = sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 11)
                    dateCol = sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 12)
                    valCol = sheetMgr.GetCellValue(importSheetConfig, sheetName, i, 13)
                    
                    # Create a new empty workbook set. 
                    workbookSet = Factory.GetWorkbookSet(); 
                    # Open the saved workbook from memory. 
                    workbook = workbookSet.Workbooks.Open(fileFullName); 

                    # System.Threading.Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo("en-US")
#                    workbook = excel.Workbooks.Open(fileFullName)
                    ws = workbook.Worksheets[xmlSheetName]
                    
                    r = numberOfHeaderLines
                    newItems = []
                    updateItems = []
                    totalUpdate = 0
                    while (True):
                        r = r + 1
                        #ddd = ws.Cells(r, 2).Value[default]
                        #vvv = ws.Cells(r, 3).Value2
#                        rowDate = ws.Cells[r, dateCol].Value[default]
#                        rowDate = ws.Cells[r, dateCol].Value   
                        A = int(r - 1)
                        B = int(dateCol - 1)
                        print A, B
                        rowDate = ws.Cells[A,B].Value
                        if (rowDate == None):
                            break
                        rowDate = DateTime.FromOADate(rowDate) 
                        rowDate = rowDate.AddHours(-curTimeShift)
                        C = int(valCol - 1)
                        if hindcastTime <= rowDate and rowDate <= forecastEndTime:
                            rowValue = ws.Cells[A, C].Value
                            # add/update steps in TS
                            curStep = ts.CreateNew()
                            curStep.XValue = rowDate
                            curStep.YValue = rowValue
                            if ts.Contains(rowDate):
                                updateItems.append(curStep)
                            else:
                                newItems.append(curStep)
                    ts.Query(Query())
                    ts.Add(newItems)
                    ts.Update(updateItems)
                    tsMgr.TimeSeriesList.Update(ts, True)
                    if newItems.Count==0 and updateItems.Count==0:
                        logString = logString + "\n!!! No Data."
                        success = False
                    else:
                        logString = logString + "\n Inserted: {0}. Updated: {1}.".format(newItems.Count, updateItems.Count)
                        logString = logString + "\n Last imported time step: {0}.".format(curStep.XValue)
                else:
                    logString = logString + "\n!!! Unknown file format!"
                    success = False
                
            else:
                logString = logString + "\n!!! Cannot find file."
                success = False
                
            i += 1
            
    except Exception as exc:
        logString = logString + "\n!!! Cannot import timeseries!\n!!! Error: {0}".format(exc)
        success = False
        # console.show(locals())
        
#    if excel != None:
#        excel.Quit()

    # log
    print logString
    if success is False:
        raise NameError(logString) 

    pass;
