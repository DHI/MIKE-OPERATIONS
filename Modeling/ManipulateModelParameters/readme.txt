This set of scripts illustrates how to edit model parameters.
The example is based on the MIKE HYDRO BASIN model found there (for MIKE ZERO 2017 version)
C:\Program Files (x86)\DHI\2017\MIKE Zero\Examples\MIKE_HYDRO\Basin\Demo

To test this yourself, you should:
- copy the model on your desktop (or in any folder you can edit)
- run the model
- register the model with MIKE HYDRO BASIN adaptor
- Open the model, go to ReservoirNote, right click on "R5 (Reservoir1)" and select "include all parameters"
- Run the scenarion and update variable 'simulation' with correct simulation path

ListModelObject shows how the Get* functions work and will iterate over all model objects in model setup, scenario or simulation and display the properties and values. 

UpdateModelObject will edit the Initial Water Level (single precision number) and the SedimentDistributionType (string) parameters for model object called "R5 (Reservoir 1)" in two different ways (with and without the use of Parameter object). You should get in touch with MIKE if you want to edit a specific parameters and are unsure of their name.

UpdateCrossSectionObject is usefull for MIKE 11 and MIKE HYDRO River models.
