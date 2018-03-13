import sys
sys.path.append(r'C:\Program Files (x86)\DHI\2011\bin')
import clr
clr.AddReference('DHI.TimeSeries')
clr.AddReference('DHI.TimeSeries.TSPlot')
clr.AddReference('TSPlotCtrl')
import DHI.TimeSeries
clr.AddReference('System.Windows.Forms')
import System.Windows.Forms
    
def PlotTimeSeriesFromDisk():
    """
    <Script>
    <Author>Anders Klinting</Author>
    <Description>This script reads a time series from file using TS library and 
    plots them in a new window</Description>
    </Script>
    """
    # read timeseries data from files
    tsobj1 = DHI.TimeSeries.TSObjectClass();
    tsobj1.Connection.FilePath = r'C:\temp\CALI-DEMO.DFS0 - 1 - DISCHARGE, CALI_INFLOW.dfs0';
    tsobj1.Connection.Open();

    # initialize visual components
    
    form = System.Windows.Forms.Form();
    plotCtrl = DHI.TimeSeries.TSPlot();
    plotCtrl.Dock = System.Windows.Forms.DockStyle.Fill;
    form.Controls.Add(plotCtrl);
    form.Width=600;
    form.Height=500;
    form.Show();

    # set data for plotting
    plotCtrl.AddTSObject(tsobj1);

    # run winforms app
    System.Windows.Forms.Application.Run(form);
