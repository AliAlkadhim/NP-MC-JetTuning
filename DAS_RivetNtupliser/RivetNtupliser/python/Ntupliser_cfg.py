import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

# memory check (deactivated)
SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",
        ignoreTotal = cms.untracked.int32(1))

# command line parser
options = VarParsing.VarParsing ('analysis')
options.register('configFile',
        '',
        VarParsing.VarParsing.multiplicity.singleton,
        VarParsing.VarParsing.varType.string,
        "JSON config file")
options.parseArguments()

from os.path import exists
params = {}
if exists(options.configFile):
    import json
    with open(options.configFile, "r") as f:
        params = json.load(f)

flavour = 'flags' in params and 'flavour' in params['flags']
muons = 'flags' in params and 'muons' in params['flags']
photons = 'flags' in params and 'photons' in params['flags']
dump = 'flags' in params and 'dump' in params['flags']
triggers = 'flags' in params and 'triggers' in params['flags']
radius = params['radius'] if 'radius' in params else 0.4

import sys

if flavour and radius != 0.4:
    raise ValueError("Flavour tagging is only supported for ak4")

inputFiles = options.inputFiles if len(options.inputFiles) else ['root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16MiniAODv2/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/270000/030D9093-0513-0340-A5A4-15DE53778266.root']

isMC = 'MINIAODSIM' in inputFiles[0]

if any(x in inputFiles[0] for x in ['2016UL','UL16','UL2016']):
    year = 2016
elif any(x in inputFiles[0] for x in ['2017UL','UL17','UL2017']):
    year = 2017
elif any(x in inputFiles[0] for x in ['2018UL','UL18','UL2018']):
    year = 2018
else:
    raise ValueError("Year is not recognised")

# definition of the process (note: the name is used when reclustering)
process = cms.Process('Darwin')

# definition of the output file
process.TFileService=cms.Service("TFileService",fileName=cms.string(options.outputFile))

# definition of the max number of events
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))
if options.maxEvents > 0:
    print("MaxEvents="+str(options.maxEvents))

# definition of the source file(s)
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(inputFiles)
)

# message logger (not much used in the current setup)
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger = cms.Service("MessageLogger",
    categories = cms.untracked.vstring('FwkReport', 'JetPtMismatch', 'MissingJetConstituent'),
    destinations = cms.untracked.vstring('cerr'),
    cerr = cms.untracked.PSet(
            threshold = cms.untracked.string('WARNING'),
            JetPtMismatch = cms.untracked.PSet(limit = cms.untracked.int32(0)),
            MissingJetConstituent = cms.untracked.PSet(limit = cms.untracked.int32(0)),
            FwkReport = cms.untracked.PSet(reportEvery = cms.untracked.int32(1000)),
            )
    )

# definition of jets

from RecoJets.JetProducers.GenJetParameters_cfi import *

# gen particles are used both for muons and for flavours
# (so not relevant for analyses working with all-flavour inclusive jets)
genParticleCollection = 'prunedGenParticles'

# TODO: clarify how much it matters... (in the n-tuples, we take the
# uncorrected, but what about DeepJet for instance??)
from Configuration.AlCa.GlobalTag import GlobalTag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# See summary table from PdmV:
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable
# https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysisSummaryTable
if isMC:
    if year == 2016:
        if 'HIPM' in inputFiles[0] or 'VFP' in inputFiles[0]:
            GT = '106X_mcRun2_asymptotic_preVFP_v11'
        else:
            GT = '106X_mcRun2_asymptotic_v17'
    elif year == 2017:
        GT = '106X_mc2017_realistic_v9'
    elif year == 2018:
        GT = '106X_upgrade2018_realistic_v16_L1v1'
    else:
        raise RuntimeError("No GT could be determined")
else:
    GT = '106X_dataRun2_v35'

print(GT)

process.GlobalTag = GlobalTag(process.GlobalTag, GT, '')

# TODO: add forward triggers for 2017 and 2018
# TODO: clarify if there are efficient triggers in 2016 for forward region

