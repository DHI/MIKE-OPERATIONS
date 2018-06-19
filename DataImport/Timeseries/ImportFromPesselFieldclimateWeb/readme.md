# Data Import from fieldclimate.com (Pessl Weather Stations)

Pessl Instruments ([www.pesslinstruments.com](http://www.pesslinstruments.com)) is a vendor for weather stations.  Measurement data is provided through the vendors Web GUI [www.fieldclimate.com](http://www.fieldclimate.com).

This script downloads data from the irrimax platform into the MO database through the vendors [REST-API](http://www.fieldclimate.com/api/intro.html).

The user needs to provide username and password for the fieldclimate.com platform and provide this in the configuration spreadsheet in MO. Upon execution, all available data from this user is downloaded into MO's Time Series Manager.