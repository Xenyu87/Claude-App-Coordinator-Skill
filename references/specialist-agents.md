# Specialist Agents

Quando e come delegare a un sotto-agente in Claude Code.

## Strumento

In Claude Code la delega avviene tramite il tool `Agent`. I `subagent_type` disponibili includono tipicamente:

- `Explore` — ricerca read-only nel codice
- `Plan` — disegno di un piano di implementazione
- `code-reviewer` — review indipendente di un diff
- `general-purpose` — ricerca multi-step e task open-ended
- `doc-writer`, `architect`, ecc. quando registrati

I nomi disponibili dipendono dall'ambiente. Se non sei sicuro che un subagent type esista, non inventarlo: o usi `general-purpose`, o chiarisci col main agent.

## Quando attivare

Solo se almeno una è vera:

- la ricerca attraversa molti file e tornerebbe troppo contesto al main
- serve un secondo parere indipendente (review, audit)
- il task è chiaramente fuori scope dal main agent corrente
- richiesta esplicita dell'utente

## Quando NON attivare

- task di <3 step che il main agent chiude rapido
- editing localizzato su 1-3 file noti
- ogni volta che il task è "thorough" o "multi-angolo": gestiscilo inline

## Briefing del subagent

Il subagent parte freddo. Il prompt deve essere autocontenuto:

- obiettivo del task
- contesto necessario (path, file, vincoli)
- cosa hai già escluso
- formato di risposta atteso (es. "report sotto 200 parole")

Niente "fai del tuo meglio". Niente "in base ai risultati, implementa X" — la sintesi resta al main agent.

## Modello del subagent

Imposta sempre il parametro `model` del tool `Agent` in base al tipo di task. Vedi tabella in SKILL.md §3:

- `haiku` — ricerca cross-file, summary, lookup
- `sonnet` — code review, implementazione singolo file, debug 2-3 file
- `opus` — architettura, refactor cross-modulo, security/auth, audit ampi

In dubbio scegli il più piccolo. Se il main agent è già Opus e il sub-task è leggero, `haiku` riduce il costo senza perdere qualità.

## Background vs foreground

- Foreground: quando ti serve il risultato per il prossimo passo
- Background: solo se hai lavoro indipendente realmente parallelo

Default: foreground.

## Verifica

Il summary del subagent dice cosa ha provato a fare. Quando un subagent scrive codice, controlla i diff effettivi prima di dichiarare fatto.

## Anti-pattern

- delegare la comprensione ("decidi tu cosa cambiare")
- spawnare subagent in cascata senza riusare quelli già attivi
- duplicare lavoro tra main e subagent
