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

- macOS
- Python 3.x

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/ajrpeggio/splicer.git
    cd splicer
    ```

1. **Run Script**

    ```bash
    python3 app.py
    ```

Once you run the command `python3 app.py`, you will be prompted to fill in two values:

- Splice Folder
- Final / Desintination Folder

## Reconfigure

If you need to reconfigure the folder locations, you can do so by running the app with a --reconfigure flag like so:

    ```bash
    python3 app.py --reconfigure
    ```
