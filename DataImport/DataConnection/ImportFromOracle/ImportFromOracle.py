import System
from System import DateTime
import subprocess
import clr
clr.AddReference('Oracle.DataAccess')
clr.AddReference("System.Data.OracleClient")
from System.Data.OracleClient import *
import os.path
    
def Import(refdate, hindcastperiod, forecastperiod):
    """
    <Script>
    <Author>AUG</Author>
    <Description>This </Description>
    <Parameters>
    <Parameter name="refdate" type="string">Parameter of type IType</Parameter>
    <Parameter name="hindcastperiod" type="int">Hindcast period in hours (Parameter of type int)</Parameter>
    <Parameter name="forecastperiod" type="int">Forecast period in hours (Parameter of type int)</Parameter>
    </Parameters>
    <ReturnValue type="IType">Function returns object of type IType</ReturnValue>
    </Script>
    """
    timeSeriesManager = app.Modules.Get('Time series Manager')
    if timeSeriesManager == None:
        raise Exception('Can''t obtain a reference to Time series Manager.')
            
    refdate= DateTime.ParseExact(refdate, 'MM/dd/yyyy HH:mm', System.Globalization.CultureInfo.InvariantCulture, System.Globalization.DateTimeStyles.None)

    timesteps = GetDataFromOracle("Station1", refdate.AddHours(-hindcastperiod), refdate.AddHours(forecastperiod))

    ts = timeSeriesManager.TimeSeriesList.Fetch('/Station1');
    if(ts == None):
        print 'timeseries not found'
    else:
        if(len(timesteps) > 0):
            ts.Delete(timesteps[0].Date, timesteps[len(timesteps)-1].Date)
            for step in timesteps:
                p = ts.CreateNew();
                p.XValue = step.Date;
                p.YValue = step.Value;
                ts.Add(p);
        else:
            print 'No timestep found for timeseries'
    
def GetDataFromOracle(strExtIDRef, fromDate, toDate):    
    timesteps = []
    if strExtIDRef != None:
        dateFormat = 'yyyy-MM-dd hh:mm:ss';
        dateFormatOracle = 'yyyy-MM-dd HH24:MI:SS';
        
        oradb = "Data Source=(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=pc-sv)(PORT=1521)))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=XE)));User Id=MyID;Password=MyPassword;";
        conn = OracleConnection(oradb); 
        conn.Open(); 
        
        try:
            strSQL  = "SELECT DATE_HEURE as DT, VALEUR "
            strSQL  = strSQL  + "FROM BARPAPI.CG35_ACQUISITION "
            strSQL  = strSQL  + " WHERE MNEMONIQUE LIKE '" + strExtIDRef +  "%'"
            strSQL  = strSQL  + " AND DATE_HEURE BETWEEN to_date('" + fromDate.ToString(dateFormat) + "','" + dateFormatOracle + "') AND to_date('" + toDate.ToString(dateFormat) + "','" + dateFormatOracle + "')"
            strSQL  = strSQL  + " ORDER BY 1"
            cmd = OracleCommand();
            cmd.Connection = conn;
            cmd.CommandText = strSQL;
            dr = cmd.ExecuteReader();
            oldTime=""
            while (dr.Read()):
               if (dr[0] != oldTime):
                    ts = Timestep(dr[0], dr[1].strip())
                    timesteps.append(ts)
                    oldTime=dr[0]
                    
        except Exception as inst:
            print inst
        finally:
            conn.Dispose();       
    return timesteps

        
