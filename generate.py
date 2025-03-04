import argparse
import numpy as np
from pathlib import Path
from visualization import manipulation

from gpt_4.prompts.prompt_manipulation import generate_task as generate_task_manipulation
from gpt_4.reflection import edit_task_config
from manipulation.partnet_category import partnet_categories

temperature_dict = {
    "task_generation": 0.6,
    "llm_missing_objects": 0.0,
    "vlm_missing_objects": 0.0,
    "reward": 0.2,
    "yaml": 0.3,
    "size": 0.1,
    "joint": 0,
    "spatial_relationship": 0,
    "reflection": 0.3,
    "editing": 0.3,
}

llm_name = "gpt-4"
vlm_name = "gpt-4o"

model_dict = {
    "task_generation": llm_name,
    "llm_missing_objects": llm_name,
    "vlm_missing_objects": vlm_name,
    "reward": llm_name,
    "yaml": llm_name,
    "size": llm_name,
    "joint": llm_name,
    "spatial_relationship": llm_name,
    "reflection": vlm_name,
    "editing": llm_name

}

def create_task_configs(output_dir, category, task=None, image_dir=None):
    all_task_config_paths = generate_task_manipulation(category,
                                                       temperature_dict=temperature_dict,
                                                       model_dict=model_dict,
                                                       meta_path="configs",
                                                       output_dir=output_dir,
                                                       task=task,
                                                       image_dir=image_dir)
    return all_task_config_paths


def edit_task_configs(output_dir, task_config_paths, task, image_dir, model_dict, temperature_dict):
    edited_task_config_paths = []

    for task_config_path in task_config_paths:
        edited_task_config_path = edit_task_config(output_dir=output_dir,
                                                   task_config_path=task_config_path,
                                                   task=task,
                                                   image_dir=image_dir,
                                                   model_dict=model_dict,
                                                   temperature_dict=temperature_dict)
        edited_task_config_paths.append(edited_task_config_path)

    return edited_task_config_paths

def main(args):
    output_dir = Path(args.output_dir)
    image_dir = Path(args.image_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.task_config_path is None:
        task_config_paths = create_task_configs(output_dir, category=args.category, task=args.task, image_dir=image_dir)
    else:
        task_config_paths = [args.task_config_path]

    edited_task_config_paths = edit_task_configs(output_dir=output_dir,
                                                 task_config_paths=task_config_paths,
                                                 task=args.task,
                                                 image_dir=image_dir,
                                                 model_dict=model_dict,
                                                 temperature_dict=temperature_dict)

    for task_config_path in task_config_paths:
        output_path = output_dir / f"{Path(task_config_path).stem}.gif"

        env = manipulation.get_env(task_config_path)
        manipulation.visualize(env, output_path)


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
    parser.add_argument('--task_config_path',
                        type=str,
                        help="Task config path, if you want to load an existing rather than generating one.",
                        default=None)
    parser.add_argument('--image_dir',
                        type=str,
                        help="Path to Ego4D images",
                        default="data/ego4d")
    parser.add_argument('--env',
                        default='open_the_dishwasher_door-v0',
                        help='Environment to train on (default: open_the_dishwasher_door-v0)')
    parser.add_argument('--output_dir',
                        default='output',
                        help='Output directory')

    # Parse the arguments
    args = parser.parse_args()
    main(args)
