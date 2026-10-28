#!/bin/bash

#SBATCH --account=bgmp                    # REQUIRED: which account to use
#SBATCH --partition=bgmp                  # REQUIRED: which partition to use
#SBATCH --cpus-per-task=1                 # optional: number of cpus, default is 1
#SBATCH --mem=64GB                        # optional: amount of memory, default is 4GB per cpu
#SBATCH --time=6:00:00
#SBATCH --job-name=deduplicate
#SBATCH --output=slurm/slurm-%j-%x.out

# #fixing header of input sam file; sort will not work with incorrect header
# /usr/bin/time -v pixi run samtools reheader -o /scratch/bgmp/gmich/deduper/C1_SE_uniqAlign_sorted.sam \
#  /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam

# #initial sorting of input sam file; file is not sorted
# /usr/bin/time -v pixi run samtools sort -o /scratch/bgmp/gmich/deduper/C1_SE_uniqAlign_sorted.sam \
#  /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam

# #running python script on sorted input
/usr/bin/time -v ./Michaels_deduper.py -u STL96.txt \
 -f /scratch/bgmp/gmich/deduper/C1_SE_uniqAlign_sorted.sam \
 -o /scratch/bgmp/gmich/deduper/C1_SE_uniqAlign_deduped.sam -l deduper_log.tsv

## postrun sorting of deduplicated sam file
# /usr/bin/time -v pixi run samtools sort  -o /scratch/bgmp/gmich/deduper/C1_SE_uniqAlign_deduped.sam \
#  -o /scratch/bgmp/gmich/deduper/C1_SE_uniqAlign_deduped_sorted.sam

