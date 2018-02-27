import clr
clr.AddReference("DHI.Solutions.TimeseriesManager.Tools.TsUtilities")
from DHI.Solutions.TimeseriesManager.Tools import TsUtilities

from System.IO import File, Path, Directory
from System.Globalization import *
from System import DateTime, Double, Activator
from System.Diagnostics import Process, ProcessStartInfo

def RunICM(Adapter):
    """
    <Script>
    <Author>ANK</Author>
    <Description>run an ICM model</Description>
    <Parameters>
    <Parameter name="Adapter" type="IRuntimeAdapter">handle to the adapter</Parameter>
    </Parameters>
    </Script>
    """
    tsMgr = app.Modules.Get("Time series Manager")

    # get the adapter root folder
    rootfolder = Adapter.RootFolderPath
    
    # convert dfs0-input files to Dummy_Inflow.csv
    
    # open dummy inflow and read all lines
    inflowPath = Path.Combine(rootfolder, "MODEL_SETUP\\import\\Dummy Inflow.csv")
    inflowLines = File.ReadAllLines(inflowPath)
    
    # read dfs0-files one by one
    l=8
    tslist = []
    while inflowLines[l].split(",")[0]!="P_DATETIME" :
        tsname = inflowLines[l].split(",")[0]
        tsFile = Path.Combine(rootfolder, "INPUT_DATA", tsname+".dfs0")
        tslist.extend(TsUtilities.ReadFromDFS0(tsMgr, tsFile))
        l = l + 1;

    # make new lines
    newLines = []
    i=0
    while True:
        if i==6:
            # replace startdate
            line = tslist[0].Start.ToString("dd/MM/yyyy HH:mm:ss") + inflowLines[i][19:]
        else:
            line = inflowLines[i]

        newLines.append(line)
        
        if inflowLines[i].split(",")[0]=="P_DATETIME" :
            break;
        i = i + 1;
    
    # continue with timesteps
    for t in range(tslist[0].Count):
        line = tslist[0].Get(t).XValue.ToString("dd/MM/yyyy HH:mm:ss")
        for ds in tslist:
            line += "," + ds.Get(t).YValue.ToString(CultureInfo.InvariantCulture)
        
        newLines.append(line)

    # rewrite the input file
    File.WriteAllLines(inflowPath, newLines)
        
    # run the adapter bat-file
    startInfo = ProcessStartInfo()
    startInfo.CreateNoWindow = False;
    startInfo.UseShellExecute = False;
    startInfo.FileName = Path.Combine(rootfolder, "MODEL_SETUP", "run.bat");
    startInfo.WorkingDirectory = Path.Combine(rootfolder, "MODEL_SETUP")
    with Process.Start(startInfo) as exeProcess :
        exeProcess.WaitForExit();

    # convert exported csv-files to dfs0
    # convert node depths
    dslist = []
    for fil in Directory.GetFiles(Path.Combine(rootfolder,"MODEL_SETUP\\export"),"Node_*_depnod.csv"):
        lines = File.ReadAllLines(fil)
        
        headers = lines[0].split(",")
        for h in headers[2:]:
            ds = tsMgr.TimeSeriesList.CreateNew()
            ds.Name = h.strip()
            ds.YAxisVariable = "Water Level"
            
            dslist.append(ds)
            
    
        for line in lines[1:] :
            if not "[" in line:
                values = line.split(",")
                t = DateTime.ParseExact(values[0].strip(),"dd/MM/yyyy HH:mm:ss", CultureInfo.InvariantCulture)
                for v in range(2,values.Count):
                    ds = dslist[v-2]
                    vp = ds.CreateNew()
                    vp.XValue = t
                    vp.YValue = Double.Parse(values[v].strip(), CultureInfo.InvariantCulture)
                    ds.Add(vp)    
        
        # save to dfs0
        for ds in dslist:
            fil = Path.Combine(rootfolder,"OUTPUT_DATA",ds.Name+".dfs0")
            TsUtilities.ExportToDfs0(ds,fil)
        
def teststub():
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
    </Script>
    """
    # write your code here
    scm = app.Modules.Get('Scenario Manager');
    pass
    for a in scm.Adapters.GetEnumerator():
        if a.Name == "Generic Adapter":
            adaptertype = scm.Adapters.GetAdapter(a.Id);
            adapter = Activator.CreateInstance(adaptertype.Type);
            adapter.RootFolderPath = r"C:\Users\TestUser\Desktop\ANK\Adapter"
    RunICM(adapter);
    pass;
