#!/usr/bin/env python

# Author: <YOU> <optional@email.address>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say''' 

__version__ = "1"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = set("ATGCNatgcn")
RNA_bases = set("AUGCNaugcn")

def convert_phred(letter: str) -> int:
    """Converts a single character into a phred score"""
    x=ord(letter)
    score=x-33
    return score

def qual_score(phred_score: str) -> float:
    total_num_score=0
    for i, barcode in enumerate(phred_score):
        num_score=convert_phred(barcode)
        total_num_score+=num_score
    return total_num_score/(i+1)  

def validate_base_seq(seq, RNAflag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts, Gs, and Cs. False otherwise. Case insensitive.'''
    seq=seq.upper()
    seq=set(seq)
    return seq<=(RNA_bases if RNAflag else DNA_bases)


def gc_content(DNA):
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    assert validate_base_seq(DNA)
    DNA=DNA.upper()
    return (DNA.count("G")+DNA.count("C"))/len(DNA)

    '''Given a sorted list, returns the median value of the list'''
def calc_median(lst: list) -> float:
    if len(lst)%2==0:
        med=((lst[len(lst)//2]+lst[len(lst)//2 -1])/2)
        return med
    else:
        med=lst[len(lst)//2]
        return med

def oneline_fasta(infile, outfile):
	with open(infile, "r") as fhin, open(outfile, "w") as fhout:
		line1=fhin.readline()
		fhout.write(line1)
		for line in fhin:
			if ">" in line:
				fhout.write('\n')
				fhout.write(line)
			else:
				line=line.strip('\n')
				fhout.write(line)

if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")

    assert qual_score("C") == 34
    assert qual_score("@@@") == 31
    assert qual_score("?BBE") == 33
    assert qual_score(">BF") == 33
    print("You calcluated the correct average phred score")
  
    assert validate_base_seq("AATAGAT", False) == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("ACGUUAC", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("ATGCU",False) == False
    assert validate_base_seq("AGCAGCUUU", False) == False
    print("Passed DNA and RNA tests")

    assert gc_content("GCGCGC") == 1
    assert gc_content("AAAAT") == 0
    assert gc_content("GCGCATAT") == 0.5
    print("correctly calculated GC content")

    assert calc_median([1,2,3,4]) == 2.5
    assert calc_median([1,2,3]) == 2
    assert calc_median([2,4,6,8]) == 5
    print('median successfully calculated')