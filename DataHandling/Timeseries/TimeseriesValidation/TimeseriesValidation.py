import sys
import clr
import System
from System import DateTime
import datetime
from System.Globalization import CultureInfo
from System.Collections.Generic import List, Dictionary

clr.AddReference('DHI.Solutions.TimeseriesManager.Interfaces')
clr.AddReference('DHI.Solutions.TimeseriesManager.Business')
clr.AddReference('DHI.Solutions.TimeseriesManager.Tools.Processing')
from DHI.Solutions.TimeseriesManager.Tools.Processing import *

worksheetName = 'Sheet1' # Name of the first worksheet.
   
def ExecuteValidation(validationSpreadsheetPath, tOF, hindcast, forecast, logFilePath):
    """
    <Script>
    <Author>KTH</Author>
    <Description>Executes the time series validation according to the validation spreadsheet specified.</Description> 
    <Parameters>
    <Parameter name="validationSpreadsheetPath" type="string">Path to the spreadsheet</Parameter>
    <Parameter name="tOF" type="string">Time of Forecast for simulation</Parameter>
    <Parameter name="hindcast" type="int">Hindcast period in day.</Parameter>
    <Parameter name="forecast" type="int">Forecast period in day.</Parameter>
    <Parameter name="logFilePath" type="string">Path where the log file importLog.txt should be written.</Parameter>
    </Parameters>
    </Script>
    """
    
    fileName = 'ValidationLog_' + System.DateTime.Now.ToString('yyyy-MM-dd_HH-mm-ss') + '.txt';
    
    global logFileName;
    logFileName = System.IO.Path.Combine(logFilePath, fileName);

    validationInfoList = LoadValidationSpreadsheet(validationSpreadsheetPath);
    
    timeSeriesManager = app.Modules.Get('Time series Manager')
    if timeSeriesManager == None:
        raise Exception('Can''t obtain a reference to Time series Manager.')
        
    tof = DateTime.ParseExact(tOF, 'MM/dd/yyyy HH:mm:ss', CultureInfo.InvariantCulture)

    for validationInfo in validationInfoList:
        ts = timeSeriesManager.TimeSeriesList.Fetch(validationInfo.TsPath);
        print(validationInfo.TsOutputPath)
        if (ts == None):
            message = 'Time series ' + validationInfo.TsPath + ' must be created before import.';
            WriteError(message);
        else:
            periodOption = PeriodOption.Entire_timeseries;
            replaceOption = ReplaceOption.Replace_all_hits;
            
            startDate = System.DateTime.MinValue;
            endDate = System.DateTime.MaxValue;
            startValidationDate = tof.AddDays(-hindcast)
            endValidationDate = tof.AddDays(forecast)

            if (startValidationDate != None and endValidationDate != None):
                if type(startValidationDate) is System.DateTime:
                    startDate = tof.AddDays(-hindcast);
                else:
                    startDate = System.DateTime.ParseExact(tof.AddDays(-hindcast), 'MM/dd/yyyy HH:mm:ss', System.Globalization.CultureInfo.InvariantCulture)
                #Convert dates from String format to DateTime format
                if type(endValidationDate) is System.DateTime:
                    endDate = tof.AddDays(forecast);
                else:
                    endDate = System.DateTime.ParseExact(tof.AddDays(forecast), 'MM/dd/yyyy HH:mm:ss', System.Globalization.CultureInfo.InvariantCulture)
                
                periodOption = PeriodOption.Sub_period;

            rangeOption = RangeOption.Replace_outside_range;
            rangeMax = 0;
            rangeMin = 0;
            maxGapUnit = MaxGapUnit.Hours;
            maxGap = 1;
            replaceByValueForExceededRate = None;
            replaceByValue = None;
            replaceValue = 0;
            maxRateOfChange = 0;
            rateOfChangeOption = RateOfChangeOption.With_constant;
            rateOfChangeUnit = ReplaceTool_RateOfChangeUnit.Per_hour;

            # Change input time series or copy.
            if (validationInfo.TsOutputPath <> None and validationInfo.TsOutputPath.Length > 0):
                processOption = ProcessOption.Process_copy;
            else:
                processOption = ProcessOption.Process_input_timeseries;
                
            # Remplace les valeurs nulles par une valeur de remplacement (interpolationlineaire)
            if (validationInfo.ReplaceValue <> None):
                replaceValueMethod = ReplaceValueMethod.With_constant;
                replaceByValue = validationInfo.ReplaceValue
                replaceValue = None
       
                try:
                    outputTimeSeries = ReplaceValuesTool(ts, replaceValueMethod, periodOption,
                        replaceOption, processOption, startDate, endDate, replaceValue, 
                        replaceByValue, replaceByValueForExceededRate, rangeMax, 
                        rangeMin, rangeOption, maxRateOfChange, rateOfChangeUnit, 
                        rateOfChangeOption, maxGapUnit, maxGap);
                
                    if (outputTimeSeries <> None and outputTimeSeries.Count > 0):
                        ts = outputTimeSeries[0];

                except Exception, e:
                    message = 'Execute Replace Value Tool: ' + e.ToString();
                    WriteError(message);
         
            # Limit_Rate_Of_Change
            if (validationInfo.MaxRateOfChange <> None):
                replaceValueMethod = ReplaceValueMethod.Limit_rate_of_change;
                maxRateOfChange = validationInfo.MaxRateOfChange;
                rateOfChangeOption = RateOfChangeOption.With_constant;
                rateOfChangeUnit = ReplaceTool_RateOfChangeUnit.Per_hour;
                replaceByValue = validationInfo.ReplaceValue
                replaceValue = validationInfo.ReplaceValue
                replaceByValueForExceededRate = validationInfo.ReplaceValue
                
                try:
                    outputTimeSeries = ReplaceValuesTool(ts, replaceValueMethod, periodOption,
                        replaceOption, processOption, startDate, endDate, replaceValue, 
                        replaceByValue, replaceByValueForExceededRate, rangeMax, 
                        rangeMin, rangeOption, maxRateOfChange, rateOfChangeUnit, 
                        rateOfChangeOption, maxGapUnit, maxGap);
                
                    if (outputTimeSeries <> None and outputTimeSeries.Count > 0):
                        ts = outputTimeSeries[0];
                except Exception, e:
                    message = 'Execute Replace Value Tool: ' + e.ToString();
                    WriteError(message);
                
            # Replace_Range_With_Constant
            if (validationInfo.RangeMax <> None and validationInfo.RangeMin <> None):
                replaceValueMethod = ReplaceValueMethod.Replace_range_with_constant;
                rangeOption = RangeOption.Replace_outside_range;
                rangeMax = validationInfo.RangeMax;
                rangeMin = validationInfo.RangeMin;
                replaceByValue = validationInfo.ReplaceValue
                replaceValue = validationInfo.ReplaceValue

                try:
                    outputTimeSeries = ReplaceValuesTool(ts, replaceValueMethod, periodOption,
                        replaceOption, processOption, startDate, endDate, replaceValue, 
                        replaceByValue, replaceByValueForExceededRate, rangeMax, 
                        rangeMin, rangeOption, maxRateOfChange, rateOfChangeUnit, 
                        rateOfChangeOption, maxGapUnit, maxGap);
                
                    if (outputTimeSeries <> None and outputTimeSeries.Count > 0):
                        ts = outputTimeSeries[0];
                except Exception, e:
                    message = 'Execute Replace Value Tool: ' + e.ToString();
                    WriteError(message);
                        
    
            # Remove_From_Max_Gap
            if (validationInfo.MaxGap <> None and validationInfo.MaxGap > 0):
                replaceValueMethod = ReplaceValueMethod.Remove_from_max_gap;
                maxGapUnit = MaxGapUnit.Hours;
                maxGap = validationInfo.MaxGap;
                replaceByValue = validationInfo.ReplaceValue
                replaceValue = validationInfo.ReplaceValue
        
                try:
                    outputTimeSeries = ReplaceValuesTool(ts, replaceValueMethod, periodOption,
                        replaceOption, processOption, startDate, endDate, replaceValue, 
                        replaceByValue, replaceByValueForExceededRate, rangeMax, 
                        rangeMin, rangeOption, maxRateOfChange, rateOfChangeUnit, 
                        rateOfChangeOption, maxGapUnit, maxGap);
                
                    if (outputTimeSeries <> None and outputTimeSeries.Count > 0):
                        ts = outputTimeSeries[0];

                except Exception, e:
                    message = 'Execute Replace Value Tool: ' + e.ToString();
                    WriteError(message);
                    
            # Replace_with interpolation
            if (validationInfo.ReplaceValue <> None):
                replaceValueMethod = ReplaceValueMethod.Interpolation;
                replaceValue = validationInfo.ReplaceValue

                try:
                    outputTimeSeries = ReplaceValuesTool(ts, replaceValueMethod, periodOption,
                        replaceOption, processOption, startDate, endDate, replaceValue, 
                        replaceByValue, replaceByValueForExceededRate, rangeMax, 
                        rangeMin, rangeOption, maxRateOfChange, rateOfChangeUnit, 
                        rateOfChangeOption, maxGapUnit, maxGap);
                
                    if (outputTimeSeries <> None and outputTimeSeries.Count > 0):
                        ts = outputTimeSeries[0];
                except Exception, e:
                    message = 'Execute Replace Value Tool: ' + e.ToString();
                    WriteError(message);
            WriteTimeSeries(validationInfo.TsOutputPath, ts);
                    
                    
    return;
	
