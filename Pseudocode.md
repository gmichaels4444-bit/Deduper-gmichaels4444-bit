#########! usr/bin/env python

###Problem: The same RNA fragment may be sequenced multiple times due to duplicates present in pcr step prior to sequencing. Transcriptomic data should correlate

##use samtools sort prior to running to sort by chromosome, then by position

import bioinfo
import gzip
import argparse

#set up args for input and output filepaths and file names and umi txt file

import argparse 
	add argument: ("-u", "--umi", help="umi index file", type=str, default="STL96.txt")
	add argument: ("-ip", "--inpath", help="filepath for input", type=str, default="/unittests/")
	add argument: ("-if", "--infile", help="input sam filename", type=str, default="test.sam")
	add argument: ("-op", "--outpath", help="output filepath", type=str, default="")
	add argument: ("-of", "--outfile", help="output  samfilename", type=str, default="testout.sam")



def reverse_comp(sequence: str)-> str:
	'''takes sequence and outputs the reverse complement'''
	comp_dict=[keys as bases ATGCUN, keys' reverse complements ie TACGAN]
	complement_string=""
	reverse_complement_string=""
	for letter in sequence:
		#replace letter with complement in reverse_complement_string; ie
			complement_string+="value in comp_dict when letter is key"
	reverse_complement_string = complement_string[::-1] #reverses order
	return reverse_complement_string
# if __name__ == "__main__":
# 	assert reverse_comp("ATGCN") == "NGCAT"
#	assert reverse_comp("NNNT") == "ANNN"
# 	print("reverse_comp works")

def tail_sc(cig: str)-> int:
	'''takes cigar string with end soft clipping and outputs number of soft clipped sites'''
	clipped_sites=0
	if last position in cig is "S" 
		strip "S"
			clipped_sites=tailing digits
	return clipped_sites
# if __name__ == "__main__":
# 	assert tail_sc("10S14M2S") == "2"
#	assert reverse_comp("10S") == "10" 
#	assert reverse_comp("12M") == "0" 
#	assert reverse_comp("6S12M") == "0" 
# 	print("tail_sc works")


#empty dictionary for storing UMIS
umidict=[]
with open args.umi for reading as umi
	for line in umi:
		add umi as key, set value to 0

##first occurrence of a duplicate will be written out with this method, output may be slightly out of order due to soft clipping

Flags to be set: first_line (for printing formatting), 
Variables to be set: flag for bitwise flag, strand for fwd or reverse complemented reads, UMI (from end of qname), chromosome, start position (accounting for soft clipping), cigar string

note: all write lines begin with newline character except for first line
#for storing individual positions within sam for duplicate comparisons
posdict=[] #format:key is "chromosome-start position-umi-strand", value is 
#contains requirements for determining if single-end reads are pcr duplicates
#all requirements for duplicates must be in key; can move strand parameter to values if doing 2

with open f'{args.inpath}{args.infile}' for reading as fh ###gzip.open if zipped
with open f'{args.outpath}{args.outfile}' for writing as outfile
	first_line=True #flag used for avoiding leading or trailing newline character in output file, unnecessary if header not in output
	for line in input file: #each entry is one line
		strip newline character
		if line at position 0 is not "@": #ie is not header line
			splitline= line split by tabs #####for setting variables###
			flag= splitline position 1 #bitwise flag
			if ((flag & 4) == 4): #checks if bitwise flag is set to "unmapped" for removing unmapped reads
				skip this line in the file, is unmapped and cannot be checked for duplication
			qname= split splitline position 0 by ":" #allows for indexing of qname column
			UMI= qname position 7
			if UMI in umidict: #else condition has misread; will be thrown out
				###variable setup###
				if ((flag & 16) == 16):
					strand=rev
				else:
					strand=fwd
				chr=splitline position 2 #chromosome
				pos=splitline position 3 #mapping position, next if statement adjusts for soft clipping
				cig= splitline position 5 #cigar string
				if strand=fwd: # check for soft clipping at BEGINNING of CIGAR string
					splitcig=split cig by "S"
					if first position in splitcig is a number: # only occurs if leading bases are soft clipped
						update pos to be pos minus splitcig pos 0
					else no leading soft clipping; no update needed
				else: #reverse complemented, check for soft clipping at END of cigar string
					if final position is "S":
						sc= tail_sc(cig) #function defined at top of document
						update pos to be pos minus sc
					else no 5' soft clipping; no update needed
				if "chr-start-strand-umi" is in posdict: 
					duplicate, do not write out
				else: #is unique entry, write out
					write line to output file
		else (ie if line begins with "@"): #header is written out with this configuration, can delete lines with "?" if header not desired in output
			if first_line=False:?
				write line to output file?
			else: #only true for first header line
				write line to output file with no newline character?
				set first_line=False 

