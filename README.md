# CloudStrike

## CloudStrike — Multi-Cloud Threat Modeling & Attack Simulation

**L'idea** è progettare una piattaforma di cybersecurity multicloud, compatibile con **AWS, Azure e Google Cloud**, capace di analizzare infrastrutture cloud, identificare potenziali minacce e vulnerabilità e simulare possibili percorsi di attacco.

La piattaforma dovrebbe permettere di visualizzare le infrastrutture attraverso un grafo interattivo, evidenziare configurazioni insicure, permessi eccessivi e relazioni di trust rischiose, anche tra cloud provider differenti.

Una volta identificato un potenziale threat, sarebbe possibile **simulare un attacco controllato**, visualizzarne i passaggi, verificare quali controlli di sicurezza intervengono e individuare le possibili remediation.

L'obiettivo finale è mostrare come una modifica architetturale o di sicurezza possa interrompere un percorso di attacco, confrontando la situazione prima e dopo l'intervento.

### Obiettivo dell'hackathon

**Non sviluppare l'applicazione**, ma progettare e strutturare il contesto necessario affinché Kiro possa realizzarla in modo autonomo, coerente e controllato.

Il lavoro si concentrerà sui quattro pillar:

- **Specs:** definire requisiti, funzionalità e comportamento atteso della piattaforma.
- **Steering:** stabilire principi architetturali, regole di sicurezza e standard di sviluppo multicloud.
- **Skills:** fornire a Kiro competenze specializzate su threat modeling, cloud security, attack simulation e remediation.
- **Hooks:** definire controlli automatici per validare la qualità, la coerenza e la sicurezza di quanto prodotto.

**Il vero deliverable sarà quindi il sistema di Context Engineering**, non CloudStrike stessa: un insieme strutturato di istruzioni, conoscenze, procedure e controlli capace di guidare Kiro nello sviluppo della piattaforma.

---

## Context Engineering — come è organizzato

Il deliverable è il **contesto** che guida Kiro, non l'applicazione. È organizzato nei quattro
pillar nativi di Kiro, sotto `.kiro/`:

| Pillar | Dove | Ruolo |
| --- | --- | --- |
| **Steering** | `.kiro/steering/` | Regole permanenti con ID stabili (`SEC-`, `ARC-`, `AG-`, `MC-`, `QA-`, `SPEC-`, `PROV-`) e glossario |
| **Specs** | `.kiro/specs/` | Requisiti verificabili per feature (EARS), design, task — citano le regole per ID |
| **Skills** | `.kiro/skills/` | Competenze riutilizzabili: come si fa threat modeling, analisi IAM, attack path, remediation |
| **Hooks** | `.kiro/hooks/` | Controlli automatici che richiamano `tools/context-lint` |

Principio anti-duplicazione: ogni ID è definito in un solo posto e referenziato ovunque. Il
dettaglio è in `.kiro/steering/context-governance.md` (si richiama con `#context-governance`).

### Steering attuale

- `product.md`, `tech.md`, `structure.md`, `security-guardrails.md` — sempre attivi.
- `agent-architecture.md`, `multicloud-model.md`, `provider-aws/azure/gcp.md`, `spec-authoring.md`
  — attivati dal file su cui si lavora (`fileMatch`).
- `context-governance.md` — manuale.

### Validatore del contesto

`tools/context-lint/` controlla formato, unicità degli ID, riferimenti `#[[file:]]` e (nelle fasi
successive) la tracciabilità requisito ↔ task. Solo stdlib Python, eseguibile da qualunque hook:

```
python3 tools/context-lint/context_lint.py all
```

### Decisioni architetturali (indice AD)

`AD-01` grafo canonico · `AD-02` ports & adapters · `AD-03` ingestion read-only ·
`AD-04` simulazione deterministica · `AD-05` catalogo tecniche data-driven · `AD-06` trust cross-cloud ·
`AD-07` remediation = patch al grafo · `AD-08` scoring esplicito · `AD-09` stack approvato ·
`AD-10` gestione dati sensibili · `AD-11` architettura agentica · `AD-12` sonde deploy-anywhere ·
`AD-13` API native dei CSP · `AD-14` modello di autorizzazione e scope · `AD-15` modalità Simulated + Live.

### Modalità di esecuzione

- **Simulated** (default, usata nella demo): ragionamento sul grafo / digital twin, nessuna azione
  reale sui cloud.
- **Live / Probe** (visione di prodotto): azioni reali via sonde deployate dall'utente, solo entro
  uno scope autorizzato esplicito (`SEC-05`), con audit immutabile e kill-switch.
