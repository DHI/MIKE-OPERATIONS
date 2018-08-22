import clr
clr.AddReference('SpreadsheetGear2017.Core')
from SpreadsheetGear import *

def SpreadsheetToCSV(spreadsheet, outputPath):
    """
    <Script>
    <Author>AUG</Author>
    <Description>This script exports the active worksheet of a spreadsheet to csv</Description>
    <Parameters>
    <Parameter name="spreadsheet" type="string">Spreadsheet to export</Parameter>
    <Parameter name="outputPath" type="string">Output CSV file</Parameter>
    </Parameters>
    </Script>
    """
    ssMgr = app.Modules.Get('Spreadsheet Manager')
    ss = ssMgr.OpenSpreadsheet(spreadsheet)
    workbook = ss.Workbook
    workbook.SaveAs(outputPath, FileFormat.CSV)
