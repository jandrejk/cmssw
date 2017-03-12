#!/usr/bin/env python

import argparse
import os
import sys
import shutil
import subprocess

def readInput():
	parser = argparse.ArgumentParser(description="Plot all standard validation distributions")
	parser.add_argument("paths", nargs=2,
	                    help="Two paths to compare.")
	parser.add_argument("-o", "--old-dm", action="store_true", default=False,
	                    help="Use old DecayModes instead of new ones. [default: %(default)s]")
	
	args = parser.parse_args()
	return args


def main():
	args = readInput()

	exe = "python "+os.path.expandvars("$CMSSW_BASE4/src/Validation/RecoTau/Tools/MultipleCompare.py")

	#exe + '-T ' + testsample  + "-R " + referencesample + "-t" +testtag+ " -r " + referencetag + distribution + " --logScaleY --maxLogY=100000 --maxYR=2.0 --rebin=10 --maxXaxis=80 -o " + outputfile
	if args.old_dm:
		discriminator_list = [
				["DecayModeFindingOldDMsEff", "/MVA6*ElectronRejectionEff", "_AntiEle"],
				["DecayModeFindingOldDMsEff","*CombinedIsolationDBSumPtCorr3HitsEff", "_Comb_Iso"],
				["DecayModeFindingOldDMsEff", "*IsolationMVArun2v1DBoldDMwLTEff", "_MVA_Iso"],
				["DecayModeFindingOldDMsEff", "/*MuonRejection3Eff", "_AntiMu"],
		]
	else:
		discriminator_list = [
				["DecayModeFindingNewDMsEff", "/MVA6*ElectronRejectionEff", "_AntiEle"],
				["DecayModeFindingNewDMsEff","*CombinedIsolationDBSumPtCorr3HitsEff", "_Comb_Iso"],
				["DecayModeFindingNewDMsEff", "*IsolationMVArun2v1DBnewDMwLTEff", "_MVA_Iso"],
				["DecayModeFindingNewDMsEff", "/*MuonRejection3Eff", "_AntiMu"],
		]

	type_list = ["eff", "fake"]

	kinematic_list = ["pt", "eta", "phi", "pileup"]

	distribution_list = []
	for kinematic in kinematic_list:
		for discriminator_tuple in discriminator_list:
			temp_list = []
			for discriminator in discriminator_tuple[:-1]:
				distribution = discriminator + kinematic
				temp_list.append(distribution)
			temp_list.append(discriminator_tuple[-1])
			distribution_list.append(temp_list)

	input_list_t = os.listdir(args.paths[0])
	input_list_r = os.listdir(args.paths[1])

	release_t = args.paths[0].split("_CMSSW_")[-1]
	release_r = args.paths[1].split("_CMSSW_")[-1]

	#print input_list_t
	#print input_list_r

	input_output_tuple_list = []
	for sample in input_list_t:
		if "DQM_V" in sample:
			continue

		output_name = sample.split(".ro")[0]
		identifier = sample.split("_13_")[0]
		sampleMatch = ""
		for sample2 in input_list_r:
			if "DQM_V" in sample2:
				continue
			if identifier in sample2:
				sampleMatch = sample2
		input_output_tuple_list.append([output_name, sample, sampleMatch])

	for type in type_list:
		for tuple in input_output_tuple_list:
			for distribution_tuple in distribution_list:

				type_postfix = ""
				rebin = ""
				maxXaxis = ""
				maxLogY = " --maxLogY=1000 "
				if "eff" in type:
					maxLogY = " --maxLogY=100 "
					if not "ZTT" in str(tuple[0]):
						continue
				else:
					type_postfix = "--fakeRate"
					rebin = " --rebin=10 "
					if "_AntiEle" in distribution_tuple[-1]and not "ZEE" in tuple[0]:
						continue
					if "_AntiMu" in distribution_tuple[-1] and not "ZMM" in tuple[0]:
						continue
					if "_Iso" in distribution_tuple[-1] and not ("TTbar" in tuple[0] or "QCD" in tuple[0]):
						continue

				distribution_str = " "
				for distribution in distribution_tuple[:-1]:
					distribution_str +=  " '" + distribution + "' "
				kin_str = ""
				if "eta" in distribution_str:
					kin_str = "_eta_"
				elif "phi" in distribution_str:
					kin_str = "_phi_"
					maxXaxis = " --maxXaxis=200 --minXaxis=-200 "
				elif "pileup" in distribution_str:
					kin_str = "_pileup_"
					maxXaxis = " --maxXaxis=80  "
				else:
					kin_str = "_pt_"
					maxXaxis = " --maxXaxis=200  "


				print exe + " -T '" + str(args.paths[0]) + "/" +  str(tuple[1])   + "' -R '" + str(args.paths[1]) + "/" + str(tuple[2]) + \
				"' -t '" + release_t + "' -r '" + release_r + "'" + str(distribution_str) + rebin + maxXaxis + maxLogY + \
				" --logScaleY --maxYR=2.0 " + \
				" -o " + str(tuple[0]) + distribution_tuple[-1] + kin_str + type + ".png " + type_postfix

# --logScaleY --maxLogY=100000 --maxYR=2.0 --rebin=10 --maxXaxis=80 " +



if __name__ == "__main__":
	main()
