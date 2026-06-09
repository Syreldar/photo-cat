# Layout sorgente

PHOTO-CAT usa un layout Python standard `src/`.

- `photo_cat/` contiene il pacchetto applicativo importabile.
- I nomi di pacchetti/moduli usano `snake_case` minuscolo.
- Le classi usano `PascalCase`.
- Gli entry point per sviluppatori sono definiti in `pyproject.toml`.
- I launcher per utenti finali restano nella cartella root del progetto.

Gli utenti finali devono continuare ad avviare PHOTO-CAT con `START_WINDOWS.bat` o `START_UNIX.sh`.
