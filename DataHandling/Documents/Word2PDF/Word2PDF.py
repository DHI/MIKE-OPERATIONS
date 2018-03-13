import clr
clr.AddReference('WordToPDFConverterBusiness')
from WordToPDFConverterBusiness import WordToPDFConvert

def ConvertWordToPDF(wordDocFullPath):
    """
    <Script>
    <Author>SNI</Author>
    <Description>Converts Word document to PDF.</Description>
    <Parameters>
    <Parameter name="wordDocFullPath" type="string">Word document full path.</Parameter>
    </Parameters>
    <ReturnValue type="string">PDF full path</ReturnValue>
    </Script>
    """
    pdfFullPath = WordToPDFConvert().Convert(wordDocFullPath)
    print pdfFullPath
    return pdfFullPath
