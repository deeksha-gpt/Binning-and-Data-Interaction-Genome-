# Define the input filenames for BED and BEDPE files
bed_file = "5y_loop_end_with_invitroG4s_enh_hist.bed"
bedpe_file = "5y_merged_loops.bedpe"
output_bed_file = "5y_invitroG4s_enh_hist_interactions.bed"

# Create dictionaries to store the BEDPE data in both forward and reverse mappings
bedpe_forward_data = {}
bedpe_reverse_data = {}

# Read the BEDPE file and store data in the forward dictionary
with open(bedpe_file, "r") as bedpe:
    for line in bedpe:
        fields = line.strip().split("\t")
        key = tuple(fields[:3])  # First 3 columns as a tuple (BEDPE key)
        value = fields[3:6]      # 4th, 5th, and 6th columns as a list
        bedpe_forward_data[key] = value

# Read the BEDPE file again and store data in the reverse dictionary
with open(bedpe_file, "r") as bedpe:
    for line in bedpe:
        fields = line.strip().split("\t")
        key = tuple(fields[3:6])  # 4th, 5th, and 6th columns as a tuple (BEDPE key)
        value = fields[:3]      # First 3 columns as a list
        bedpe_reverse_data[key] = value

# Create a new BED file using the BED data and the BEDPE data (forward)
with open(bed_file, "r") as bed, open(output_bed_file, "w") as output_bed:
    for line in bed:
        fields = line.strip().split("\t")
        key = tuple(fields[:3])  # First 3 columns as a tuple (BED key)
        if key in bedpe_forward_data:
            value = bedpe_forward_data[key]
            output_line = "\t".join(value)  # Only include columns from BEDPE
            output_bed.write(output_line + "\n")

# Expand the new BED file using the BED data and the BEDPE data (reverse)
with open(bed_file, "r") as bed, open(output_bed_file, "a") as output_bed:
    for line in bed:
        fields = line.strip().split("\t")
        key = tuple(fields[:3])  # First 3 columns as a tuple (BED key)
        if key in bedpe_reverse_data:
            value = bedpe_reverse_data[key]
            output_line = "\t".join(value)  # Only include columns from BEDPE
            output_bed.write(output_line + "\n")