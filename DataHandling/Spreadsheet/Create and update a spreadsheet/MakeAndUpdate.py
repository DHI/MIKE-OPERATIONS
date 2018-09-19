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
    
    # add a sheet tot he open workbook
    wb = ssmgr.OpenSpreadsheet(ss);
    ssmgr.AddWorksheet(wb, "MySheet");
    
    # update cell C4 in the sheet
    ssmgr.SetCellValue(wb, "MySheet", 3, 2, "Anders");
    
    # insert the sheet into the database in the root
    ssmgr.SpreadsheetList.Add(wb);
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
    
    # modify cell E5 in the sheet
    ssmgr.SetCellValue(ss, "MySheet", 4, 4, "Mekuria");
    
    # save the changes
    ssmgr.SaveSpreadsheet(ss);
    pass;

def UpdateSpreadsheet4(value, spreadsheet, tab, cell):
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
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
    
    # modify cell E5 in the sheet
    ssmgr.SetCellValue(ss, tab, cell, value);
    
    # save the changes
    ssmgr.SaveSpreadsheet(ss); 
