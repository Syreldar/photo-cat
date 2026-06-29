# Pipeline e output

PHOTO-CAT ha due fasi principali di pipeline.

## Fase 1: creazione indice dei vicini

La fase di build legge il catalogo, valida le colonne configurate, converte le coordinate e crea un indice delle sorgenti vicine.

I file indice generati vengono scritti nella cartella indice/output configurata.
Gli indici in formato versione 2 includono `index_manifest.json`, che registra
l'impronta del catalogo, il raggio di build, il numero di sorgenti e lo stato di
completamento. Checkpoint e file finali vengono pubblicati in modo atomico.

Gli indici creati con PHOTO-CAT 1.x devono essere ricostruiti. La versione 2 non
carica il precedente formato pickle/object-array. La chiave config obsoleta
`KDTREE_FILENAME` viene ignorata e l'opzione CLI `--kdtree-filename` è stata rimossa.

## Fase 2: query contaminazione

La fase di query carica l’indice e processa i target selezionati.

Per ogni target, PHOTO-CAT identifica le sorgenti vicine dentro il campo di vista configurato e applica i criteri di magnitudine configurati.
La query viene rifiutata se il campo di vista supera il raggio rappresentato
dall'indice. Il flusso extra e l'elenco dei contaminanti usano gli stessi filtri.

## Output JSON

La fase di query scrive un file risultato JSON nella cartella di output configurata.

Ogni risultato target include:

- source ID del target
- coordinate del target
- magnitudine del target, quando disponibile
- frazione di flusso extra
- numero di contaminanti
- lista delle sorgenti contaminanti
- coordinate, magnitudini e separazioni dei contaminanti

## Output console

La console della pipeline mostra:

- fase corrente della pipeline
- barre di progresso
- percorso di salvataggio del risultato
- riepilogo finale dei target

Il percorso del JSON salvato è evidenziato nella console, così è più facile trovarlo dopo il completamento dell’esecuzione.
