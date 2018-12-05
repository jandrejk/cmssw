# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step1 --fileout file:HIG-RunIIFall17NanoAOD-00518.root --mc --eventcontent NANOEDMAODSIM --datatier NANOAODSIM --conditions 94X_mc2017_realistic_v14 --step NANO --nThreads 2 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --python_filename HIG-RunIIFall17NanoAOD-00518_1_cfg.py --filein /store/mc/RunIIFall17MiniAODv2/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/90000/E04EE70F-B643-E811-9970-0CC47ABB5178.root --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 100
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('NANO',eras.Run2_2017,eras.run2_nanoAOD_94XMiniAODv2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/mc/RunIIFall17MiniAODv2/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/90000/E04EE70F-B643-E811-9970-0CC47ABB5178.root'),
    # fileNames = cms.untracked.vstring('E8FA5DC4-5245-E811-A293-0019B9CABF55.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step1 nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# process.NANOEDMAODSIMoutput = cms.OutputModule("PoolOutputModule",
process.NANOEDMAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:ntuple_NanoAOD.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '94X_mc2017_realistic_v15', '')

from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

runMetCorAndUncFromMiniAOD(
        process,
        isData = False, # false for MC
        fixEE2017 = True,
        fixEE2017Params = {'userawPt': True, 'PtThreshold':50.0, 'MinEtaThreshold':2.65, 'MaxEtaThreshold': 3.139} ,
        postfix = "ModifiedMET"
)
# Path and EndPath definitions
# process.modifyMETstep = cms.Path(process.fullPatMetSequenceModifiedMET)

process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
# process.nanoAOD_step = cms.Path( process.jecSequence * process.nanoSequenceMC)
# process.nanoAOD_step = cms.Path( process.jecSequence * process.fullPatMetSequenceModifiedMET * process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOEDMAODSIMoutput_step = cms.EndPath(process.NANOEDMAODSIMoutput)

# Schedule definition
# process.schedule = cms.Schedule(process.modifyMETstep, process.nanoAOD_step,process.endjob_step,process.NANOEDMAODSIMoutput_step)
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOEDMAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
# process.options.numberOfThreads=cms.untracked.uint32(2)
# process.options.numberOfStreams=cms.untracked.uint32(0)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC 

#call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeMC(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
