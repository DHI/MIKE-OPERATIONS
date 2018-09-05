This set of scripts illustrates how to edit model parameters.
The example is based on the MIKE HYDRO BASIN model found there (for MIKE ZERO 2017 version)
C:\Program Files (x86)\DHI\2017\MIKE Zero\Examples\MIKE_HYDRO\Basin\Demo

To test this yourseld, you should:
- copy the model on your desktop (or in any folder you can edit)
- run the model
- register the model with MIKE HYDRO BASIN adaptor
- Open the model, go to ReservoirNote, right click on "R5 (Reservoir1)" and select "include all parameters"


Script TestListModelObject shows how the Get* functions work and will iterate over all model objects in model setup, scenario or simulation and display the properties and values. 
It assumes a default naming of group, scenario and simulations as a function of the model setup name.

GetObject – it will return an object representing the properties of a model object. If you know the structure of the model object the properties can be manipulated directory.

GetPathAndParameters -  get a dictionary of all the parameter values object with their path

GetParameter – knowing the path, get the parameter object

SetParameter – updating the model object with a new parameter value. Only possible on a Scenario Model Object 

SetParameterValue – setting the parameter value directory, knowing the path. Only possible on a Scenario Model Object
