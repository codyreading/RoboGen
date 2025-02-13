import argparse
from pathlib import Path

from visualization import manipulation

def get_env(task_config_path):
    env = manipulation.get_env(task_config_path)
    return env

def visualize(env, output_path):
    manipulation.visualize(env, output_path)

def main(args):
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir /  f"{Path(args.task_config_path).stem}.gif"

    env = get_env(args.task_config_path)
    visualize(env, output_path)



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
