This script :
- reads text files from a folder
- creates a timeseries with the file name in a given time series group, if the timeseries does not already exist
- reads all lines
- parse date time and value from several columns
- add/append timestep to the timeseries, if the timestamp is after last existing value
