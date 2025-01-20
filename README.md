# Python_code

A collection of Python scripts for bioinformatics analysis and data processing.

## Overview

This repository contains various Python scripts designed for genomic data analysis, sequence processing, and bioinformatics tasks. Each script serves a specific purpose in the bioinformatics workflow.

## Scripts

### Sequence Analysis
- `GC_calculator.py` - Calculates GC content from FASTA files
- `Blast_parse.py` - Parses BLAST output files
- `Pennmed_match_primer.py` - Primer matching tool
- `Pennmed_unique_AA.py` - Identifies unique amino acid sequences

### Genomic Analysis
- `Bamstats.py` - Generates statistics from BAM files including:
  - Total reads
  - QC metrics
  - Mapping quality
  - Paired-end information
- `CNVator.py` - Copy Number Variation analysis tool
- `SV_extract.py` - Structural Variant extraction tool supporting:
  - Insertions
  - Deletions
  - Duplications
  - Inversions

### Data Processing
- `Filter_dotplot.py` - Filters and processes dotplot data
- `Randomranges.py` - Generates random genomic ranges
- `Crossover_count.py` - Analyzes genetic crossover events

### Project Directories
- `Project1/` - Project-specific scripts and data
- `Project2/` - Project-specific scripts and data
- `Project3/` - Project-specific scripts and data
- `Project4/` - Project-specific scripts and data
- `Project5/` - Project-specific scripts and data

## Requirements

- Python 3.x
- Required packages:
  - pysam
  - biopython
  - numpy
  - pandas

## Installation

```bash
# Clone the repository
git clone https://github.com/ChaseRushton/Python_code.git

# Install required packages
pip install pysam biopython numpy pandas
```

## Usage

### BAM File Analysis
```bash
python Bamstats.py input.bam
```

### GC Content Calculation
```bash
python GC_calculator.py input.fasta
```

### Structural Variant Extraction
```bash
python SV_extract.py input_file
```

### Random Range Generation
```bash
python Randomranges.py
```

## Contributing

Feel free to contribute by:
1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

## Author

**Chase Rushton**

## License

This project is open source. Please contact the repository owner for specific licensing information.

---
Last Updated: January 20, 2025
