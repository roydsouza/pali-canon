# Mātika (Buddhist Lists Index)

**Navigation**: [[Matika-Index|Pali Canon Vault]] / [[matika/Matika-Index|Mātika]]

This directory contains systematic registers of Buddhist lists (*mātika*) compiled from the Pali Canon. Each list is stored in a dedicated file with Romanized Pali and item-by-item English translations, fully cross-referenced. Each list also has individual **factor detail files** with canonical definitions, practice descriptions, and sutta links.

**22 canonical lists · 105+ factor detail files · 0 broken links**

---

## ✦ Recommended Entry Points

| Practice question | Start here |
|---|---|
| Where am I on the path? | [[noble_eightfold_path]] (8 factors) |
| Why is there suffering? | [[four_noble_truths]] (4 factors) → [[dependent_origination]] (12 links) |
| What am I meditating with? | [[four_foundations_of_mindfulness]] (4 factors) |
| What blocks concentration? | [[five_hindrances]] (5 factors) |
| What supports awakening? | [[seven_awakening_factors]] (7 factors) |
| How to develop loving-kindness? | [[four_sublime_states]] (4 factors) → [[loving_kindness]] |
| What is the mind made of? | [[five_aggregates]] (5 factors) |
| What chains rebirth? | [[ten_fetters]] (10 factors) |
| What does virtue look like? | [[five_precepts]] · [[eight_precepts]] · [[gradual_training]] |
| What is the practice roadmap? | [[seven_purifications]] (7 stages) |

---

## 📋 Doctrinal Lists

```dataview
TABLE title_pali AS "Pāḷi Title"
WHERE contains(file.path, "matika/") 
  AND contains(list("four_noble_truths", "noble_eightfold_path", "three_marks", "five_aggregates", "dependent_origination", "five_precepts", "five_hindrances", "seven_awakening_factors", "four_foundations_of_mindfulness", "eight_precepts", "three_refuges", "ten_perfections", "four_sublime_states", "five_spiritual_faculties", "three_unwholesome_roots", "four_right_exertions", "ten_fetters", "seven_purifications", "five_powers", "four_jhanas", "six_recollections", "gradual_training"), file.name)
SORT file.name ASC
```

---

## 🏷️ Individual Factors & Mental States

```dataview
TABLE title_pali AS "Pāḷi Title"
WHERE contains(file.path, "matika/") 
  AND file.name != "INDEX"
  AND !contains(list("four_noble_truths", "noble_eightfold_path", "three_marks", "five_aggregates", "dependent_origination", "five_precepts", "five_hindrances", "seven_awakening_factors", "four_foundations_of_mindfulness", "eight_precepts", "three_refuges", "ten_perfections", "four_sublime_states", "five_spiritual_faculties", "three_unwholesome_roots", "four_right_exertions", "ten_fetters", "seven_purifications", "five_powers", "four_jhanas", "six_recollections", "gradual_training"), file.name)
SORT file.name ASC
```

---
*Back to [[Matika-Index|Vault Home]]*
