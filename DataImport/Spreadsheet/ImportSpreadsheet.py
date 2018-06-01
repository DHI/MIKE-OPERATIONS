
def ImportSpreadsheet(spreadsheetPath, spreadsheetDirectory):
    """
    <Script>
    <Author>AUG</Author>
    <Description>Import a spreadsheet from a folder on disk</Description>
    <Parameters>
    <Parameter name="spreadsheetPath" type="string">Full path to the spreadsheet</Parameter>
    <Parameter name="spreadsheetDirectory" type="string">directory path on disk</Parameter>
    </Parameters>
    </Script>
    """
    
    # Get a reference to the Time series Manager
    ssMgr = app.Modules.Get('Spreadsheet Manager')
    ssMgr.SpreadsheetList.Import(spreadsheetDirectory, spreadsheetPath);
