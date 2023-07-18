# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Configuration/GenProduction/python/ThirtheenTeV/QCD_Pt-15To7000_TuneCUETP8M1_Flat_13TeV-pythia8_cff.py -s GEN --datatier=GEN-SIM-RAW --conditions auto:mc --eventcontent RAWSIM --no_exec -n 10000 --python_filename=rivet_azimuthal_cfg.py --customise=Configuration/GenProduction/rivet_customize.py
import FWCore.ParameterSet.Config as cms
import os

process = cms.Process('GEN')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic50ns13TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(2000)
)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

#process.RandomNumberGeneratorService.generator.initialSeed = int(os.getenv('SEED'))

# Production Info
# Ali: maybe I can produce my own pythia hepmc or root here?
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/GenProduction/python/ThirtheenTeV/QCD_Pt-15To7000_TuneCUETP8M1_Flat_13TeV-pythia8_cff.py nevts:10000'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-RAW'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('QCD_Pt-15To7000_TuneCUETP8M1_Flat_13TeV-pythia8_cff_py_GEN.root'),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')


process.generator = cms.EDFilter("Pythia8GeneratorFilter",
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring('pythia8CommonSettings', 
            'pythia8CUEP8M1Settings', 
            'processParameters'),
        # PARAMETERS RELATING TO THE PROCESS
        processParameters = cms.vstring(
            'HardQCD:all = on', 
          #  'PhaseSpace:pTHatMin = 15', 
          # Previously had
          #PhaseSpace:pTHatMin     = 10       ! minimum pT of parton (GeV)
            'PhaseSpace:pTHatMin = 2500',  
            'PhaseSpace:pTHatMax = 7000', 
            'PhaseSpace:bias2Selection = on', 
            'PhaseSpace:bias2SelectionPow = 4.5', 
          'PhaseSpace:bias2SelectionRef = 15.'),
            # 'PhaseSpace:bias2SelectionRef = 2500.
            '), 
        #TUNE PARAMETERS
        # See https://gitlab.cern.ch/cms-sw/cmssw/-/blob/master/Configuration/Generator/python/Pythia8CUEP8M1Settings_cfi.py
        
        ##Tune:pp=18 #15 for CMS UE Tune CUETP8S1-CTEQ6L1, the default is Monash2013, 18 for CUETP8M1-NNPDF2.3LO
        
        pythia8CUEP8M1Settings = cms.vstring(
            'Tune:pp 14', 
            'Tune:ee 7', 
            # CHECK THE 2 PARAMETERS BELOW
            'MultipartonInteractions:pT0Ref=2.4024', 
            'MultipartonInteractions:ecmPow=0.25208', 
            'MultipartonInteractions:expPow=1.6'),
        # https://gitlab.cern.ch/cms-sw/cmssw/-/blob/master/Configuration/Generator/python/Pythia8CommonSettings_cfi.py
        pythia8CommonSettings = cms.vstring('Tune:preferLHAPDF = 2', 
            'Main:timesAllowErrors = 10000', 
            'Check:epTolErr = 0.01', 
            'Beams:setProductionScalesFromLHEF = off', 
            #'SLHA:keepSM = on', 
            'SLHA:minMassSM = 1000.', 
            'ParticleDecays:limitTau0 = on', 
            'ParticleDecays:tau0Max = 10', 
            'ParticleDecays:allowPhotonRadiation = on')
    ),
    comEnergy = cms.double(13000.0),
    #check what should be done to the crossSection value
    crossSection = cms.untracked.double(2022100000.0),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(1)
)


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RAWSIMoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

# customisation of the process.

# Automatic addition of the customisation function from Configuration.GenProduction.rivet_customize
#from Configuration.GenProduction.rivet_customize import customise 
#process.rivet_customize.rivetAnalyzer.AnalysisNames = cms.vstring('CMS_2016_SMPJAzimuthal')
#process.rivet_customize.rivetAnalyzer.OutputFile = cms.string('mcfile1.yoda')

def customise(process):
     process.load('GeneratorInterface.RivetInterface.rivetAnalyzer_cfi')
     process.rivetAnalyzer.AnalysisNames = cms.vstring('RivetNtupliser')
     #  process.rivetAnalyzer.OutputFile = cms.string(os.getenv('OUTPUT')) #('Pythia8MPIHADon.yoda')process.rivetAnalyzer.OutputFile = cms.string('Pythia8MPIHADon.yoda')
     #process.rivetAnalyzer.OutputFile = cms.string('Pythia8MPIHADon.yoda')
     process.rivetAnalyzer.CrossSection = cms.double(1.995e+09)
     process.generation_step+=process.rivetAnalyzer
     process.schedule.remove(process.RAWSIMoutput_step)
     return(process)


#call to customisation function customise imported from Configuration.GenProduction.rivet_customize
process = customise(process)

# End of customisation functions

