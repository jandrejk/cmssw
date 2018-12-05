from CRABClient.UserUtilities import config
config = config()

tag = "${tag}"
prodLabel = 'ReRunNao2017_181114'
file_dataset = "${sample}"
# General section - user specifies generic parameters
config.General.requestName = tag
config.General.transferLogs = True
config.General.workArea = 'crab_{0}'.format( prodLabel )

# JobTyp section - contains all the parameters of job related configurables
config.JobType.pluginName = 'Analysis'
config.JobType.maxMemoryMB = 3000
# config.JobType.maxJobRuntimeMin = 1440
config.JobType.psetName = "HIG-RunIIFall17NanoAOD-00518_${datatier}_cfg.py"

# Data section - contains all paramters related to the data to be analyzed
config.Data.inputDataset = file_dataset
config.Data.splitting = 'FileBased' 
config.Data.unitsPerJob = 1
# is the following needed?
config.Data.publication = False
config.Data.totalUnits = -1
# This string is used to construct the output dataset name
config.Data.outputDatasetTag = tag 
config.Data.ignoreLocality = True

# Site section - where the output files will be transmitted to
config.Site.storageSite = 'T2_AT_Vienna'
config.Site.whitelist=['T2_FR_*','T2_DE*','T2_IT_Bari','T2_IT_Legnaro','T2_US_*','T1_RU_JINR']
# config.Site.ignoreGlobalBlacklist = True
# config.Site.blacklist = ['*_US_*']
