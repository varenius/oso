function main()
{
    if (args.length > 1) {
        print(args);
        //handler.fileName = "/home/eskil/vgosdb/NewAnalysisOctober2020/2020/20AUG15VB/20AUG15VB_V003_iOSO_kall.wrp";
        handler.fileName = args[0];
        //setup.path2ReportOutput ="/home/eskil/nuSolve/Reports/PH_oct20";
        var delayMode = args[2];
        setup.path2ReportOutput = args[1] + delayMode + "/";
        var save = args[3];
    }

    // Input
    handler.inputType = "VDB";
    // Output
    setup.have2KeepSpoolFileReports = true;
    // Read session
    handler.importSession();
    if (!session.isOk)
    {
        print('Session reading failed.');
        return;
    };

    // Setup and process session
    makeSetup();
    processSession(delayMode);
    printInfo();

    if  (save=="save") {
        print(' -- Saving updated version:');
        handler.saveResults();
        print(' ++ done.');
    }

    print(' -- Generating report:');
    handler.generateReport();
    print(' ++ done.');
};

function makeSetup()
{
    session.resetAllEditings(); // Reset any editings being present already in this wrapper
    session.suppressNotSoGoodObs(); // turn off everything that has low QCs:
    session.pickupReferenceClocksStation();  // set up a reference clock station:
    session.pickupReferenceCoordinatesStation();  // set up a reference station station:
    session.checkUseOfManualPhaseCals();  // scan correlator's report and search for applied manual phase calibrations:
    //
    var baselines = session.baselines;
    for (var i=0; i<baselines.length; i++) {
        baselines[i].sigma2add = 5.0e-12;
    }
    // Only fit ONSA13SW and ONSA13NE
    var stations = session.stations;
    for (var i=0; i<stations.length; i++) {
        if (stations[i].name == "ONSA13SW" || stations[i].name == "ONSA13NE") {
            stations[i].estimateCoords=true;
        }
        else {
            stations[i].estimateCoords=false;
        }
    }
};

function processSession(delayMode)
{
    // Set outlier parameters
    var maxNumOfPasses  = 0.20;         //
    var upperLimit      = 25.0e-9;      //

    // Define parameters to solve for
    parsDescript.unsetAllParameters();
    parsDescript.setMode4Parameter(Parameters.Clocks,   Parameters.EstimatePwl);
    parsDescript.setMode4Parameter(Parameters.StnCoo,   Parameters.EstimateLocal);

    config.activeBandIdx = session.primaryBandIdx;
    config.useDelayType = CFG.VD_GRP_DELAY;
    config.WeightCorrectionMode = CFG.WCM_BASELINE;
    config.opMode = CFG.OPM_BASELINE;
    session.doReWeighting();
    session.setNumOfClockPolynoms4Stations(3);
    // Run initial GR delay processing steps and remove initial outliers
    session.process();
    session.eliminateOutliersSimpleMode(session.primaryBandIdx, session.numOfObservations*maxNumOfPasses, 7, upperLimit);

    config.activeBandIdx = session.primaryBandIdx;
    if (delayMode=="PH") {
        // Switch to phase-delays
        config.useDelayType = CFG.VD_PHS_DELAY;
    }
    // Initial processing runs
    session.process();
    session.process();
    session.process();
    // Resolve ambiguities. Needs to be done iteratively for phase-delays it seems
    for (var i=0; i<10; i++)
    {
        session.scanAmbiguityMultipliers(i);
        session.process();
    };
    // Remove final outliers, after convergence
    session.eliminateOutliersSimpleMode(session.primaryBandIdx, session.numOfObservations*maxNumOfPasses, 3, upperLimit);
    // Run 7 processing runs, maximum for reweighting
    session.process();
    session.process();
    session.process();
    session.process();
    session.process();
    session.process();
    session.process();
};

function printInfo()
{
    var primaryBand = session.bands[session.primaryBandIdx];
    print(' -- printInfo(): Session name           : ' + session.name);
    print(' -- printInfo(): Session scheduled by   : ' + session.schedulerName);
    print(' -- printInfo(): Session submitted by   : ' + session.submitterName);
    print(' -- printInfo(): Session correlator name: ' + session.correlatorName);
    print(' -- printInfo(): Session official name  : ' + session.officialName);
    print(' -- printInfo(): Session sessionCode    : ' + session.sessionCode);
    print(' -- printInfo(): Session description    : ' + session.description);
    print(' -- printInfo(): Session suffix         : ' + session.networkSuffix);
    print(' -- printInfo(): Session networkID      : ' + session.networkID);
    print(' -- printInfo(): Session #bands         : ' + session.numOfBands);
    print(' -- printInfo(): Session #stations      : ' + session.numOfStations);
    print(' -- printInfo(): Session #baseline      : ' + session.numOfBaselines);
    print(' -- printInfo(): Session #sources       : ' + session.numOfSources);
    print(' -- printInfo(): Session #observs       : ' + session.numOfObservations);
    print(' -- printInfo(): Session created on     : ' + session.tCreation);
    print(' -- printInfo(): Session started on     : ' + session.tStart);
    print(' -- printInfo(): Session stopped on     : ' + session.tFinis);
    print(' -- printInfo(): Session mean epoch     : ' + session.tMean);

    print(' -- printInfo(): Primary band key       : ' + primaryBand.key);
    print(' -- printInfo(): Epoch of the first obs : ' + primaryBand.tFirst);
    print(' -- printInfo(): Epoch of the last obs  : ' + primaryBand.tLast);
    print(' -- printInfo(): Number of total obs    : ' + primaryBand.numTotal);
    print(' -- printInfo(): Number of usable obs   : ' + primaryBand.numUsable);
    print(' -- printInfo(): Number of used obs     : ' + primaryBand.numProcessed);
    print(' -- printInfo(): WRMS                   : ' + (primaryBand.wrms*1.0e12).toFixed(2) + ' (ps)');
    print(' -- printInfo(): DoF                    : ' + primaryBand.dof);
    print(' -- printInfo(): Chi^2/DoF              : ' + (primaryBand.chi2/primaryBand.dof).toFixed(4));
};

main();