triggerNames = []
metNames=['Flag_goodVertices','Flag_globalSuperTightHalo2016Filter','Flag_HBHENoiseFilter','Flag_HBHENoiseIsoFilter','Flag_EcalDeadCellTriggerPrimitiveFilter','Flag_BadPFMuonFilter', 'Flag_BadPFMuonDzFilter', 'Flag_BadChargedCandidateFilter','Flag_eeBadScFilter']
if year == 2017 or year ==2018:
    metNames+=['Flag_hfNoisyHitsFilter','Flag_ecalBadCalibFilter']
print("Size MET names: "+str(len(metNames)))
if radius == 0.8:
    ## reclustering:
    from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox
    jetToolbox(process, 'ak8', 'jetSequence', 'noOutput', # change 'noOutput' to 'out' to get an intermediate ROOT file
            PUMethod='CHS', JETCorrPayload='AK8PFchs', JETCorrLevels=[ '' ],
            runOnMC=isMC, Cut='pt > 10.0 && abs(rapidity()) < 5.0',
            bTagDiscriminators='')
    genJetCollection = 'selectedPatJetsAK8PFCHS'
    JetCollection = 'selectedPatJetsAK8PFCHS'

    triggerNames = ['HLT_AK8PFJet40_v', 'HLT_AK8PFJet60_v', 'HLT_AK8PFJet80_v',
            'HLT_AK8PFJet140_v', 'HLT_AK8PFJet200_v', 'HLT_AK8PFJet260_v',
            'HLT_AK8PFJet320_v', 'HLT_AK8PFJet400_v', 'HLT_AK8PFJet450_v',
            'HLT_AK8PFJet500_v']
    if year > 2016:
        triggerNames += ['HLT_AK8PFJet550_v']

    ## default:
    #genJetCollection = 'slimmedGenJetsAK8'
    #JetCollection = 'slimmedJetsAK8'
    # does not work: "This PAT jet was not made from a JPTJet nor from PFJet."
elif radius == 0.4:
    genJetCollection = 'slimmedGenJets'
    JetCollection = 'slimmedJets'
    if 'FSQJet' in inputFiles[0] and year == 2017:
        triggerNames += ['HLT_HIAK4PFJet15_v','HLT_HIAK4PFJet40_v','HLT_HIAK4PFJet60_v','HLT_HIAK4PFJet80_v']
        ##triggerNames += [
        ##triggerNames += ['HLT_HIPFJet15_v', 'HLT_HIPFJet25_v', 'HLT_HIPFJet40_v', 'HLT_HIPFJet60_v',
        ##                'HLT_HIPFJet80_v','HLT_HIPFJetFwd40_v', 'HLT_HIPFJetFwd60_v', 'HLT_HIPFJetFwd80_v']
    else:
        triggerNames += ['HLT_PFJet40_v' , 'HLT_PFJet60_v' , 'HLT_PFJet80_v' , 'HLT_PFJet140_v',
                         'HLT_PFJet200_v', 'HLT_PFJet260_v', 'HLT_PFJet320_v', 'HLT_PFJet400_v',
                         'HLT_PFJet450_v', 'HLT_PFJet500_v']
        if year > 2016:
            triggerNames += ['HLT_PFJet550_v']
else:
    raise ValueError("Only ak4 and ak8 are implemented")

#if muons and 'SingleMuon' in inputFiles[0]:
#    triggerNames += ['HLT_Mu8_v', 'HLT_Mu17_v', 'HLT_Mu20_v', 'HLT_Mu27_v', 'HLT_Mu50_v']

if (not isMC) and ('ZeroBias' in inputFiles[0]):
    triggerNames = ['HLT_ZeroBias_v']

