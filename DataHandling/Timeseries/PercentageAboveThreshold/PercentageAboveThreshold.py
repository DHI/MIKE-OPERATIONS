import clr
clr.AddReference('DHI.Solutions.Generic.Tools')
clr.AddReference('DHI.Solutions.Generic.Tools')
mgr = app.Modules.Get('Time series Manager')

def Threshold(FlowPath, threshold):
    """
    <Script>
    <Author>NN</Author>
    <Description>Reads a time series and calculate 
    how often the value is above a certain given threshold valud</Description>
    <Parameters>
    <Parameter name="FlowPath" type="IDataseries">Timeseries to analyse</Parameter>
    <Parameter name="threshold" type="double">Threshold value</Parameter>
    </Parameters>
    <ReturnValue type="double">Percentage above threshold</ReturnValue>
    </Script>
    """
    AboveTimes = 0
    TotalTimes = 0
    for FlowPair in FlowPath.GetAll():
        if FlowPair.YValue >= threshold:
            AboveTimes=AboveTimes+1
        TotalTimes = TotalTimes+1
    PercentAboveThreshold =   AboveTimes * 100.0 / TotalTimes
    return PercentAboveThreshold
