When creating scripts using the MIKE OPERATIONS Desktop (RealtimeManager) API, the following section should be added to the runtime.config, 
to make sure that threshold caching tables can be updated.

<Product
    Name="OperatorUI">
    <Plugins>
      <Plugin
        Name="DHI.Solutions.RealtimeManager.Data.FakeDTO"
        Type="DHI.Solutions.Generic.IDTO"
        Assembly="DHI.Solutions.RealtimeManager.Data.dll" />
      <Plugin
        Name="DHI.Solutions.RealtimeManager.Business.RealtimeModule"
        Type="DHI.Solutions.Generic.IModule"
        Assembly="DHI.Solutions.RealtimeManager.Business.dll" />
      <Plugin
        Name="DHI.Solutions.RealtimeManager.Business.ThresholdCache"
        Type="DHI.Solutions.Generic.IDTO"
        Assembly="DHI.Solutions.RealtimeManager.Business.dll" />
    </Plugins>
  </Product>
