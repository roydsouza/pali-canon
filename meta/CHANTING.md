🏠 [[INDEX|Dashboard]]

# Audio Chanting Integration Guide
[[INDEX|Dashboard]] > [[topics/topics|Topics Hub]] > [[topics/texts/texts|Texts & Canon]] > [[topics/texts/pali-canon/pali-canon|Pāḷi Canon]] > Audio Chanting Integration Guide

This guide describes how audio chanting recitations are integrated into the Pali Canon Vault to support recitation, memorization, and daily meditation practice.

---

## 1. Overview

Audio chanting integration allows you to play high-quality recitations of Pali verses, suttas, and monastic codes directly from within their respective Obsidian notes. This bridges the gap between scholastic text study and oral recitation practice.

---

## 2. Directory Structure

All chanting audio files are stored in the git-ignored practice directory:
*   Path: `practice/audio/`
*   Format: `.mp3` (recommended for broad system compatibility)

> [!NOTE]
> The `practice/audio/` directory is **git-ignored** (audio files are large binaries).
> You must manually place your `.mp3` files in this folder.
> To open the folder, right-click any note in Obsidian and choose "Reveal in Finder", then navigate to `practice/audio/`.

---

## 3. How Audio Works in Obsidian

Obsidian renders an inline audio player when you **embed** a vault-relative audio file using a wikilink:

```
![[bhikkhu_patimokkha.mp3]]
```

This renders a playback bar directly in the note. Standard markdown links (`[text](path)`) will attempt to open the file externally instead.

> [!IMPORTANT]
> Do **not** use `file://` absolute paths for audio embeds — they do not render in Obsidian.
> Always use vault-relative wikilink embeds: `![[filename.mp3]]`

---

## 4. Current Audio Integrations

The following files contain audio player integrations (place the files in `practice/audio/` to activate):

1.  **Bhikkhu Pātimokkha (227 Rules)**: [[patimokkha_bhikkhu|Bhikkhu Pātimokkha]]
    *   Audio file to place: `bhikkhu_patimokkha.mp3`
    *   Embed syntax used: `![[bhikkhu_patimokkha.mp3]]`
2.  **Bhikkhunī Pātimokkha (311 Rules)**: [[patimokkha_bhikkhuni|Bhikkhunī Pātimokkha]]
    *   Audio file to place: `bhikkhuni_patimokkha.mp3`
    *   Embed syntax used: `![[bhikkhuni_patimokkha.mp3]]`

---

## 5. Audio Player Test

If you have placed the audio files in `practice/audio/`, the players below should render:

**Bhikkhu Pātimokkha:**
![[bhikkhu_patimokkha.mp3]]

**Bhikkhunī Pātimokkha:**
![[bhikkhuni_patimokkha.mp3]]

> [!NOTE]
> If the `.mp3` files do not exist yet in your `practice/audio/` folder, the embeds above will show as unresolved links. Once you place the files, they will immediately render as audio players.

---

## 6. How to Follow Links in Obsidian

To test or follow links in Obsidian:
*   **In Reading Mode**: Left-click the link directly.
*   **In Editing Mode (Live Preview/Source)**: Hold down the **`Cmd`** key (on macOS) and click the link.
