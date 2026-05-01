# Agent Handoff

Come passare lo stato tra agenti diversi (Claude Code, altri assistenti AI, sviluppatori umani).

## Principio

Comunicazione tramite file versionati nella repo. Nessuna memoria nascosta, nessun assunto su sessione precedente.

## File coinvolti

- `AI_CONTEXT.md` — contesto stabile (cos'è il progetto, stack, scopi)
- `AI_STRUCTURE.md` — mappa stabile di moduli, contratti, file critici
- `AI_DECISIONS.md` — decisioni durevoli (append-only)
- `AI_AGENT_LOG.md` — errori, sprechi, lezioni di processo
- `AI_HANDOFF.md` — stato corrente, sostituibile turno per turno
- `AGENTS.md` — regole condivise per qualsiasi agente
- `CLAUDE.md` — regole specifiche di Claude Code

## All'inizio del turno

Se subentri dopo un altro agente, leggi in ordine:

1. `AI_HANDOFF.md` (priorità)
2. `AI_CONTEXT.md` (se ti manca contesto base)
3. `AGENTS.md`, `CLAUDE.md` (regole vincolanti)
4. `AI_DECISIONS.md` (solo se la decisione corrente le tocca)

Non leggere `AI_AGENT_LOG.md` salvo task di skill maintenance o se sospetti pattern già visto.

## Durante il turno

- Aggiorna `AI_HANDOFF.md` solo se la modifica è non banale.
- Decisioni durevoli → vanno promosse in `AI_DECISIONS.md` con data e motivazione.
- Cambiamenti di struttura → aggiornano `AI_STRUCTURE.md`.
- Errori ripetibili → riga in `AI_AGENT_LOG.md`.

## Fine turno

Lascia `AI_HANDOFF.md` in stato pulito:

- è subito leggibile in <30 secondi
- contiene solo lo stato attuale, non la storia
- punta a file specifici e prossimo passo concreto

## Cosa NON mettere in AI_HANDOFF.md

- diari ("oggi ho fatto…")
- commenti sulle scelte fatte: vanno in `AI_DECISIONS.md`
- output di test: vanno nel terminale o in CI
- segreti, chiavi, credenziali
- considerazioni filosofiche

## Conflitti

Se `AI_HANDOFF.md` contraddice il codice: il codice vince. Aggiorna handoff.
Se `AI_DECISIONS.md` contraddice una richiesta utente nuova: chiedi se la decisione precedente va revocata, e marcala revocata.
