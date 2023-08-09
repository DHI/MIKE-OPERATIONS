from __future__ import division
import subprocess

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import clr
clr.AddReference("DHI.Solutions.Generic")
from DHI.Solutions.Generic import *

clr.AddReference('DHI.Solutions.TimeseriesManager.UI')
from DHI.Solutions.TimeseriesManager.UI import Chart

clr.AddReference('System.Windows.Forms.DataVisualization')
clr.AddReference('DHI.Solutions.TimeseriesManager.Tools.Processing')
from System.Windows.Forms.DataVisualization.Charting import ChartImageFormat, Legend

from System import DateTime, Guid, Convert, Array, Environment
from System.IO import File, FileMode, Path, Directory, DirectoryInfo
from System.Net import *
from System.Net.Mail import *
from System.Net.Security import *
import UpdateMergeSensorToMC

from ftplib import FTP
import zipfile
import os

dtruntime = DateTime.Now

tsMgr = app.Modules.Get('Time series Manager')    
tsglist = tsMgr.TimeSeriesGroupList.GetAll()
tslist = tsMgr.TimeSeriesList.GetAll()

def MakeDailyDataReport(emails, pwd):
    """
    <Script>
    <Author>jalu</Author>
    <Description>Generate a HTML table with station detail</Description>
    <Parameters>
    <Parameter name="emails" type="string">recipients comma separated</Parameter>
    <Parameter name="pwd" type="string">password to mail server</Parameter>
    </Parameters>
    </Script>
    """
    
    html = "<HTML><HEAD>"
    html = html + "<TITLE>System overview " + dtruntime.ToString("yyyy-MM-dd") + " @ " + os.environ['COMPUTERNAME'] + "</TITLE>"
    html = html + "<style>body {font-family: Calibri, Verdana, sans-serif } </style>"
    html = html + "</HEAD>"
    html = html + "<BODY>generated: " + dtruntime.ToString("yyyy-MM-dd HH:mm")
    
    # Jobs and simulation status
    html = html + _MakeDailyMiscReport();
    
    # add free disk size for C and E
    try:
        drives = ['c', 'e']
        gb = 1024*1024*1024
        for drive in drives:        
            cmd = 'cmd /C wmic /node:"%COMPUTERNAME%" LogicalDisk Where DriveType="3" Get DeviceID,FreeSpace|find /I "{0}:"'.format(drive)
            x = subprocess.check_output(cmd)
            size = float(x.split()[1])/gb
            html = html + "<br/>Drive {0} has {1} free GB<br/>".format(drive,str(size))
    except:
        html = html + "<br/>failed to calculate disk space<br/>"
      
    html = html + "</BODY></HTML>"

    # send as email
    _log("send email")
    _SendMail("mikeoperationsnz@gmail.com", pwd, emails, "Daily Report: BathingServer", "", html)
    
    _log("Email sent to: " + emails)
    _log("Done" );
            

