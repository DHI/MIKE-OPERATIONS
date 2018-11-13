from  System.Diagnostics import *
from System.Collections.Generic import *
from System import DateTime 
from System.IO import *
from System.Threading import *

def Lauch_MIKE21FM_Postprocessors():
    """
    <Script>
    <Author>AUG</Author>
    <Description>This script run several MIKE ZERO post processing tools (DataStatisticsFM, DataExtractionFM, DataVerticalAveragingFM as well as plot composer)</Description>
    </Script>
    """
    bin = r'C:\Program Files (x86)\DHI\2017\bin\x64'
    DataStatisticsFM = bin + r'\DataStatisticsFM.exe'
    DataExtractionFM = bin + r'\DataExtractionFM.exe'
    DataVerticalAveragingFM = bin + r'\DataVerticalAveragingFM.exe'
    MZPlotComposer = bin + r'\MzPlotCompApp.exe'
    
    MT= r'c:\WORK\Simulations\ResultsMT\Analyse'
    
    process = Process.Start(DataExtractionFM, MT + '\Extract_MT-3D_SSC.dxfm');
    process.WaitForExit();
    
    Process.Start(DataVerticalAveragingFM, MT + '\Extract_SSC_-100m.pfs')
    Process.Start(DataVerticalAveragingFM, MT + '\Extract_SSC_Fond.pfs')
    process = Process.Start(DataVerticalAveragingFM, MT + '\Extract_SSC_Max_Colonne.pfs')
    process.WaitForExit();
    
    Process.Start(DataStatisticsFM, MT + '\Extract_SSC_Max_Temporel_Max_Colonne.pfs');
    process.WaitForExit();
    
    Process.Start(MZPlotComposer, MT + '\MyPlot.plc' +  ' -printtofile ' + MT + '\MyPlot.png');
    process.WaitForExit();
