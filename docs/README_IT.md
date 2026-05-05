# PHOTO-CAT - Photometric Contamination Analyzer Tool

PHOTO-CAT è uno strumento Python per la valutazione della contaminazione fotometrica in cataloghi astronomici. Il software costruisce un indice spaziale dei vicini a partire da un catalogo fotometrico e valuta le possibili sorgenti contaminanti intorno a un insieme selezionato di target.

Il pacchetto è pensato per workflow di analisi fotometrica a livello di catalogo, dove sono richieste configurazioni riproducibili, esecuzione locale e validazione chiara dei dati in ingresso.

## Panoramica

PHOTO-CAT svolge due operazioni principali:

1. costruzione di un indice dei vicini da un catalogo fotometrico in ingresso;
2. interrogazione dell'indice per identificare potenziali sorgenti contaminanti associate ai target selezionati.

Il progetto include un configuratore grafico per la preparazione di `config.yaml`, launcher multipiattaforma per l'esecuzione locale e controlli di validazione per gli errori di configurazione più comuni.

## Piattaforme supportate

PHOTO-CAT fornisce launcher per:

```text
Windows       START_WINDOWS.bat
macOS/Linux   sh START_UNIX.sh
```

I launcher creano un virtual environment Python locale e installano le dipendenze richieste nella cartella `.venv`.

È richiesto Python 3.10 o successivo.

## Dati in ingresso

PHOTO-CAT utilizza file CSV come dati in ingresso.

Lo schema predefinito del catalogo segue nomi di colonna di tipo Gaia:

```text
source_id
ra
dec
phot_g_mean_mag
```

La colonna identificativa predefinita per i target è:

```text
source_id
```

I nomi delle colonne sono case-sensitive e devono coincidere esattamente con l'header del CSV. Schemi di catalogo differenti possono essere configurati tramite l'interfaccia grafica.

È anche possibile utilizzare una lista manuale di valori `source_id` invece di un file CSV dei target.

## Configurazione

Il file principale di configurazione è:

```text
config.yaml
```

Il metodo raccomandato per modificarlo è utilizzare il configuratore grafico avviato dal launcher della piattaforma.

Quando viene selezionato un catalogo CSV, PHOTO-CAT può inizializzare automaticamente il file dei target e i percorsi di output/index corrispondenti. Tutti questi valori restano modificabili prima dell'esecuzione.

## Struttura del progetto

```text
START_WINDOWS.bat      Launcher Windows
START_UNIX.sh          Launcher macOS/Linux
START_HERE.txt         Note minime di avvio
config.yaml            Configurazione runtime
requirements.txt       Dipendenze Python
data/                  Piccoli file di input di riferimento
src/                   Codice sorgente
scripts/               Script di supporto ai launcher
docs/                  Documentazione aggiuntiva
```

## Validazione e gestione degli errori

PHOTO-CAT valida, dove possibile prima dell'esecuzione, i file selezionati, i nomi delle colonne configurate, le cartelle di output, i campi numerici del catalogo e i percorsi dell'indice.

Gli errori di configurazione vengono riportati in forma leggibile per ridurre la dipendenza da traceback Python durante l'uso ordinario.

## Documentazione

La documentazione aggiuntiva è disponibile in:

```text
docs/
```

Le note per pubblicazione e release sono disponibili in:

```text
docs/PUBLISHING.md
```

## Citazione

In qualsiasi materiale pubblicato che utilizzi PHOTO-CAT, includere la seguente citazione e il seguente acknowledgement.

### Riferimento

```text
<paper reference>
```

### Acknowledgement

```text
This research made use of Photo-cat, a Python package for photometric contamination analysis (<paper reference>), developed with the support of Blue Skies Space Ltd. (www.bssl.space).
```

Sostituire `<paper reference>` con il riferimento bibliografico definitivo quando disponibile.
