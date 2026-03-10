# Read the bed file into a list of lists, assuming tab-separated format
with open("5y_invitroG4s_enh_hist_interactions.bed", "r") as f:
    intervals = [line.strip().split("\t") for line in f]
# Initialize an empty list to store the unique intervals
unique = []
# Loop over each interval in the input list
for i in intervals:
    # Assume it is not a duplicate by default
    duplicate = False
    # Loop over each interval in the output list
    for j in unique:
        # Check if they have the same chromosome, start, end and strand
        if i[0] == j[0] and i[1] == j[1] and i[2] == j[2]:
            # Mark it as a duplicate
            duplicate = True
            # Break out of the inner loop
            break
    # If it is not a duplicate, append it to the output list
    if not duplicate:
        unique.append(i)
# Write the output to a new bed file, assuming tab-separated format
with open("5y_invitroG4s_enh_hist_interactions_1.bed", "w") as f:
    for i in unique:
        f.write("\t".join(i) + "\n")
