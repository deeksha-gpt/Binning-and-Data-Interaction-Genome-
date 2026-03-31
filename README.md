[5y_enh_atlas_interacting_genes_NAMES.txt](https://github.com/user-attachments/files/25868721/5y_enh_atlas_interacting_genes_NAMES.txt)<img width="633" height="530" alt="Screenshot 2026-03-10 163217" src="https://github.com/user-attachments/assets/e4631ed8-af52-4af8-9356-42adaba69b50" />
# 🔬 Chromatin Loop → Enhancer → Gene Expression Pipeline

## 📌 Overview

This pipeline identifies genes interacting with enhancer-associated chromatin loops and maps their expression levels using FPKM values.

It integrates:

* Chromatin loop data (**BEDPE**)
* Enhancer regions (**BED**)
* Gene TSS annotations (**BED**)
* Gene expression data (**FPKM**)

---

## 📂 Input Files

| File                           | Description                                |
| ------------------------------ | ------------------------------------------ |
| `5y_merged_loops.bedpe`        | Chromatin loop interactions (BEDPE format) |
| `SH-SY5Y_enh_atlas.bed`        | Enhancer atlas regions                     |
| `gene_name_tss_human_sort.bed` | Gene TSS coordinates                       |
| `5Y-FPKM.txt`                  | Gene expression values (FPKM)              |

---

## ⚙️ Workflow Steps

### 1️⃣ Convert BEDPE → BED (Loop Anchors)

Extract both loop anchors and remove duplicates:

```bash
awk '{print $1"\t"$2"\t"$3"\n"$4"\t"$5"\t"$6}' 5y_merged_loops.bedpe \
| sort -u > 5y_merged_loops.bed
```

---

### 2️⃣ Identify Loop Ends Overlapping Enhancers

```bash
bedtools intersect \
-a 5y_merged_loops.bed \
-b SH-SY5Y_enh_atlas.bed \
-u > 5y_loop_end_with_enh_atlas.bed
```

---

### 3️⃣ Extract Interacting Regions

Find the interacting partner of enhancer-overlapping loop anchors.

```python
bed_file = "5y_loop_end_with_enh_atlas.bed"
bedpe_file = "5y_merged_loops.bedpe"
output_file = "5y_enh_atlas_interactions.bed"

bed_set = set()
with open(bed_file) as f:
    for line in f:
        fields = line.strip().split("\t")
        bed_set.add(tuple(fields[:3]))

interactions = set()

with open(bedpe_file) as f:
    for line in f:
        flds = line.strip().split("\t")
        a1 = tuple(flds[:3])
        a2 = tuple(flds[3:6])

        if a1 in bed_set:
            interactions.add(a2)
        if a2 in bed_set:
            interactions.add(a1)

with open(output_file, "w") as out:
    for i in interactions:
        out.write("\t".join(i) + "\n")
```

---

### 4️⃣ Identify Interacting Genes

```bash
bedtools intersect \
-a gene_name_tss_human_sort.bed \
-b 5y_enh_atlas_interactions.bed \
-u > 5y_enh_atlas_interacting_genes.bed
```

---

### 5️⃣ Extract Gene Names

```bash
awk '{print $NF}' 5y_enh_atlas_interacting_genes.bed \
| sort -u > genes.txt
```

---

### 6️⃣ Map Genes to Expression (FPKM)

```python
selected = set(line.strip() for line in open("genes.txt"))

fpkm = {}
with open("5Y-FPKM.txt") as f:
    for line in f:
        gene, val = line.split()
        fpkm[gene] = float(val)

with open("final_expression.txt", "w") as out:
    for g in selected:
        if g in fpkm:
            out.write(f"{g}\t{fpkm[g]}\n")
```

---

## 🧹 Duplicate Removal

Use efficient methods instead of nested loops:

```bash
sort -u file.bed > clean.bed
```

or

```bash
awk '!seen[$0]++' file.bed > clean.bed
```

---

## 🔍 File Integrity Check (MD5)

```bash
md5sum file1 file2
```

In Excel:

```
=A1=B1
```

---

## 📤 Output Files

| File                                 | Description                    |
| ------------------------------------ | ------------------------------ |
| `5y_merged_loops.bed`                | Loop anchors                   |
| `5y_loop_end_with_enh_atlas.bed`     | Enhancer-overlapping loop ends |
| `5y_enh_atlas_interactions.bed`      | Interacting regions            |
| `5y_enh_atlas_interacting_genes.bed` | Interacting genes              |
| `genes.txt`                          | Unique gene list               |
| `final_expression.txt`               | Genes with FPKM values         |

---

## 🚀 Summary

This pipeline:

* Maps chromatin loops to enhancers
* Identifies distal interacting regions
* Links interactions to genes
* Quantifies gene expression

---

## 🛠️ Requirements

* `bedtools`
* `awk`, `sort` (Unix tools)
* Python 3.x

---

## 💡 Notes

* Ensure all BED files are **sorted and same genome build**
* Use `sort -u` frequently to avoid duplicates
* Python sets improve performance significantly

---

## 📈 Future Improvements

* Convert to **Snakemake / Nextflow pipeline**
* Add visualization (Hi-C loops, genome browser)
* Integrate differential expression analysis

---
