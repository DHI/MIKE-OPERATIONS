from System.IO import *
from System import DateTime
from System.Globalization import *

import clr
clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import *

def ImportTimeseriesFromTextFile():
    """
    <Script>
    <Author>AUG</Author>
    <Description>This script imports timeseries from text files.</Description>
    </Script>
    """
    
    # Set parameters
    folderPath = 'C:\\MGI' # the folder where the files to import are located
    targetTimeseriesGroupName = '/Output' # the group where the timeseries will be created / updated
    datetimeFormat = "dd.MM.yyyy  HH:mm" # tge date time format
    fileExtention="*.txt" # the extention of the input files
    variable = "Rainfall Depth" # the variable type
    valueType = DataSeriesValueType.Step_Accumulated # the value type
    firstLine = 11 # the first line with value (start at zero. 11 means 12th line)
    valueLength = 3 # the number of characters describing the value (e.g. "0.2" -> 3 characters, "11.248" -> 6 characters)
    
    # Set variables
    count = 0
    tmgr = app.Modules.Get('Time series Manager');
    
    # import
    files = Directory.GetFiles(folderPath, fileExtention)
    group = tmgr.TimeSeriesGroupList.Fetch(targetTimeseriesGroupName)
    for file in files:
            filename = Path.GetFileNameWithoutExtension(file)
            ts = tmgr.TimeSeriesList.Fetch(targetTimeseriesGroupName + "/" + filename)
            if ts == None:
                ts = tmgr.TimeSeriesList.CreateNew()
                ts.Name = filename
                ts.YAxisVariable = variable
                ts.ValueType = valueType
                ts.GroupId = group.Id
                tmgr.TimeSeriesList.Add(ts)
                lastTimestep = DateTime.MinValue
            else:
                timestepts = ts.FetchAll()
                if(timestepts.Count > 0):
                    lastTimestep = timestepts[timestepts.Count - 1].XValue
                else:
                    lastTimestep = DateTime.MinValue
            lines = File.ReadAllLines(file);
            for line in lines:
                if count >= firstLine:
                    date = DateTime.ParseExact(line[0:datetimeFormat.Length], datetimeFormat, CultureInfo.InvariantCulture)
                    if date > lastTimestep:
                        value = float(line[-valueLength:])
                        step = ts.CreateNew()
                        step.XValue = date
                        step.YValue = value
                        ts.Add(step)
                count+=1
            tmgr.TimeSeriesList.Update(ts)
