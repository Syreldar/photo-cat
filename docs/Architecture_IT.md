<!-- SPDX-FileCopyrightText: 2026 PHOTO-CAT contributors -->
<!-- SPDX-License-Identifier: GPL-3.0-only -->
# Architettura e confini dei test

PHOTO-CAT è organizzato attorno a comportamenti pubblici stabili e a un'implementazione interna sostituibile.

## Interfacce pubbliche

Le seguenti interfacce sono considerate contratti verso gli utenti:

- `photo-cat` e i relativi sottocomandi documentati.
- I nomi delle sezioni di `config.yaml` e le impostazioni documentate.
- Il configuratore grafico.
- I file prodotti dalla costruzione dell'indice.
- I campi JSON prodotti dalla query.
- Le modalità package-install e cartella progetto di `photo-cat doctor`.

I test di regressione devono proteggere queste interfacce mentre il codice interno viene suddiviso o migliorato.

## Fasi della pipeline

La pipeline runtime ha tre confini:

1. **Configurazione**: interpreta YAML, risolve i percorsi e valida tipi e intervalli delle impostazioni.
2. **Build/index**: carica il catalogo e crea l'indice dei vicini riprendibile.
3. **Query/contaminazione**: legge l'indice e produce risultati di contaminazione per i target configurati.

`config_and_run.py` è limitato all'orchestrazione della pipeline. Stabilisce quali fasi sono abilitate e invoca i moduli build e query; non esegue direttamente calcoli scientifici.

## Mappa delle responsabilità dei moduli

| Modulo | Responsabilità attuale | Rischio per i contratti durante il refactoring |
|---|---|---|
| `path_policy.py` | Risolve i percorsi runtime non-GUI, valida i confini del filesystem e denomina i file dell’indice/query. | Regole per percorsi relativi, contenimento degli output e layout della directory dell’indice. |
| `load_config.py` | Interpreta YAML e valida dataclass di configurazione tipizzate usando la politica dei percorsi condivisa. | Chiavi di configurazione, valori predefiniti, messaggi di validazione e percorsi relativi al file config. |
| `cli.py` e `cli_overrides.py` | Interpretano i comandi CLI documentati e creano override runtime temporanei usando la politica dei percorsi condivisa. | Nomi dei comandi, opzioni, override relativi alla directory di lavoro, stati di uscita e convenzione `ERROR:`. |
| `config_and_run.py` | Seleziona e invoca le fasi della pipeline abilitate. | Ordine build-prima-query e flag delle fasi. |
| `build_neighbors_index.py` | Carica cataloghi e crea l'indice dei vicini riutilizzabile. | Layout della directory dell'indice e convenzioni numeriche dei vicini. |
| `query_contamination_from_index.py` | Legge un indice e scrive risultati JSON di contaminazione per target. | Campi JSON, gestione degli ID target e convenzioni di flusso/separazione. |
| `doctor.py` | Riporta diagnostiche per pacchetto e progetto sorgente. | Comportamento diagnostico in modalità pacchetto installato e cartella progetto. |

Il refactoring futuro dovrebbe iniziare estraendo una sola responsabilità focalizzata da un modulo, quindi proteggendo il confine pubblico circostante con test di regressione. La politica dei percorsi è ora separata dall’esecuzione runtime non-GUI: configurazione e CLI risolvono i percorsi rispetto a una directory base esplicita, mentre la query consuma `IndexPaths` nominati e validati senza ricostruire inline i nomi dei file dell’indice.

## Confine della politica dei percorsi

La risoluzione dei percorsi è separata intenzionalmente dall’esecuzione scientifica e della pipeline:

- I percorsi scritti in `config.yaml` sono risolti rispetto alla directory che contiene quel file di configurazione.
- I percorsi CLI espliciti `--config` e gli override diretti dei percorsi CLI sono risolti rispetto alla directory di lavoro da cui viene invocato `photo-cat`.
- `path_policy.py` gestisce espansione, risoluzione assoluta, validazione di file/directory, denominazione del layout dell’indice e collocamento controllato degli output della query.
- Il modulo query valida un oggetto `IndexPaths` prima di aprire memory map o eseguire lavoro numerico.

Questo rende le regole del filesystem testabili in modo indipendente ed evita di modificare la directory di lavoro del processo soltanto per interpretare un percorso.

## Mappa dei refactoring rimanenti

I seguenti candidati sono identificati per future attività mirate; non richiedono una riscrittura estesa:

| Modulo o area | Responsabilità candidata da isolare | Protezione suggerita prima della modifica |
|---|---|---|
| `configure_gui.py` | Stato UI, presentazione dei percorsi e persistenza della configurazione sono ancora strettamente collegati. | Test di regressione GUI/salvataggio config e verifica manuale dei launcher. |
| `build_neighbors_index.py` | Ciclo di resume/checkpoint e persistenza finale dei file dell’indice restano lavoro runtime procedurale. | Test di regressione del layout dell’indice e test mirati dei checkpoint. |
| `query_contamination_from_index.py` | Interpretazione degli input target e persistenza JSON possono essere ulteriormente separate dal calcolo numerico. | Test di regressione dello schema dei risultati query. |
| `doctor.py` e `install.py` | Diagnostica dell’ambiente e workflow di installazione sono intenzionalmente operativi ma estesi. | Test della diagnostica in modalità pacchetto installato e progetto sorgente. |

Usa questa mappa per selezionare una responsabilità circoscritta per release. Strategy o Chain of Responsibility rimangono non necessari finché non emergono politiche realmente intercambiabili.

## Strategia di test

I test sono raggruppati per scopo:

- I **test di regressione** (`@pytest.mark.regression`) proteggono CLI, pipeline e comportamento dei risultati pubblici.
- I **test unitari** (`@pytest.mark.unit`) verificano helper puri come validazione di percorsi/configurazione, conversioni di coordinate, risoluzione degli ID e calcoli di flusso.
- I **test di integrazione** usano il catalogo e i target di esempio inclusi per verificare insieme build e query.
- I **report di coverage** individuano i percorsi non testati; guidano le priorità ma non sostituiscono le asserzioni sul comportamento.

Gli input temporanei condivisi appartengono a `tests/conftest.py`. Ogni test è classificato esplicitamente con `@pytest.mark.regression` o `@pytest.mark.unit`; la CI usa una gestione rigorosa dei marker. I test devono includere una docstring quando il risultato atteso dipende da una regola scientifica, da una convenzione numerica o da un comportamento di compatibilità non ovvio. Vedi [Workflow di sviluppo](Development_IT.md) e [Contratti pubblici](Public-Contracts_IT.md) per le regole rivolte ai contributori.

## Indicazioni per il refactoring

Il refactoring deve prima preservare i contratti pubblici. È preferibile estrarre un helper focalizzato da una funzione ampia, aggiungere test unitari e solo dopo semplificare il chiamante. Non introdurre un design pattern solo per il suo nome: Strategy o Chain of Responsibility vanno adottati soltanto quando esistono realmente più politiche di esecuzione o validazione intercambiabili.
