
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from visualization import manipulation

def find_first_directory_starting_with(parent_dir, prefix):
    """
    Find the first subdirectory under parent_dir that starts with the given prefix.

    Args:
        parent_dir (str or Path): The parent directory to search in
        prefix (str): The prefix to match directory names against

    Returns:
        Path or None: Path object for the first matching directory, or None if no match is found
    """
    parent_path = Path(parent_dir)

    # Check if the parent directory exists
    if not parent_path.exists() or not parent_path.is_dir():
        raise ValueError(f"The specified path '{parent_dir}' is not a valid directory")

    # Find the first subdirectory that starts with the prefix
    for p in parent_path.iterdir():
        if p.is_dir() and p.name.startswith(prefix):
            return p

    # Return None if no matching directory is found
    return None

    return matching_dirs

def main(args):
    output_dir = Path(args.output_dir)

    config_dir = find_first_directory_starting_with(args.config_dir, prefix=args.category)
    config_paths = list(config_dir.glob("*.yaml"))

    if args.single_thread:
        for config_path in config_paths:
            manipulation.visualize(config_path=config_path, output_dir=output_dir)
    else:
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Submit all tasks to the executor
            futures = [
                executor.submit(
                    manipulation.visualize,
                    config_path=config_path,
                    output_dir=output_dir,
                )
                for config_path in config_paths
            ]

            # Wait for all futures to complete
            for future in futures:
                future.result()  # This will re-raise any exceptions that occurred

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generates a scene for a given task description.")
    parser.add_argument('--config_dir',
                         type=str,
                         default="output/config")
    parser.add_argument('--category',
                        type=str,
                        default="WashingMachine")
    parser.add_argument('--env',
                        default='open_the_dishwasher_door-v0',
                        help='Environment to train on (default: open_the_dishwasher_door-v0)')
    parser.add_argument('--output_dir',
                        default='output',
                        help='Output directory')
    parser.add_argument('--single_thread',
                        action="store_true",
                        help='Only run in a single thread')
    # Parse the arguments
    args = parser.parse_args()
    main(args)