def WriteTimeSeries(outputPath, outputTimeSeries):
    if (outputTimeSeries == None or outputTimeSeries.Count == 0):
        return;

    timeSeriesManager = app.Modules.Get('Time series Manager')
    if timeSeriesManager == None:
        raise Exception('Can''t obtain a reference to Time series Manager.')

    ts = outputTimeSeries;
    ts.UseChangeLog = False;
    data = ts.GetAll();

    if (outputPath <> None and outputPath.Length > 0):
        tsPath = outputPath.TrimEnd('/');
        tsPath = tsPath + '/' + outputTimeSeries.Name;
        existingTs = timeSeriesManager.TimeSeriesList.Fetch(tsPath);
        
        if (existingTs <> None):
            existingTs.DeleteAll();
            existingTs.Add(data);
            timeSeriesManager.TimeSeriesList.Update(existingTs);
        else:
            # Get group id from the output ts path.
            groupPath = outputPath;
            tsGroup = timeSeriesManager.TimeSeriesGroupList.Fetch(groupPath);
            
            if (tsGroup <> None):
                ts.GroupId = tsGroup.Id;
                timeSeriesManager.TimeSeriesList.Add(ts);
            else:
                WriteError('Time series group: ' + groupPath + ' was not found.')
    else:
        ts.DeleteAll()
        ts.Add(data);
        timeSeriesManager.TimeSeriesList.Update(ts);
        pass;

