import argparse
from pathlib import Path

from visualization import manipulation
from utils import io_utils

def get_env(task_config_path):
    env = manipulation.get_env(task_config_path)
    return env

def generate_images(env):
    images = manipulation.generate_images(env=env, num_images=1)
    return images

def main(args):
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    env = get_env(args.task_config_path)

    simulated_images = generate_images(env=env)
    io_utils.save_image(image=simulated_images[0], path=output_dir / "test.png")





if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generates a scene for a given task description.")
    parser.add_argument('--task_config_path',
                         type=str,
                         default="example_tasks/Adjust_Chair_Position/Adjust_Chair_Position_The_robot_arm_will_adjust_the_position_of_the_unfolded_chair.yaml")
    parser.add_argument('--env',
                        default='open_the_dishwasher_door-v0',
                        help='Environment to train on (default: open_the_dishwasher_door-v0)')
    parser.add_argument('--output_dir',
                        default='output',
                        help='Output directory')

    # Parse the arguments
    args = parser.parse_args()
    main(args)
