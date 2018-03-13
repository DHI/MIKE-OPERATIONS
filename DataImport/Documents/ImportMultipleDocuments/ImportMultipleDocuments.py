import os
import clr
clr.AddReference("System")
from System.IO import Directory

def ImportMultipleDocuments(directory, documentFolder):
    """
    <Script>
    <Author>ANK</Author>
    <Description>load all files in a directory into a documentfolder. If a document already exists with the same name as a new file it wil be replaced</Description>
    <Parameters>
    <Parameter name="directory" type="string">directory path</Parameter>
    <Parameter name="documentFolder" type="string">document folder</Parameter>
    </Parameters>
    </Script>
    """
    dm = app.Modules.Get("Document Manager")
    dg = dm.DocumentFolderList.Fetch(documentFolder)
    if (dg == None):
        dg = dm.DocumentFolderList.CreateNew(documentFolder);
        dm.DocumentFolderList.Add(dg);
        
    for f in Directory.GetFiles(directory):
        print f
        fname = os.path.split(f)[1];
        d = dm.DocumentList.Fetch(documentFolder + "/" + fname)
        if d is not None:
            print "  - deleting old document"
            dm.DocumentList.Delete(d);
        dm.DocumentList.Import(f, dg.Id, fname);
        print "  - importing"

    print "done"