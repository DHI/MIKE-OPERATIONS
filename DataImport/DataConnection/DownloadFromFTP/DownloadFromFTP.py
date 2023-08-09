import ftplib
import System
from System import DateTime
import subprocess
import clr
import os.path

def DownloadFromFtp(server, serverPath, username, password, localPath):
    """
    <Script>
    <Author>ANK</Author>
    <Description>download a specific file from ftp to a local filename</Description>
    <Parameters>
    <Parameter name="server" type="string">server name or ip address, e.g. ftp.dhigroup.com</Parameter>
    <Parameter name="serverPath" type="string">relative path to the root of the server, e.g. /pub/ank2svi/myfile.txt</Parameter>
    <Parameter name="username" type="string">ftp login</Parameter>
    <Parameter name="password" type="string">ftp password</Parameter>
    <Parameter name="localPath" type="string">full path to the download location, e.g. c:\temp\mydownloads\myNewFile.txt</Parameter>
    </Parameters>
    </Script>
    """

    try:
        print("opening ftp server ...")
        ftp = ftplib.FTP(server)
        print("login ...")
        ftp.login(username, password)
        
        print("open local file and download ...")
        with open(localPath, "wb") as file: 
            ftp.retrbinary("RETR " + serverPath, file.write)
            
        print("Successful download of " + serverPath + " to " + localPath)
    except Exception as e:
        print("Error downloading " + serverPath + " : " + str(e));        
        
