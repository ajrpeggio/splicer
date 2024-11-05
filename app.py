#!/usr/bin/env python3

import shutil
import argparse
import json
from pathlib import Path
from typing import List, Optional

# List of file extensions for audio files to copy (e.g., WAV, MP3, AIFF)
audio_extensions: List[str] = [".wav", ".mp3", ".aiff"]

def get_audio_files(source: Path, extensions: List[str]) -> List[Path]:
    """
    Walks through the source directory and returns a list of audio files
    that match the specified extensions.

    Args:
        source (Path): The root directory to search for audio files.
        extensions (List[str]): A list of file extensions to look for.

    Returns:
        List[Path]: A list of file paths for the audio files found.
    """
    files_to_copy: List[Path] = []
    
    for file_path in source.rglob('*'):
        if any(file_path.suffix.lower() == ext for ext in extensions):
            files_to_copy.append(file_path)

    return files_to_copy


def file_exists_in_dir(file_path: Path, directory: Path) -> bool:
    """
    Checks if a file with the same name and size exists in the specified directory or its subdirectories.

    Args:
        file_path (Path): The path of the file to check.
        directory (Path): The directory to check within.

    Returns:
        bool: True if a matching file is found in the directory or subdirectories, False otherwise.
    """
    for existing_file in directory.rglob(file_path.name):
        if existing_file.stat().st_size == file_path.stat().st_size:
            return True
    return False


def copy_files(file_list: List[Path], destination: Path, final_dir: Optional[Path], dryrun: bool) -> None:
    """
    Copies files from the source list to the destination directory,
    skipping files that already exist in destination or final_dir and match in size.
    If dryrun is enabled, only prints the actions without actually copying.

    Args:
        file_list (List[Path]): A list of file paths to be copied.
        destination (Path): The target directory where files should be copied.
        final_dir (Optional[Path]): A directory to check for duplicates before copying.
        dryrun (bool): If True, only prints actions instead of copying files.

    Returns:
        None
    """
    if not dryrun:
        destination.mkdir(parents=True, exist_ok=True)

    for file_path in file_list:
        destination_path = destination / file_path.name

        # Check if the file exists in destination or final_dir
        if destination_path.exists() and destination_path.stat().st_size == file_path.stat().st_size:
            if dryrun:
                print(f"Skipped {file_path.name}, already exists and matches in destination.")
            continue
        if final_dir and file_exists_in_dir(file_path, final_dir):
            if dryrun:
                print(f"Skipped {file_path.name}, already exists and matches in final_dir.")
            continue

        # Copy or simulate copying the file
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
        dict: The parsed JSON configuration with keys 'splice_dir' and 'destination_dir'.
    """
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config file: {e}")
        return {}


def main(args: argparse.Namespace) -> None:
    """
    Main function to initiate the process of copying audio files
    from the Splice directory to the destination directory.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    # Load config file if paths are not provided
    if args.splice_dir is None or args.destination_dir is None:
        config = load_config(resolve_path(args.config))
        
        if args.splice_dir is None:
            args.splice_dir = config.get('splice_dir')
        
        if args.destination_dir is None:
            args.destination_dir = config.get('destination_dir')
        
        # Validate that paths are now defined
        if not args.splice_dir or not args.destination_dir:
            print("Error: Splice directory or destination directory is not specified in arguments or config file.")
            return

    # Resolve both source and destination directories to Path objects
    splice_dir = resolve_path(args.splice_dir)
    destination_dir = resolve_path(args.destination_dir)
    final_dir = resolve_path(args.final_dir) if args.final_dir else None

    # Get a list of audio files that need to be copied
    files_to_copy = get_audio_files(splice_dir, audio_extensions)

    # Copy the files to the destination directory
    copy_files(files_to_copy, destination_dir, final_dir, args.dryrun)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy audio files from Splice folder to a staging directory.")
    parser.add_argument('--splice-dir', '-s', default=None, help="The root directory where Splice downloads are saved.")
    parser.add_argument('--destination-dir', '-d', default=None, help="The staging directory where the audio files will be copied.")
    parser.add_argument('--final-dir', '-f', default=None, help="The final directory to check for duplicates before copying.")
    parser.add_argument('--config', '-c', default='/opt/splicer/config.json', help="Path to the JSON configuration file.")
    parser.add_argument('--dryrun', action='store_true', help="If set, only print the files that would be copied without performing the copy.")
    
    args = parser.parse_args()
    main(args)
