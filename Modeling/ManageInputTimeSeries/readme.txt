This folder contains scripts for maintaining scenario input time series.

# Script Storage: CreateScenarioInputTimeSeriesSpreadsheet
Script for creating a spreadsheet containing all input time series of a model setup.
If a scenario is specified, the path of any time series mapped to an input time series will be addded as information.
The spreadsheet can be used for maintaining what time series to include and map to input time series of a scenario. 

The spreadsheet contains the model setup path, the scenario name and four columns:

1. Include (TRUE/FALSE) default TRUE (If TRUE, then the input time series will be mapped when running the UpdateScenarioInputTimeSeries script)
1. Model object name (model object name used as reference)
2. Input Ts name (input time series name used as reference)
3. Time Series Path (Path to the time series mapped to the input time series)

# Script Storage: UpdateScenarioInputTimeSeries (Work in progress)
Script for updating input time series included in a scenario as well as the time series mapped to an input time series.
The script uses the spreadsheet created with CreateInputTimeSeriesSpreadsheet function of the CreateScenarioInputTimeSeriesSpreadsheet storage.
