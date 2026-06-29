# Dati di input

PHOTO-CAT lavora con file CSV in input.

## Catalogo CSV

Il CSV catalogo è la tabella sorgente principale usata per creare l’indice dei vicini.

Le colonne attese di default sono:

- `source_id`
- `ra`
- `dec`
- `phot_g_mean_mag`

I valori `source_id` devono essere univoci anche dopo la normalizzazione numerica
(`1` e `001` sono ambigui). `ra` deve essere finito e compreso in `[0, 360)`,
`dec` in `[-90, 90]` e `phot_g_mean_mag` deve essere finito.

## CSV target

Il CSV target identifica le sorgenti da interrogare usando l’indice dei vicini creato.

La colonna identificatore target predefinita è:

- `source_id`

I valori target devono corrispondere agli ID del catalogo.

## Target manuali

PHOTO-CAT può anche usare una lista manuale di source ID target invece di un CSV target.

È utile per controlli rapidi o piccole liste di target.

## Nomi colonne

I nomi delle colonne sono case-sensitive. Devono corrispondere esattamente all’header del CSV.

Se il tuo catalogo usa nomi diversi, configurali nella configurazione grafica prima di eseguire la pipeline.

## File di esempio

La cartella `data/` include piccoli file di esempio:

- `example_catalog.csv`
- `example_targets.csv`

Servono solo a testare il workflow. Sostituiscili con cataloghi e target reali per l’analisi.
