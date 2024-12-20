# Splicer - Audio File Copy Script

## Overview

This Python script is designed to copy audio files from a specified Splice download directory to a designated final directory's staging directory. It efficiently checks for duplicate files, ensuring that only new or modified files are copied, thereby maintaining an organized audio library.

## Features

- Recursively searches for audio files in the specified Splice directory.
- Copies supported audio file formats: `.wav`, `.mp3`, `.aiff`.
- Creates a "staging" directory inside the final directory if it does not exist.
- Skips files that already exist in the final directory and its subdirectories, or that match in size.
- Provides a dry run option to preview actions without making any changes.

## Requirements

- macOS / Windows
- Python 3.x

## Installation

From your terminal / commandline, perform the following steps the following:

1. **Install CLI from Pypi**

    ```bash
    pip install splicer-cli
    ```

1. **Run App**

    ```bash
    splicer --help
    ```

Once you run the command `splicer`, you will be prompted to fill in two values:

- Splice Folder
- Final / Desintination Folder

## Reconfigure

If you need to reconfigure the folder locations, you can do so by running the app with a --reconfigure flag like so:

```bash
splicer --reconfigure
```
