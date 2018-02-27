You should 
1. download and unzip Adaptor1.zip and Adaptor2.zip
2. copy the content of Adaptor2 into the folder structure of Adaptor1 (content of folder MODEL_SETUP\3B57FCE5-0A71-4CBE-8B8C-D404E94F9FD8\GM000001)
3. register the setup  with Scenario Manager
4. The Adapter executes the model using RunICM.py, which does the following:
  •	Replace values in “Dummy Inflows.csv” with data from dfs0
  •	Call the run.bat to execute the model
  •	Read the results from export subfolder Node_*_depnod.csv N and make dfs0-files in the OUTPUT_DATA

The setup contains:
•	MODEL_SETUP folder contains 
o	a copy of an ICM standalone database with the setup
o	shp subfolder with exported shapefiles of the network
o	import subfolder with the csv-file used to load inflows
o	run.bat – a batch file to start ICMExchange
o	run.rb – the ruby-script used to execute the model wikth ICMExchange
This script is commented, so it should be possible to read, but basically it will
	create results, working and export subfolders
	replace inflows in the model with values from the csv-file
	Get start+end from the inflows
	Prepare w new run – setting start date to start of inflows and duration in minutes matching the data
	Execute the simulation – ticking each second
	Exporting the entire setup as CSV-files to export folder
	Create a transportable database (thought that could be a possibility to use initial conditions – have not worked that out yet)
•	INPUT_DATA folder contains three dfs0-files with inflows. Generic Adapter sees these as the input time series
•	OUTPUT_DATA folder contains templates for the results. So far my script will convert data in Node_*_depnod.csv to dfs0
•	GenericConfig.xml – the adapter configuration file specifying the setup
•	Configuration.cfg – an adapter workfile

The configuration uses the shape files exported in the shp folder to get nodes for Conduit and Node objects, which are then associated with the input a nd output dfs0-files
I use OSGD 1936 / British Grid projection which seems to work


Warning:
Some things are still specific to this setup
