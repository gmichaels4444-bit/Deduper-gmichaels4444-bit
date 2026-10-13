##Conditions to account for in testing

Same chromosome, start base, UMI, opposite strand (write both)
^ repeat for each part of dict

Same mapped everything, but one read has 2 bp of 5` soft clipping (different real starts, write both)

Same everything (same real starts, only write 1)

different mapping position, but same after accounting for soft clipping (same real starts, only write 1)

Unique, but error in UMI (do not write out)
2 duplicates, first with UMI error (write out second entry)


On reverse complement: same mapped everything, but one read has 5` soft clipping (different real starts, write both)
Reverse complemented strands have different starts but match when accounting for soft clipping


Unmapped read (do not write out)