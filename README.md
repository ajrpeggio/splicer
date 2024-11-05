# Audio File Copying Script

This script is designed to copy audio files from a specified Splice download directory to a staging directory. It checks for duplicates in both the staging directory and a designated final directory to avoid unnecessary copying.

## Features

- Recursively searches for audio files with specified extensions in the Splice directory.
- Copies audio files to a specified destination directory.
- Skips files that already exist in the destination or final directory with matching sizes.
- Supports a dry run mode to preview actions without performing any file operations.
- Configuration options can be specified via command-line arguments or a JSON configuration file.

## Requirements

- Python 3.x
- The following standard libraries:
  - `shutil`
  - `argparse`
  - `json`
  - `pathlib`
  - `typing`

## Installation

1. Clone this repository or download the script file.
2. Ensure you have Python 3 installed on your system.

## Usage

### Command-Line Arguments

```bash
python3 audio_file_copy.py --splice-dir <splice_directory> --destination-dir <destination_directory> --final-dir <final_directory> [--config <config_file>] [--dryrun]

