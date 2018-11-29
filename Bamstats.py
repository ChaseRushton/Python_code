#!/usr/bin/python

import sys
import pysam 
from collections import Counter 

if len(sys.argv) < 2
	sys.exit("usage: alnstat.py in.bam") 
	
fname = sys.argv[1]
bamfile = pysam.AlignmentFile(fname) 


#total reads+reads passed

stats = Counter()
for read in bamfile:
	stats[ 'total'] += 1 
	stats['qcfail'] += int(read.is+_qcfail) 
	
	#record paired end info
	stats['paired'] += int(read.is_paired)
	stats['read1'] += int(read.is_read1)
	stats['read2'] += int(read.is_read2)
	
	if read.is_unmapped
		stats['unmapped'] += 1
		continue 
		
		
	stats["mapping quality <=30"] += int(read.mapping_quality <=30)
	
	stats['mapped'] += 1
	stats['proper pair'] += int(read.is_proper_pair)
	
output_order = ("total" , "mapped" , "unmapped" , "paired" , "read1" , "read2" , "proper pair" , "qcfail" , "mapping quality <=30") 

for key in output_order
	format_args = ( key , stats[key], 100*stats[key]/float(stats["total"]))
	sys.stdout.write("%s: %d (%0.2f%%\n" % format_args)
