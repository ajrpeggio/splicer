#!/usr/bin/env python3
import shutil
import argparse
import json
import sys
import logging
import os

from pathlib import Path
from typing import Optional, Tuple
import platform

# Set up the logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# List of file extensions for audio files to copy (e.g., WAV, MP3, AIFF)
audio_extensions = (".wav", ".mp3", ".aiff")


def get_audio_files(source: Path, extensions: Tuple[str]) -> list[Path]:
    """
    Recursively retrieves audio files with specific extensions from the source directory.

    Args:
        source (Path): The directory to search for audio files.
        extensions (Tuple[str]): File extensions to filter for audio files.

    Returns:
        list[Path]: List of file paths that match the specified audio extensions.
    """
    extensions_set = {ext.lower() for ext in extensions}
    return [
        file_path
        for file_path in source.rglob("*")
        if file_path.suffix.lower() in extensions_set
    ]


def copy_files(file_list: list[Path], final_dir: Path, dryrun: bool) -> None:
    """
    Copies files from a list to the staging directory within the final directory.
    Skips files if they already exist with the same size.

    Args:
        file_list (list[Path]): List of file paths to be copied.
        final_dir (Path): The final destination directory.
        dryrun (bool): If True, only prints the actions without copying.

    Returns:
        None
    """
    staging_dir = final_dir / "staging"
    if not dryrun:
        staging_dir.mkdir(parents=True, exist_ok=True)

    existing_files = {file.name: file for file in final_dir.rglob("*") if file.is_file()}

    for file_path in file_list:
        destination_path = staging_dir / file_path.name

        if file_path.name in existing_files:
            if dryrun:
                log.info(f"Skipped {file_path.name}, already exists in final directory.")
            continue

        if destination_path.exists():
            source_size = file_path.stat().st_size
            dest_size = destination_path.stat().st_size

            if source_size == dest_size:
                if dryrun:
                    log.info(
                        f"Skipped {file_path.name}, already exists in staging and matches."
                    )
                continue
            else:
                log.info(f"Overwriting {file_path.name}, different size in staging.")

        if dryrun:
            log.info(f"Would copy {file_path.name} to {destination_path}")
        else:
            shutil.copy2(file_path, destination_path)
            log.info(f"Copied {file_path.name} to {destination_path}")


def resolve_path(path: Optional[str]) -> Optional[Path]:
    """
    Expands and resolves the given path string to an absolute Path object.

    Args:
        path (Optional[str]): The path to resolve.

    Returns:
        Optional[Path]: The resolved Path object or None if input is None.
    """
    if path is None:
        return None
    return Path(path).expanduser().resolve()


def create_config(config_path: Path) -> None:
    """
    Creates a JSON configuration file with user-provided paths for 'splice' and 'final' directories.

    Args:
        config_path (Path): The path where the configuration file will be created.

    Returns:
        None
    """
    config_path.parent.mkdir(parents=True, exist_ok=True)
    splice = input("Enter the Splice directory path: ")
    final = input("Enter the Final directory path: ")

    config_data = {"splice": splice, "final": final}

    with open(config_path, "w") as config_file:
        json.dump(config_data, config_file, indent=4)

    log.info(f"Configuration file created at {config_path} with the following values:")
    log.info(f"Splice Folder: {splice}")
    log.info(f"Final / Destination Folder: {final}")


def load_config(config_path: Path) -> dict:
    """
    Loads a JSON configuration file if it exists.

    Args:
        config_path (Path): The path to the configuration file.

    Returns:
        dict: Dictionary with configuration data, empty if file not found or invalid.
    """
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log.error(f"Error loading config file: {e}")
        return {}


def main(args: argparse.Namespace) -> None:
    """
    Main function to handle argument parsing, config loading, and file copying.

    Args:
        args (argparse.Namespace): Parsed arguments from the command line.

    Returns:
        None
    """
    _config = args.config
    if not args.config:
        # Determine default config path based on operating system
        if platform.system() == "Windows":
            _config = Path(os.getenv("APPDATA", "~")) / "splicer" / "config"
        else:
            _config = Path("~/.splicer/config").expanduser()
    config_path = resolve_path(_config)

    if not config_path.exists() or args.reconfigure:
        create_config(config_path)

    config = load_config(config_path)

    splice = config.get("splice")
    final = config.get("final")

    if not splice or not final:
        log.error(
            "Error: Splice directory or final directory is not specified in arguments or config file."
        )
        return

    splice_dir = resolve_path(splice)
    final_dir = resolve_path(final)

    if not final_dir.exists():
        log.info(f"Creating final directory: {final_dir}")
        final_dir.mkdir(parents=True, exist_ok=True)

    files_to_copy = get_audio_files(splice_dir, audio_extensions)
    copy_files(files_to_copy, final_dir, args.dryrun)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy audio files from Splice folder to a final directory's staging directory."
    )
    parser.add_argument(
        "--config",
        "-c",
        default=None,
        help="Path to the JSON configuration file.",
    )
    parser.add_argument(
        "--reconfigure",
        action="store_true",
        help="If set, only print the files that would be copied without performing the copy.",
    )
    parser.add_argument(
        "--dryrun",
        action="store_true",
        help="If set, only print the files that would be copied without performing the copy.",
    )
    args = parser.parse_args()
    try:
        main(args)
    except RuntimeError as e:
        log.error(e)
        sys.exit(1)
