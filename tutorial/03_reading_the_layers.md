---
id: tutorial_03
title: "Tutorial 3: The Three Layers — Mūla, Commentary, and Sub-commentary"
type: tutorial
tags:
  - tutorial
  - layers
  - atthakatha
  - tika
  - study
---
🏠 [[INDEX|Dashboard]]

# Tutorial 3: The Three Layers
**Navigation**: [[Tutorial-Index|Vault Home]] / [[tutorial/Tutorial-Index|Tutorials]] / ← [[tutorial/02_satipatthana_as_map|Tutorial 2]]

> [!NOTE]
> **What you will be able to do after this tutorial:**
> Know when to read each layer, navigate between them fluidly, and use the commentary and sub-commentary as reference tools rather than obstacles.

---

## What the three layers are

Every sutta in this vault has up to three corresponding files:

| Layer | Pali term | What it is | Example |
|---|---|---|---|
| Root text | *Mūla* | The canonical sutta in Pali, interleaved with Sujato's English | [[mn118\|mn118.md]] |
| Commentary | *Aṭṭhakathā* | Buddhaghosa's (5th c. CE) systematic exegesis, in classical Pali | [[mn118_att\|mn118_att.md]] |
| Sub-commentary | *Ṭīkā* | Later scholars' commentary on Buddhaghosa, in classical Pali | [[mn118_tik\|mn118_tik.md]] |

The commentaries are in Pali. You do not need to read Pali to benefit from them — but even without Pali, you can use them as structural reference: the paragraph anchors (§1, §2, …) in the commentary align with passages in the mūla, so you can see which commentary paragraphs correspond to which root-text passages.

---

## When to read each layer

**Read the mūla for practice.** It is the living instruction. Sit with it, recite from it, memorize it. The Pali/English interleaving means you are always in contact with the original register of the teaching — the Buddha's cadence, word choices, and repetitions are preserved, not smoothed over.

**Consult the commentary when a passage raises a question.** Not as a first response — sit with the question first. But when you genuinely need precision: "What exactly does *kāya* mean here?" "What is the difference between *vitakka* and *vicāra*?" — the commentary answers this from within the tradition. Buddhaghosa was working from an unbroken interpretive lineage going back centuries before him.

**Use the sub-commentary rarely.** It is for when the commentary itself raises a question — a philosophical distinction, a terminological conflict, a doctrinal edge case. For daily practice and most study, the mūla and commentary are sufficient.

---

## Navigating between layers

Every mūla file has links to its commentary and sub-commentary in the frontmatter. You can see them by opening the file properties panel in Obsidian (**Cmd+,** → Properties).

Alternatively, every tutorial and reading path links directly to `_att` and `_tik` files alongside the mūla link. For example, in the reading paths you will see entries like:

> *Commentaries*: [[mn118_att|Commentary]] · [[mn118_tik|Sub-commentary]]

Click either link to open the corresponding layer.

---

## The paragraph anchors

The commentaries use `### §NNN` headers to mark paragraph boundaries. These align with passages in the root text so you can cross-reference without reading Pali. For example:

- Open [[mn10_att|MN 10 Commentary]] and search (Cmd+F) for `§1` — this is Buddhaghosa's opening definition of *sati*
- Open [[dn22_att|DN 22 Commentary]] and search for `§50` — this is the commentary on the Four Noble Truths section

The crosslinker (a vault automation script) has injected collapsible callouts in many mūla files that pull the corresponding commentary paragraph directly into the root-text view. Look for `> [!NOTE]- §NNN` blocks while reading the mūla. You can expand them without leaving the sutta.

---

## A worked example: MN 118, step 1

Open [[mn118|MN 118]] and find the first step of ānāpānasati:

> **Dīghaṁ vā assasanto 'dīghaṁ assasāmī'ti pajānāti,**
> *Breathing in long, they know: 'I'm breathing in long.'*

Now open [[mn118_att|MN 118 Commentary]] and search for `§1` or `kāya`. Buddhaghosa's first question is: *what is "the body" in "mindfulness of the body"?* His answer: in the context of breath meditation, the "body" (*kāya*) of the first tetrad refers specifically to the **breath-body** — the in-and-out breath experienced as a whole continuous process, not the gross anatomical body. This single clarification changes how you sit with step 1: you are attending to the breath as a body, a continuous stream, not to individual inhales and exhales as discrete events.

This is the commentary at its best: a precise answer to a precise question, directly serving the practice.

---

## Reading the commentary in Pali

If you are developing your Pali, the commentaries are excellent reading material. Buddhaghosa's prose is clear, highly repetitive (helpful for learners), and technically consistent. Open [[tutorial/05_pali_reading|Tutorial 5]] for the tools that support Pali reading in this vault: the DPD double-click lookup, the vocabulary callouts, and the graded reader.

---

## Going deeper

- **The full commentary index**: [[atthakatha/Atthakatha-Index|Aṭṭhakathā Index]] — all migrated commentary files
- **The sub-commentary index**: [[tika/Tika-Index|Ṭīkā Index]]
- **For MN 10 specifically**: [[mn10_att|Commentary]] has 362 paragraphs — one of the most detailed canonical treatments of any meditation sutta
- **Next tutorial**: [[tutorial/04_matika_web|Tutorial 4]] — following a doctrinal theme through the canon using the mātikā web
