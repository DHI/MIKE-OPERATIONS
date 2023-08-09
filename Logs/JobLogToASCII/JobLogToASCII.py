import clr
clr.AddReference("DHI.Solutions.JobManager.JobRunner")
from DHI.Solutions.JobManager.JobRunner import JobContext
from System.IO import File
 
def GetJobInstanceLog():

    """
    <Script>
    <Author>LPE</Author>
    <Description>Please enter script description here</Description>
    </Script>
    """

    # get id of the current instance    
    id = JobContext.Instance.JobInstanceID
    print(id.ToString())
   

    # get the currently logged data from the database
    jobMgr = app.Modules.Get("Job Manager")
    ji = jobMgr.JobInstanceList.Fetch(id);
 
    # output it

    # print ji.Log
    File.WriteAllText(r"c:\temp\ji_"+id.ToString()+".xml", ji.Log)
