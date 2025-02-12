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
    output_path = output_dir / "scene.gif"

    env = get_env(args.task_config_path)
    visualize(env, output_path)



if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generates a scene for a given task description.")
    parser.add_argument('--task_config_path',
                         type=str,
                         default="/home/c84399429/Projects/RoboGen/data/generated_tasks_release/Fan_101494_2025-02-11-15-22-51/Adjust_Fan_Speed_The_robotic_arm_will_interact_with_the_speed_control_knob_assumed_to_be_on_the_fan_frame_to_adjust_the_speed_of_the_fan.yaml")
    parser.add_argument('--env',
                        default='open_the_dishwasher_door-v0',
                        help='Environment to train on (default: open_the_dishwasher_door-v0)')
    parser.add_argument('--output_dir',
                        default='output',
                        help='Output directory')

    # Parse the arguments
    args = parser.parse_args()
    main(args)
