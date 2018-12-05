import string
import os
import shutil
import glob
import json
import sys
from samples import to_run


def main():
	submit_to_crab()

def read_sampels(path = "samples.json"):
    samples = []    
    for datatier in to_run[os.environ["USER"]]:
    	for sample in to_run[os.environ["USER"]][datatier]:
	        add = ""
	        if "_ext" in sample:
	              add = "ext"
	        if datatier == "mc":
	        	tag = sample.split("/")[1]+add
	        if datatier == "data":
	        	tag = sample.split("/")[1]+sample.split("/")[2]

	        samples.append( (datatier, tag, sample ) )    
    return samples

def write_templates():
	if not os.path.exists("submit"):
		os.mkdir("submit")

	for f in glob.glob("submit/*"):
		os.remove(f)

	samples = read_sampels()

	with open("crab_submit_template.py","r") as FSO:
		templ = string.Template(FSO.read())

	for datatier, tag, sample in samples:
		json = "#"
		#if datatier == "data":
		#	json = ""
		tmp = templ.substitute(tag = tag,
							   sample = sample,
							   datatier = datatier,
							   )
		with open( "submit/crab"+ sample.replace("/","_")+".py","w") as FSO:
			FSO.write( tmp )


def submit_to_crab():
    write_templates()
    subs = glob.glob("submit/*.py" )
    subs.sort()
    for f in subs:
        print "crab submit {0}".format(f) 
		#os.system("crab submit {0}".format(f)  )


if __name__ == '__main__':
	main()

