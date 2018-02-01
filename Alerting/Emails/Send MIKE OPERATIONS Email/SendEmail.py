def SendEmail():
    """
    <Script>
    <Author>admin</Author>
    <Description>Please enter script description here</Description>
    </Script>
    """
    # Get the real-time module.
    configurationName = 'Realtime' #'HistoricalEvents' 
    recepients = 'rask@dhigroup.com;pawel.werbowy@dhigroup.com'#;jaroslaw.rolnicki@umelblag.pl'#'aug@dhigroup.com'
    
    realtimeModule = app.Modules.Get('RealtimeModule');
    if realtimeModule == None:
        raise Exception('Can not obtain a reference to the Real-time Module.')
    
    realtimeModule.StartUp(app);
    app.Modules.Add(realtimeModule);


    # Load the real-time configurations spreadsheet to get all the configurations available.
    realtimeModule.LoadRealtimeConfigurations();
    
    # Loop all the configurations and load the setup of the configuration name in question.  
    for configuration in realtimeModule.RealtimeConfigurations:
        if (configuration.Name == configurationName):
            realtimeModule.CurrentConfiguration = configuration;
            configuration.LoadConfiguration(False);
    
    if (realtimeModule.CurrentConfiguration == None):
        return;
    
    # Set the current date time for the configuration. 
    currentDateTime = realtimeModule.CurrentConfiguration.LatestSimulation.TimeOfForecast;
    collection = [0, 1, 2, 3, 4, 5, 6, 7];
    error = [];
    messageNB = 'N.B. Rainfall timeseries are accumulated over 6 hours and the maximum is extracted from the water level timeseries.'
    messageIntro  = 'Prognoza powodzi dla miasta Elbląg. <br>  Czas prognozy modelowej : ' + currentDateTime.ToString('dd MMM HH:mm') + ' <br> (Otrzymałeś ten e-mail ponieważ jesteś w grupie adresowej Elektronicznego Systemu Ostrzegania Powodziowego dla miasta Elbląg). <br> <br> <br>'   
    #realtimeModule.CurrentConfiguration.AccumulatedWarningLevelVariable = 6; # For accumulated timeseries (step_accumulated, mean_step_accumulated and accumulated)
    #realtimeModule.CurrentConfiguration.InstantaneousWarningLevelVariable = 6; #For instantaneous timeseries
    contactSpreadsheet = realtimeModule.CurrentConfiguration.ContactSpreadsheet.LoadSpreadsheet(True);
    messageSubject = 'Elbląg - prognoza - TOF(czas prognozy) = ' + currentDateTime.ToString('dd MMM at HH:mm');
    errorMessage = None
    messageBody = '';
    alert = False;
    
    for x in collection:
        # Set the current date time for the configuration.
        realtimeModule.CurrentConfiguration.CurrentDateTime = currentDateTime.AddHours(x * 6);
        
        # Generate the mail subject and message body (HTML).
        messageCurrentAlert, emptySugject = realtimeModule.CurrentConfiguration.GenerateAlertMailMessageBody();
        if('table ' in messageCurrentAlert):
            alert = True;
            messagePeriod = 'Prognoza powodzi dla okresu od ' + realtimeModule.CurrentConfiguration.CurrentDateTime.ToString('dd MMM HH:mm') + ' do ' + realtimeModule.CurrentConfiguration.CurrentDateTime.AddHours(6).ToString('dd MMM HH:mm')
            messageBody = messageBody + '\n' + messagePeriod + '\n' + messageCurrentAlert
    
    if(alert):
        errorMessage = realtimeModule.CurrentConfiguration.SendMail(messageSubject, messageIntro + messageBody + messageNB, recepients); #'aug@dhigroup.com');
    
    if (errorMessage != None):
        error.append(errorMessage);
    
    if(error.Count > 0):
        raise Exception('Error occured when sending emails : ' + ', '.join(error));

