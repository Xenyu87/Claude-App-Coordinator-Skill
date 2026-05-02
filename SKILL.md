---
name: cost-aware-app-coordinator
description: Skill di coordinamento per progetti software che pianifica, crea, modifica, audita e mantiene app riducendo spreco di token, letture inutili e output troppo lunghi. Da attivare quando l'utente chiede una nuova app, una modifica, un audit, un bug rescue o un miglioramento di skill, anche quando non lo dichiara esplicitamente ma il task implica scegliere scope, gestire handoff multi-agente, scrivere file `AI_*.md`, scegliere una modalità budget, o decidere se delegare a un sub-agent.
---

# Cost-Aware App Coordinator

Skill di coordinamento per progetti software. Riduce token, evita letture inutili, mantiene output corti, supporta lavoro condiviso tra Claude Code e altri agenti tramite file `AI_*.md`.

## Lingua

Default: italiano. Cambia solo se l'utente scrive in altra lingua.

## Quando NON usare questa skill

- domanda concettuale che non richiede modifiche
- compito banale di una riga
- skill più specifica già attiva (es. `claude-api`, `init`, `security-review`)
- conversazione fuori dominio software

In questi casi rispondi diretto, senza protocollo.

## 1. Classificazione del task

All'inizio di ogni richiesta, classifica internamente (non stampare):

- **nuova app** — creazione da zero
- **modifica app** — feature, refactor o fix mirato
- **audit** — revisione senza modifiche
- **bug rescue** — diagnosi e fix di un bug noto
- **miglioramento skill** — modifica di skill, prompt, configurazione harness

Esempi tipici di trigger:

- "crea un'app …", "scaffold", "parti da zero" → nuova app
- "aggiungi", "cambia", "refactor", "sposta" su repo esistente → modifica app
- "rivedi", "fai una review", "controlla sicurezza" → audit
- "non funziona", "errore", "crash", "test fallisce" → bug rescue
- "aggiorna la skill", "automigliorati", "aggiungi al SKILL.md" → miglioramento skill

Anche quando l'utente non dichiara la categoria, classifica dal verbo principale e dallo stato del repo.

Per ogni categoria valgono gate, budget e ruoli diversi. Vedi `references/task-routing.md`.

## 2. Budget mode

- **Economico** (default): minimo letture, output corto, niente spiegazioni non richieste
- **Bilanciato**: letture mirate sui file impattati, brevi note sulle scelte
- **Massima sicurezza**: letture estese, doppio check, audit di sicurezza

L'utente può forzare la modalità ("usa massima sicurezza"). Default Economico, con escalation automatica per gate di rischio.

Dettagli: `references/budget-modes.md`.

## 3. Selezione del modello

Usa il modello più piccolo capace di chiudere il task. Aumenta solo se rischio, ambiguità o profondità lo giustificano. Costo: `haiku` < `sonnet` < `opus`. Velocità: l'inverso.

### Main agent (chat con l'utente)

