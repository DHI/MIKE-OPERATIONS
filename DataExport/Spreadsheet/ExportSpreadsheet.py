from System.IO import * 

def ExportSpreadsheet(spreadsheetPath, directory):
    """
    <Script>
    <Author>AUG</Author>
    <Description>Export a spreadsheet to a folder on disk</Description>
    <Parameters>
    <Parameter name="spreadsheetPath" type="string">Full path to the spreadsheet</Parameter>
    <Parameter name="directory" type="string">directory path on disk</Parameter>
    </Parameters>
    </Script>
    """
    ssMgr = app.Modules.Get('Spreadsheet Manager')
    sheet = ssMgr.SpreadsheetList.Fetch(spreadsheetPath)
    
    sheetFile = Path.Combine(directory, sheet.Name + '.xlsx')
    ssMgr.SpreadsheetList.Export(sheet, sheetFile, True);
