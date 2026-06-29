# Pipeline and output

PHOTO-CAT has two main pipeline stages.

## Stage 1: Build neighbour index

The build stage reads the catalogue, validates the configured columns, converts coordinates, and builds an index of neighbouring sources.

Generated index files are written to the configured index/output directory.
Format version 2 indexes include `index_manifest.json`, which records the
catalogue fingerprint, build radius, source count, and completion state.
Checkpoints and final files are published atomically so interrupted builds can
resume without appending uncommitted records.

Indexes built by PHOTO-CAT 1.x must be rebuilt. Version 2 does not load the
legacy pickle/object-array format. The obsolete `KDTREE_FILENAME` config key is
ignored, and the `--kdtree-filename` CLI option has been removed.

## Stage 2: Query contamination

The query stage loads the index and processes the selected targets.

For each target, PHOTO-CAT identifies neighbouring sources inside the configured field of view and applies the configured magnitude criteria.
The query is rejected if its field of view is larger than the radius represented
by the index. The extra-flux metric and contaminant list use the same field-of-view
and magnitude selection.

## Output JSON

The query stage writes a JSON result file to the configured output folder.

Each target result includes:

- target source ID
- target coordinates
- target magnitude, when available
- extra flux fraction
- number of contaminants
- contaminant source list
- contaminant coordinates, magnitudes, and separations

## Console output

The pipeline console shows:

- current pipeline stage
- progress bars
- result save path
- final target summary

The saved JSON path is highlighted in the console so it is easier to find after the run completes.
