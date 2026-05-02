# Claude App Coordinator Skill

Skill personale per Claude Code che coordina lavoro su progetti software riducendo spreco di token, letture inutili e output troppo lunghi. Pensata per nuove app, modifiche, audit, bug rescue e miglioramenti di skill, con supporto a handoff multi-agente tramite file `AI_*.md`.

Versione gemella per Codex: [Xenyu87/codex-app-coordinator-skill](https://github.com/Xenyu87/codex-app-coordinator-skill).

## Struttura

```
SKILL.md                    # core sempre caricato
references/                 # 25 reference, caricati on-demand (progressive disclosure)
recipes/                    # 5 ricette di app pronte all'uso (scheletro modulare)
assets/templates/           # 7 file copiabili (AI_*.md, AGENTS.md, CLAUDE.md)
assets/scripts/             # script di deploy (Vercel, Netlify, Railway)
scripts/validate_skill.py   # validator (frontmatter, soglie righe, coerenza)
scripts/sync_skill.py       # sync sorgente → skill installata
evaluations/scenarios.md    # comportamenti attesi documentati
```

## Installazione

Copia o symlinka la cartella in:

- globale (per-utente): `~/.claude/skills/cost-aware-app-coordinator/`
- progetto: `<progetto>/.claude/skills/cost-aware-app-coordinator/`

Su Windows: `%USERPROFILE%\.claude\skills\cost-aware-app-coordinator\`.

Claude Code rileva automaticamente le skill installate e le attiva in base alla `description` di frontmatter di `SKILL.md`.

## Comportamento principale

- Classifica ogni richiesta in 5 categorie: nuova app, modifica, audit, bug rescue, miglioramento skill
- Sceglie un budget mode (Economico / Bilanciato / Massima sicurezza) e un modello (Haiku / Sonnet / Opus) appropriato
- Legge solo i file rilevanti (no scan repo per default)
- Output corto: formato `Fatto: / Verifica:` di default
- Coordina sub-agent solo quando il rischio o il tempo risparmiato giustifica il costo in token
- Gestisce handoff multi-agente tramite `AI_HANDOFF.md`, `AI_CONTEXT.md`, `AI_DECISIONS.md`, `AI_AGENT_LOG.md`, `AI_STRUCTURE.md`

## Scenari di test

In [evaluations/scenarios.md](evaluations/scenarios.md) trovi 6 scenari di comportamento atteso, scritti in italiano semplice. Servono come riferimento per verificare manualmente che modifiche future non rompano il comportamento della skill.

## Validator

```bash
python scripts/validate_skill.py
```

Controlla: frontmatter, sezioni obbligatorie, soglie righe (SKILL.md <350, reference <120), coerenza tra `SKILL.md` ↔ `references/` ↔ `assets/`.

## Versioning

Vedi [references/release-notes.md](references/release-notes.md). Versione corrente: **v0.3.0**.

## Lingua

La skill opera in italiano per default (cambia in base alla lingua dell'utente).

## License

MIT — vedi [LICENSE](LICENSE).
