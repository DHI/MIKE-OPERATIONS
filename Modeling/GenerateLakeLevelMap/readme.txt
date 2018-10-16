This script will:
- look for the latest simulation of a given scenario
- pick a particular output timeseries (should be water level)
- get the maximum value of the forecast period
- use this value as input to Raster Calculator

This Raster Calculator tool:
- takes as input a DEM (same datum as water level in model) 
- takes as input the maximum value from timeseries 
- creates a raster showing the water level and the emerged DEM
