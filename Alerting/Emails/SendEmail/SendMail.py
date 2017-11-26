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



def _SendMail(emails, subject, msgtxt, msghtml):

        # mail_user = r'myemail@my.smtpserver.com'

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

        # sending via local smtp

        # smtpserver = smtplib.SMTP("my.stmpserver.com")



        # sending via gmail

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
