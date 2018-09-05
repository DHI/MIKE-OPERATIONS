Script TestListModelObject shows how the Get* functions work and will iterate over all model objects in model setup, scenario or simulation and display the properties and values. 
It assumes a default naming of group, scenario and simulations as a function of the model setup name.

GetObject – it will return an object representing the properties of a model object. If you know the structure of the model object the properties can be manipulated directory.

GetPathAndParameters -  get a dictionary of all the parameter values object with their path

GetParameter – knowing the path, get the parameter object

SetParameter – updating the model object with a new parameter value. Only possible on a Scenario Model Object 

SetParameterValue – setting the parameter value directory, knowing the path. Only possible on a Scenario Model Object
