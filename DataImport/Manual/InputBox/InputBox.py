import clr
import os
import sys

clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Form, DockStyle, WebBrowser, TextBox, Keys, MessageBox, Button

value = 1
tb = TextBox()
f = Form()

def TestWebPub():
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
    </Script>
    """
    
    if sys.platform != 'cli':
        import pythoncom
        pythoncom.CoInitialize()
    
    f.Text = 'Select Factor'
    f.Width = 300
    f.Height = 60
    
    tb.Text = value.ToString()
    tb.Dock = DockStyle.Left
    
    bt = Button()
    bt.Click += OnKeyPress
    bt.Text = "OK"
    bt.Dock = DockStyle.Right
    
    f.Controls.Add(tb)
    f.Controls.Add(bt)
    f.ShowDialog()
    
def OnKeyPress(sender, args):
    factor = tb.Text
    TSCalculator_Factor(int(factor))
    f.Close()
    

def TSCalculator_Factor(factor):
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
    <Parameters>
    <Parameter name="factor" type="int">Parameter of type int</Parameter>
    </Parameters>
    </Script>
    """
    print factor
