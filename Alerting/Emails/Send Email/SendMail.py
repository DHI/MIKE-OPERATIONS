import clr
clr.AddReference("DHI.Solutions.Generic")
from DHI.Solutions.Generic import *

from System.IO import Path, Directory

from System.Net import *
from System.Net.Mail import *
from System.Net.Security import *

def customCertValidation(s, certificate, chain, sslPolicyErrors):
    return True;
    
def _SendMail(emails, msgsubj, msghtml, filename = ""):
    print("_SendMail " + emails)
    
    mail_user = r'andersklinting@gmail.com'
    mail_pwd = r'password'    
    mail_server = 'smtp.gmail.com'
    mail_port = 587
    mail_ssl = True
    
    try:
        ServicePointManager.ServerCertificateValidationCallback = RemoteCertificateValidationCallback(customCertValidation);
        
        message = MailMessage()
        message.From = MailAddress(mail_user)
        for em in emails.split(";"):
            message.To.Add(MailAddress(em.strip()));
        message.Subject = msgsubj
        if msghtml != "" :
            message.AlternateViews.Add(AlternateView.CreateAlternateViewFromString(msghtml, None, "text/html"));
        if filename != "":            
            att = Attachment(filename)
            message.Attachments.Add(att)
            
        client = SmtpClient(mail_server, mail_port);
        client.EnableSsl = mail_ssl
        client.UseDefaultCredentials = False
        client.Credentials = NetworkCredential(mail_user, mail_pwd)
        
        client.Send(message);
    except Exception as e:
        print(str(e))


def _GetDoc(docPath):
    
    docMgr = app.Modules.Get("Document Manager")
    doc = docMgr.DocumentList.Fetch(docPath)
    
    # make unique dir and file under the application temprorary dir
    dir = Path.Combine(DssPath.GetTemporaryDirectory(), Path.GetRandomFileName())
    Directory.CreateDirectory(dir)
    filename = Path.Combine(dir, doc.Name)
    
    docMgr.DocumentList.Export(doc, filename, True)

    return filename

def TestEmailDocument():
    """
    <Script>
    <Author>ANK</Author>
    <Description>get a document and send it by email as attachment</Description>
    </Script>
    """

    filename = _GetDoc("/AUG/EUR_MIKEPoweredByDHI_Pricelist_Corporate_Rel2017_21June2017.pdf")
    _SendMail("ank@dhigroup.com", "test send doc subject", "this is a test body, <b>HTML tags</b> are possible", filename)
    print("done")
