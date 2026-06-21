🏠 [[INDEX|Dashboard]]

# Simsapa + Digital Pāli Dictionary (DPD) Integration
[[INDEX|Dashboard]] > [[topics/topics|Topics Hub]] > [[topics/texts/texts|Texts & Canon]] > [[topics/texts/pali-canon/Texts-Index|Pāḷi Canon]] > Simsapa + Digital Pāli Dictionary (DPD) Integration

## What It Does

Simsapa is an Obsidian plugin that connects to the **Digital Pāli Dictionary (DPD)** — a comprehensive Pali lexicon with grammatical analysis, roots, compound breakdowns, and usage examples. It lets you look up any Pali word while reading in the vault, without leaving Obsidian.

---

## How to Look Up a Word

**Double-click any Pali word** in a note (reading view or live preview).

A sidebar panel opens on the right showing:
- The dictionary entry from DPD (definition, grammar, root, compounds)
- Sutta references where the word appears
- Links to open the full entry in the Simsapa [Dhamma]() Reader app (if installed)

**That's it.** No hotkey is configured — double-click is the only trigger.

---

## Prerequisite: Simsapa App

The plugin queries the local Simsapa Dhamma Reader application for dictionary data. If the app is not running:

1. Launch **Simsapa Dhamma Reader** from your Applications folder
2. Return to Obsidian — the sidebar lookup will now work

If the app is not installed, download from: simsapa.github.io (the plugin will show connection errors otherwise).

---

## Changing the Lookup Trigger (Optional)

Simsapa does not currently support a keyboard shortcut for looking up the word under the cursor. Double-click is the only trigger.

If you want to configure plugin behavior (e.g., sidebar vs. popup, which dictionary to use):

1. Open **Settings** → **Community Plugins** → **Simsapa** → **Options**
2. Adjust lookup mode, dictionary source, or sidebar position

---

## Sidebar Controls

Once open, the Simsapa sidebar stays visible until you close it. You can:
- Type a Pali word directly into the search box at the top
- Click through related entries
- Use the back/forward arrows for lookup history

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Sidebar shows "connection error" | Launch the Simsapa desktop app first |
| Double-click opens a URL or does nothing | Check plugin is enabled: Settings → Community Plugins |
| Word not found | Try the root form (e.g., `dhamma` not `dhammassa`); DPD is comprehensive but stems may differ |
| Sidebar doesn't appear | Toggle it: ribbon icon on left sidebar (book icon) |
