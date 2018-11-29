#!/usr/bin/python
from sys import argv
# Get args passed
if len(argv) > 1 :
    script, primer1,primer2,inname = argv
else :
    print ("No input file specified")
    exit(2)
    
def check(a,b):
    t = sum(s1 == s2 for s1, s2 in zip(a,b))
    return t

seqfile = open(inname,"r")
lines = seqfile.readlines()
for line in lines:
    if line[0] != ">":
        sequence = line.strip()
        print "Looking in sequence ", sequence, "for ",primer1," and ",primer2
        i = 0
        #print "lensequence=", len(sequence)
        #print "lenprimer1=" ,len(primer1), "lenprimer2=" ,len(primer2)
        #print "diflen=",len(sequence)-len(primer2)
        p1start = 0
        p1found = False
        p2start = 0
        p2found = False
        while i < len(sequence)-len(primer2)-2:
            #print "index=",i
            string1 = sequence[i:len(primer1)+i]
            #print "comparing string=",string1, " against primer=",primer1
            m = check(string1,primer1)
            #print "characters in common=",m
            if m > len(primer1)-2:
                p1found = True
                p1start = i
                i = len(sequence)
                print ">First primer ",sequence[p1start:p1start+len(primer1)], " found at location=",p1start
            i += 1
        if p1found:
            print ">Looking for primer2"
            i = p1start+len(primer1)
            while i < len(sequence):
                #print "index=",i
                string2 = sequence[i:len(primer2)+i]
                #print "comparing string=",string2, " against primer=",primer2
                m = check(string2,primer2)
                #print "characters in common=",m
                if m > len(primer2)-2:
                    p2found = True
                    p2start = i
                    i = len(sequence)
                    print ">Second primer ",sequence[p2start:p2start+len(primer2)], " found at location=",p2start
                i += 1
        if p1found and p2found:
            #print ">primer1 and primer2 found"
            variant = sequence[p1start+len(primer1)-1:p2start]
            print ">Variant between primer1 and primer2 is ",variant
        else:
            print ">Primer1 and primer2 not found"
seqfile.close()
