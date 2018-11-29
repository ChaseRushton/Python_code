#!/bin/python
#
#This script parses a sliding window csv file with binary 0/1 inputs for genotpying
#Dependencies are the imported modules
#Modification from GC_calc.py (creation Chase Rushton)
#Created by Chase Rushton, 19th January 2017
#Created for D.pseudo experiment in Laurie Stevisons lab Auburn University, Auburn Alabama



#Load in required modules

from sys import argv
import numpy as np
import pandas as pd
import scipy.stats as stats

# Get args passed
if len(argv) > 1 :
    script, inname = argv
    outname = str(inname).split('.',1)[0] + '_crossover.txt'
else :
    print ("No input file specified")
    exit(2)
# Print Start
print ("Analyzing File: %s" % inname)

# Process file
import csv
input_file = open(inname, 'r')
output_file = open(outname,'w')
output_file.write('Treatment\tSum0\tSum1\tCrossover\tsumcross\n')
reader = csv.reader(input_file, delimiter=',', quotechar='"', skipinitialspace=True)

# read header
header = reader.next()
samplecount = 0
totzero = 0
totone = 0
totcross = 0
totinv = 0
totobs = 0
totsamplecross = 0

#read rows, apply values to lists
for row in reader:
    sumzero = 0
    sumone = 0
    sumcross = 0
    sumobs = 0
    suminv = 0
    crossover = 0
    lastvalue = None
    samplename = None
    for i, value in enumerate(row):
        if samplename is None:
            samplename = value
            samplecount += 1
            print("..processing %s" % samplename)
        else :
            if value == '0' or value == '1' :
                if value == '0' :
                    sumzero += 1
                    totzero += 1
                    totobs += 1
                else :
                    sumone += 1
                    totone += 1
                    totobs += 1
                if lastvalue is None :
                    lastvalue = value
                elif value != lastvalue :
                    sumcross += 1
                    totcross += 1
                    crossover = 1
                    lastvalue = value
            else :
                print ("....invalid value found %s" % value)
                suminv += 1
                totinv += 1
    output_line = "%s\t%i\t%i\t%i\t%i\n" % (samplename,sumzero,sumone,crossover,sumcross)
    output_file.write(output_line)
    totsamplecross += crossover

# Done, close files
input_file.close()
output_file.close()
# Calcualte Chi-squared value
test = float(((totsamplecross-samplecount)**2))/samplecount
# Print summary
print ("Output File: %s, With: %i observations, %i zeros, %i ones, %i crossovers, %i invalid values in %i samples with a test of %.2f" % (outname,totobs,totzero,totone,totsamplecross,totinv,samplecount,test))
#
#
#Figure out the P value
chi_squared_stat = test
crit = stats.chi2.ppf(q = 0.95, # Find the critical value for 95% confidence*
    df = 1)   # Df = number of variable categories - 1
#
print("Critical value")
print(crit)
#
p_value = 1 - stats.chi2.cdf(x=chi_squared_stat,  # Find the p-value
                            df=1)
print("P value")
print(p_value)
##reads through every line and parses the lines to write a value out to be looked at with a chi squared tabe\
#
#
#
#
chi_squared_stat2 = sumcross
crit = stats.chi2.ppf(q = 0.95, # Find the critical value for 95% confidence*
                   df = 1)   # Df = number of variable categories - 1
#
#
print("Critical value_sumcross")
print(crit)
#
p_value = 1 - stats.chi2.cdf(x=chi_squared_stat2,  # Find the p-value
                             df=1)
print("P value_sumcross")
print(p_value)
