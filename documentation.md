## Bash Script for Annotation and TSV generation

**Usage:**

1. **Install Prerequisites:**
   - Ensure you have Java installed.
   - Download and set up [snpEff](https://pcingola.github.io/SnpEff/) and [SnpSift](https://pcingola.github.io/SnpEff/).
   - Obtain the necessary databases: [dbSNP](https://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/All_20180423.vcf.gz), [ClinVar](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz), [gnomAD](https://console.cloud.google.com/storage/browser/_details/gcp-public-data--gnomad/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.vcf.bgz), [dbNSFP](https://snpeff.blob.core.windows.net/databases/dbs/GRCh37/dbNSFP_4.1a/dbNSFP4.1a.txt.gz)and [GRCh37.p13](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.39_GRCh38.p13/)

2. **Run the Script:**

   - Execute the script using the following commands:
     ```bash
     # Make the script executable
     chmod +x annotate_script.sh

     # Run the script
     ./annotate_script.sh
     ```

3. **Input:**
   - Provide the path to your input VCF file when prompted.

4. **Output:**
   - Annotated VCF files are generated at each annotation step.
   - The final annotated TSV file is named `${output_vcf}.extractedTSV.tsv`.

**The Bash Script - annotate_script.sh**
```bash
#!/bin/bash
# Paths to tools and databases
# (Update these paths according to your setup)
snpEff="/home/hansi98/Databases/other_db/snpEff/snpEff.jar"
snpSift="/home/hansi98/Databases/other_db/snpEff/SnpSift.jar"
java="/usr/bin/java"
dbsnp="/mnt/d/Hansi/All_20180423.vcf.gz"
clinvar="/home/hansi98/Databases/other_db/clinvar.vcf"
gnomad="/mnt/d/Hansi/release_2.1.1_vcf_exomes_gnomad.exomes.r2.1.1.sites.vcf.bgz"
dbnsfp="/mnt/d/Hansi/dbNSFP4.1a.txt.gz"

# Prompt for the input VCF file path
read -p "Enter the path to your input VCF file: " input_vcf
# Verify that the input VCF file exists
if [ ! -f "$input_vcf" ]; then
    echo "Error: Input VCF file not found: $input_vcf"
    exit 1
fi

# Prompt for the desired output VCF file name
read -p "Save the annotated VCF as (.vcf): " output_vcf

# Annotation using SNPSift and dbSNP
$java -Xmx4g -jar "$snpSift" annotate -v "$dbsnp" "$input_vcf" > "${output_vcf}.snpSift.vcf"

# Annotation using SNPeff
$java -Xmx4g -jar "$snpEff" -canon -v GRCh37.p13 -noStats "${output_vcf}.snpSift.vcf" > "${output_vcf}.snpEff.vcf" 
# Annotation using SNPSift and ClinVar
$java -Xmx4g -jar "$snpSift" annotate -v "$clinvar" "${output_vcf}.snpEff.vcf" > "${output_vcf}.clinvar.vcf"

# Annotation using SNPSift and GNOMAD
$java -Xmx4g -jar "$snpSift" annotate -v "$gnomad" "${output_vcf}.clinvar.vcf" > "${output_vcf}.gnomad.vcf"

# Annotation using SNPSift and dbNSFP
$java -Xmx4g -jar "$snpSift" dbnsfp -v -db "$dbnsfp" -f rs_dbSNP151,HGVSc_snpEff,HGVSp_snpEff,VEP_canonical,Denisova,FATHMM_pred,fathmm-MKL_coding_score,Eigen-raw_coding,GERP++_RS,phyloP100way_vertebrate,phyloP30way_mammalian,1000Gp3_AF,1000Gp3_SAS_AF,genename,ExAC_AF,phastCons100way_vertebrate,Polyphen2_HDIV_pred,MutationTaster_pred,SIFT_pred,PROVEAN_pred,CADD_raw_hg19,CADD_phred_hg19,gnomAD_exomes_AF,gnomAD_exomes_SAS_AF,ExAC_AF,ExAC_SAS_AF,gnomAD_exomes_SAS_nhomalt,gnomAD_genomes_AF,gnomAD_genomes_nhomalt,gnomAD_genomes_SAS_AF,gnomAD_genomes_SAS_nhomalt,clinvar_id,clinvar_clnsig,clinvar_trait,clinvar_review "${output_vcf}.gnomad.vcf" > "${output_vcf}.dbnsfp.vcf"

# Cleanup intermediate files (comment out if you want to keep them)
rm "${output_vcf}.snpSift.vcf" "${output_vcf}.snpEff.vcf" "${output_vcf}.clinvar.vcf" "${output_vcf}.gnomad.vcf" 

# Extract relevant fields and form TSV
$java -Xmx4g -jar "$snpSift" extractFields -v -s "," -e "N/A" "${output_vcf}.dbnsfp.vcf" FILTER QUAL CHROM POS ID AF REF ALT \
ANN[0].ANNOTATION ANN[0].IMPACT ANN[0].GENE ANN[0].FEATUREID ANN[0].BIOTYPE ANN[0].RANK ANN[0].HGVS_C ANN[0].HGVS_P \
non_cancer_AF non_neuro_AF controls_AF non_topmed_AF AF_sas AF_amr AF_nfe AF_eas AF_afr AF_nfe_onf AF_eas_oea AF_nfe_nwe AF_nfe_seu AF_nfe_swe AF_eas_jpn AF_eas_kor AF_fin AF_asj AF_nfe_est AF_oth \
non_neuro_nhomalt_popmax controls_nhomalt_popmax non_topmed_nhomalt_popmax nhomalt_popmax non_cancer_nhomalt_popmax \
rs_dbSNP151 HGVSc_snpEff HGVSp_snpEff VEP_canonical Denisova FATHMM_pred fathmm-MKL_coding_score Eigen-raw_coding GERP++_RS phyloP100way_vertebrate phyloP30way_mammalian 1000Gp3_AF 1000Gp3_SAS_AF genename ExAC_AF phastCons100way_vertebrate Polyphen2_HDIV_pred MutationTaster_pred SIFT_pred PROVEAN_pred CADD_raw_hg19 CADD_phred_hg19 gnomAD_exomes_AF gnomAD_exomes_SAS_AF ExAC_AF ExAC_SAS_AF gnomAD_exomes_SAS_nhomalt gnomAD_genomes_AF gnomAD_genomes_nhomalt gnomAD_genomes_SAS_AF gnomAD_genomes_SAS_nhomalt clinvar_id clinvar_clnsig clinvar_trait clinvar_review > "${output_vcf}.extractedTSV.tsv"

echo "Annotation completed. Output written to: ${output_vcf}.dbnsfp.vcf and ${output_vcf}.extractedTSV.tsv"

```
**Explanation of Annotation Steps:**

- **Annotation using SNPSift and dbSNP:**
  - Annotates variants with dbSNP information.

- **Annotation using SNPeff:**
  - Annotates variants with SNP effect predictions.

- **Annotation using SNPSift and ClinVar:**
  - Annotates variants with ClinVar information.

- **Annotation using SNPSift and gnomAD:**
  - Annotates variants with gnomAD allele frequency information.

- **Annotation using SNPSift and dbNSFP:**
  - Annotates variants with various functional predictions from dbNSFP.

**Cleanup:**

- Intermediate files are removed by default. If you want to keep them, comment out the cleanup section at the end of the script.

**Note:**
- Update the paths in the script to match your local setup.

---

For additional resources, refer to the [README](https://github.com/Hansi-Thewarapperuma/Inherited_Risk_Detector/blob/master/README.md).

For questions or support, contact us at [hansithewarapperuma@gmail.com](mailto:hansithewarapperuma@gmail.com).
