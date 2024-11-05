#!/usr/bin/env python3
import shutil
import argparse
import json

from pathlib import Path
from typing import List, Optional, Tuple


# List of file extensions for audio files to copy (e.g., WAV, MP3, AIFF)
audio_extensions: Tuple[str] = (".wav", ".mp3", ".aiff")


def get_audio_files(source: Path, extensions: Tuple[str]) -> List[Path]:
    """
    Walks through the source directory and returns a list of audio files
    that match the specified extensions.

    Args:
        source (Path): The root directory to search for audio files.
        extensions (Tuple[str]): A list of file extensions to look for.

    Returns:
        List[Path]: A list of file paths for the audio files found.
    """
    files_to_copy: List[Path] = []

    for file_path in source.rglob("*"):
        if any(file_path.suffix.lower() == ext for ext in extensions):
            files_to_copy.append(file_path)

    return files_to_copy


def copy_files(file_list: List[Path], final_dir: Path, dryrun: bool) -> None:
    """
    Copies files from the source list to the final directory's staging directory,
    skipping files that already exist in final_dir and match in size. If dryrun is enabled,
    only prints the actions without actually copying.

    Args:
        file_list (List[Path]): A list of file paths to be copied.
        final_dir (Path): The target directory where files should be copied.
        dryrun (bool): If True, only prints actions instead of copying files.

    Returns:
        None
    """
    staging_dir = final_dir / "staging"

    if not dryrun:
        staging_dir.mkdir(parents=True, exist_ok=True)

    for file_path in file_list:
        destination_path = staging_dir / file_path.name

        # Check if the file already exists in the final_dir or its subdirectories
        if any(
            (final_dir / sub_path).exists()
            and (final_dir / sub_path).name == file_path.name
            for sub_path in final_dir.rglob("*")
        ):
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
        default="/opt/splicer/config.json",
        help="Path to the JSON configuration file.",
    )
    parser.add_argument(
        "--dryrun",
        action="store_true",
        help="If set, only print the files that would be copied without performing the copy.",
    )

    args = parser.parse_args()
    main(args)