def _log(msg):
    print("%s - %s" %(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"), msg));



def _MakeDailyMiscReport():

    scmgr = app.Modules.Get("Scenario Manager")
    jobmgr= app.Modules.Get("Job Manager")
    d = DateTime.Now.AddHours(-24)
    html = "<h1>Jobs</h1><p>last 3 job instances per jobhost in the past 24 hours "    
    html = html + "<table cellpadding=3 border=1><tr><th>job</th><th>At</th><tr>"
    for job in sorted(jobmgr.JobList.FetchAll(),key=lambda j: j.Name):
        
        if job != None:
            _log ( job.Name)
            html = html + "<tr><td>" + job.Name + "</td><td>"
            jobinstances = filter(lambda ii: ii.ExecutedAt > d, jobmgr.JobInstanceList.FetchJobInstance(job.Id))
            c=0
            cntOK = 0
            oldComputer = ""
            for ji in sorted(sorted(jobinstances, key=lambda ii: ii.ExecutedAt), key=lambda jj: jj.Computer.lower(),reverse=True)[::-1]:
                if oldComputer == "" or oldComputer != ji.Computer.lower():
                    c=1
                    cntOK = 0
                    if oldComputer != "":
                        html = html + "<br>"
                    oldComputer = ji.Computer.lower()
                else:
                    c=c+1
                bError = not ji.Succeeded and int(ji.Status)<>1
                if not bError: cntOK = cntOK + 1
                if c<=3 and oldComputer == ji.Computer.lower():
                    _log( ji.ExecutedAt.ToString("yyy-MM-dd HH:mm:ss") + " @ " + ji.Computer )
                    html = html + ji.Computer + " @ ";
                    if bError:
                        html = html + "<font color=red>" + ji.ExecutedAt.ToString("yyy-MM-dd HH:mm:ss") + "</font> - " + ji.Status.ToString() + " - " + ji.Duration.ToString() + "<br>"
                    else:
                        html = html + ji.ExecutedAt.ToString("yyy-MM-dd HH:mm:ss") + " - " + ji.Status.ToString() + " - " + ji.Duration.ToString() + "<br>"
                
            html = html + "<br>OK:" + str(cntOK) + "/" + str(jobinstances.Count)                        
            html = html + "&nbsp;</td>"                        
            html = html + "</tr>"
    html = html + "</table>"
    
    
    html = html + "<h1>Simulation</h1><p>last 4 simulations in the past 24 hours"    
    html = html + "<table cellpadding=3 border=1>"
    html = html + "<tr><th>scenario</th><th>at</th><th>status</th><th>tof</th></tr>"
    for sc in sorted(scmgr.ScenarioList.FetchAll(), key=lambda s: s.ModelSetup.Name + s.Name) :
        if sc!=None:
            _log( sc.Name)
            c=0
            cntOK = 0
            sims = filter(lambda s: s.TimeOfSimulationRun > d, scmgr.GetSimulationsForScenario(sc.Id))
            xhtml = ""
            for sim in sorted(sims, key=lambda s: s.TimeOfSimulationRun)[::-1]:
                _log( sim.TimeOfSimulationRun.ToString("yyy-MM-dd HH:mm:ss") )
                bOK = (sim.Status == "OUTPUT_DATA_OK" or sim.Status == "APPROVED") 
                if bOK: 
                    cntOK = cntOK + 1
                if c<4:
                    if c>0:
                        xhtml = xhtml + "<tr>"
                    xhtml = xhtml + "<td>" + sim.TimeOfSimulationRun.ToString("yyy-MM-dd HH:mm:ss") + "</td>"
                    if not (sim.Status == "OUTPUT_DATA_OK" or sim.Status == "APPROVED") :
                        xhtml = xhtml + "<td><font color=red>" + sim.Status + "</font></td>"
                    else:
                        xhtml = xhtml + "<td>" + sim.Status + "</td>"
    
                    xhtml = xhtml + "<td>" + sim.TimeOfForecast.ToString("yyy-MM-dd HH:mm:ss") + "</td></tr>"
                c = c+ 1;

            if sims.Count>0:
                span = c if c<=4 else 4
                html = html + "<tr><td rowspan='" + str(span)+ "'>" + sc.Name  + "<br>OK: " + str(cntOK) + "/" + str(c) + "</td>" + xhtml
                # horizontal lines
                html = html + "<tr><td><hr/><td><hr/><td><hr/><td><hr/></td></tr>" ;

    html = html + "</table>"
    
    
    return html;   

 
def _SendMail(fromMail, pwd, emails, subject, msgtxt, msghtml):
    try:
        # set up the certificate validation bypass function
        ServicePointManager.ServerCertificateValidationCallback = RemoteCertificateValidationCallback(customCertValidation);
 
        # make a new message        
        message = MailMessage()
        
        # give it a sender
        message.From = MailAddress(fromMail)
        
        # assign recipients
        for em in emails.split(","):
            message.To.Add(MailAddress(em.strip()));
        
        # set the subject
        message.Subject = subject
        
        # set the body - as text or as HTML as provided
        if msgtxt != "":
            message.AlternateViews.Add(AlternateView.CreateAlternateViewFromString(msgtxt, None, "text/plain"));
        if msghtml != "" :
            message.AlternateViews.Add(AlternateView.CreateAlternateViewFromString(msghtml, None, "text/html"));
 
        # send email
        # connect to Gmail, set credentials
        client = SmtpClient("imap.gmail.com", 587);
        client.EnableSsl = True
        client.UseDefaultCredentials = False
        client.Credentials = NetworkCredential(fromMail, pwd)
        
        # send the message
        client.Send(message);
    except Exception as e:
        print(str(e))
        raise
    finally:
        ServicePointManager.ServerCertificateValidationCallback = None
     
    # the certificate validation bypass function
    
def customCertValidation(s, certificate, chain, sslPolicyErrors):
    return True;
    
def _SendMail_python(fromMail, emails, subject, msghtml, smtpServer):
    # Create a html message
    msg = MIMEText(msghtml, 'html')
    msg['Subject'] = subject
    msg['From'] = fromMail
    msg['To'] = emails
    
    recepientArray = emails.strip().split(',')
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    if smtpServer == None or smtpServer.strip() == '':
        smtpServer = 'smtpserv.dhigroup.com'
         
    s = smtplib.SMTP(smtpServer)
    
    try:        
        s.sendmail(fromMail, recepientArray, msg.as_string())
    except Exception as e:
        _log("Daily Report failed: " + str(e))
        raise 
    finally:
        s.quit()