# get flavour at gen level
if flavour:

    if isMC:
        from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
        from PhysicsTools.JetMCAlgos.AK4PFJetsMCFlavourInfos_cfi import ak4JetFlavourInfos
        process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone(
            particles = genParticleCollection
        )
        process.ak4genJetFlavourInfos = ak4JetFlavourInfos.clone(
            jets = genJetCollection,
            hadronFlavourHasPriority = cms.bool(True), # only affect the parton flavour, actually
            #relPtTolerance = cms.double(1.), # not sure that we should touch any of these
            #ghostRescaling_ = cms.double(1e-24) # default is 1e-18
        )

    process.load('Configuration.Geometry.GeometryRecoDB_cff')
    process.load('Configuration.StandardSequences.MagneticField_cff')

    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

    # https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/PatAlgos/test/patTuple_updateJets_fromMiniAOD_cfg.py
    updateJetCollection(
            process,
            #labelName = 'UndoneJEC',
            jetSource = cms.InputTag('slimmedJets'),
            pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
            svSource = cms.InputTag('slimmedSecondaryVertices', '', 'PAT' if isMC else 'DQM'),
            jetCorrections = ('AK4PFchs', cms.vstring([]), 'None'),
            # NOTE: if you want to know the list of all possible btag
            # discriminators, just enter a random/dummy/wrong one and check the
            # error message while trying to run the N-tupliser...
            btagDiscriminators = [
                # JP
                'pfJetProbabilityBJetTags', 'pfNegativeOnlyJetProbabilityBJetTags',
                # CSVv2
                'pfCombinedInclusiveSecondaryVertexV2BJetTags', 'pfNegativeCombinedInclusiveSecondaryVertexV2BJetTags',
                # DeepJet/DeepFlavour
                'pfDeepCSVJetTags:probb',     'pfNegativeDeepCSVJetTags:probb',
                'pfDeepCSVJetTags:probbb',    'pfNegativeDeepCSVJetTags:probbb',
                'pfDeepCSVJetTags:probc',     'pfNegativeDeepCSVJetTags:probc',
                'pfDeepCSVJetTags:probudsg',  'pfNegativeDeepCSVJetTags:probudsg',
                # DeepJet/DeepFlavour
                'pfDeepFlavourJetTags:probb',     'pfNegativeDeepFlavourJetTags:probb',
                'pfDeepFlavourJetTags:probbb',    'pfNegativeDeepFlavourJetTags:probbb',
                'pfDeepFlavourJetTags:problepb',  'pfNegativeDeepFlavourJetTags:problepb',
                'pfDeepFlavourJetTags:probc',     'pfNegativeDeepFlavourJetTags:probc',
                'pfDeepFlavourJetTags:probuds',   'pfNegativeDeepFlavourJetTags:probuds',
                'pfDeepFlavourJetTags:probg',     'pfNegativeDeepFlavourJetTags:probg'
                ],
            postfix='Retrained'
            )
    JetCollection = 'selectedUpdatedPatJetsRetrained'

process.ntupliser = cms.EDAnalyzer('Ntupliser',
    isMC            = cms.bool(isMC),
    year            = cms.int32(year),
# event
    vertices        = cms.InputTag('offlineSlimmedPrimaryVertices'),
    rho             = cms.InputTag('fixedGridRhoFastjetAll'),
    pileupInfo      = cms.untracked.InputTag('slimmedAddPileupInfo'),
# jets
    lhe             = cms.InputTag('externalLHEProducer'),
    genjets         = cms.InputTag(genJetCollection, 'genJets' if radius != 0.4 else ''),
    recjets         = cms.InputTag(JetCollection, '', '' if radius == 0.4 else 'Darwin'),
# flavour stuff
    flavour_flag = cms.bool(flavour),
    jetFlavourInfos = cms.InputTag('ak4genJetFlavourInfos'),
    SV_infos        = cms.InputTag('slimmedSecondaryVertices', '', 'PAT' if isMC else 'DQM'),
    genparticles    = cms.InputTag(genParticleCollection),
# muons
    muons_flag      = cms.bool(muons),
    genLeptons      = cms.InputTag("particleLevel:leptons"),  # Rivet-based definitions
    recmuons        = cms.InputTag('slimmedMuons'),
# photons
    photons_flag    = cms.bool(photons),
    recphotons      = cms.InputTag('slimmedPhotons'),
# trigger
    triggers_flag   = cms.bool(triggers),
    triggerNames    = cms.vstring(triggerNames),
    triggerPrescales = cms.InputTag('patTrigger'),
    triggerPrescalesl1min = cms.InputTag('patTrigger', 'l1min'),
    triggerPrescalesl1max = cms.InputTag('patTrigger', 'l1max'),
    triggerResults   = cms.InputTag('TriggerResults','','HLT'),
    triggerObjects  = cms.InputTag('PatTrigger' if isMC else 'slimmedPatTrigger'),
# MET
    met              = cms.InputTag('slimmedMETs'),
    metNames              = cms.vstring(metNames),
    metResults   = cms.InputTag('TriggerResults','',  'PAT'),
)

