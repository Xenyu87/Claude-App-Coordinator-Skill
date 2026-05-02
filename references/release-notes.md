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

## Esempio iniziale

```
## v0.1.0 — 2026-04-29
### Aggiunto
- skill `cost-aware-app-coordinator` con 19 reference.
- validator `scripts/validate_skill.py`.
- supporto a file condivisi `AI_*.md` per handoff multi-agente.
### Cambiato
- (n/a)
### Rimosso
- (n/a)
### Note di migrazione
- nessuna: prima release.
```

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
