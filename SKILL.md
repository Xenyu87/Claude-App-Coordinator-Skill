---
name: cost-aware-app-coordinator
description: Skill di coordinamento per task software non triviali: nuova app, audit, bug rescue, migrazioni, deploy, modifiche cross-modulo, miglioramento skill. Da attivare quando il task richiede pianificazione, scelta di scope/stack, gestione multi-agente, file `AI_*.md`, o coordinamento di più step. NON attivare per fix di una stringa, rename locale, cambio colore, modifica isolata di 1 file noto, domande concettuali: in quei casi rispondi diretto senza protocollo.
---

# Cost-Aware App Coordinator

Coordina lavoro su progetti software riducendo spreco di token e output troppo lunghi. Supporta handoff multi-agente tramite file `AI_*.md`.

## Lingua

Default: italiano. Cambia solo se l'utente scrive in altra lingua.

## Quando NON usare questa skill

- domanda concettuale che non richiede modifiche
- compito banale di una riga
- skill più specifica già attiva (es. `claude-api`, `init`, `security-review`)
- conversazione fuori dominio software

In questi casi rispondi diretto, senza protocollo.

## 0. Fast path (modifiche piccole)

Se il task è una modifica locale (1-3 file noti, scope chiaro, niente auth/dati/migrazioni/deploy):

- non aprire `references/`, non aprire `recipes/`, non spawnare `Agent`
- modifica e basta
- output in 2 righe: `Fatto: ... / Verifica: ...`

Tutto il resto della skill (sezioni 1-19) è per task che NON rientrano qui. Nel dubbio, parti dal fast path; sali al protocollo completo solo se scopri scope o rischio maggiori.

## 1. Classificazione del task

Categorie (interne, non stampare): **nuova app**, **modifica app**, **audit**, **bug rescue**, **miglioramento skill**.

Trigger tipici → categoria:
- "crea/scaffold/parti da zero" → nuova app
- "aggiungi/cambia/refactor/sposta" → modifica app
- "rivedi/review/controlla sicurezza" → audit
- "non funziona/errore/crash" → bug rescue
- "aggiorna la skill/automigliorati" → miglioramento skill

Anche senza dichiarazione esplicita, classifica dal verbo principale e dallo stato del repo. Dettagli: `references/task-routing.md`.

## 2. Budget mode

- **Economico** (default): minimo letture, output corto
- **Bilanciato**: letture mirate sui file impattati
- **Massima sicurezza**: letture estese, doppio check, audit

Default Economico, escalation automatica per gate di rischio. L'utente può forzare. Dettagli: `references/budget-modes.md`.

## 3. Selezione del modello

Modello più piccolo capace di chiudere il task (`haiku` < `sonnet` < `opus` per costo).

**Main agent**: scelto dall'utente, non cambiabile dalla skill. Se il rischio sale (auth, migrazioni), suggerisci di passare a Opus, non assumere.

**Sub-agent**: imposta automaticamente `model` su `Agent` in base al task — tabella decisionale in `references/specialist-agents.md`. In dubbio, scegli più piccolo.

## 4. Lettura iniziale del contesto

Solo questi file se esistono, in ordine:

1. `AI_HANDOFF.md` (se subentri da un altro agente)
2. `AI_CONTEXT.md`
3. `AGENTS.md`
4. `CLAUDE.md`
5. `README.md` (solo se i precedenti non bastano)

Non leggere tutta la repo: la lettura preventiva brucia contesto su file mai usati.

## 5. Progressive loading

`SKILL.md` è il core sempre caricato. I `references/*.md` solo quando un trigger concreto è presente. Se una reference è già stata letta in questo turno, riusa la comprensione invece di rileggerla.

Mappa attivazione reference:

- task → `references/task-routing.md`
- budget → `references/budget-modes.md`, `references/response-economy.md`
- gate decisionali → `references/decision-risk-gates.md`
- ruoli → `references/role-profiles.md`, `references/specialist-agents.md`, `references/qa-test-agent.md`
- handoff → `references/agent-handoff.md`, `references/cross-agent-handoff-template.md`
- creazione app → `references/app-creation-blueprint.md`, `references/default-stacks.md`, `references/project-context-template.md`, `references/structure-memory-template.md`, `references/second-brain-template.md`, `references/agent-autolog-template.md`; ricette pronte in `recipes/`
- deploy app → `references/deploy-paths.md` + script in `assets/scripts/deploy-*.sh`
- testing visivo (UI) → `references/visual-first-testing.md`
- manutenzione → `references/maintenance-compaction.md`, `references/compression-pass.md`, `references/skill-sync.md`, `references/improvement-log.md`, `references/release-notes.md`
- sicurezza coordinatore → `references/coordinator-safety.md`
- self-improvement → `references/self-improvement.md`
- tuning del loading → `references/progressive-loading.md`

## 6. Working loop

Per task non banali: budget+modello internamente → contesto minimo → mini-piano se serve → patch piccole → verifica mirata → chiusura corta. Smetti di pianificare quando il prossimo passo è ovvio.

## 7. Output economy

Default:

```
Fatto: <azione concisa>
Verifica: <come l'utente controlla>
```

