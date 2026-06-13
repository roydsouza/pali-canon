---
id: INDEX
title: Practice Dashboard
type: practice
tags:
  - practice/index
---

<div class="db-header">
  <h1>Pali Canon Practice Hub</h1>
  <p>Daily recollection, chanting recitation, and meditation logging</p>
</div>

<div class="db-grid-wide">

  <div class="db-card practice">
    <div>
      <span class="db-badge practice">Statistics</span>
      <h3>🧘 Meditation Overview</h3>
      <p>Live summary of your meditation practice aggregated via Dataview.</p>
      
```dataview
TABLE WITHOUT ID length(rows) as "Total Sessions", sum(rows.duration_minutes) as "Total Minutes", round(sum(rows.duration_minutes)/60, 1) as "Total Hours"
FROM #practice/session
GROUP BY true
```

```dataview
TABLE WITHOUT ID meditation_type as "Meditation Type", length(rows) as "Sessions", sum(duration_minutes) as "Total Min"
FROM #practice/session
GROUP BY meditation_type
```
    </div>
  </div>

  <div class="db-card jhana">
    <div>
      <span class="db-badge jhana">Memorization</span>
      <h3>📖 Active Recitation Log</h3>
      <p>Key Pali verses selected for memorization and daily chanting practice.</p>
      <ul class="db-link-list">
        <li><a class="internal-link" href="../mula/sutta/anguttara_nikaya/an11_15.md">AN 11.15 / Snp 1.8: Karaṇīyamettāsutta</a> <span class="db-badge jhana">Reviewing</span></li>
        <li><a class="internal-link" href="../mula/sutta/khuddaka_nikaya/dhammapada/dhp_01_yamakavagga.md">Dhammapada: Dhp 1 (Manopubbaṅgamā)</a> <span class="db-badge jhana">Reviewing</span></li>
        <li><a class="internal-link" href="../mula/sutta/khuddaka_nikaya/dhammapada/dhp_14_buddhavagga.md">Dhammapada: Dhp 183 (Sabbapāpassa)</a> <span class="db-badge jhana">Reviewing</span></li>
        <li><a class="internal-link" href="../matika/three_refuges.md">Tisarana (Refuges)</a> <span class="db-badge jhana">Reviewing</span></li>
        <li><a class="internal-link" href="../mula/sutta/majjhima_nikaya/mn19.md">MN 19: Dvedhāvitakkasutta Verse</a> <span class="db-badge jhana">Reviewing</span></li>
      </ul>
      <p style="margin-top: 15px; font-size: 0.9em;">👉 Go to full <a class="internal-link" href="memorization_log.md">Verse Memorization Log</a></p>
    </div>
  </div>

  <div class="db-card vipassana">
    <div>
      <span class="db-badge vipassana">Chanting</span>
      <h3>🎧 Monastic Chanting Playlists</h3>
      <p>Listen to Pali recitations directly within the vault using local files.</p>
      
      <ul class="db-link-list">
        <li><a class="internal-link" href="../mula/vinaya/patimokkha_bhikkhu.md">Bhikkhu Pātimokkha (227 Rules)</a></li>
        <li><a class="internal-link" href="../mula/vinaya/patimokkha_bhikkhuni.md">Bhikkhunī Pātimokkha (311 Rules)</a></li>
      </ul>

> [!NOTE] Audio not yet configured
> Place `bhikkhu_patimokkha.mp3` and `bhikkhuni_patimokkha.mp3` in `practice/audio/` to enable embedded playback. See [[../meta/CHANTING|Audio Chanting Integration Guide]] for setup instructions.
    </div>
  </div>

  <div class="db-card matika">
    <div>
      <span class="db-badge matika">Logs & Templates</span>
      <h3>📝 Practice Logs & Navigation</h3>
      <p>Log a session or create customized practice notes.</p>
      <ul class="db-link-list">
        <li><a class="internal-link" href="../templates/practice_note.md">Meditation Session Template</a></li>
        <li><a class="internal-link" href="../Texts-Index.md">Return to Root Vault Index</a></li>
      </ul>
      <p style="margin-top: 15px; font-size: 0.85em; opacity: 0.8;">
        <strong>How to log a sit:</strong><br>
        1. Create a new note using the session template.<br>
        2. Apply the `#practice/session` tag.<br>
        3. Log your duration, type, and associated suttas to dynamically update this dashboard.
      </p>
    </div>
  </div>

</div>

---

## 🧘 Recent Meditation Sessions

*This list is generated automatically via Dataview using the `#practice/session` tag.*

```dataview
TABLE duration_minutes as "Duration (min)", associated_suttas as "Focus Suttas", hindrances as "Hindrances encountered"
FROM #practice/session
SORT date DESC
LIMIT 10
```

---

## 📍 Currently Studying

*Update these links manually as you move through your reading programme.*

| | |
|---|---|
| **Active reading path** | — |
| **Last sutta read** | — |
| **Next up** | — |
| **Graded reader position** | — |

---
*Created and maintained as a structured database for Buddhist studies and daily monastic practice.*
