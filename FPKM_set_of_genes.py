# 1. Read the first file and store the selected genes in a list
with open('5y_strong_pqsG4s_enh_hist_interacting_genes.txt', 'r') as file1:
    selected_genes = [line.strip() for line in file1]

# 2. Read the second file and store the genes and their FPKM values in a dictionary
gene_fpkm = {}
with open('5Y-FPKM.txt', 'r') as file2:
    for line in file2:
        gene, fpkm = line.strip().split()  # Assuming space or tab separated
        gene_fpkm[gene] = float(fpkm)

# 3. Write the selected genes and their corresponding FPKM values to the output file

with open('exp_5y_strong_pqsG4s_enh_hist_interacting_genes.txt', 'w') as outfile:
    for gene in selected_genes:
        if gene in gene_fpkm:
            fpkm_value = gene_fpkm[gene]
            outfile.write(f"{gene}\t{fpkm_value}\n")