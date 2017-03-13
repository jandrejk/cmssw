# Check-out CMSSW

```bash
# cd to directory where the CMSSW environment should be located
wget https://raw.githubusercontent.com/thomas-mueller/cmssw/CMSSW_9_0_X_tau-pog_validation-tools/Validation/RecoTau/scripts/checkout_cmssw.sh
bash ./checkout_cmssw.sh
rm checkout_cmssw.sh
```

# Validation

## Download samples

```bash
searchAndCopyInputFileFromWeb.py <campaign> -n <number of processes>
searchAndCopyInputFileFromWeb.py <[CMSSW_]9_0_0_pre6> -n 8
```
Per default, the outputs are written to `$CMSSW_BASE/src/Validation/RecoTau/data/relval_inputs/<campaign>`.

## Process samples

```bash
skimSamplesInFolder.py <$CMSSW_BASE/src/Validation/RecoTau/data/relval_inputs/CMSSW_9_0_0_pre6_> -n <number of processes>
```
Per default, the outputs are written to `$CMSSW_BASE/src/Validation/RecoTau/data/relval_skims/<campaign>`.

## Produce comparison plots

```bash
makeValPlots.py \
<$CMSSW_BASE/src/Validation/RecoTau/data/relval_skims/CMSSW_9_0_0_pre6_/DQM_V0001_R000000001__RelValZTT_13__CMSSW_9_0_0_pre6-PU25ns_90X_mcRun2_asymptotic_v4-v1__DQMIO.root> \
<$CMSSW_BASE/src/Validation/RecoTau/data/relval_skims/CMSSW_9_0_0_pre6_/DQM_V0001_R000000001__RelValZTT_13__CMSSW_9_0_0_pre6-PUpmx25ns_90X_mcRun2_asymptotic_v4-v1__DQMIO.root> \
-n 8 -t 7100
makeValPlots.py \
<$CMSSW_BASE/src/Validation/RecoTau/data/relval_skims/CMSSW_9_0_0_pre6_/DQM_V0001_R000000001__RelValZTT_13__CMSSW_9_0_0_pre6-PU25ns_90X_mcRun2_asymptotic_v4_FastSim-v1__DQMIO.root> \
<$CMSSW_BASE/src/Validation/RecoTau/data/relval_skims/CMSSW_9_0_0_pre6_/DQM_V0001_R000000001__RelValZTT_13__CMSSW_9_0_0_pre6-PUpmx25ns_90X_mcRun2_asymptotic_v4_FastSim-v1__DQMIO.root> \
-n 8 -t 7100
```

The outputs are collected in a folder and a HTML index is created. After copying them to some public (web-) directory, the information about the validation results need to be entered here: [https://cms-pdmv.cern.ch/valdb/](https://cms-pdmv.cern.ch/valdb/).


# Push to and pull from forked repository

```bash
git push my-tau-pog CMSSW_9_0_X_tau-pog_validation-tools

git pull my-tau-pog CMSSW_9_0_X_tau-pog_validation-tools
git fetch my-tau-pog && git merge my-tau-pog/CMSSW_9_0_X_tau-pog_validation-tools
```
