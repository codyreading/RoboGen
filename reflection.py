import argparse
from pathlib import Path

from visualization import manipulation
from utils import io_utils
from gpt_4.reflection import reflect_vlm, revise_task_config

def generate_images(env):
    images = manipulation.generate_images(env=env, num_images=1)
    return images

def load_simulated_image():
    path = "/home/c84399429/RoboGen/output/initial/Clean_Trash/33.jpeg"
    image = io_utils.load_image(path)
    return [image]

def load_real_image():
    path = "/home/c84399429/RoboGen/data/ego4d/Dishwasher.png"
    image = io_utils.load_image(path)
    return [image]

def main(args):
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get images
    # env = manipulation.get_env(args.task_config_path)
    # simulated_images = generate_images(env=env)
    simulated_images = load_simulated_image()
    real_images = load_real_image()

    # Reflect with VLM
    reflection = reflect_vlm(task="Clean the forks, knives, and plates using the dishwasher",
                             simulated_images=simulated_images,
                             real_images=real_images)

    # Update configs
    updated_config_path = revise_task_config(task_config_path=args.task_config_path,
                                             reflection=reflection,
                                             temperature=0.2,
                                             model="gpt-4")

    # Visualize
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir /  f"{Path(updated_config_path).stem}.gif"
    env = manipulation.get_env(updated_config_path)
    manipulation.visualize(env, output_path)


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generates a scene for a given task description.")
    parser.add_argument('--task_config_path',
                         type=str,
                         default="output/generated/WashingMachine_103490_2025-02-19-13-05-57/Wash_and_Dry_Clothes.yaml")
    parser.add_argument('--env',
                        default='open_the_dishwasher_door-v0',
                        help='Environment to train on (default: open_the_dishwasher_door-v0)')
    parser.add_argument('--output_dir',
                        default='output',
                        help='Output directory')

    # Parse the arguments
    args = parser.parse_args()
    main(args)
