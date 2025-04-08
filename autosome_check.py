#!/usr/bin/env python3
import sys
import subprocess
import smtplib
from email.message import EmailMessage
from pathlib import Path

def log_error(message):
    """Log error message to stderr"""
    print(f"ERROR: {message}", file=sys.stderr)

def count_variants(vcf_file, chromosome):
    """Count variants for a specific chromosome in VCF file"""
    try:
        result = subprocess.run(['grep', '-c', f'^chr{chromosome}', vcf_file], 
                              capture_output=True, text=True)
        return int(result.stdout) if result.returncode == 0 else 0
    except Exception:
        return 0

def send_email_alert(name, missing_chromosomes):
    """Send email alert about missing variants"""
    recipients = [
  
    ]
    
    missing_list = ','.join(map(str, missing_chromosomes))
    email_body = f"""WARNING: Sample {name} is missing variant calls on the following chromosomes: {missing_list}
This may indicate an issue with:
- Sequencing coverage
- Variant calling
- Sample quality
- Pipeline processing
Please review the sample and check {name}.chromosome_distribution.txt for detailed variant distribution."""

    msg = EmailMessage()
    msg.set_content(email_body)
    msg['Subject'] = f"Missing Variant Calls Alert - Sample {name}"
    msg['From'] = "autosome_check@server.com"  # Replace with actual sender
    msg['To'] = ', '.join(recipients)

    # Note: This requires proper SMTP configuration
    try:
        with smtplib.SMTP('localhost') as server:  # Replace with actual SMTP server
            server.send_message(msg)
    except Exception as e:
        log_error(f"Failed to send email: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python autosome_check.py <sample_name>")
        sys.exit(1)
    
    name = sys.argv[1]
    vcf_file = f"{name}.final.smallvariants.vep.vcf"
    
    if not Path(vcf_file).exists():
        log_error(f"VCF file not found: {vcf_file}")
        sys.exit(1)

    print("Checking variant distribution across autosomes...")
    missing_chromosomes = []
    
    # Check variants on each autosome
    with open(f"{name}.chromosome_distribution.txt", 'w') as dist_file:
        dist_file.write("Chromosome\tVariant_Count\n")
        
        for chr_num in range(1, 23):
            count = count_variants(vcf_file, chr_num)
            dist_file.write(f"chr{chr_num}\t{count}\n")
            
            if count == 0:
                log_error(f"No variants found on chromosome {chr_num}")
                print(f"WARNING: No variants found on chromosome {chr_num}. "
                      f"This may indicate an issue with sequencing or variant calling.")
                missing_chromosomes.append(chr_num)
            else:
                print(f"Found {count} variants on chromosome {chr_num}")
    
    # Send email if any autosomes are missing variants
    if missing_chromosomes:
        send_email_alert(name, missing_chromosomes)

if __name__ == "__main__":
    main()
