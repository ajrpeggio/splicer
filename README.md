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

- macOs
- Python 3.x

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/ajrpeggio/splicer.git
    cd splicer
    ```
    If you don't have `git` installed, you can run the following in   your terminal to install `homebrew` and `git`
    ```bash
    #!/bin/bash

    # Function to check if a command exists
    command_exists() {
        command -v "$1" >/dev/null 2>&1
    }

    # Install Homebrew if it is not already installed
    if ! command_exists brew; then
        echo "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew is already installed."
    fi

    # Add Homebrew to the PATH for the current session
    if ! command_exists brew; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi

    # Install Git if it is not already installed
    if ! command_exists git; then
        echo "Git not found. Installing Git with Homebrew..."
        brew install git
    else
        echo "Git is already installed."
    fi
    ```
1. **Run Setup Script**
This will prompt you for two (2) directories as input:
    - Splice Folder
    - Final / Desination Folder
    ```bash
    /bin/bash setup.sh
    ```
1. **Run Script**
    ```bash
    python3 app.py
    ```

## No Config Option
This script can be ran without a config file set if you use the `--splice` & `--final` arguments to pass in the folder names.

    ```bash
    python3 app.py -s ~/Splice -f ~/Final
    ```

## Configuration

If you prefer not to specify the Splice directory in the command line, you can create a JSON configuration file (default path: /opt/splicer/config.json) with the following script

    ```bash
    ./setup.sh
    ```

This will prompt you for two (2) directories as input:

- Splice Directory
- Final Directory (where files are copied to)

To which you can then invoke the script without commandline arguments

```
./app.py
```
