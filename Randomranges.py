#!/usr/bin/env python3

#random sampling algorith
#5th Feb 2018
#Genome size 3.2gb
#50kb segments
#Rushton masters thesis: Computational analysis of hybridation and specation in two macaque species

import random
segments = 54000
compare = 1000
samples = 1000
outfile = open('randomranges.txt','w')
i = 1
print "comparing ",compare," sets with ",samples," samples in ",segments," segments"
while i <= compare :
    if (i%100==0) :
        print "...compared sample sets", i
    sample1 = random.sample(range(segments),samples)
    sample2 = random.sample(range(segments),samples)
    overlap = frozenset(sample1).intersection(sample2)
    duplicates = len(overlap)
    outline = '%i\t%i\t%f\n' % (i,duplicates,(float(duplicates)/samples)*100)
    outfile.write(outline)
    i += 1
outfile.close()
