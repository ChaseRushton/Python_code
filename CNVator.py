#!/bin/py

import os
import subprocess
 
import numpy as np
import pandas as pd
 
from sample_class import Sample
from custom_parser import Parser
from pipeline_tools import file_checker
 
 
parser = Parser(description = "Variant call samples using CNVnator")
parser.add_argument('-sample', type=str, required=True, help="Sample name")
parser.add_argument('-root', type=str, required=True, help="Filepath to root file for CNVnator calling")
parser.add_argument('-histroot', type=str, required=True, help="Filepath to histroot file for CNVnator calling")
parser.add_argument('-bam', type=str, required=True, help="Path to bam for variant calling")
parser.add_argument('-window', type=int, help='Window size for CNVnator partitioning')
parser.add_argument('-chromosomes', type=str, help="Path to chromosome fasta files for CNVnator.")
 
ARGS = parser.parse_args()
SAMPLE = ARGS.sample
ROOT = ARGS.root
HISTROOT = ARGS.histroot
BAM = ARGS.bam
WINDOW = ARGS.window
CHROMOSOMES = ARGS.chromosomes
 
def call_constructor():
    calls = {}
    calls['1'] = 'cnvnator -root %s -tree %s -unique' % (ROOT, BAM)
    calls['2'] = 'cnvnator -root %s -outroot %s -his %s -d %s' % (ROOT, HISTROOT, WINDOW, CHROMOSOMES)
    calls['3'] = 'cnvnator -root %s -stat %s'  % (HISTROOT, WINDOW)
    calls['4'] = 'cnvnator -root %s -partition %s'  % (HISTROOT, WINDOW)
    calls['5'] = 'cnvnator -root %s -call %s'  % (HISTROOT, WINDOW)
    return calls
 
def cnvnator_calling(calls):
    for stage in range(1,4):
        print calls[str(stage)]
        subprocess.call(calls[str(stage)], shell=True)
    output = subprocess.check_output(calls['5'], shell=True)
    return output
 
def write_output(output):
    fout = '%s.cnvnator.txt' % (SAMPLE)
    with open(fout, 'w+') as out:
        out.writelines(output)
 
 
def main():
    calls = call_constructor()
    output = cnvnator_calling(calls)
    write_output(output)
 
main()
