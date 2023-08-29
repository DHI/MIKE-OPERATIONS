import clr
clr.AddReference('DHI.Solutions.Generic')
import DHI.Solutions.Generic
import System

def MakeSpreadsheet():
    """
    <Script>
    <Author>Ander Klinting</Author>
    <Description>Make a spreadsheet and write my name in cell C4</Description>
    </Script>
    """
    # write your code here
    ssmgr = app.Modules.Get('Spreadsheet Manager');
    
    # make a new spreadsheet entity and give it a name
    ss = ssmgr.SpreadsheetList.CreateNew();
    ss.Name = 'AndersTest';
    
    # Open the spreadsheet document
    wb = ssmgr.OpenSpreadsheet(ss);

    try:
        # add a sheet to the open workbook
        ssmgr.AddWorksheet(wb, "MySheet");
        
        # update cell C4 in the sheet
        ssmgr.SetCellValue(wb, "MySheet", 3, 2, "Anders");
        
        # insert the sheet into the database in the root
        ssmgr.SpreadsheetList.Add(wb);
        ssmgr.SaveSpreadsheet(ss)
    finally:
        # Make sure to close the spreadsheet, even if an exception is raised.
        ssmgr.CloseSpreadsheet(ss);
    pass;
    
def UpdateSpreadsheet():
    """
    <Script>
    <Author>Ander Klinting</Author>
    <Description>Update an existing spreadsheet with a new name in cell D4</Description>
    </Script>
    """
    # write your code here
    ssmgr = app.Modules.Get('Spreadsheet Manager');
    
    # open an existing spreadsheet
    ss = ssmgr.OpenSpreadsheet('/AndersTest');

    try:
        # modify cell E5 in the sheet
        ssmgr.SetCellValue(ss, "MySheet", 4, 4, "Mekuria");
        
        # save the changes
        ssmgr.SaveSpreadsheet(ss);
    finally:
        ssmgr.CloseSpreadsheet(ss);
       
    pass;

def UpdateSpreadsheetWithParameters(value, spreadsheet, tab, cell):
    """
    <Script>
    <Author>admin</Author>
    <Description>This will update the value in a specific cell</Description>
    <Parameters>
    <Parameter name="value" type="string">Value to write</Parameter>
    <Parameter name="spreadsheet" type="string">spreadsheet path</Parameter>
    <Parameter name="tab" type="string">tab name</Parameter>
    <Parameter name="cell" type="string">cell name (e.g. 'C3')</Parameter>    
    </Parameters>
    </Script>
    """
    ssmgr = app.Modules.Get('Spreadsheet Manager');
    
    # open an existing spreadsheet
    ss = ssmgr.OpenSpreadsheet(spreadsheet);
    
    try:
        # modify cell E5 in the sheet
        ssmgr.SetCellValue(ss, tab, cell, value);
        
        # save the changes
        ssmgr.SaveSpreadsheet(ss); 
    finally:
        ssmgr.CloseSpreadsheet(ss); 

def WriteFile():
    """
    <Script>
    <Author>admin</Author>
    <Description>Writes a file in the temp directory.</Description>
    </Script>
    """

    tempPath = DHI.Solutions.Generic.DssPath.GetTemporaryDirectory()
    tempFile = System.IO.Path.Combine(tempPath, "dhitest.txt")

    if (System.IO.File.Exists(tempFile)):
        System.IO.File.Delete(tempFile)
    
    System.IO.File.WriteAllText(tempFile, "test text")
