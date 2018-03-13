
_tofPath = r'c:\temp\tof.txt'
_tempImgPath = r'c:\temp\mcTempImgForReport.png'
_dateTimeFormat = 'dd-MM-yyyy HH:mm:ss'

def GenerateImageForFloodForecastReport(stationId, mikeOperationSpreadsheetPath, obsTsPath, forTsPath):
    """
    <Script>
    <Author>SNI</Author>
    <Description>This method generatea a binary image output corresponding to input parameters. It is written for flood forecasting reports. With capability to show TOF and threshold lines in the image. For accurate TOF line it needs to be used in coordination with ExportSimulationOutputToMC() above.</Description>
    <Parameters>
    <Parameter name="stationId" type="string">Id of the station for which thresholds will be read from mike operation spreadsheet.</Parameter>
    <Parameter name="mikeOperationSpreadsheetPath" type="string">Mike operation spreadsheet path for reading threshold values.</Parameter>
    <Parameter name="obsTsPath" type="string">Observed time series path.</Parameter>
    <Parameter name="forTsPath" type="string">Forecast time series path.</Parameter>
    </Parameters>
    <ReturnValue type="byte[]">image output</ReturnValue>
    </Script>
    """
    
    # colors dictionary to be used
    colorList = {'0': Color.Green, '1': Color.Blue, '2': Color.Orange, '3': Color.Yellow, '4': Color.Red, '5': Color.DarkRed}
    
    #raise Exception('line 1676')
    
    # read mike op spreadsheet.
    ssMgr = app.Modules.Get('Spreadsheet Manager')
    ss = ssMgr.OpenSpreadsheet(ssMgr.SpreadsheetList.Fetch(mikeOperationSpreadsheetPath))
    
    #raise Exception('line 1682')
    
    rangeValues = ssMgr.GetUsedRangeValue(ss, 'Sheet1')
    columnCount = rangeValues.GetLength(1)
    #totalRowCount = rangeValues.GetLength(0)
    #valuesRowCount = totalRowCount - 1
    headers = list(rangeValues)[0:columnCount]
    
    #raise Exception('line 1690')
    
    # find columns with name: 'Name' and name starting with 'WarningLevel_Forecast_'
    nameColumnIndex = 1
    thresholdColumnsIndexArr = []
    
    for headerIndex in range(0, len(headers)):
        if headers[headerIndex] != None:
            if headers[headerIndex] == 'Name':
                nameColumnIndex = headerIndex
            if headers[headerIndex].startswith('WarningLevel_Forecast_'):
                thresholdColumnsIndexArr.append(headerIndex)
    
    #raise Exception('line 1703')
    
    workbook = ss.Workbook
    worksheet = workbook.Worksheets['Sheet1']
    startCellWData = worksheet.Cells['A2']
    endCellWData = worksheet.UsedRange.Cells[worksheet.UsedRange.RowCount-1, worksheet.UsedRange.ColumnCount-1]
    cells = worksheet.Cells[startCellWData.Address + ':' + endCellWData.Address]
    
    ssRowDataArr = GetRangeContent(worksheet = worksheet, range = startCellWData.Address + ':' + endCellWData.Address, ignoreEmptyCells = True) #lambda(cell): _GetCellValue(cell))
    
    dictStationIdThresholds = None
    
    #raise Exception('line 1715')
    
    # iterate over spreadsheet data and find matching station id. prepare dictionary for it.
    for row in ssRowDataArr:
        if row != None and len(row) > 0:
            if row[nameColumnIndex] == stationId:
                # read thresholds
                if dictStationIdThresholds == None:
                    dictStationIdThresholds = {}
                
                dictStationIdThresholds[stationId] = []
                
                for thresholdColumnIndex in thresholdColumnsIndexArr:
                    if row[thresholdColumnIndex] != None:
                        dictStationIdThresholds[stationId].append(float(row[thresholdColumnIndex]))

    #raise Exception('line 1731')

    if dictStationIdThresholds != None and len(dictStationIdThresholds[stationId]) > 0:
        dictStationIdThresholds[stationId] = sorted(dictStationIdThresholds[stationId], key=float)
        #dictStationIdThresholds = {'test':[1,2,3.5]}
    
    # generate plot and return image
    plotCtrl = Chart();
    if app.Shell != None:
        plotCtrl.Shell = app.Shell;
    else:
        plotCtrl.Application = app;
    tsMgr = app.Modules.Get('Time series Manager')
    array = []
    
    #raise Exception('line 1744')
    
    if obsTsPath != None and obsTsPath.Trim() != '' and obsTsPath.Trim() != '-':
        array.append(tsMgr.TimeSeriesList.Fetch(obsTsPath))
    if forTsPath != None and forTsPath.Trim() != '' and forTsPath.Trim() != '-':
        array.append(tsMgr.TimeSeriesList.Fetch(forTsPath))
    
    if len(array) == 0:
        raise Exception('Neither of the specified timeseries path is valid.')
    
    singleTsPlot = len(array) == 1
    plotCtrl.TimeseriesModule = tsMgr;
    plotCtrl.Width = 800;
    plotCtrl.Height = 400;
    plotCtrl.Top = 10;
    plotCtrl.Left = 10;
    plotCtrl.Legends.Add(System.Windows.Forms.DataVisualization.Charting.Legend());
    plotCtrl.AddDataSeries(array, '');
    plotCtrl.LegendDocking = 0
    
    # Set the line colors
    if singleTsPlot:
        plotCtrl.Series[0].Color = Color.Orange
        plotCtrl.Series[0].LegendText = 'Forecast - ' + forTsPath.split('/')[-1]
    else:
        plotCtrl.Series[0].Color = Color.Blue
        plotCtrl.Series[0].LegendText = 'Observed - ' + obsTsPath.split('/')[-1]
        plotCtrl.Series[1].Color = Color.Orange
        plotCtrl.Series[1].LegendText = 'Forecast - ' + forTsPath.split('/')[-1]

    chartArea = plotCtrl.ChartAreas[0];
    #raise Exception('plotCtrl chart areas count: ' + str(len(plotCtrl.ChartAreas)))
    
    chartArea.AxisY.MajorGrid.LineWidth = 0;
    
    yAxisInterval = None
    if len(dictStationIdThresholds) > 0 and len(dictStationIdThresholds[stationId]) > 0:
        chartArea.AxisY.Maximum = dictStationIdThresholds[stationId][-1]
        yAxisInterval = (chartArea.AxisY.Maximum - dictStationIdThresholds[stationId][0]) / 10
        
    if yAxisInterval != None:
        chartArea.AxisY.Interval = yAxisInterval
    
    for legendCount in range(0, len(plotCtrl.Legends)):
        plotCtrl.Legends[legendCount].Title = array[legendCount].YAxisVariable
       
    # the tof line
    tofLine = System.Windows.Forms.DataVisualization.Charting.VerticalLineAnnotation()    
    xValueToDrawTofLine = None
    
    #raise Exception('line 1783')
    
    with open(_tofPath) as f:
        tofOADateStr = f.read()
        xValueToDrawTofLine = Double.Parse(tofOADateStr)
    
    if xValueToDrawTofLine == None:
        # place the tof line in the middle.
        if singleTsPlot:
            xValueToDrawTofLine = (plotCtrl.Series[0].Points[len(plotCtrl.Series[0].Points) - 1].XValue - plotCtrl.Series[0].Points[0].XValue) / 2
            xValueToDrawTofLine = plotCtrl.Series[0].Points[0].XValue + xValueToDrawTofLine
        else:
            xValueToDrawTofLine = (plotCtrl.Series[1].Points[len(plotCtrl.Series[1].Points) - 1].XValue - plotCtrl.Series[1].Points[0].XValue) / 2
            xValueToDrawTofLine = plotCtrl.Series[1].Points[0].XValue + xValueToDrawTofLine
        
    anchorDataPoint = None
    
    #raise Exception('line 1801')
    
    if xValueToDrawTofLine != None:
        points = None
        
        if singleTsPlot:
            points = plotCtrl.Series[0].Points
        else:
            points = plotCtrl.Series[1].Points
            
        for point in points:
            if point.XValue >= xValueToDrawTofLine:
                anchorDataPoint = point
                break
        
        tofLine.AnchorDataPoint = anchorDataPoint #plotCtrl.Series[0].Points[len(plotCtrl.Series[0].Points) / 2];
        tofLine.LineColor = Color.Red;
        tofLine.Width = 3;
        tofLine.Visible = True;
        tofLine.IsInfinitive = True;
        tofLine.ClipToChartArea = chartArea.Name;
        
        plotCtrl.Annotations.Add(tofLine);
    
    #raise Exception('line 1818')
    
    for stationId, thresholds in dictStationIdThresholds.items():
        for thresholdValueCounter in range(0, len(thresholds)):
            # the threshold line
            thresholdLine = System.Windows.Forms.DataVisualization.Charting.HorizontalLineAnnotation();
            thresholdLine.IsInfinitive = True; # make the line infinite
            thresholdLine.ClipToChartArea = chartArea.Name;
            thresholdLine.LineDashStyle = System.Windows.Forms.DataVisualization.Charting.ChartDashStyle.Dash;
            thresholdLine.LineColor = colorList[str(thresholdValueCounter)]
            thresholdLine.AxisY = chartArea.AxisY
            thresholdLine.Y = float(thresholds[thresholdValueCounter])
            plotCtrl.Annotations.Add(thresholdLine)
    
    #raise Exception('line 1832')
    
    imageBytes = None
    memStream = System.IO.MemoryStream()
    plotCtrl.SaveImage(memStream, System.Windows.Forms.DataVisualization.Charting.ChartImageFormat.Png)
    imageBytes = memStream.GetBuffer()
    return imageBytes
    #plotCtrl.SaveImage(_tempImgPath, System.Windows.Forms.DataVisualization.Charting.ChartImageFormat.Png);
    #return System.IO.File.ReadAllBytes(_tempImgPath)
    
    
    #return System.IO.File.ReadAllBytes(_tempImgPath)
