import clr
import System
clr.AddReference("System.Drawing")
clr.AddReference("DHI.Solutions.Shell")
clr.AddReference("DHI.Solutions.RealtimeManager.UI")
clr.AddReference("System.Windows.Forms");

from System import *
from System.Drawing import *
import DHI.Solutions.RealtimeManager.UI
import DHI.Solutions.Shell
import System.Windows.Forms

def SaveActiveMapImage():
    """
    <Script>
    <Author>admin</Author>
    <Description>Sample code for getting map information from the current session of MIKE OPERATIONS Desktop. The script should be called from a script item.</Description>
    </Script>
    """

    # Get the real-time data view of the current MO session.
    realtimeDataViewControl = app.Shell.DataViewControls[0];
    
    # Get the map user control, containing map, date time slider an zoom control.
    mapControl = realtimeDataViewControl.MapUserControl;
    
    # Create the image from the map control.
    bitmap = System.Drawing.Bitmap(mapControl.Width, mapControl.Height);
    mapControl.DrawToBitmap(bitmap, mapControl.ClientRectangle);
    
    # Save the image to a file.
    bitmap.Save('c:\\temp\\mymap.png', System.Drawing.Imaging.ImageFormat.Png)
    
    # Save the image to the clipboard.
    System.Windows.Forms.Clipboard.SetImage(bitmap);
   
    pass;
