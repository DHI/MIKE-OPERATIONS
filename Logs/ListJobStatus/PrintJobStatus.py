import clr

clr.AddReference('DHI.Solutions.Generic')
from DHI.Solutions.Generic import *

def PrintJobStatus():
    """
    <Script>
    <Author>jalu</Author>
    <Description>This script prints a list of all running job instances</Description>
    </Script>
    """
    # write your code here
    jobMgr = app.Modules.Get("Job Manager")
    
    # Make Query for running jobs
    # 1 = Running, 3 = FinishedSuccess, 6 = Terminated
    q = Query()
    q.Add(QueryElement("Status", 1, QueryOperator.Eq))
    
    jobs = jobMgr.JobInstanceList.Fetch(q)
    
    # Report how many jobs are running
    if jobs.Count > 0:
        print str(jobs.Count) + " running job(s): "
        for job in jobs:
            print job.Job.Name + " is running"
    else:
        print "no job is running"
    
    print "...done."
