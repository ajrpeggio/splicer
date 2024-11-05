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

- Python 3.x
- `shutil`, `argparse`, `json`, `pathlib` libraries (included in the standard library)

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
1. **Run Script**
    ```bash
    python3 app.py --splice-dir <splice-directory> --final-dir <final-directory> [--config <config-path>] [--dryrun]
    ```

## Example Command

```bash
python3 app.py -s ~/Splice -f ~/Final
```

## Configuration

If you prefer not to specify the Splice directory in the command line, you can create a JSON configuration file (default path: /opt/splicer/config.json) with the following structure:

```bash
#!/bin/bash

# Create the directory and set ownership
mkdir -p /opt/splicer
chown $(whoami):staff /opt/splicer

# Write the config file
cat <<EOF > /opt/splicer/config.json
{
  "splice_dir": "/path/to/splice",
  "final_dir": "/path/to/final"
}
EOF

# Change ownership of the config file
chown $(whoami):staff /opt/splicer/config.json

echo "Configuration directory and file created with ownership set to $(whoami):staff"
```