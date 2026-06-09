# Pipeline e output

PHOTO-CAT ha due fasi principali di pipeline.

## Fase 1: creazione indice dei vicini

La fase di build legge il catalogo, valida le colonne configurate, converte le coordinate e crea un indice delle sorgenti vicine.

I file indice generati vengono scritti nella cartella indice/output configurata.

## Fase 2: query contaminazione

La fase di query carica l’indice e processa i target selezionati.

Per ogni target, PHOTO-CAT identifica le sorgenti vicine dentro il campo di vista configurato e applica i criteri di magnitudine configurati.

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
