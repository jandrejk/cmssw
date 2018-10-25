import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *



##################### User floats producers, selectors ##########################

mergedGenParticles = cms.EDProducer("MergedGenParticleProducer",
    inputPruned = cms.InputTag("prunedGenParticles"),
    inputPacked = cms.InputTag("packedGenParticles"),
)

genParticles2HepMC = cms.EDProducer("GenParticles2HepMCConverter",
    genParticles = cms.InputTag("mergedGenParticles"),
    genEventInfo = cms.InputTag("generator"),
    signalParticlePdgIds = cms.vint32(),
)

myGenerator = cms.EDProducer("GenParticles2HepMCConverter",
    genParticles = cms.InputTag("mergedGenParticles"),
    genEventInfo = cms.InputTag("generator"),
    signalParticlePdgIds = cms.vint32(25), ## for the Higgs analysis
)

rivetProducerHTXS = cms.EDProducer('HTXSRivetProducer',
  HepMCCollection = cms.InputTag('myGenerator:unsmeared'),
  LHERunInfo = cms.InputTag('externalLHEProducer'),
  #ProductionMode = cms.string('GGF'),
  ProductionMode = cms.string('AUTO'),
)


particleLevel = cms.EDProducer("ParticleLevelProducer",
    src = cms.InputTag("genParticles2HepMC:unsmeared"),
    
    usePromptFinalStates = cms.bool(True), # for leptons, photons, neutrinos
    excludePromptLeptonsFromJetClustering = cms.bool(False),
    excludeNeutrinosFromJetClustering = cms.bool(True),
    
    particleMinPt  = cms.double(0.),
    particleMaxEta = cms.double(5.), # HF range. Maximum 6.0 on MiniAOD
    
    lepConeSize = cms.double(0.1), # for photon dressing
    lepMinPt    = cms.double(15.),
    lepMaxEta   = cms.double(2.5),
    
    jetConeSize = cms.double(0.4),
    jetMinPt    = cms.double(10.),
    jetMaxEta   = cms.double(999.),
    
    fatJetConeSize = cms.double(0.8),
    fatJetMinPt    = cms.double(170.),
    fatJetMaxEta   = cms.double(999.),
)


htxsTable = cms.EDProducer("HiggsClassificationTableProducer",
    src = cms.InputTag("rivetProducerHTXS:HiggsClassification"),
    name= cms.string("GenHiggs"),
    doc = cms.string("Dressed leptons from Rivet-based ParticleLevelProducer"),
    variables = cms.PSet(
        njets30 =       Var("jets30.size()",int,doc="number fo jets with pt larger 30"),
        stage1PtJet30 = Var("stage1_cat_pTjet30GeV", int, doc="Stage 1 Higgs classification"),
        pt =            Var("higgs.Pt()", float, doc="pt of the gen Higgs",precision=-1),        
        eta =           Var("higgs.eta()",float, doc="eta of the gen Higgs",precision=-1),
        phi =           Var("higgs.phi()",float, doc="phi of the gen Higgs",precision=-1),
        mass =             Var("higgs.M()",float,   doc="mass of the gen Higgs",precision=-1),

    )
)
# htxsTable = cms.EDProducer("GlobalVariablesTableProducer",
#     variables = cms.PSet(
#         htxsclass = ExtVar(cms.InputTag("rivetProducerHTXS:HiggsClassification"),"HTXS::HiggsClassification",doc="mini PF relative isolation, charged component",precision=10),
#     )
# )
##################### Tables for final output and docs ##########################
rivetLeptonTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("particleLevel:leptons"),
    cut = cms.string(""),
    name= cms.string("GenDressedLepton"),
    doc = cms.string("Dressed leptons from Rivet-based ParticleLevelProducer"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table
    variables = cms.PSet(
        P4Vars,
        pdgId = Var("pdgId", int, doc="PDG id"), 
    )
)

#rivetJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
#    src = cms.InputTag("particleLevel:jets"),
#    cut = cms.string(""),
#    name= cms.string("RivetJet"),
#    doc = cms.string("AK4 jets from Rivet-based ParticleLevelProducer"),
#    singleton = cms.bool(False), # the number of entries is variable
#    extension = cms.bool(False),
#    variables = cms.PSet(
#        # Identical to GenJets, so we just extend their flavor information
#        P4Vars,
#        hadronFlavour = Var("pdgId", int, doc="PDG id"),
#    )
#)

#rivetFatJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
#    src = cms.InputTag("particleLevel:fatjets"),
#    cut = cms.string(""),
#    name= cms.string("GenFatJet"),
#    doc = cms.string("AK8 jets from Rivet-based ParticleLevelProducer"),
#    singleton = cms.bool(False), # the number of entries is variable
#    extension = cms.bool(False), # this is the main table
#    variables = cms.PSet(
#        P4Vars,
#        hadronFlavour = Var("pdgId", int, doc="PDG id"), 
#    )
#)

#rivetTagTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
#    src = cms.InputTag("particleLevel:tags"),
#    cut = cms.string(""),
#    name= cms.string("RivetTag"),
#    doc = cms.string("Tag particles from Rivet-based ParticleLevelProducer, momenta scaled down by 10e-20"),
#    singleton = cms.bool(False), # the number of entries is variable
#    extension = cms.bool(False), # this is the main table
#    variables = cms.PSet(
#        P4Vars,
#        pdgId = Var("pdgId", int, doc="PDG id"), 
#    )
#)

rivetMetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("particleLevel:mets"),
    name = cms.string("MET"),
    doc = cms.string("MET from Rivet-based ParticleLevelProducer in fiducial volume abs(eta)<5"),
    singleton = cms.bool(True),  # there's always exactly one MET per event
    extension = cms.bool(True), # this is the main table
    variables = cms.PSet(
       fiducialGenPt  = Var("pt",  float, precision=10),
       fiducialGenPhi = Var("phi", float, precision=10),
    ),
)

particleLevelSequence = cms.Sequence(mergedGenParticles  + genParticles2HepMC + particleLevel )
particleLevelTables = cms.Sequence(rivetLeptonTable + rivetMetTable)

htxsSequence = cms.Sequence(myGenerator + rivetProducerHTXS)
htxsTables = cms.Sequence(htxsTable)
