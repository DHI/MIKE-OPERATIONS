The ManageScenarioInputTimeSeries script storage contains scripts for maintaining scenario input time series.

# Script: CreateInputTimeSeriesSpreadsheet
Script for creating a spreadsheet containing all input time series of a model setup.
If a scenario is specified, the path of any time series mapped to an input time series will be addded as information.
The spreadsheet can be used for maintaining what time series to include and map to input time series of a scenario. 

The spreadsheet contains the model setup path, the scenario name and four columns:

1. Include (TRUE/FALSE) default set to TRUE if a time series is mapped to the input time series (If TRUE, then the input time series will be mapped when running the UpdateScenarioInputTimeSeries script)
2. Model object name (model object name used as reference)
3. Input Ts name (input time series name used as reference)
4. Time Series Path (Path to the time series mapped to the input time series)

# Script: UpdateScenarioInputTimeSeries
Script for updating scenario input time series included in a scenario as well as the time series mapped to an input time series.
The script uses the spreadsheet created with CreateInputTimeSeriesSpreadsheet function of the CreateScenarioInputTimeSeriesSpreadsheet storage.

The script supports the following:

1. Include/exclude input time series depending on the first column "Include"
2. Update time series associations so that an scenario input time serties are mapping to the time series specified in the spreadsheet.
