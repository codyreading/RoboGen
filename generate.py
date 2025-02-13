import argparse
import numpy as np
from pathlib import Path
from visualization import manipulation

from gpt_4.prompts.prompt_manipulation import generate_task as generate_task_manipulation
from manipulation.partnet_category import partnet_categories
from visualize import get_env, visualize

temperature_dict = {
    "task_generation": 0.6,
    "reward": 0.2,
    "yaml": 0.3,
    "size": 0.1,
    "joint": 0,
    "spatial_relationship": 0
}

model_name = "gpt-4"

model_dict = {
    "task_generation": model_name,
    "reward": model_name,
    "yaml": model_name,
    "size": model_name,
    "joint": model_name,
    "spatial_relationship": model_name
}

def create_task_configs(output_dir, category, task=None):
    all_task_config_paths = generate_task_manipulation(category,
                                                       temperature_dict=temperature_dict,
                                                       model_dict=model_dict,
                                                       meta_path="generated",
                                                       output_dir=output_dir,
                                                       task=task)
    return all_task_config_paths

def main(args):
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    task_config_paths = create_task_configs(output_dir, category=args.category, task=args.task)

    for task_config_path in task_config_paths:
        output_path = output_dir / f"{Path(task_config_path).stem}.gif"

        env = get_env(task_config_path)
        visualize(env, output_path)


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generates a scene for a given task description.")
    parser.add_argument('--task',
                        type=str,
                        help="Task description",
                        default=None)
    parser.add_argument('--category',
                        type=str,
                        help="Object category",
                        default=None)
    parser.add_argument('--env',
                        default='open_the_dishwasher_door-v0',
                        help='Environment to train on (default: open_the_dishwasher_door-v0)')
    parser.add_argument('--output_dir',
                        default='output',
                        help='Output directory')

    # Parse the arguments
    args = parser.parse_args()
    main(args)
