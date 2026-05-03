# Release Notes

Note di rilascio sul comportamento osservabile della skill. Pensate per chi la usa, non per chi la sviluppa.

## Formato

```
## vX.Y.Z — YYYY-MM-DD
### Aggiunto
- ...
### Cambiato
- ...
### Rimosso
- ...
### Note di migrazione
- ...
```

## v0.1.0 — 2026-04-29
### Aggiunto
- prima release: skill con 19 reference, validator, file `AI_*.md` per handoff multi-agente.

## v0.6.0 — 2026-05-03
### Aggiunto
- §0 "Fast path" in SKILL.md: per modifiche locali (1-3 file noti, niente auth/dati/deploy) la skill salta tutto il protocollo (no reference, no `Agent`, output 2 righe).
- scenario 9 in `evaluations/scenarios.md` dedicato alla fast path.
### Cambiato
- frontmatter `description` esplicita i casi in cui NON attivare (fix di stringa, rename locale, modifica isolata, domande concettuali).
- SKILL.md compattato da 307 a ~190 righe; tabella sub-agent spostata in `specialist-agents.md` (single source of truth).
### Note di migrazione
- per task piccoli la skill consuma molti meno token (no reference né spawn). Per task non triviali, comportamento invariato. Motivazione: feedback utente — modifica semplice consumava 40% del budget in 5 ore.

## v0.5.0 — 2026-05-02
### Aggiunto
- `recipes/` con 5 ricette pronte (landing-page, crud-with-auth, data-dashboard, content-site, bot): scheletro modulare con stack + struttura + primi passi + deploy + costi + punti di personalizzazione.
- `references/default-stacks.md`: 3 stack default (A: Next.js+Supabase+Vercel, B: Astro+Vercel, C: Node+Railway) per evitare di chiedere "quale framework" ad ogni nuova app.
- `references/deploy-paths.md` + `assets/scripts/deploy-{vercel,netlify,railway}.sh`: percorsi concreti per mettere l'app online, con costi.
- `references/visual-first-testing.md`: protocollo "URL / cosa fare / cosa vedere / cosa segnalare" per utente non programmer.
- scenario 8 in `evaluations/scenarios.md`.
### Cambiato
- SKILL.md §12: workflow nuova app esteso con Step 0 (ricetta) / Step 2 (deploy presto) / Step 3 (test visivo). Copre il ciclo idea → online.
- mappa progressive loading allineata.
### Note di migrazione
- niente. Per nuove app la skill propone subito stack + ricetta senza interrogare l'utente sulle scelte tecniche.

## v0.4.1 — 2026-05-02
### Aggiunto
- pattern di comunicazione tra sub-agent dello stesso coordinator in `references/agent-handoff.md`: handoff via coordinator (default), via `AI_HANDOFF.md` (task lunghi), `SendMessage` (riprendere agent attivo).
- scenario 7 in `evaluations/scenarios.md`: ricerca + refactor in due passaggi con filtro del coordinator.
### Cambiato
- SKILL.md §10 distingue esplicitamente "tra agenti diversi" da "tra sub-agent dello stesso coordinator".
### Note di migrazione
- comportamento osservabile: per task multi-step (es. "cerca X poi proponi refactor") il coordinator orchestra due sub-agent passando solo le parti utili del primo al secondo, anziché far ripetere il lavoro.