if dump:
   print(process.dumpPython())
   sys.exit()

from GeneratorInterface.Core.genXSecAnalyzer_cfi import *
process.GenXSecAnalyzer = cms.EDAnalyzer("GenXSecAnalyzer")

paths = process.ntupliser

if flavour:
    paths = ( process.patJetCorrFactorsRetrained *
              process.updatedPatJetsRetrained *
              process.pfImpactParameterTagInfosRetrained *

              #JP
              process.pfJetProbabilityBJetTagsRetrained *
              process.pfNegativeOnlyJetProbabilityBJetTagsRetrained *

              #CSVv2
              # get negative vertices
              process.inclusiveCandidateNegativeVertexFinderRetrained *
              process.candidateNegativeVertexMergerRetrained *
              process.candidateNegativeVertexArbitratorRetrained *
              process.inclusiveCandidateNegativeSecondaryVerticesRetrained *
              # info for tags and NegativeTags
              process.pfInclusiveSecondaryVertexFinderTagInfosRetrained *
              process.pfInclusiveSecondaryVertexFinderNegativeTagInfosRetrained *
              # tags and " negative tags "
              process.pfCombinedInclusiveSecondaryVertexV2BJetTagsRetrained *
              process.pfNegativeCombinedInclusiveSecondaryVertexV2BJetTagsRetrained *

              #DeepCSV
              # info for tags and NegativeTags
              process.pfDeepCSVTagInfosRetrained *
              process.pfDeepCSVNegativeTagInfosRetrained *
              # tags and " negative tags "
              process.pfDeepCSVJetTagsRetrained *
              process.pfNegativeDeepCSVJetTagsRetrained *
              #DeepJet
              process.pfDeepFlavourTagInfosRetrained *
              process.pfDeepFlavourJetTagsRetrained *
              process.pfNegativeDeepFlavourTagInfosRetrained *
              process.pfNegativeDeepFlavourJetTagsRetrained *

              process.patJetCorrFactorsTransientCorrectedRetrained *
              process.updatedPatJetsTransientCorrectedRetrained *
              process.selectedUpdatedPatJetsRetrained *
              paths )

    if isMC:
        paths = ( process.selectedHadronsAndPartons *
                  process.ak4genJetFlavourInfos *
                  paths )

if muons and isMC:
    # Pull dressed lepton definitions used in NanoAOD
    # This comes with a basic selection
    from PhysicsTools.NanoAOD.particlelevel_cff import mergedGenParticles, genParticles2HepMC, particleLevel
    from SimGeneral.HepPDTESSource.pythiapdt_cfi import HepPDTESSource
    process.HepPDTESSource = HepPDTESSource
    process.mergedGenParticles = mergedGenParticles  # Merges prunedGenParticles and slimmedGenParticles
    process.genParticles2HepMC = genParticles2HepMC  # Converts to HepMC for Rivet
    process.particleLevel = particleLevel            # Retrieves particle definitions from Rivet
    paths = (process.mergedGenParticles * process.genParticles2HepMC * process.particleLevel * paths)

if isMC:
    paths = process.GenXSecAnalyzer * paths

process.p = cms.Path(paths)

