#!/usr/bin/python

from sys import argv

class BlastDefaultOutfmt6:
	def __init__(self, qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore ):
		self.qseqid=qseqid
		self.sseqid=sseqid
		self.pident=float(pident)
		self.length=int(length)
		self.mismatch=float(mismatch)
		self.gapopen=float(gapopen)
		self.qstart=int(qstart)
		self.qend=int(qend)
		self.sstart=int(sstart)
		self.send=int(send)
		self.evalue=evalue
		self.bitscore=float(bitscore)

def StayClassy(LIST):
#Quick script to generate python stuff
    OUT=BlastDefaultOutfmt6(LIST[0], LIST[1], LIST[2], LIST[3], LIST[4], LIST[5], LIST[6], LIST[7], LIST[8], LIST[9], LIST[10], LIST[11])
    return OUT

# determines the orientation of blast coordinates. 

def Orient(start,end):
	if int(start) <int(end):
		O="+"		
	else :
		O="-"
	return O

# validate the array
def Validate(array) :
    Qplus = 0
    Qminus = 0
    if len(array) > 1 :
        for i in range(len(array)):
            P=StayClassy(array[i])
            Qor=Orient(P.qstart,P.qend)
            if Qor == "+" :
                Qplus += 1
            else :
                Qminus += 1
    if Qplus > 0 and Qminus > 0 :
        return 1
    else :
        return 0

# Get args passed
if len(argv) > 1 :
    script, inname = argv
    outname = str(inname).split('.',1)[0] + '_valid.txt'
else :
    print ("No input file specified")
    exit(2)

# Print Start
print ("Analyzing File: %s" % inname)

input_file = open(inname, 'r')
output_file = open(outname,'w')

# Initialize variables
LineSet = []
LastId = None
inputcnt = 0
outputcnt = 0
setcnt = 0
validcnt = 0

# Process the input file
import csv

outcsv = csv.writer(output_file,delimiter='\t')

for Line in csv.reader(input_file,delimiter='\t') :
    inputcnt += 1
    if len(Line) > 0 :
        if LastId is None :
            LastId = str(Line[0])
            setcnt += 1
        elif LastId != str(Line[0]) :
            if Validate(LineSet) :
                print "Set: ",setcnt," valid"
                validcnt += 1
                for i in range(len(LineSet)):
                    outputcnt +=1
                    outcsv.writerow(LineSet[i])
            else :
                print "Set: ",setcnt," not valid"
            LineSet = []
            LastId = str(Line[0])
            setcnt += 1
        if len(Line) > 11 :
            LineSet.append(Line)
        else :
            print "Line: ",inputcnt,"invalid number of values: ",len(Line)
            print Line

# Process the last line set
if Validate(LineSet) :
    print "Set: ",setcnt," valid"
    validcnt += 1
    for i in range(len(LineSet)):
        outputcnt +=1
        outcsv.writerow(LineSet[i])

# Done, close files
print ("Processed: %s, input lines: %i input sets: %i output lines: %i valid sets: %i" % (outname,inputcnt,setcnt,outputcnt,validcnt))
input_file.close()
output_file.close()
