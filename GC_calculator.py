#!/usr/bin/python
#  fastagc.py
#
from sys import argv
# Get args passed
if len(argv) > 1 :
    script, inname = argv
    outname = inname + '.txt'
else :
    print ("No input file specified")
    exit(2)
# Define fasta file parser
def fastaread():
    global record
    name = ''
    seq = ''
    if len(record) < 1 :
        record = input_file.readline()
    if record.startswith(">"):
        name = record.strip()[:-1]
        record = input_file.readline()
    while len(record) > 1 and not record.startswith(">"):
        seq += record.strip()
        record = input_file.readline()
    return name, seq;
#
# Print Start
print ("Analyzing File: %s" % inname)
gene_count = 0
bad_gene_count = 0
record = ''
gene = ''
sequence = ''
# Process file
input_file = open(inname, 'r')
output_file = open(outname,'w')
output_file.write('Gene\tC\tG\tTotal\tCG%\n')
gene, sequence = fastaread()
while len(gene) > 1 :
    gene_count += 1
    print("..processing %s" % gene)
    C_count = sequence.count('C')
    G_count = sequence.count('G')
    total_count = len(sequence)
    if total_count > 0 :
        percentage = float(C_count + G_count) / total_count*100.0
        output_line = '%s\t%i\t%i\t%i\t%f\n' % \
        (gene, C_count, G_count, total_count, percentage)
        output_file.write(output_line)
    else :
        print ("Skipping invalid format ID record")
        print ("gene:",gene)
        bad_gene_count += 1
    gene, sequence = fastaread()
# Done, close files
output_file.close()
input_file.close()
# Print summary
print ("Output File: %s, %i genes found, %i genes skipped" % (outname,gene_count,bad_gene_count))
