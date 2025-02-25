import argparse
from pathlib import Path

from visualization import manipulation
from utils import io_utils
from gpt_4.reflection import reflect_vlm, revise_task_config

def generate_images(env):
    images = manipulation.generate_images(env=env, num_images=1)
    return images

def load_simulated_image():
    path = "/home/c84399429/RoboGen/output/initial/Wash_and_Dry_Clothes/33.jpeg"
    image = io_utils.load_image(path)
    return [image]

def load_real_image():
    path = "/home/c84399429/RoboGen/data/ego4d/washing_machine.jpeg"
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

    # # Reflect with VLM
    # reflection = reflect_vlm(task="Wash and dry my clothes",
    #                          simulated_images=simulated_images,
    #                          real_images=real_images)
    reflection = """SCALE ISSUES:

1. Washing Machine: Slightly smaller in simulation | May affect spatial planning | Increase size to match real-world dimensions.
2. Detergent Bottles: Larger in simulation | Could impact user interaction | Reduce size for realistic handling.

PLACEMENT ISSUES:

1. Detergent Bottles: Positioned on the floor in simulation | Unnatural and impractical | Place on top of the washing machine.
2. Laundry Pile: Floating slightly above the floor in simulation | Unrealistic appearance | Adjust to ensure contact with the floor.

SUMMARY:
The primary issues involve the scaling of objects like the washing machine and detergent bottles, which could affect user interaction and spatial planning. Additionally, the placement of detergent bottles and laundry needs adjustment to reflect a more realistic setup. Addressing these issues will enhance the simulation's accuracy and usability.
"""

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
                        default='output/reflection',
                        help='Output directory')

    # Parse the arguments
    args = parser.parse_args()
    main(args)
