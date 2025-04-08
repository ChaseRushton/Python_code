# Check for variant calls on each autosome
echo "Checking variant distribution across autosomes..."
missing_chromosomes=()
for chr in {1..22}; do
    count=$(grep -c "^chr${chr}" ${name}.final.smallvariants.vep.vcf || true)
    if [ "$count" -eq 0 ]; then
        log_error "No variants found on chromosome ${chr}"
        echo "WARNING: No variants found on chromosome ${chr}. This may indicate an issue with sequencing or variant calling."
        missing_chromosomes+=("$chr")
    else
        echo "Found ${count} variants on chromosome ${chr}"
    fi
done
# Send email if any autosomes are missing variants
if [ ${#missing_chromosomes[@]} -gt 0 ]; then
    missing_list=$(IFS=,; echo "${missing_chromosomes[*]}")
    email_body="WARNING: Sample ${name} is missing variant calls on the following chromosomes: ${missing_list}
This may indicate an issue with:
- Sequencing coverage
- Variant calling
- Sample quality
- Pipeline processing
Please review the sample and check ${name}.chromosome_distribution.txt for detailed variant distribution."
    echo "$email_body" | mail -s "Missing Variant Calls Alert - Sample ${name}" 
fi
# Calculate total variants per autosome for QC report
echo -e "Chromosome\tVariant_Count" > ${name}.chromosome_distribution.txt
for chr in {1..22}; do
    count=$(grep -c "^chr${chr}" ${name}.final.smallvariants.vep.vcf || true)
    echo -e "chr${chr}\t${count}" >> ${name}.chromosome_distribution.txt
done
