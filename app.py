#!/usr/bin/env python3
import shutil
import argparse
import json
import sys

from pathlib import Path
from typing import List, Optional, Tuple


# List of file extensions for audio files to copy (e.g., WAV, MP3, AIFF)
audio_extensions = (".wav", ".mp3", ".aiff")


def get_audio_files(source: Path, extensions: Tuple[str]) -> List[Path]:
    """
    Recursively retrieves a list of audio files from the specified source directory
    that match the given file extensions.

    Args:
        source (Path): The root directory to search for audio files.
        extensions (Tuple[str]): A tuple of file extensions to look for, e.g., (".wav", ".mp3").

    Returns:
        List[Path]: A list of Path objects representing the audio files found in the source directory.
    """
    extensions_set = {ext.lower() for ext in extensions}
    return [
        file_path
        for file_path in source.rglob("*")
        if file_path.suffix.lower() in extensions_set
    ]


def copy_files(file_list: List[Path], final_dir: Path, dryrun: bool) -> None:
    """
    Copies audio files from the provided list to the final directory's staging subdirectory.
    Skips files that already exist in the final directory and match in size. If dryrun is enabled,
    only prints the actions without actually copying files.

    Args:
        file_list (List[Path]): A list of Path objects representing the audio files to be copied.
        final_dir (Path): The target directory where files should be copied, which contains a "staging" subdirectory.
        dryrun (bool): If True, only prints the actions that would be taken without performing the copy.

    Returns:
        None: This function does not return any value. It performs file copy operations.
    """
    staging_dir = final_dir / "staging"
    if not dryrun:
        staging_dir.mkdir(parents=True, exist_ok=True)

    existing_files = {
        file.name: file for file in final_dir.rglob("*") if file.is_file()
    }

    for file_path in file_list:
        destination_path = staging_dir / file_path.name

        # Check if the file already exists in existing_files
        if file_path.name in existing_files:
            if dryrun:
                print(f"Skipped {file_path.name}, already exists in final directory.")
            continue

        if destination_path.exists():
            source_size = file_path.stat().st_size
            dest_size = destination_path.stat().st_size

            if source_size == dest_size:
                if dryrun:
                    print(
                        f"Skipped {file_path.name}, already exists in staging and matches."
                    )
                continue
            else:
                print(f"Overwriting {file_path.name}, different size in staging.")

        if dryrun:
            print(f"Would copy {file_path.name} to {destination_path}")
        else:
            shutil.copy2(file_path, destination_path)
            print(f"Copied {file_path.name} to {destination_path}")


def resolve_path(path: Optional[str]) -> Optional[Path]:
    """
    Resolves a given path by expanding ~ to the home directory if present,
    otherwise converts it to an absolute path. If None, returns None.

    Args:
        path (Optional[str]): The path to resolve.

    Returns:
        Optional[Path]: The resolved absolute path, or None if input is None.
    """
    if path is None:
        return None
    return Path(path).expanduser().resolve()


def load_config(config_path: Path) -> dict:
    """
    Loads configuration from a JSON file.

    Args:
        config_path (Path): The path to the configuration file.

    Returns:
        dict: The parsed JSON configuration with key 'splice_dir'.
    """
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config file: {e}")
        return {}


def main(args: argparse.Namespace) -> None:
    """
    Main function to initiate the process of copying audio files
    from the Splice directory to the final directory's staging directory.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    # Load config file if paths are not provided
    if args.splice is None or args.final is None:
        config = load_config(resolve_path(args.config))

        if args.splice is None:
            args.splice = config.get("splice")

        if args.final is None:
            args.final = config.get("final")

        # Validate that paths are now defined
        if not args.splice or not args.final:
            print(
                "Error: Splice directory or final directory is not specified in arguments or config file."
            )
            return

    # Resolve both source and destination directories to Path objects
    splice_dir = resolve_path(args.splice)
    final_dir = resolve_path(args.final)

    # Create the final directory if it doesn't exist
    if not final_dir.exists():
        print(f"Creating final directory: {final_dir}")
        final_dir.mkdir(parents=True, exist_ok=True)

    # Get a list of audio files that need to be copied
    files_to_copy = get_audio_files(splice_dir, audio_extensions)

    # Copy the files to the final directory's staging directory
    copy_files(files_to_copy, final_dir, args.dryrun)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy audio files from Splice folder to a final directory's staging directory."
    )
    parser.add_argument(
        "--splice",
        "-s",
        default=None,
        help="The root directory where Splice downloads are saved.",
    )
    parser.add_argument(
        "--final",
        "-f",
        default=None,
        help="The final directory where the audio files will be moved to.",
    )
    parser.add_argument(
        "--config",
        "-c",
        default="~/.splicer/config",
        help="Path to the JSON configuration file.",
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
        print(e)
        sys.exit(1)
