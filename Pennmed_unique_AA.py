#!/usr/bin/python
from sys import argv
import requests

# Get args passed
if len(argv) > 1 :
    script, inname = argv
    outname = str(inname) + '_Unique_AA.txt'
else :
    print ("No input file specified")
    exit(2)
#print ("File accepted")
#Get gene names      
#print ("Extracting Gene ID")
Genes = open("genes.txt",'w')
with open(inname) as bed:
    for line in bed:
        parts = line.split() # split line into parts
        if len(parts) > 1:   # if at least 2 parts/columns
            print >> Genes, parts[3]    # print genes into new file
#print ("Gene ID Extracted")
##print ("Querying Cbioportal")
Genes.close()
#loop over file for 


Genes = open("genes.txt", "r")
Genelist = Genes.readlines()
aa = open("aachange.txt",'w')
#print Genelist
for x in Genelist:
    #print (x)
    print ("Analyzing Gene: %s" % x )
    uniques = []
    cbioportal = "http://www.cbioportal.org/webservice.do?cmd=getMutationData&case_set_id=gbm_tcga_all&genetic_profile_id=gbm_tcga_mutations&gene_list=" + x 
    req = requests.get(cbioportal).content
    reqlines = req.split("\n")
    #print "reqlines"
    #print len(reqlines)
   # print reqlines
    y = 2
    while y < len(reqlines):
        #print y
        #print "reqline"
        #print reqlines[y]
        reqlist = reqlines[y].split("\t")
        #print "reqlist"
        #print reqlist
        #print len(reqlist)
        if len(reqlist) > 6:
            #print reqlist[7]
            if reqlist[7] not in uniques:
                uniques.append(reqlist[7])        
        y+=1
    print x.strip() + " has " , len(uniques) , "Unique AA changes in the TCGA data set" 
        
Genes.close()







#print ("Cbioportal queried")
#print ("Calculating AA differences")
#just need to uniq then line count column 8 and store/print w/ gene ID
#print ("AA differences calcualted")

# Print summary
#print ("Output File: %s, %i genes found, %i genes skipped" % (outname,AA difference))
