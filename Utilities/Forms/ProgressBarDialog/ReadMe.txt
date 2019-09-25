The ProgressBarDialog can be used to inform the user progress of long running scripts.
It takes a progress value in the interval 0-100 and a text string which is appended to a scrolling text box.

The script using the dialog needs to be split into two: 
  - one which starts the dialog and 
  - another which does the work including reporting the progress using  dialog.ReportProgress method.

The sample script contains a dialog ready to use, as well as some commented code which – when un-commented -  can be used as a test and inspiration of how to use it.
Note how “TestProgress” creates and shows the dialog with a reference to “worker_DoWork” which performs the work and ReportProgress on the dialog through calls to “_reportProgress” which only formats the message
