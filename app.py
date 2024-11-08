#!/usr/bin/env python3
import argparse
import concurrent.futures
import json
import logging
import os
import platform
import shutil
import sys
import time

from pathlib import Path
from typing import Optional, Tuple

# Set up the logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# List of file extensions for audio files to copy (e.g., WAV, MP3, AIFF, FLAC, OGG, M4A)
audio_extensions = (".wav", ".mp3", ".aiff", ".flac", ".ogg", ".m4a")


def get_audio_files(source: Path, extensions: Tuple[str]) -> list[Path]:
    """
    Recursively get all audio files with the specified extensions from a source directory.

    Args:
        source (Path): The source directory where audio files are located.
        extensions (Tuple[str]): A tuple of file extensions to match.

    Returns:
        list[Path]: A list of Path objects representing the audio files found.
    """
    extensions_set = {ext.lower() for ext in extensions}
    return [
        file_path
        for file_path in source.rglob("*")
        if file_path.suffix.lower() in extensions_set
    ]


def copy_single_file(
    file_path: Path, staging_dir: Path, dryrun: bool, verbose: bool, stats: dict
) -> None:
    """
    Copies a single audio file to the final directory’s staging folder, with checks for file existence and size.

    Args:
        file_path (Path): The path to the source audio file.
        final_dir (Path): The target directory where the file should be copied.
        dryrun (bool): If True, the file copy is simulated, and no files are actually copied.
        verbose (bool): If True, log entries for skipped files are shown.
        stats (dict): A dictionary to track the number of copied and skipped files.
    """
    destination_path = staging_dir / file_path.name

    # Check if the file already exists and matches size
    if (
        destination_path.exists()
        and destination_path.stat().st_size == file_path.stat().st_size
    ):
        if verbose:
            log.info(f"Skipped {file_path.name}, already exists with matching size.")
        stats["skipped"] += 1
        return

    # Perform dry run or actual copy
    try:
        if dryrun:
            log.info(f"Dry Run: Would copy {file_path.name}")
        else:
            shutil.copy2(file_path, destination_path)
            log.info(f"Copied {file_path.name}")
        stats["copied"] += 1
    except IOError as e:
        log.error(f"Failed to copy {file_path.name}: {e}")
        stats["skipped"] += 1


def copy_files(
    file_list: list[Path],
    final_dir: Path,
    dryrun: bool,
    max_threads: int,
    verbose: bool,
) -> None:
    """
    Copies a list of files to the final directory, using parallelization if enabled.

    Args:
        file_list (list[Path]): The list of file paths to copy.
        final_dir (Path): The target directory where the files should be copied.
        dryrun (bool): If True, the file copy is simulated.
        parallel (bool): If True, files will be copied in parallel.
        max_threads (int): The maximum number of threads to use for parallel copying.
        verbose (bool): If True, log entries for skipped files are shown.
    """
    staging_dir = final_dir / "staging"
    staging_dir.mkdir(parents=True, exist_ok=True)
    stats = {"skipped": 0, "copied": 0}
    start_time = time.time()  # Start timer
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(
                copy_single_file, file_path, staging_dir, dryrun, verbose, stats
            )
            for file_path in file_list
        ]
        # Wait for all threads to complete
        concurrent.futures.wait(futures)

    elapsed_time = time.time() - start_time  # Calculate elapsed time
    log.info(f"Copy Summary: {stats}")
    log.info(f"Total time taken: {elapsed_time:.2f} seconds.")

def resolve_path(path: Optional[str]) -> Optional[Path]:
    """
    Resolves a given path to an absolute path, expanding user directories.

    Args:
        path (Optional[str]): The path to resolve. If None, returns None.

    Returns:
        Optional[Path]: The resolved absolute path or None if the input is None.
    """
    if path is None:
        return None
    return Path(path).expanduser().resolve()


def create_config(config_path: Path) -> None:
    """
    Creates a new configuration file by prompting the user for input.

    Args:
        config_path (Path): The path where the configuration file should be saved.
    """
    config_path.parent.mkdir(parents=True, exist_ok=True)
    splice = input("Enter the Splice directory path: ")
    final = input("Enter the Final directory path: ")

    config_data = {"splice": splice, "final": final}

    with open(config_path, "w") as config_file:
        json.dump(config_data, config_file, indent=4)

    log.info(f"Configuration file created at {config_path}.")


def load_config(config_path: Path) -> dict:
    """
    Loads the configuration data from a JSON file.

    Args:
        config_path (Path): The path to the configuration file.

    Returns:
        dict: The configuration data as a dictionary.
    """
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log.error(f"Error loading config file: {e}")
        return {}


def platform_config() -> Path:
    # Determine default config path based on OS
    if platform.system() == "Windows":
        appdata_path = os.getenv("APPDATA")
        if appdata_path:
            config = Path(appdata_path) / "splicer" / "config"
        else:
            log.warning("APPDATA environment variable not found on Windows.")
            log.warning("Using home directory for configuration file.")
            config = Path.home() / "splicer" / "config"
    else:
        config = Path("~/.splicer/config").expanduser()
    return config


def main(args: argparse.Namespace) -> None:
    """
    Main function to handle the execution of the file copying operation, including configuration loading,
    file discovery, and copying (with optional parallelization).

    Args:
        args (argparse.Namespace): The arguments parsed from the command line.
    """
    _config = args.config
    if not _config:
        _config = platform_config()
    config_path = resolve_path(_config)

    if not config_path.exists() or args.reconfigure:
        create_config(config_path)

    config = load_config(config_path)

    splice = config.get("splice")
    final = config.get("final")

    if not splice or not final:
        log.error("Splice directory or final directory is not specified.")
        return

    splice_dir = resolve_path(splice)
    final_dir = resolve_path(final)

    if not final_dir.exists():
        log.info(f"Creating final directory: {final_dir}")
        final_dir.mkdir(parents=True, exist_ok=True)

    files_to_copy = get_audio_files(splice_dir, audio_extensions)

    # Determine max_threads based on the system CPU cores or user input
    try:
        max_threads = int(args.max_threads) if args.max_threads else min(os.cpu_count(), 8)
        if max_threads <= 0:
            raise ValueError("Maximum number of threads must be a positive integer.")
    except ValueError as e:
        log.error(f"Invalid value for max-threads: {e}")
        sys.exit(1)
    
    log.info(f"Using up to {max_threads} threads for parallel file copying.")

    copy_files(
        files_to_copy, final_dir, args.dryrun, max_threads, args.verbose
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy audio files from Splice folder to a final directory's staging directory."
    )
    parser.add_argument(
        "--config", "-c", default=None, help="Path to the JSON configuration file."
    )
    parser.add_argument(
        "--reconfigure", action="store_true", help="Recreate the configuration file."
    )
    parser.add_argument(
        "--dryrun",
        action="store_true",
        help="Only print the files that would be copied.",
    )
    parser.add_argument(
        "--max-threads",
        type=int,
        default=None,
        help="Maximum number of threads for parallel processing.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging, including skipped file entries.",
    )
    args = parser.parse_args()
    try:
        main(args)
    except RuntimeError as e:
        log.error(e)
        sys.exit(1)
