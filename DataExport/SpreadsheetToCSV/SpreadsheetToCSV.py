import clr
clr.AddReference('SpreadsheetGear2017.Core')
from SpreadsheetGear import *

def SpreadsheetToCSV():
    """
    <Script>
    <Author>AUG</Author>
    <Description>This script exports the active worksheet of a spreadsheet to csv</Description>
    </Script>
    """
    ssMgr = app.Modules.Get('Spreadsheet Manager')
    ss = ssMgr.OpenSpreadsheet('/MySpreadsheet')
    workbook = ss.Workbook
    workbook.SaveAs('c:\\Output\\MySpreadsheet.csv', FileFormat.CSV)
