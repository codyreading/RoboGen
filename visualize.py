import argparse
from pathlib import Path

from visualization import manipulation

def main(args):
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    name = Path(args.task_config_path).stem
    if args.as_images:
        output_path = output_dir / name
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = output_dir /  f"{name}.gif"

    env = manipulation.get_env(args.task_config_path)
    manipulation.visualize(env, output_path, as_images=args.as_images, num_images=args.num_images)



if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generates a scene for a given task description.")
    parser.add_argument('--task_config_path',
                         type=str,
                         default="output/generated/Microwave_7349_2025-02-13-13-45-40/Close_Microwave_Door_The_robotic_arm_will_close_the_microwave_door.yaml")
    parser.add_argument('--env',
                        default='open_the_dishwasher_door-v0',
                        help='Environment to train on (default: open_the_dishwasher_door-v0)')
    parser.add_argument('--output_dir',
                        default='output/initial',
                        help='Output directory')
    parser.add_argument('--as_images',
                        action='store_true',
                        help='Output as images rather than as gif')
    parser.add_argument('--num_images',
                        type=int,
                        default=72,
                        help='Number of images in visualization')
    # Parse the arguments
    args = parser.parse_args()
    main(args)
