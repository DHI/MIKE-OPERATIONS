import clr
import sys
clr.AddReference('DHI.Solutions.Generic')
import DHI.Solutions.Generic
import System

def RemovePreparedScripts(scriptPath):
    """
    <Script>
    <Author>admin</Author>
    <Description>Script to remove associated prepared scripts (parameters stored) for a script.</Description>
    <Parameters>
    <Parameter name="scriptPath" type="string">Full path to the script to remove prepared script for.</Parameter>
    </Parameters>
    </Script>
    """
    
    if scriptPath == None:
        raise System.ArgumentException('ScriptPath should be specified')
        
    scriptModule = app.Modules.Get('Script Manager')
    
    script = scriptModule.ScriptList.Fetch(scriptPath)
    
    if script == None:
        raise System.ArgumentException('A script with the specified path does not exist.')
    
    query = DHI.Solutions.Generic.Query()
    query.Add(DHI.Solutions.Generic.QueryElement("ScriptId", script.Id, DHI.Solutions.Generic.QueryOperator.Eq))
    associatedPpreparedScripts = scriptModule.PreparedScriptList.Fetch(query);
    
    if associatedPpreparedScripts.Count == 0:
        raise System.ArgumentException('No prepared scripts found for the script.')
    
    scriptModule.PreparedScriptList.Delete(associatedPpreparedScripts);
    pass;