Dettagli solo per: rischi, scelte non banali, blocchi, azioni utente. Quando l'utente deve configurare/scegliere/confermare/pagare/testare, aggiungi un blocco `Da fare per te:`.

Regole complete: `references/response-economy.md`.

## 8. Gate decisionali e rischio

Prima di azioni rischiose o irreversibili (delete, force-push, modifica DB, migrazioni, rimozione dipendenze, segreti) fermati e chiedi.

Confidenza: alta → procedi; media → verifica/specialista; bassa → chiedi/red team. Vedi `references/decision-risk-gates.md`.

## 9. Specialisti

Sub-agent solo se il rischio o il tempo risparmiato giustifica il costo in token. **Mai parallelizzare per default**: il costo cresce non-lineare con il numero di agent.

**Attiva** per: ricerca cross-file ampia, secondo parere, slice indipendente, audit ampio. **NON attivare** per: <3 file, fix locale, copy change, single-fact lookup ispezionabile dal main.

In Claude Code: tool `Agent` con `subagent_type` (`code-reviewer`, `Explore`, `Plan`, `general-purpose`, `doc-writer`, `architect`). Briefing autocontenuto: obiettivo, contesto minimo, formato. Mai "decidi tu".

Profili: `references/role-profiles.md`, `references/specialist-agents.md`, `references/qa-test-agent.md`.

## 10. Handoff tra agenti

Due livelli:

- **tra agenti diversi** (sessioni separate, altri tool): file condivisi nella repo (`AI_CONTEXT.md`, `AI_STRUCTURE.md`, `AI_DECISIONS.md`, `AI_AGENT_LOG.md`, `AI_HANDOFF.md`).
- **tra sub-agent stessa sessione**: non si parlano direttamente, il coordinator è router. Task brevi: passa il risultato di A nel prompt di B (filtrato). Task lunghi: usa `AI_HANDOFF.md` come bacheca. Riprendere agent attivo: `SendMessage`.

Quando subentri leggi `AI_HANDOFF.md` per primo. Aggiornalo dopo modifiche non banali. Decisioni durevoli → promosse a `AI_DECISIONS.md`.

Dettagli: `references/agent-handoff.md`, `references/cross-agent-handoff-template.md`.

## 11. Definition of Done

Task chiuso quando: il comportamento è gestito, file toccati limitati al task, check rilevanti eseguiti (o motivo di skip dichiarato), output finale corto. Per UI/funzionale a rischio medio/alto: l'utente conferma in linguaggio piano + valuta screenshot Playwright.

## 12. Creazione di una nuova app

- **Step 0** — riconosci ricetta in `recipes/` (landing, CRUD, dashboard, blog, bot). Se non c'è match, scegli da `references/default-stacks.md` (A/B/C) — non chiedere "quale framework".
- **Step 1** — scaffolding minimo: struttura + `AI_CONTEXT.md`, `AI_STRUCTURE.md`, `AGENTS.md`, `CLAUDE.md`. Niente "per il futuro", niente test/CI non richiesti.
- **Step 2** — deploy presto: già al primo `npm run dev` configura Vercel/Netlify/Railway. Vedi `references/deploy-paths.md` + `assets/scripts/`.
- **Step 3** — test visivo: dopo cambi UI usa il pattern di `references/visual-first-testing.md`.

File `AI_*.md`, `AGENTS.md`, `CLAUDE.md` pronti in `assets/templates/`. Regole d'uso nei reference `*-template.md`. Blueprint completo: `references/app-creation-blueprint.md`.

## 13. Modifica di app esistente

1. Leggi `AI_HANDOFF.md` o `AI_CONTEXT.md`.
2. Identifica il minimo set di file impattati.
3. Modifica solo ciò che serve. Niente refactor opportunistico (aumenta diff e rischio senza valore).
4. Aggiorna `AI_HANDOFF.md` se la modifica non è banale.
5. Output corto come da §7.

## 14. Audit

Solo lettura, no modifiche senza ok. Output: findings con severità, file:riga, fix proposto. Niente narrazione.

## 15. Bug rescue

Riproduci con minime letture → proponi fix se causa non ovvia → aggiorna `AI_AGENT_LOG.md` se pattern ricorrente.

## 16. Miglioramento skill

Per modifiche a skill: `references/skill-sync.md` per il drift, `references/improvement-log.md` per le voci, `references/release-notes.md` se cambia comportamento, `python scripts/validate_skill.py` prima di chiudere.

La skill **non si modifica senza approvazione esplicita** ("procedi"/"automigliorati" valgono per il run corrente). Template di proposta e flow completo in `references/self-improvement.md`.

## 17. Manutenzione

Compattazione periodica dei file `AI_*.md`. Vedi `references/maintenance-compaction.md` e `references/compression-pass.md`.

## 18. Sicurezza del coordinatore

Regole anti-loop, anti-overwrite, anti-spreco: `references/coordinator-safety.md`.

## 19. Validator

`scripts/validate_skill.py` controlla: frontmatter conforme (name <=64 char, description <=1024), reference ↔ SKILL ↔ assets coerenti, mappa di progressive loading completa, heading duplicati, sezioni obbligatorie, `SKILL.md` <350 righe, reference <120 righe.

```bash
python scripts/validate_skill.py
```
