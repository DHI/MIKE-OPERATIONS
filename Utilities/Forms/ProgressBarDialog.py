import clr
from System import *
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import *
clr.AddReference("System.Drawing")
from System.Drawing import *
clr.AddReference("System.Threading")
from System.Threading import *
clr.AddReference("System.ComponentModel")
from System.ComponentModel import BackgroundWorker 

worker = None

def ProgressBarDialog(Form):
    """
    <Script>
    <Author>admin</Author>
    <Description>Progress Bar Dialog for showing progress when running time consuming tasks.</Description>
    <Parameters>
    <Parameter name="From" type="System.Windows.Forms.Form">Form to add the progress bar to.</Parameter>
    </Parameters>
    </Script>
    """

    def _BackgroundWorker_ProgressChanged(self, sender, e):
        self.pb.Value = e.ProgressPercentage

        self.txt.AppendText (str(e.UserState) + Environment.NewLine)

        #self.txt.SelectionStart = self.txt.Text.Length
        #self.txt.ScrollToCaret()

    def _BackgroundWorker_RunWorkerCompleted(self, sender, e):
        #self.Close();
        self.pb.Visible = False;
        self.btn.Visible = True;
        #MessageBox.Show("_BackgroundWorker_RunWorkerCompleted")   
        pass

    def _Button_Click(self, sender, e):
        self.Close();

    def _startworker(self, sender, event):
        self.bgworker.RunWorkerAsync();


    def __init__(self, dowork):
        self.Text = 'Progress...'
        self.Size = Size(630,420)
        #self.FormBorderStyle = FormBorderStyle.SizableToolWindow
        self.ShowInTaskbar = False
        self.ControlBox = False
        
        self.btn = Button()
        self.txt = TextBox()
        self.pb = ProgressBar()

        self.Controls.Add(self.txt)
        self.Controls.Add(self.btn)        
        self.Controls.Add(self.pb)        

        self.txt.Multiline =True
        self.txt.Width = 600
        self.txt.Height = 300
        self.txt.ScrollBars = ScrollBars.Both
        self.txt.Location = Point(5, 5)        
        self.txt.Anchor = AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Top | AnchorStyles.Bottom
                
        self.btn.Width = 60
        self.btn.Height = 30
        self.btn.Text = "Close"
        self.btn.Location = Point(270, 10 + self.txt.Bottom)
        self.btn.Anchor = AnchorStyles.Bottom
        self.btn.Visible = False
        self.btn.Click += self._Button_Click

        self.pb.Minimum = 0
        self.pb.Maximum = 100
        self.pb.Step = 1
        self.pb.Value = 0
        
        self.pb.Width = 600
        self.pb.Height = 40
        self.pb.Location = Point(5, 5  + self.txt.Bottom)
        self.pb.Anchor = AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Bottom

        worker = BackgroundWorker() 
        worker.WorkerReportsProgress = True;
        worker.DoWork += dowork;
        worker.ProgressChanged += self._BackgroundWorker_ProgressChanged;
        worker.RunWorkerCompleted += self._BackgroundWorker_RunWorkerCompleted;
        
        self.bgworker = worker
        self.Shown += self._startworker


# ----------------- test method example -----------------
# similar methods can be made in anotyher storage in which case on simply need
#   import progress
# and prefix the constructor with the storage name
#   progress.ProgressBarDialog
#
# uncomment the below cde to activate the test method
#def TestProgress():
#    """
#    <Script>
#    <Author>ANK</Author>
#    <Description>show the progressbar dialog in action - including exception handling</Description>
#    </Script>
#    """
#    try:
#       
#        with ProgressBarDialog(worker_DoWork) as frmProgress:
#            frmProgress.ShowDialog()
#            
#    finally:       
#        if worker!=None:
#            worker.Dispose()
#
#def worker_DoWork(sender, event):
#    try:
#        for i in range(1,101):
#            msg = "msg = " + str(i)
#            val = i
#            _reportProgress(sender, i, msg);
#
#            if i==77:                
#               raise Exception("test exception at i= " + str(i))
#
#            # mimic activity
#            Thread.Sleep(100);
#
#        _reportProgress(sender, 100, "Done");
#    except Exception as e:
#        _reportProgress(sender, i, "Error: " + str(e))
#        
#def _reportProgress(progresdlg, progress, msg):
#    msg = str(progress) + " - " + msg
#    if progress > 100:
#        progress = 99
#    elif progress < 0:
#        progress = 0
#    progresdlg.ReportProgress(progress, msg)
#    print msg
