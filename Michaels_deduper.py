#!/usr/bin/env python

###Problem: The same RNA fragment may be sequenced multiple times due to duplicates present in pcr step prior to sequencing. 
# Pcr duplicates confound differential expression analysis and should be removed. These duplicates have the same chromosome, 5' start position, strand, and UMI (unique molecular identifier).

##use samtools sort prior to running to sort by chromosome, then by position

import bioinfo
import gzip
import argparse
import re
import itertools
import textwrap

#set up args for input and output files, umi txt file, and help message

def get_args():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
		Removes pcr duplicates from SORTED single end read.sam file and outputs into new .sam file.
		Duplicates identified by 5' start site by chromosome, strand, and unique molecular identifier (UMI).
		'''))
	parser.add_argument("-u", "--umi", help="umi index file name", type=str, default="STL96.txt")
	parser.add_argument("-f", "--infile", help="input sam file name", type=str, default="unittests/intest.sam")
	parser.add_argument("-o", "--outfile", help="output sam file name", type=str, default="unittests/testrun.sam")
	parser.add_argument("-t", "--testing", help="Checks ", type=bool, default=False)
	parser.add_argument("-l", "--logfile", help="Run log statistics filename", type=str, default="deduper_log_test.tsv")
	return parser.parse_args()
args= get_args()

def rev_pos(pos:int, cig:str)-> int:
	'''takes cigar string'''
	site_5=pos-1 #accounts for SAM file nomenclature
	splitcig=re.split(r"([A-Z])",cig)
	splitcig=list(filter(None, splitcig))
	op_set=set("NMSHDX=") #do not include I (insertions from reference)
	first_iteration=True #used to avoid adding left clipping
	for entry in itertools.batched(splitcig, 2):
		num=int(entry[0])
		op=entry[1]
		if first_iteration==False: #ensures left clipping is not included in calculating position
				if op in op_set:
					site_5+=num
		else: 
			first_iteration=False #change flag
			if op!="S" and op!="H":
				if op in op_set:
					site_5+=num
	return site_5 


# print(rev_pos(100,"10S14M2S"))

# if __name__ == "__main__":
# 	assert rev_pos(100,"10S14M2S") == 115, "115 wrong"
# 	assert rev_pos(100, "10S") == 99, "99 wrong"
# 	assert rev_pos(1,"12M") == 12, "12 wrong"
# 	assert rev_pos(999, "6S12M") == 1010, "1010 wrong"
# 	print("rev_pos works")


#initialize set for storing UMIs
umiset=set()
with open(args.umi, "r") as umi:
	for line in umi:
		line=line.strip()
		umiset.add(line)

#note: all write lines begin with newline character except for first line (for output file formatting)
#Initializing variables and dictionary used for recording metrics
header_lines=0
unique_reads=0
wrong_umis=0
duplicates=0
chr_dict={} #dictionary for identifying new chromosomes (key) and counting reads per chromosome (value)

#for storing individual positions within sam for duplicate comparisons
chr=0 #for storing current chromosome
posset=set() #format: "5' start position, umi, strand"; erased at each new chromosome to save memory
first_line=True #flag used for avoiding leading or trailing newline character in output file, unnecessary if header not in output
with open(args.infile, "r") as fh, open(args.outfile, "w") as outfile: ###gzip.open and "rt" if zipped
	for line in fh: #each entry is one line
		line=line.strip()
		if line[0] !="@": #ie is not header line
			splitline= line.split("\t") #####for setting variables###
			qname= splitline[0].split(":")#allows for indexing of qname column
			UMI= qname[7]
			linechr=splitline[2]
			pos=int(splitline[3]) #mapping position, adjusted to 5' start site later
			cig= splitline[5] #cigar string
			flag= int(splitline[1]) #bitwise flag
			if ((flag & 4) != 4): #checks if bitwise flag is set to "unmapped" for removing unmapped reads
				if UMI in umiset: #else condition has misread; will be thrown out
					###variable setup###
					if ((flag & 16) == 16):
						strand="r"
					else:
						strand="f"
					if chr!=linechr: #new chromosome
						posset=set()
						chr=linechr #sets current chromosome
						chr_dict.setdefault(chr,0)
					if strand=="f": # check for soft clipping at BEGINNING of CIGAR string
						splitcig=cig.split("S")
						if splitcig[0].isdigit(): # only occurs if leading bases are soft clipped, otherwise will be alphanumeric
							pos-=int(splitcig[0])
					else: #reverse complemented, need to calculate 5' start site via CIGAR string
						pos=rev_pos(pos,cig)
					dupe_check=(pos, strand, UMI)
					if dupe_check in posset: #is duplicate
						duplicates+=1
						#print(f"Duplicate entry:" pos, strand, UMI)
					else: #is unique entry, write out
						posset.add(dupe_check)
						outfile.write(f'\n{line}')
						unique_reads+=1
						chr_dict[chr]+=1
				else: #invalid UMI
					wrong_umis+=1
		else: #line begins with "@"
			if first_line==False:
				outfile.write(f'\n{line}')
				header_lines+=1
			else: #only true for first line of file
				outfile.write(f'{line}')
				first_line=False 
				header_lines+=1

with open(args.logfile, "w") as logfile:
	logfile.write(f'Header Lines\t{header_lines}')
	logfile.write(f'\nUnique Reads\t{unique_reads}')
	logfile.write(f'\nWrong UMIs\t{wrong_umis}')
	logfile.write(f'\nPCR Duplicates\t{duplicates}')
	logfile.write(f'\nChromosome\tCount of Reads')
	for key in chr_dict:
		logfile.write(f'\n{key}\t{chr_dict[key]}')