## v0.4.0 — 2026-05-02
### Aggiunto
- selezione automatica del modello per i sub-agent: tabella decisionale haiku/sonnet/opus in SKILL.md §3, ripresa in `references/specialist-agents.md`. Quando Claude lancia un `Agent`, il parametro `model` viene scelto in base al tipo di task (ricerca → haiku, review/implementazione → sonnet, audit/security/architettura → opus).
- scenario 6 in `evaluations/scenarios.md` per coprire il nuovo comportamento.
### Cambiato
- §3 SKILL.md ora distingue esplicitamente main agent (modello fisso, scelto dall'utente; la skill può solo segnalare di passare a un modello più grande) da sub-agent (modello impostato automaticamente dalla skill).
### Note di migrazione
- comportamento osservabile: i sub-agent ora partono con il modello giusto senza domande, riducendo il costo dei task leggeri (ricerche, lookup) e aumentando l'affidabilità di quelli rischiosi (audit auth).

## v0.3.1 — 2026-05-02
### Aggiunto
- checklist copiabile in `references/self-improvement.md` (pattern Anthropic: `- [ ]` step da spuntare).
- riferimento al pattern "test su istanza fresca" (Claude A → Claude B) nella self-improvement.
- check di conformità frontmatter al validator: `name` (<=64 char, regex lowercase-hyphens, no reserved words) e `description` (<=1024 char).
- cartella `evaluations/` con `scenarios.md`: 6 scenari di comportamento atteso in italiano semplice, da usare come riferimento per verificare manualmente che modifiche future non rompano il comportamento.
### Cambiato
- costanti del validator (`SKILL_MAX_LINES`, `REFERENCE_MAX_LINES`, `DESCRIPTION_MAX_CHARS`) ora documentate con commento esplicativo (anti-pattern voodoo constants).

## v0.3.0 — 2026-05-02
### Aggiunto
- cartella `assets/templates/` con 7 file copiabili (`AI_CONTEXT.md`, `AI_STRUCTURE.md`, `AI_DECISIONS.md`, `AI_HANDOFF.md`, `AI_AGENT_LOG.md`, `AGENTS.md`, `CLAUDE.md`).
- check coerenza `assets/` nel validator.
- esempi di trigger per categoria nella sezione "Classificazione del task".
- ragionamento causale a 3 regole atomiche del SKILL.md (lettura repo, parallelizzazione, refactor opportunistico).
- `scripts/sync_skill.py`: sync cross-platform sorgente → installata (sostituisce Copy-Item manuale).
- `README.md` e `.gitignore` alla root del progetto, in vista della pubblicazione su GitHub.
### Cambiato
- `description` di frontmatter riscritta in terza persona con trigger phrases (best-practice ufficiale Anthropic).
- `references/app-creation-blueprint.md` punta a `assets/templates/` per i file pronti.
- i 5 reference `*-template.md` non duplicano più i blocchi markdown ora presenti come asset; mantengono solo regole d'uso ed esempi compilati ridotti.
- check duplicati heading nei reference: il validator considera ora solo H1/H2 (release-notes ha H3 ricorrenti per versione).
### Rimosso
- (n/a)
### Note di migrazione
- per nuovi progetti: copia `assets/templates/*.md` nella root invece di estrarre template dai reference.

## v0.2.0 — 2026-05-02
### Aggiunto
- sezione "Selezione del modello" allineata a Opus/Sonnet/Haiku.
- sezione "Working loop" con il ciclo standard a 6 passi.
- sezione "Definition of Done" con conferma user-facing per UI a rischio medio/alto.
- template di proposta di automiglioramento nella sezione miglioramento skill.
- `references/progressive-loading.md` per il tuning del caricamento delle reference.
- `references/self-improvement.md` allineato nel progetto sorgente.
### Cambiato
- sezione "Specialisti" estesa con criteri espliciti "quando NON attivare un sub-agent".
- mappa di progressive loading aggiornata con i nuovi reference.
- `references/maintenance-compaction.md` non duplica più le soglie di `compression-pass.md`: queste ultime sono fonte unica.
- `scripts/validate_skill.py` ora richiede anche le sezioni "Working loop" e "Definition of Done".
### Rimosso
- (n/a)
### Note di migrazione
- nessuna: nessuna sezione rimossa, solo aggiunte e ampliamenti.
- la copia installata in `~/.claude/skills/cost-aware-app-coordinator` può richiedere sync per recepire le novità.

## Quando incrementare la versione

- patch (x.y.Z): correzioni che non cambiano il comportamento atteso
- minor (x.Y.z): aggiunta sezione, reference o ruolo
- major (X.y.z): cambio default (es. budget mode), rimozione di sezioni, rinomina file

## Regole

- una voce per release, non una per modifica
- registra solo ciò che un utente nota usando la skill
- niente note interne (refactoring puro), che restano in `improvement-log.md`
