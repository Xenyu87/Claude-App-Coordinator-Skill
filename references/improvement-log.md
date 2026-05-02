# Improvement Log

Diario sintetico delle modifiche alla skill. Una riga per modifica.

## Formato

```
- YYYY-MM-DD — <area> — <cosa è cambiato> — <motivo breve>
```

## Esempi

```
- 2026-04-29 — SKILL.md — aggiunta sezione 13 miglioramento skill — separare il flow di self-update
- 2026-04-29 — references/budget-modes.md — chiarito de-escalation — evitare permanenza inutile in Massima sicurezza
```

## Voci

- 2026-05-02 — references/progressive-loading.md — nuovo reference dedicato al tuning del loading — porta in chiaro la mappa trigger e dà un punto unico per affinare cosa caricare
- 2026-05-02 — references/self-improvement.md — replicato dalla skill installata al progetto sorgente — risolto drift tra le due copie
- 2026-05-02 — SKILL.md — aggiunta sezione "Selezione del modello" — esplicita la regola "smallest capable model" allineata a Opus/Sonnet/Haiku
- 2026-05-02 — SKILL.md — aggiunta sezione "Working loop" — rende esplicito il ciclo budget→contesto→piano→implementazione→verifica→chiusura
- 2026-05-02 — SKILL.md — aggiunta sezione "Definition of Done" — chiude i task con conferma user-facing per UI a rischio medio/alto
- 2026-05-02 — SKILL.md — sezione "Specialisti" estesa con criteri "quando NON attivare" — riduce sub-agent inutili per task piccoli
- 2026-05-02 — SKILL.md — sezione "Miglioramento skill" estesa con template di proposta di automiglioramento — formalizza la richiesta di approvazione
- 2026-05-02 — references/maintenance-compaction.md — rimossa duplicazione soglie con compression-pass.md — single source of truth
- 2026-05-02 — scripts/validate_skill.py — aggiunte "Working loop" e "Definition of Done" a REQUIRED_SECTIONS — protegge la spina dorsale procedurale
- 2026-05-02 — SKILL.md — frontmatter description riscritta in terza persona con trigger phrases — best-practice ufficiale Anthropic, evita under-trigger
- 2026-05-02 — assets/templates/ — creati 7 file copiabili (AI_*.md, AGENTS.md, CLAUDE.md) — tier-3 progressive disclosure, evita di estrarre template embedded dai reference
- 2026-05-02 — scripts/validate_skill.py — aggiunto check coerenza assets/ — rileva citazioni a file mancanti
- 2026-05-02 — references/app-creation-blueprint.md — aggiornato per puntare a assets/templates/ — workflow di scaffolding ora usa file pronti
- 2026-05-02 — SKILL.md §1 — aggiunti esempi di trigger per categoria — migliora il discovery, riduce under-trigger
- 2026-05-02 — SKILL.md §4/§9/§13 — aggiunto ragionamento causale a 3 regole atomiche — best-practice writing-skills, gli LLM seguono meglio reasoning che istruzioni meccaniche
- 2026-05-02 — scripts/validate_skill.py — check duplicati heading nei reference ora ignora H3+ — falso positivo su release-notes.md (Aggiunto/Cambiato si ripetono per versione)
- 2026-05-02 — references/{project-context,structure-memory,second-brain,cross-agent-handoff,agent-autolog}-template.md — rimossi blocchi markdown embedded duplicati con assets/templates/ — single source of truth, riduce contesto al caricamento
- 2026-05-02 — scripts/sync_skill.py — nuovo script cross-platform per sync sorgente → installata — sostituisce Copy-Item PowerShell manuale, riduce drift
- 2026-05-02 — README.md, .gitignore — aggiunti alla root in vista del repo pubblico — README descrive struttura/installazione, gitignore protegge settings.local.json
- 2026-05-02 — references/self-improvement.md — checklist copiabile in formato `- [ ]` — pattern raccomandato dalla doc Anthropic per workflow lunghi (Claude può copiare e spuntare)
- 2026-05-02 — references/self-improvement.md — aggiunto pattern "test su istanza fresca" (Claude A → Claude B) — best-practice ufficiale di iterative skill development
- 2026-05-02 — scripts/validate_skill.py — documentate le costanti SKILL_MAX_LINES, REFERENCE_MAX_LINES, DESCRIPTION_MAX_CHARS — anti-pattern voodoo constants (Ousterhout)
- 2026-05-02 — scripts/validate_skill.py — aggiunti check conformità frontmatter Anthropic (name <=64 char, regex `[a-z0-9-]+`, no reserved word; description <=1024 char) — protegge le regole ufficiali
- 2026-05-02 — evaluations/scenarios.md — aggiunti 6 scenari di comportamento atteso in italiano semplice — best-practice "build evaluations first" adattata a utente non programmatore (no JSON, no infra di test)
- 2026-05-02 — SKILL.md §3, references/specialist-agents.md, evaluations/scenarios.md — selezione modello sub-agent automatizzata via tabella decisionale haiku/sonnet/opus; main-agent solo segnalato all'utente — l'utente vuole switch automatico, ma è fattibile solo per i sub-agent

## Regole

- una riga per cambio
- niente narrazione
- niente correzioni minori (typo) salvo che indichino un problema sistemico
- se la modifica cambia comportamento osservabile, aggiungila anche in `release-notes.md`

## Cosa registrare

- nuova sezione o reference
- regola modificata
- soglia modificata (righe, budget)
- aggiunta o rimozione di un ruolo

## Cosa NON registrare

- formattazione
- typo
- modifiche che il validator avrebbe imposto comunque

## Manutenzione

Quando il file supera ~150 righe, archivia voci più vecchie di 6 mesi in `release-notes.md` come riepilogo.
