CreateStation.py

Python script for creating a station on a feature type in MIKE OPERATIONS.

Make sure that the relatime manager has been loaded in the runtime.config file in order to execute the script from MIKE WORKBENCH.

If the realtime manager has not been loaded, insert the following section into the runtime.config.

  <Product
    Name="DHI.Solutions.RealtimeManager">
    <Plugins>
      <Plugin
        Name="DHI.Solutions.RealtimeManager.Business.RealtimeModule"
        Type="DHI.Solutions.Generic.IModule"
        Assembly="DHI.Solutions.RealtimeManager.Business.dll" />
    </Plugins>
  </Product>
