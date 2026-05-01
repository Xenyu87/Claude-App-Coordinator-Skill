# Self-Improvement

Procedura quando l'utente chiede "automigliorati", "audita la skill", "rivedi le tue regole".

## Trigger

- "automigliorati", "self-improve", "rivedi te stessa"
- "audita la skill"
- richiesta esplicita di refactor delle reference o del SKILL.md

Categoria: **miglioramento skill**. Budget default: Bilanciato.

## Step

1. Esegui `python scripts/validate_skill.py` come baseline. Annota errori e warning.
2. Leggi `SKILL.md` e ogni reference solo una volta.
3. Identifica gap usando la checklist sotto. Non inventare migliorie estetiche.
4. Proponi all'utente **solo** se la modifica è ampia (nuova sezione di SKILL.md, rimozione reference, cambio default budget). Per fix mirati, procedi.
5. Applica modifiche minime.
6. Aggiorna `improvement-log.md` (riga per cambio).
7. Aggiorna `release-notes.md` se cambia il comportamento osservabile.
8. Esegui di nuovo il validator. Non chiudere finché non è verde.

## Checklist di gap

Cerca questi sintomi prima di scrivere:

- **copertura**: una richiesta utente comune non ha un flow chiaro
- **duplicazione**: due reference dicono la stessa cosa con piccole differenze
- **drift**: una reference cita file/sezioni che non esistono più
- **opacità**: SKILL.md menziona una regola senza puntare alla reference
- **spreco**: una reference > 120 righe o non citata da SKILL.md
- **rumore**: esempi che non aggiungono nulla rispetto al testo
- **anti-pattern emersi**: pattern visti in `AI_AGENT_LOG.md` non ancora codificati
- **piattaforma**: regole valide solo Unix in ambiente Windows o viceversa

## Cosa NON fare

- non riscrivere reference solide per ragioni stilistiche
- non aggiungere reference "che potrebbero servire"
- non spostare contenuto tra file solo per equilibrare le righe
- non rimuovere esempi che spiegano un caso non ovvio
- non bumpare version major senza confermare con l'utente

## Stop conditions

Ferma e chiedi se:

- la modifica richiede rinominare un file `references/*.md` (rompi link esterni)
- elimini un'intera sezione di `SKILL.md` (cambio comportamento)
- cambi un default (budget mode, lingua, soglia righe)
- la modifica supera 3 reference contemporaneamente

## Output finale

```
Fatto: <N> migliorie applicate. Validator: ok.
Verifica: python scripts/validate_skill.py
```

Se hai aggiornato `release-notes.md`, cita la nuova versione.
