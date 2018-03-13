What is it doing?
Changes source type of all time series from Blob to Raw. 

Why?
Source type of time series is in MIKE INFO by default set to "Blob". 
This type is not possible to view in some web applications where "Raw" is required

How?
If you already have some time series in Blob values follow steps below:
	1) Go to "C:\Program Files (x86)\DHI\2017\MIKE OPERATIONS 7\DHI.Solutions.TimeseriesManager.Config"  
	2) change line "<add key="TimeSeriesStorageType" value="Blob"/> to <add key="TimeSeriesStorageType" value="Raw"/> 
	3) Import BlobToRaw.py to your project.    
	4) Copy Blobfixer.dll to MIKE OPERATIONS bin (e.g. C:\Program Files (x86)\DHI\2017\MIKE OPERATIONS 7 )
	5) Run BlobToRaw.py
	6) Go to MIKE OPERATIONS bin and find there file "BlobFixer_output.sql"
	7) Run that sql in your database
