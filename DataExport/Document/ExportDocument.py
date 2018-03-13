
def ExportDocument(docPath, directory):
    """
    <Script>
    <Author>ANK</Author>
    <Description>Export a document to a folder on disk</Description>
    <Parameters>
    <Parameter name="docPath" type="string">Full path to the document</Parameter>
    <Parameter name="directory" type="string">directory path on disk</Parameter>
    </Parameters>
    </Script>
    """
    
    # Get a reference to the Time series Manager
    docMgr = app.Modules.Get('Document Manager')
    doc = docMgr.DocumentList.Fetch(docPath)
    
    docFile = Path.Combine(directory, doc.Name)
    docMgr.DocumentList.Export(doc, docFile, True);