def WriteError(message):
    """
    <Script>
    <Author>KTH</Author>
    <Description>Writes an entry in the validation log file.</Description> 
    <Parameters>
    <Parameter name="message" type="string">Message to write.</Parameter>
    </Parameters>
    </Script>
    """
    messageNewLine = System.Environment.NewLine + message;
    System.IO.File.AppendAllText(logFileName, messageNewLine);
    
    return; 
	
def LoadValidationSpreadsheet(validationSpreadsheetPath):
    """
    <Script>
    <Author>KTH</Author>
    <Description>Load a station validation information spreadsheet.</Description> 
    <Parameters>
    <Parameter name="validationSpreadsheetPath" type="string">Path to the spreadsheet</Parameter>
    </Parameters>
    <ReturnValue type="List[ValidationInfo]" >time series </ReturnValue>
    </Script>
    """  

    ssmgr = app.Modules.Get('Spreadsheet Manager');
    if ssmgr == None:
        raise Exception('Can''t obtain a reference to Spreadsheet Manager.')        

    stationValidationList = List[ValidationInfo]();

    # Fetch and open the station validation spreadsheet.
    stationValidationSpreadsheet = ssmgr.SpreadsheetList.Fetch(validationSpreadsheetPath)
    if (stationValidationSpreadsheet == None):
        raise Exception('Can''t locate ' + validationSpreadsheetPath + ' station validation spreadsheet.')
        
    # Open the station validation spreadsheet.
    ssmgr.OpenSpreadsheet(stationValidationSpreadsheet);
    
    # Read all rows in the station map spreadsheet and add the maps to the 3 map dictinaries.
    rowNo = 1; # Start in the second row.

    while True:
        objectTsPath = ssmgr.GetCellValue(stationValidationSpreadsheet, worksheetName, rowNo, 0);
        
        # Stop when the value of the first column is empty.
        if objectTsPath == None:
            break;
        
        objectTsOutputPath = ssmgr.GetCellValue(stationValidationSpreadsheet, worksheetName, rowNo, 1)
        objectRangeMin = ssmgr.GetCellValue(stationValidationSpreadsheet, worksheetName, rowNo, 2)
        objectRangeMax = ssmgr.GetCellValue(stationValidationSpreadsheet, worksheetName, rowNo, 3)
        objectReplaceValue = ssmgr.GetCellValue(stationValidationSpreadsheet, worksheetName, rowNo, 4)
        objectMaxGap = ssmgr.GetCellValue(stationValidationSpreadsheet, worksheetName, rowNo, 5)
        objectMaxRateOfChange = ssmgr.GetCellValue(stationValidationSpreadsheet, worksheetName, rowNo, 6)
        
        tsPath = objectTsPath.ToString().Trim();
        tsOutputPath = None
        rangeMin = None;
        rangeMax = None;
        replaceValue = None;
        maxGap = None;
        maxRateOfChange = None;
        
        isValid = True;
        
        if (objectTsOutputPath <> None and objectTsOutputPath.ToString().Trim().Length > 0):
            tsOutputPath = objectTsOutputPath.ToString().Trim();

        if (objectRangeMin <> None):
            try:
                rangeMin = float(objectRangeMin)
            except:
                rangeMin = -999999.
            
            if (rangeMin == -999999.):
                isValid = False;
                rangeMin = None
                WriteError('StationId ' + referenceId + ' has an invalid min range.')

        if (objectRangeMax <> None):
            try:
                rangeMax = float(objectRangeMax)
            except:
                rangeMax = -999999.
            
            if (rangeMax == -999999.):
                isValid = False;
                rangeMax = None;
                WriteError('StationId ' + referenceId + ' has an invalid max range.')            
        
        if (objectReplaceValue <> None):
            try:
                replaceValue = float(objectReplaceValue)
            except:
                replaceValue = -999999.
            
            if (replaceValue == -999999.):
                isValid = False;
                replaceValue = None;
                WriteError('StationId ' + referenceId + ' has an invalid replace value.')            

        if (objectMaxGap <> None):
            try:
                maxGap = int(objectMaxGap)
            except:
                maxGap = -999999
            
            if (maxGap == -999999):
                isValid = False;
                maxGap = None;
                WriteError('StationId ' + referenceId + ' has an invalid max gap.')            

        if (objectMaxRateOfChange <> None):
            try:
                maxRateOfChange = float(objectMaxRateOfChange)
            except:
                maxRateOfChange = -999999.
            
            if (maxRateOfChange == -999999.):
                isValid = False;
                maxRateOfChange = None;
                WriteError('StationId ' + referenceId + ' has an invalid max rate of change.')            

        if isValid == True:
            validationInfo = ValidationInfo(tsPath, tsOutputPath, rangeMin, rangeMax, replaceValue, maxGap, maxRateOfChange);
            stationValidationList.Add(validationInfo);
            print(validationInfo.TsOutputPath)

        rowNo = rowNo + 1;
        
    ssmgr.CloseSpreadsheet(stationValidationSpreadsheet);
    
    return stationValidationList;

