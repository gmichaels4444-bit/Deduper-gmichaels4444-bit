##Conditions to account for in testing

For each of 4 uniqueness dict elements: keep all but 1 the same (write all entries)
Same chromosome, start base, UMI, strandedness 

Same everything, but one read has 2 bp of 5` soft clipping (different real starts, write both)

Same everything (same real starts, only write 1)

different mapping position, but same after accounting for soft clipping (same real starts, only write 1)

Unique, but error in UMI (do not write out)
2 duplicates, first with UMI error (write out second entry)


On reverse complement: same mapped everything, but one read has 5` soft clipping (different real starts, write both)
Reverse complemented strands have different starts but match when accounting for soft clipping


Unmapped read (do not write out)