Author: ank@dhigroup.com
Date: 2018/01/16
Version: 2017.2
Downloading data from yr.no is relatively easy. 
You should follow www.yr.no rules.

The script reads a configuration spreadsheet in MO looking like the on attached (two stations from Sweden)

Station is just a name
Yr is the URL of the station in yr.no – see below
TSPath is the specification of where to append the data in the database
Types are the values to grap for the station. you can choose between precipitation, temperature, pressure, windSpeed, windDirection, separate with semicolon.

Fill the spreadsheet and run the script from a job. The script takes 3 arguments:
1.	the path to the spreadsheet
2.	the name of the worksheet (I call mine ‘Mapping’)
3.	shift in hours. The data is given in local time zone, but if you need something else you can shift it. If you
The script will automatically create time series with proper types and unit with names as TSPath + “_” + type
The script will overwrite and append existing data, i.e. over time you will have a longer series.