def ReplaceValuesTool(inputItems, replaceValueMethod, periodOption, 
        replaceOption, processOption, startDate, endDate, replaceValue, 
        replaceByValue, replaceByValueForExceededRate, rangeMax, 
        rangeMin, rangeOption, maxRateOfChange, rateOfChangeUnit, 
        rateOfChangeOption, maxGapUnit, maxGap):
    """
    <Script>
    <Author>KTH</Author>
    <Description>This tool can replace a specified value using different methods.</Description> 
    <Parameters>
    <Parameter name="validationSpreadsheetPath" type="string">Path to the spreadsheet</Parameter>
    </Parameters>
    <ReturnValue type="Dictionary[string, List[ValidationInfo]]" >time series </ReturnValue>
    </Script>

    @param inputItems @type Array
        Tool input items

    @param replaceValueMethod @type 
        DHI.Solutions.TimeseriesManager.Tools.Processing.ReplaceValueMethod
        This setting determines how the specified value shall be 
        replaced.
        @values ReplaceValueMethod.With_constant, 
        ReplaceValueMethod.Last_value_before, 
        ReplaceValueMethod.First_value_after, 
        ReplaceValueMethod.Interpolation, 
        ReplaceValueMethod.Replace_range_with_constant, 
        ReplaceValueMethod.Limit_rate_of_change, 
        ReplaceValueMethod.Remove_from_max_gap

    @param periodOption @type 
        DHI.Solutions.TimeseriesManager.Tools.Processing.PeriodOption
        The tool can be applied on the entire length of the input time 
        series, or on a sub-period.
        @values PeriodOption.Entire_timeseries, PeriodOption.Sub_period

    @param replaceOption @type 
        DHI.Solutions.TimeseriesManager.Tools.Processing.ReplaceOption
        This option determines if all values that matches the Replace 
        value shall be processed, or if only the first hit shall be 
        processed.
        @values ReplaceOption.Replace_all_hits, 
        ReplaceOption.First_hit_only

    @param processOption @type 
        DHI.Solutions.TimeseriesManager.Tools.Processing.ProcessOption
        This option defines if the tool shall process the input items, 
        or a copy of the inputs.
        @values ProcessOption.Process_copy, 
        ProcessOption.Process_input_timeseries

    @param startDate @type System.DateTime
        The start date of the sub-period.

    @param endDate @type System.DateTime
        The end date of the sub-period.

    @param replaceValue @type System.Nullable<System.Double, mscorlib>
        The value that shall be replaced according to the specified 
        option.

    @param replaceByValue @type System.Nullable<System.Double, mscorlib>
        The value that will be inserted.

    @param replaceByValueForExceededRate @type 
        System.Nullable<System.Double, mscorlib>
        The value that will be inserted.

    @param rangeMax @type System.Nullable<System.Double, mscorlib>
        The upper limit of the range for which the values will be 
        replaced.

    @param rangeMin @type System.Nullable<System.Double, mscorlib>
        The lower limit of the range for which the values will be 
        replaced.

    @param rangeOption @type 
        DHI.Solutions.TimeseriesManager.Tools.Processing.RangeOption
        This setting defines if the values inside or outside the 
        specified range shall be replaced.
        @values RangeOption.Replace_outside_range, 
        RangeOption.Replace_inside_range

    @param maxRateOfChange @type System.Double
        The max allowed rate of change (absolute value).

    @param rateOfChangeUnit @type 
        DHI.Solutions.TimeseriesManager.Tools.Processing.ReplaceTool_RateOfChangeUnit
        The rate of change unit determines how the specified rate of 
        change will be interpreted.
        @values ReplaceTool_RateOfChangeUnit.Per_second, 
        ReplaceTool_RateOfChangeUnit.Per_minute, 
        ReplaceTool_RateOfChangeUnit.Per_hour, 
        ReplaceTool_RateOfChangeUnit.Per_day

    @param rateOfChangeOption @type 
        DHI.Solutions.TimeseriesManager.Tools.Processing.RateOfChangeOption
        The way that values outside the allowed rate of change should be 
        set.
        @values RateOfChangeOption.With_max_allowed_change, 
        RateOfChangeOption.With_constant

    @param maxGapUnit @type 
        DHI.Solutions.TimeseriesManager.Tools.Processing.MaxGapUnit
        The max gap unit defines the unit of the specified max gap.
        @values MaxGapUnit.Seconds, MaxGapUnit.Minutes, 
        MaxGapUnit.Hours, MaxGapUnit.Days

    @param maxGap @type System.Int32
        The max gap defines the maximum gap allowed in a time series.
    """
    tool = app.Tools.CreateNew('Replace value tool')
    
    if isinstance(inputItems,list):
        for inputItem in inputItems:
            tool.InputItems.Add(inputItem)
    else:
        if inputItems <> None:
            tool.InputItems.Add(inputItems)
    
    tool.ReplaceValueMethod = replaceValueMethod
    tool.PeriodOption = periodOption
    tool.ReplaceOption = replaceOption
    tool.ProcessOption = processOption
    tool.StartDate = startDate
    tool.EndDate = endDate
    tool.ReplaceValue = replaceValue
    tool.ReplaceByValue = replaceByValue
    tool.ReplaceByValueForExceededRate = replaceByValueForExceededRate
    tool.RangeMax = rangeMax
    tool.RangeMin = rangeMin
    tool.RangeOption = rangeOption
    tool.MaxRateOfChange = maxRateOfChange
    tool.RateOfChangeUnit = rateOfChangeUnit
    tool.RateOfChangeOption = rateOfChangeOption
    tool.MaxGapUnit = maxGapUnit
    tool.MaxGap = maxGap
    tool.Execute()
    return tool.OutputItems

    
# Class for holding validation information for a station.
class ValidationInfo(object):
    def __init__(self, tsPath, tsOutputPath, rangeMin, rangeMax, replaceValue, maxGap, maxRateOfChange):
        self.TsPath = tsPath
        self.TsOutputPath = tsOutputPath
        self.RangeMin = rangeMin
        self.RangeMax = rangeMax
        self.ReplaceValue = replaceValue
        self.MaxGap = maxGap
        self.MaxRateOfChange = maxRateOfChange
        print('serie temporelle =' + tsPath)
        print('dossier validation = ' + tsOutputPath)
        print('valeur min =',rangeMin)
        print('valeur max =',rangeMax)
        print('valeur de remplacement =',replaceValue)
        print('max gap =',maxGap)
        print('max tx evloution/h =',maxRateOfChange)       
