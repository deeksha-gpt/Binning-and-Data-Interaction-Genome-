# Define input and output filenames
bedpe_file = "5y_merged_loops.bedpe"
output_bed_file = "5y_merged_loops.bed"

# Open the BEDPE file for reading and the output BED file for writing
with open(bedpe_file, "r") as bedpe, open(output_bed_file, "w") as output_bed:
    for line in bedpe:
        fields = line.strip().split("\t")
        chrom1, start1, end1, chrom2, start2, end2 = fields[:6]

        # Write the extracted data to the output BED file
        output_line1 = "\t".join([chrom1, start1, end1])
        output_line2 = "\t".join([chrom2, start2, end2])
        output_bed.write(output_line1 + "\n")
        output_bed.write(output_line2 + "\n")
