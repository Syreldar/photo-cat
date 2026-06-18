# Layout sorgente

PHOTO-CAT usa un layout Python standard `src/`.

- `photo_cat/` contiene il pacchetto applicativo importabile.
- I nomi di pacchetti/moduli usano `snake_case` minuscolo.
- Le classi usano `PascalCase`.
- `cli.py` fornisce l’interfaccia a riga di comando unificata `photo-cat`.
- `path_policy.py` gestisce la risoluzione dei percorsi runtime non-GUI, la validazione del filesystem e la denominazione dei percorsi indice/query.
- Gli entry point per sviluppatori sono definiti in `pyproject.toml`.
- I launcher per utenti finali restano nella cartella root del progetto.

Gli utenti finali devono continuare ad avviare PHOTO-CAT con `START_WINDOWS.bat` o `START_UNIX.sh`.

## Risorse per i contributori

- [Workflow di sviluppo](../docs/Development_IT.md)
- [Contratti pubblici](../docs/Public-Contracts_IT.md)
