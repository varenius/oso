
function main()
{
    if (args.length > 1) {
        print(args);
        //handler.fileName = "/home/eskil/vgosdb/NewAnalysisOctober2020/2020/20AUG15VB/20AUG15VB_V003_iOSO_kall.wrp";
        handler.fileName = args[0];
        var delayMode = args[2];
    //delayMode = 'GR'
    //delayMode = 'PH'
        setup.path2ReportOutput = args[1] + '/' + delayMode + '/';
        //setup.path2ReportOutput ="/home/eskil/nuSolve/Reports/PH_oct20";
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
    //session.pickupReferenceClocksStation();  // set up a reference clock station:
    session.setReferenceClocksStation("ONSALA60");
    session.pickupReferenceCoordinatesStation();  // set up a reference station station:
    session.checkUseOfManualPhaseCals();  // scan correlator's report and search for applied manual phase calibrations:
    //
    var baselines = session.baselines;
    for (var i=0; i<baselines.length; i++) {
        baselines[i].sigma2add = 5.0e-12;
    }
    //
    // Only fit ONSA13SW and ONSA13NE
    var stations = session.stations;
    for (var i=0; i<stations.length; i++) {
    //print("TESTLINE " + stations[i].name + " " + stations[i].useCableCal);
        if (stations[i].name == "ONSA13SW" || stations[i].name == "ONSA13NE") {
            stations[i].estimateCoords=true;
        }
        else {
            stations[i].estimateCoords=false;
        }
    }
    var primaryBand = session.bands[session.primaryBandIdx];
    if (primaryBand.getInputFileVersion > 3) // clear previous editings:
          session.resetAllEditings();

    config.isSolveCompatible = true                     // have to be true if not testing something
    config.useRateType = CFG.VR_NONE;                   // No rate fitting
    config.WeightCorrectionMode = CFG.WCM_BASELINE;
    config.opMode = CFG.OPM_BASELINE;
    config.activeBandIdx = session.primaryBandIdx;      // there is just one band here

    // Set contributions on/off
    config.have2ApplyPxContrib = true                   // apply contributions for the polar motion, X-component
    config.have2ApplyPyContrib = true                   // apply contributions for the polar motion, Y-component
    config.have2ApplyEarthTideContrib = true            // apply contributions for solid Earth tides
    config.have2ApplyOceanTideContrib = true            // apply contributions for ocean tides loading
    config.have2ApplyPoleTideContrib = true             // apply contributions for pole tide deformations
    config.have2ApplyUt1OceanTideHFContrib = true       // apply contributions for subdiurnal UT1 variations
    config.have2ApplyPxyOceanTideHFContrib = true       // apply contributions for subdiurnal polar motion
    config.have2ApplyNutationHFContrib =  true          // apply contributions for libration in ERP (CALC 10)
    config.have2ApplyUt1LibrationContrib = true         // apply contributions for libration in UT1 (CALC 11)
    config.have2ApplyPxyLibrationContrib = true         // apply contributions for libration in polar motion (CALC 11)
    config.have2ApplyOceanPoleTideContrib = true        // apply contributions for ocean pole tide loading
    config.have2ApplyAxisOffsetContrib = true           // apply contributions for axis offsets
    config.have2ApplyFeedCorrContrib = false            // DO NOT apply contributions for feed horn rotation
    config.have2ApplyTiltRemvrContrib = false           // DO NOT apply contributions for axis tilt remover
    config.have2ApplySsm = false                        // DO NOT use the source structure model
    config.have2ApplyNdryContrib = false                // DO NOT apply contributions for refraction, hydrostatic atmosphere from CALC. Instead, use nuSolve's models.
    config.have2ApplyNwetContrib = false                // DO NOT apply contributions for refraction, wet atmosphere from CALC. Instead, use nuSolve's models.
    config.have2ApplyOldOceanTideContrib = false        // DO NOT apply contributions for old model of ocean tides
    config.have2ApplyOldPoleTideContrib = false         // DO NOT apply contributions for old model of ocean pole tides

    print("have2ApplyPxContrib"          +config.have2ApplyPxContrib)
    print("have2ApplyPyContrib"          +config.have2ApplyPyContrib)
    print("have2ApplyEarthTideContrib"   +config.have2ApplyEarthTideContrib)
    print("have2ApplyOceanTideContrib"   +config.have2ApplyOceanTideContrib)
    print("have2ApplyPoleTideContrib"    +config.have2ApplyPoleTideContrib)
    print("have2ApplyUt1OceanTideHFContrib" +config.have2ApplyUt1OceanTideHFContrib)
    print("have2ApplyPxyOceanTideHFContrin" +config.have2ApplyPxyOceanTideHFContrib)
    print("have2ApplyNutationHFContrib"  +config.have2ApplyNutationHFContrib)
    print("have2ApplyUt1LibrationContrib"+config.have2ApplyUt1LibrationContrib)
    print("have2ApplyPxyLibrationContrib"+config.have2ApplyPxyLibrationContrib)
    print("have2ApplyOceanPoleTideContrib" +config.have2ApplyOceanPoleTideContrib)
    print("have2ApplyFeedCorrContrib"    +config.have2ApplyFeedCorrContrib)
    print("have2ApplyTiltRemvrContrib"   +config.have2ApplyTiltRemvrContrib)
    print("have2ApplySsm"                +config.have2ApplySsm)
    print("have2ApplyAxisOffsetContrib"  +config.have2ApplyAxisOffsetContrib)
    print("have2ApplyNdryContrib"        +config.have2ApplyNdryContrib)
    print("have2ApplyNwetContrib"        +config.have2ApplyNwetContrib)
    print("have2ApplyOldOceanTideContrib"+config.have2ApplyOldOceanTideContrib)
    print("have2ApplyOldPoleTideContrib" +config.have2ApplyOldPoleTideContrib)
};

function processSession(delayMode)
{
    // Set outlier parameters
    var maxNumOfPasses  = 0.20*session.numOfObservations;       // 20% of number of sessions
    var upperLimit      = 20.0e-9;                              // 20ns


    // first, run a simple solution, just clock offsets and rates:
    parsDescript.unsetAllParameters();
    parsDescript.setMode4Parameter(Parameters.Clocks,   Parameters.EstimateLocal);

    config.useDelayType = CFG.VD_SB_DELAY;
    config.activeBandIdx = 0;
    session.process();
    session.eliminateOutliersSimpleMode(0, maxNumOfPasses, 7, upperLimit);
    session.process();

    // switch to Group delay and resolve ambigs:
    config.useDelayType = CFG.VD_GRP_DELAY;
    session.scanAmbiguityMultipliers(0);
    session.process();
    session.eliminateOutliersSimpleMode(0, maxNumOfPasses, 7, upperLimit);

    // add some parameters and repeat:
    session.setNumOfClockPolynoms4Stations(3);
    parsDescript.setMode4Parameter(Parameters.StnCoo,   Parameters.EstimateLocal);
    parsDescript.setMode4Parameter(Parameters.Clocks,   Parameters.EstimateLocal);
    session.process();
    session.scanAmbiguityMultipliers(session.primaryBandIdx);
    session.process();
    session.eliminateOutliersSimpleMode(session.primaryBandIdx, maxNumOfPasses, 7, upperLimit);

    // phase delays special treating:
    if (delayMode=="PH") {
        // Switch to phase-delays
        config.useDelayType = CFG.VD_PHS_DELAY;
        // phase delays are counted from group delays, we need to scan for ambigs again:
        session.scanAmbiguityMultipliers(session.primaryBandIdx);
        session.process();
        session.eliminateOutliersSimpleMode(session.primaryBandIdx, maxNumOfPasses, 7, 50.0e-12);
        session.process();
        session.scanAmbiguityMultipliers(session.primaryBandIdx);
        session.process();
    };
    // hope, it is ok

    // estimate parameters:
    parsDescript.setMode4Parameter(Parameters.Clocks,   Parameters.EstimatePwl);
    parsDescript.setPwlStep(Parameters.Clocks, 1.0/24.0); // PWL interval in days
    //
    // tropospheric parameters have strong correlation at this network, we can estimate them
    // but the results are useless...
    //parsDescript.setMode4Parameter(Parameters.Zenith, Parameters.EstimatePwl);
    //parsDescript.setPwlStep(Parameters.Zenith, 1.0/24.0); // PWL interval in days

    var numOfRestored = 0;
    var numOfEliminated = 0;
    var roiCounter = 0;
    var mdfData=0;
    do
    {
        if ( (numOfRestored = session.restoreOutliers(session.primaryBandIdx)) )
            session.doReWeighting();
        if ( (numOfEliminated = session.eliminateOutliers(session.primaryBandIdx)) )
            session.doReWeighting();
        mdfData += numOfRestored + numOfEliminated;
        roiCounter++;
    }
    while (numOfRestored + numOfEliminated);
    print(' ++ doReweightAndOutliers(): End of reweighting/outlier processing iteration. Counter=' +
        roiCounter + ', number of modified observations: ' + mdfData);
    //
    // trun off the flag (it was turned automatically in session.doReWeighting()):
    config.doWeightCorrection = false;
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
    print(' -- printInfo(): Percent of used obs    : ' + 100*primaryBand.numProcessed/primaryBand.numUsable + ' (usable) ' + 100*primaryBand.numProcessed/primaryBand.numTotal) + ' (total).' ;
    print(' -- printInfo(): WRMS                   : ' + (primaryBand.wrms*1.0e12).toFixed(2) + ' (ps)');
    print(' -- printInfo(): DoF                    : ' + primaryBand.dof);
    print(' -- printInfo(): Chi^2/DoF              : ' + (primaryBand.chi2/primaryBand.dof).toFixed(4));
};

main();


