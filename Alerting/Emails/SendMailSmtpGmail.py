import os
import smtplib
import string
import email.utils

from smtplib import * 
from email.utils import *
from email.mime.multipart import MIMEMultipart,MIMEBase
from email.mime.text import MIMEText
from email import Encoders
from DHI.Solutions.TimeseriesManager.Tools.Processing import *

def SendMail(emails, subject, msgtxt, msghtml):
    """
    <Script>
    <Author>LPE</Author>
    <Description>Please enter script description here</Description>
    <Parameters>
    <Parameter name="emails" type="string">Destination emails</Parameter>
    <Parameter name="subject" type="string">Email subject</Parameter>
    <Parameter name="msgtxt" type="string">Email body (optional)</Parameter>
    <Parameter name="msghtml" type="string">HTML email body (optional)</Parameter>
    </Parameters>
    <ReturnValue type="IType">Function returns object of type IType</ReturnValue>
    </Script>
    """
    
    mail_user = r'myemail@gmail.com'
    mail_pwd = r'mypassword'

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg['Date']    = formatdate(localtime=True)

    if msghtml != "" :
        msg.attach(MIMEText(msghtml, 'html'));

    if msgtxt != "":
        msg.attach(MIMEText(msgtxt, 'plain'));

    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)        
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(mail_user, mail_pwd)
        smtpserver.sendmail(mail_user, emails.split(";") + [mail_user], msg.as_string())
        smtpserver.quit()

    except Exception, e:
            errorMsg = "Unable to send email. Error: %s" % str(e)
            print errorMsg                   
