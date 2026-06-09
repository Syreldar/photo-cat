# Pubblicazione PHOTO-CAT

Questa pagina è per i manutentori che preparano una release GitHub.

## Test locale finale

Prima di pubblicare una release, testa il progetto da una cartella estratta pulita.

Windows:

`START_WINDOWS.bat`

macOS/Linux:

`sh START_UNIX.sh`

Conferma che:

1. il setup parta correttamente
2. venga selezionato un Python supportato oppure il runtime locale
3. `.venv/` venga creato o riutilizzato in sicurezza
4. le dipendenze vengano controllate o installate
5. la configurazione grafica si apra
6. `Save + run` avvii la pipeline
7. i dati di esempio completino correttamente
8. percorsi di output e riepiloghi siano leggibili

## File da non committare

Non committare runtime generati o file di output:

- `.venv/`
- `.runtime/`
- `__pycache__/`
- `*.pyc`
- `logs/`
- `output/`
- `data/output/`
- `.env`
- dataset privati
- credenziali o token

## File da non includere negli ZIP release

Non includere cartelle repository, duplicate o generate negli archivi release:

- `.git/`
- `.venv/`
- `.runtime/`
- `logs/`
- `output/`
- `data/output/`
- `__pycache__/`
- `docs/wiki/`

La documentazione canonica vive in `docs/`. Le pagine GitHub Wiki, se usate, appartengono al repository Wiki separato di GitHub.

## Descrizione repository

Descrizione consigliata:

`Photometric Contamination Analyzer Tool with local runtime setup and beginner-friendly launchers.`

Topic consigliati:

`python`, `astronomy`, `photometry`, `catalogue`, `csv`, `gui`, `contamination`, `gaia`

## Checklist release

1. Aggiorna `VERSION`.
2. Aggiorna `pyproject.toml` alla stessa versione.
3. Conferma che `LICENSE` contenga il testo completo della licenza GPL-3.0.
4. Conferma che `pyproject.toml` dichiari `GPL-3.0-only`.
5. Conferma che header SPDX e `REUSE.toml` siano aggiornati.
6. Prepara le note di rilascio GitHub.
7. Testa il flusso launcher su Windows.
8. Testa il flusso launcher su macOS/Linux dove possibile.
9. Testa catalogo e target di esempio.
10. Conferma che cartelle generate, `.git/` e `docs/wiki/` siano escluse dall’archivio release.
11. Crea un archivio release pulito.
12. Pubblica la release GitHub.

## Formato titolo release

Usa:

`PHOTO-CAT vX.Y.Z`

## Formato asset release

Nome asset release consigliato:

`photo-cat-vX.Y.Z.zip`

Uno ZIP con nome esplicito è più semplice per utenti non tecnici rispetto ai soli archivi automatici del codice sorgente di GitHub.
