---
id: parallels_dashboard
title: "Parallel-Texts Layer: Doctrinal Concordance"
type: meta
---
🏠 [[INDEX|Dashboard]]

# Parallel-Texts Layer: Doctrinal Concordance
**Navigation**: [[Texts-Index|Pali Canon Vault]] / [[meta/STATUS|Vault Status]]

> [!abstract] Concordance Overview
> The **Parallel-Texts Layer** maps suttas in this vault to their corresponding versions in other transmission lineages (Chinese Āgamas, Sanskrit fragments, Tibetan translations, and other Pali Nikāyas) using SuttaCentral parallel identifiers. This cross-linking exposes the common sectarian core of Early Buddhist Texts (EBTs).

---

## 🚀 Key Suttas & Doctrinal Parallels

Below are suttas in the vault that have rich parallel traditions across Sanskrit, Chinese, and other Pali collections.

### 1. Dīgha Nikāya Parallels
```dataview
TABLE length(parallels) AS "Count", parallels AS "Parallels"
WHERE contains(file.path, "mula/sutta/digha_nikaya/") AND parallels AND length(parallels) > 0
SORT length(parallels) DESC
```

### 2. Majjhima Nikāya Parallels (Top 10)
```dataview
TABLE length(parallels) AS "Count", parallels AS "Parallels"
WHERE contains(file.path, "mula/sutta/majjhima_nikaya/") AND parallels AND length(parallels) > 0
SORT length(parallels) DESC
LIMIT 10
```

### 3. Saṃyutta Nikāya Parallels (Top 10)
```dataview
TABLE length(parallels) AS "Count", parallels AS "Parallels"
WHERE contains(file.path, "mula/sutta/samyutta_nikaya/") AND parallels AND length(parallels) > 0
SORT length(parallels) DESC
LIMIT 10
```

### 4. Aṅguttara Nikāya Parallels
```dataview
TABLE length(parallels) AS "Count", parallels AS "Parallels"
WHERE contains(file.path, "mula/sutta/anguttara_nikaya/") AND parallels AND length(parallels) > 0
SORT length(parallels) DESC
```

---

## 📖 How to Query Parallels in the Vault

You can query parallels using the following Dataview snippet on any custom workspace page:

```markdown
```dataview
list parallels
where file.name = "an7_65"
```
```

This leverages the `parallels` metadata array injected into the frontmatter of every mūla sutta file.
