# PHOTO-CAT - Photometric Contamination Analyzer Tool

PHOTO-CAT is a Python-based tool for assessing photometric contamination in astronomical source catalogues. It builds a spatial neighbour index from a photometric catalogue and evaluates potential contaminating sources around a selected set of targets.

The package is intended for catalogue-level photometric analysis workflows where reproducible configuration, local execution, and clear validation of input data are required.

## Overview

PHOTO-CAT performs two main operations:

1. construction of a neighbour index from an input photometric catalogue;
2. contamination queries for target sources using the generated index.

The tool includes a graphical configurator for preparing `config.yaml`, platform launchers for local execution, and validation routines for common user-side configuration errors.

## Supported platforms

PHOTO-CAT provides launchers for:

```text
Windows       START_WINDOWS.bat
macOS/Linux   sh START_UNIX.sh
```

The launchers create a local Python virtual environment and install the required dependencies into `.venv`.

Python 3.10 or newer is required.

## Input data

PHOTO-CAT expects CSV input data.

The default catalogue schema follows Gaia-like column names:

```text
source_id
ra
dec
phot_g_mean_mag
```

The default target identifier column is:

```text
source_id
```

Column names are case-sensitive and must match the CSV header exactly. Alternative catalogue schemas can be configured through the graphical interface.

A manual list of target `source_id` values may be used instead of a targets CSV.

## Configuration

The primary configuration file is:

```text
config.yaml
```

The recommended way to edit this file is through the graphical configurator launched by the platform starter.

When a catalogue CSV is selected, PHOTO-CAT can automatically initialise the corresponding target file and output/index paths. These values remain editable before execution.

## Project structure

```text
START_WINDOWS.bat      Windows launcher
START_UNIX.sh          macOS/Linux launcher
START_HERE.txt         Minimal launch notes
config.yaml            Runtime configuration
requirements.txt       Python dependencies
data/                  Small reference input files
src/                   Source code
scripts/               Launcher support scripts
docs/                  Additional documentation
```

## Validation and error handling

PHOTO-CAT validates input files, configured column names, output locations, numeric catalogue fields, and index paths before execution where possible.

Configuration errors are reported in a user-readable form to reduce dependence on raw Python tracebacks during routine use.

## Documentation

Additional documentation is available in:

```text
docs/
```

Release and publication notes are available in:

```text
docs/PUBLISHING.md
```

## Citation

Please include the following citation and acknowledgement in any published material that makes use of PHOTO-CAT.

### Reference

```text
<paper reference>
```

### Acknowledgement

```text
This research made use of Photo-cat, a Python package for photometric contamination analysis (<paper reference>), developed with the support of Blue Skies Space Ltd. (www.bssl.space).
```

Replace `<paper reference>` with the final bibliographic reference once available.
