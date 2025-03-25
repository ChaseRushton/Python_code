#!/usr/bin/env python3
import argparse
import os
import re
import sys
import multiprocessing as mp
from functools import partial
import time

def read_gene_list(file_path):
    """Read gene list from file, stripping whitespace and return as a set for faster lookups."""
    with open(file_path, 'r') as f:
        return {line.strip() for line in f if line.strip()}

def process_chunk(chunk, gene_set, perform_replacements, hla_pattern, replacement_patterns):
    """Process a chunk of lines and return filtered results."""
    results = []
    
    for line in chunk:
        # Skip lines containing HLA-DRB1
        if hla_pattern.search(line):
            continue
        
        # Perform replacements if needed (for Solid and Comp)
        if perform_replacements:
            for pattern, replacement in replacement_patterns:
                line = pattern.sub(replacement, line)
        
        # Check if any gene from the set is in the line
        for gene in gene_set:
            # Use word boundary for exact match
            if re.search(rf'\b{re.escape(gene)}\b', line):
                results.append(line)
                break
                
    return results

def filter_by_assay(input_file, output_file, assay_type, heme_list_path, solid_list_path, comp_list_path, num_processes=None):
    """
    Filter a text file based on assay type and gene lists.
    Uses multiprocessing for faster processing.
    """
    # Determine number of processes to use
    if num_processes is None:
        num_processes = mp.cpu_count()
    
    # Pre-compile patterns
    hla_pattern = re.compile(r'HLA-DRB1')
    replacement_patterns = [
        (re.compile(r'MRE11A\t'), 'MRE11\t'),
        (re.compile(r'H3F3A\t'), 'H3-3A\t'),
        (re.compile(r'EIF1A\t'), 'EIF1AX\t')
    ]
    
    # Read the appropriate gene list based on assay type
    if assay_type.lower() == "heme":
        gene_list_path = heme_list_path
        perform_replacements = False
    elif assay_type.lower() == "solid":
        gene_list_path = solid_list_path
        perform_replacements = True
    else:  # Comp or any other value
        gene_list_path = comp_list_path
        perform_replacements = True
    
    # Read gene list as a set for faster lookups
    gene_set = read_gene_list(gene_list_path)
    
    # Read all lines from input file
    with open(input_file, 'r') as infile:
        all_lines = infile.readlines()
    
    # Calculate chunk size for multiprocessing
    chunk_size = max(1, len(all_lines) // (num_processes * 10))
    chunks = [all_lines[i:i + chunk_size] for i in range(0, len(all_lines), chunk_size)]
    
    # Process chunks in parallel
    process_func = partial(process_chunk, gene_set=gene_set, 
                          perform_replacements=perform_replacements,
                          hla_pattern=hla_pattern,
                          replacement_patterns=replacement_patterns)
    
    with mp.Pool(processes=num_processes) as pool:
        results = pool.map(process_func, chunks)
    
    # Flatten results
    filtered_lines = [line for chunk_result in results for line in chunk_result]
    
    # Write results to output file
    with open(output_file, 'w') as outfile:
        outfile.writelines(filtered_lines)

def main():
    parser = argparse.ArgumentParser(description='Filter text file based on assay type and gene lists.')
    parser.add_argument('assay', choices=['Heme', 'Solid', 'Comp'], 
                        help='Assay type (Heme, Solid, or Comp)')
    parser.add_argument('--input', '-i', required=True, help='Input file path')
    parser.add_argument('--output', '-o', required=True, help='Output file path')
    parser.add_argument('--heme-list', default=os.path.join('', 'HemeReportable2025.txt'),
                        help='Path to Heme gene list file')
    parser.add_argument('--solid-list', default=os.path.join('', 'SolidReportable2025.txt'),
                        help='Path to Solid gene list file')
    parser.add_argument('--comp-list', default=os.path.join('', 'CompReportable2025.txt'),
                        help='Path to Comp gene list file')
    parser.add_argument('--processes', '-p', type=int, default=None,
                        help='Number of processes to use (default: number of CPU cores)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.isfile(args.input):
        print(f"Error: Input file '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    # Check if gene list files exist
    for list_path, list_name in [
        (args.heme_list, "Heme"),
        (args.solid_list, "Solid"),
        (args.comp_list, "Comp")
    ]:
        if not os.path.isfile(list_path):
            print(f"Error: {list_name} gene list file '{list_path}' does not exist.", file=sys.stderr)
            sys.exit(1)
    
    # Start timing
    start_time = time.time()
    
    # Filter the file
    filter_by_assay(
        args.input,
        args.output,
        args.assay,
        args.heme_list,
        args.solid_list,
        args.comp_list,
        args.processes
    )
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    print(f"Filtering complete. Output written to '{args.output}'")
    print(f"Processing time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