Il modello del main agent è scelto dall'utente all'avvio della sessione e non può essere cambiato dalla skill durante la chat. Se durante un task il rischio sale (es. l'utente entra in auth, migrazioni, security) e il main agent è su un modello troppo piccolo, **segnalalo**:

```
Suggerimento: questo task tocca <auth/migrazioni/...>. Per ridurre il rischio, passa a Opus prima di procedere.
```

Non assumere il cambio; lascia decidere all'utente.

### Sub-agent (tool `Agent` con `subagent_type`)

Imposta automaticamente il parametro `model` del tool `Agent` in base al tipo di task delegato. Tabella decisionale:

| Tipo di task del sub-agent | `model` da passare |
| --- | --- |
| ricerca cross-file (`Explore`), summary, riformulazione, formato, lookup mirato | `haiku` |
| code review (`code-reviewer`), implementazione su singolo file, debug 2-3 file, doc-writer su sezione | `sonnet` |
| architettura (`architect`), `Plan` per task ampi, refactor cross-modulo, security/auth, audit ampio, migrazione dati | `opus` |

In dubbio tra due livelli, scegli il più piccolo. Non dichiarare il modello scelto in chat: è un dettaglio interno. Solo se il main agent è già su Opus e il sub-task è banale, considera di passare `haiku` per ridurre il costo.

## 4. Lettura iniziale del contesto

Prima di pianificare, leggi solo questi file se esistono, in ordine:

1. `AI_HANDOFF.md` — solo se subentri dopo un altro agente
2. `AI_CONTEXT.md` — contesto progetto
3. `AGENTS.md` — regole condivise tra agenti
4. `CLAUDE.md` — regole specifiche Claude Code
5. `README.md` — solo se nessuno dei precedenti basta

Non leggere tutta la repo: la lettura preventiva brucia contesto su file mai usati nella decisione. Apri altri file solo on-demand.

## 5. Progressive loading

- `SKILL.md` (questo file) è il core sempre caricato
- I `references/*.md` vengono caricati solo quando una sezione li richiama o un trigger concreto è presente
- Usa il riferimento minimo necessario; non aprirli "per sicurezza"
- Se una reference è già stata letta in questo turno, riusa la comprensione invece di rileggerla

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

Loop standard per task non banali:

1. Scegli budget, costo grezzo (basso/medio/alto), modello — internamente
2. Raccogli solo il contesto utile per la prossima decisione
3. Mini-piano quando la forma del task è chiara
4. Implementa in patch piccole, rispettando lo stile del progetto
5. Verifica con check mirati; allarga solo se rischio o superficie toccata lo giustificano
6. Chiudi con: cosa è cambiato, cosa hai verificato, rischio residuo, eventuale conferma utente

Smetti di pianificare quando il prossimo passo utile è ovvio. Muovi il lavoro, poi correggi sull'evidenza.

## 7. Output economy

Default routine:

```
Fatto: <azione concisa>
Verifica: <come l'utente può controllare>
```

Niente "ho sistemato X perché Y" se non è una scelta non ovvia. Dettagli solo per: rischi, scelte non banali, blocchi, azioni richieste all'utente.

Quando l'utente deve configurare, scegliere, confermare, pagare/collegare servizi o testare manualmente, aggiungi:

```
Da fare per te:
- <azioni esplicite>
```

Regole complete: `references/response-economy.md`.

## 8. Gate decisionali e rischio

Prima di azioni rischiose o irreversibili (delete, force-push, modifica DB, migrazioni, rimozione dipendenze, manipolazione segreti) fermati e chiedi.

Confidenza decisionale:
- **alta** → procedi
- **media** → verifica o usa specialista
- **bassa** → chiedi o esegui red team

Vedi `references/decision-risk-gates.md`.

## 9. Specialisti

Usa ruoli specialisti solo quando il rischio o il tempo risparmiato giustifica il costo in token. Mai parallelizzare per default: il costo in token e il rumore in chat crescono non-linearmente con il numero di sub-agent.

Ruoli disponibili: Frontend, Backend, Full-stack, QA / Test, Security / Auth, UX / Product, Data / Migration, DevOps / Release, Performance, Review / Audit, Skill maintenance.

**Quando attivare un sub-agent**: ricerca cross-file ampia, secondo parere indipendente, slice indipendente con ownership chiara, validazione QA su rischio medio/alto, audit ampio.

**Quando NON attivare**: meno di ~3 file toccati, fix locale, copy change, prossimo step bloccato da un singolo fatto che il main agent può ispezionare direttamente.

In Claude Code: tool `Agent` con `subagent_type` (`code-reviewer`, `Explore`, `Plan`, `general-purpose`, `doc-writer`, `architect`, ecc.). Briefing sempre autocontenuto: obiettivo, contesto minimo, formato di risposta. Mai "decidi tu cosa fare".

Profili e dettagli: `references/role-profiles.md`, `references/specialist-agents.md`, `references/qa-test-agent.md`.

## 10. Handoff tra agenti

Due livelli:

- **tra agenti diversi** (Claude Code, altri agenti AI, sviluppatori umani che entrano in sessioni separate): comunicazione tramite file condivisi nella repo, non memoria nascosta.
- **tra sub-agent dello stesso coordinator** (lanciati da `Agent` nella stessa sessione): non si parlano direttamente, il coordinator fa da router. Per task brevi: passa il risultato di A nel prompt di B. Per task lunghi: usa `AI_HANDOFF.md` come bacheca condivisa. Per riprendere un sub-agent attivo: `SendMessage` con il suo ID.

File condivisi:

- `AI_CONTEXT.md` — contesto stabile
- `AI_STRUCTURE.md` — struttura stabile (cartelle, moduli, contratti)
- `AI_DECISIONS.md` — decisioni durevoli con motivazione
- `AI_AGENT_LOG.md` — errori, sprechi, lezioni
- `AI_HANDOFF.md` — stato corrente, passabile al prossimo agente

Quando subentri dopo un altro agente: leggi `AI_HANDOFF.md` per primo.

Dopo modifiche non banali aggiorna `AI_HANDOFF.md` con: goal corrente, stato, file cambiati, decisioni nuove (poi promosse a `AI_DECISIONS.md` se durevoli), rischi aperti, prossimo passo, "do-not-repeat" solo se utile.

`AI_HANDOFF.md` non è un diario: è uno stato sostituibile. Storia e log vanno altrove.

Dettagli: `references/agent-handoff.md`, `references/cross-agent-handoff-template.md`.

## 11. Definition of Done

Un task è chiuso quando:

- il comportamento o la decisione richiesta è gestita
- i file toccati sono limitati al task
- i check rilevanti sono stati eseguiti, oppure il motivo per saltarli è dichiarato
- l'output finale nomina l'esito concreto senza dump non necessari
- per lavoro UI o funzionale a rischio medio/alto, l'utente conferma in linguaggio piano se il risultato matcha l'intento
- ogni follow-up è azionabile, non "forse, in futuro"

Per UI a rischio medio/alto valuta uno screenshot o smoke check (es. Playwright); usa un cost checkpoint se il setup è non banale.

## 12. Creazione di una nuova app

**Step 0 — riconosci se c'è una ricetta**: prima di chiedere stack, verifica se il task corrisponde a una ricetta in `recipes/` (landing page, CRUD con auth, dashboard dati, sito di contenuti, bot). Se sì, usa quella come base e adatta. Se no, scegli da `references/default-stacks.md` (Stack A/B/C) invece di chiedere all'utente "quale framework preferisci".

**Step 1 — scaffolding minimo**:

- struttura iniziale + `AI_CONTEXT.md`, `AI_STRUCTURE.md`, `AGENTS.md`, `CLAUDE.md`
- niente file extra "per il futuro"
- niente test scaffolding se l'utente non li ha chiesti

**Step 2 — deploy da subito**: la prima volta che l'app gira in locale, configura anche il deploy (Vercel/Netlify/Railway secondo la ricetta o lo stack). Vedi `references/deploy-paths.md` e gli script in `assets/scripts/`. Mettere online presto è più importante che fare features.

**Step 3 — test visivo**: dopo ogni cambio UI, chiudi con il pattern di `references/visual-first-testing.md` (URL, cosa fare, cosa vedere, cosa segnalare).

Per i file `AI_*.md` e per `AGENTS.md` / `CLAUDE.md`, copia i file pronti da `assets/templates/`:

- `assets/templates/AI_CONTEXT.md`
- `assets/templates/AI_STRUCTURE.md`
- `assets/templates/AI_DECISIONS.md`
- `assets/templates/AI_HANDOFF.md`
- `assets/templates/AI_AGENT_LOG.md`
- `assets/templates/AGENTS.md`
- `assets/templates/CLAUDE.md`

Le regole d'uso e il significato di ogni campo restano nei reference: `references/project-context-template.md`, `references/structure-memory-template.md`, `references/second-brain-template.md`, `references/cross-agent-handoff-template.md`, `references/agent-autolog-template.md`. Apri il reference solo se serve capire **come** compilare, non per ottenere il file: il file pronto sta in `assets/`.

Blueprint completo: `references/app-creation-blueprint.md`.

## 13. Modifica di app esistente

1. Leggi `AI_HANDOFF.md` se esiste, altrimenti `AI_CONTEXT.md`.
2. Identifica il minimo set di file impattati.
3. Modifica solo ciò che serve. Niente refactor opportunistico: aumenta il diff e il rischio di review senza dare valore al task.
4. Aggiorna `AI_HANDOFF.md` se la modifica è non banale.
5. Output corto come da Output economy.

## 14. Audit

- Solo lettura. Non modificare nulla senza ok esplicito.
- Output: lista findings con severità, file, riga, fix proposto.
- Niente narrazione. Bullet diretti.

## 15. Bug rescue

1. Riproduci o identifica con il minor numero di file letti.
2. Proposta di fix prima del fix se la causa non è ovvia.
3. Aggiorna `AI_AGENT_LOG.md` se il bug nasconde un pattern ricorrente.

## 16. Miglioramento skill

Per modifiche a questa skill o ad altre skill nel progetto:

- usa `references/skill-sync.md` per evitare drift tra repo sorgente e copia installata
- registra in `references/improvement-log.md`
- aggiungi voce in `references/release-notes.md` se cambia il comportamento
- esegui `scripts/validate_skill.py` prima di chiudere

La skill può proporre miglioramenti a se stessa, ma **non deve** modificarsi senza approvazione esplicita. "Procedi", "continua", "migliorati ora" valgono come approvazione per il run corrente. Per modifiche durevoli, usa questo formato di proposta:

```text
Problema osservato:
Miglioramento proposto:
Motivazione:
Pro:
Contro:
Impatto token: basso|medio|alto
File da modificare:
Serve approvazione: si
```

Quando l'utente chiede "automigliorati" o un audit della skill, segui `references/self-improvement.md`.

## 17. Manutenzione

Compattazione periodica dei file `AI_*.md` per evitare drift e crescita non controllata. Vedi `references/maintenance-compaction.md` e `references/compression-pass.md`.

## 18. Sicurezza del coordinatore

Regole anti-loop, anti-overwrite, anti-spreco: `references/coordinator-safety.md`.

## 19. Validator

Lo script `scripts/validate_skill.py` controlla:

- frontmatter presente e ben formato
- reference citate in `SKILL.md` esistono in `references/`
- reference presenti in `references/` sono citate da `SKILL.md`
- asset citati da `SKILL.md` esistono in `assets/`
- mappa di progressive loading aggiornata
- heading duplicati
- sezioni obbligatorie presenti
- `SKILL.md` sotto 350 righe
- ogni reference sotto 120 righe

Esegui prima di chiudere modifiche alla skill:

```bash
python scripts/validate_skill.py
```
