#!/usr/bin/env python3
import csv
import argparse
import sys
from typing import List, Dict

def get_header_line(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#Samplename\t'):
                return line.strip().split('\t')
    return None

def find_u2af1_variant(file_path: str) -> List[Dict[str, str]]:
    """Find the U2AF1 R156H variant in the file."""
    variants = []
    header = get_header_line(file_path)
    if not header:
        print(f"Error: Could not find header line in {file_path}")
        sys.exit(1)

    required_fields = ['Gene', 'Chrom', 'Pos', 'Ref', 'Alt', 'p_Change(SnpEff)']
    field_indices = {}
    
    try:
        for field in required_fields:
            field_indices[field] = header.index(field)
    except ValueError as e:
        print(f"Error: Required column not found in header - {str(e)}")
        print("Available columns:", header)
        sys.exit(1)
        
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
                
            row = line.strip().split('\t')
            try:
                # Check if this is the U2AF1 R156H variant
                # Only check gene, position and amino acid change
                if (row[field_indices['Gene']] == 'U2AF1' and 
                    row[field_indices['Chrom']] == 'chr21' and
                    row[field_indices['Pos']] == '43094670'):
                    protein_change = row[field_indices['p_Change(SnpEff)']]
                    # Print the protein change for debugging
                    print(f"Found U2AF1 variant with protein change: {protein_change}")
                    variant_info = {
                        'Sample': row[0],
                        'Gene': row[field_indices['Gene']],
                        'Chrom': row[field_indices['Chrom']],
                        'Pos': row[field_indices['Pos']],
                        'Ref': row[field_indices['Ref']],
                        'Alt': row[field_indices['Alt']],
                        'Protein_Change': protein_change
                    }
                    variants.append(variant_info)
            except IndexError:
                continue
    return variants

def main():
    parser.add_argument('file1', help='Path to first variant file')
    parser.add_argument('file2', help='Path to second variant file')
    args = parser.parse_args()

    # Search in both files
    variants1 = find_u2af1_variant(args.file1)
    variants2 = find_u2af1_variant(args.file2)
    
    # Output results
    if variants1:
        for v in variants1:
            print(f"Sample: {v['Sample']}")
            print(f"Location: {v['Chrom']}:{v['Pos']} {v['Ref']}>{v['Alt']}")
            print(f"Protein Change: {v['Protein_Change']}")
            print("---")
    else:
        print("Not found")
        
    print(f"\nU2AF1 variants at position chr21:43094670 in {args.file2}:")
    if variants2:
        for v in variants2:
            print(f"Sample: {v['Sample']}")
            print(f"Location: {v['Chrom']}:{v['Pos']} {v['Ref']}>{v['Alt']}")
            print(f"Protein Change: {v['Protein_Change']}")
            print("---")
    else:
        print("Not found")

if __name__ == "__main__":
    main()
