This script makes a conversion of Word document report to PDF.

This is how it works.

1. Python script calls c# dll to convert a word document full path.

2. c# dll comes back with the converted pdf file path.

ConvertWordToPDF.py, WordToPDFConverterBusiness.dll

Converted pdf file is created in the same folder as the input word document. Same name but different extension.

Note: Requirement for this to work is that MS Word should be installed on the machine. I have tested with MS Word 2013 installed.


Limitation: It doesn't run properly when running as a background job. It works only when we execute the script manualy.
