import argparse
from pathlib import Path

from visualization import manipulation
from utils import io_utils
from gpt_4.reflection import reflect_vlm, revise_task_config

def generate_images(env):
    images = manipulation.generate_images(env=env, num_images=1)
    return images

def load_simulated_image():
    path = "output/initial/Write_Smiley_Face/64.jpeg"
    image = io_utils.load_image(path)
    return [image]

def load_real_image():
    path = "output/reflection/Pen_on_paper.jpg"
    image = io_utils.load_image(path)
    return [image]

def main(args):
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get images
    # env = manipulation.get_env(args.task_config_path)
    # simulated_images = generate_images(env=env)
    # simulated_images = load_simulated_image()
    # real_images = load_real_image()

    # # Reflect with VLM
    # reflection = reflect_vlm(task="Write smiley face on a piece of paper",
    #                          simulated_images=simulated_images,
    #                          real_images=real_images)

    reflection = """
### 1. SIZE ISSUES

- **Pen**: **Too small** -> The pen appears undersized compared to the paper and the surface. -> **Fix needed**: Increase the size of the pen to better match typical pens.
- **Paper**: **Too big** -> The paper looks oversized compared to the pen. -> **Fix needed**: Resize the paper to a more standard size relative to the pen.

### 2. PLACEMENT ISSUES

- **Pen**: **Unnatural position** -> The pen is positioned awkwardly and may be seen as floating off the paper. -> **Fix needed**: Adjust the position of the pen to be placed directly on top of the paper.
- **Paper**: **Incorrectly placed** -> The paper seems misaligned or not centered on the surface. -> **Fix needed**: Center the paper on the surface to provide a more natural look for writing.


### Summary of Issues

- **Pen**: Too small -> Impact on task: Hard to write with -> Fix needed: Increase size.
- **Paper**: Too big -> Impact on task: Disproportionate for writing -> Fix needed: Resize paper.
- **Pen**: Unnatural position -> Impact on task: Not functional -> Fix needed: Place on paper.
- **Paper**: Incorrectly placed -> Impact on task: Unnatural scene -> Fix needed: Center paper.
"""

    # Update configs
    updated_config_path = revise_task_config(task_config_path=args.task_config_path,
                                             reflection=reflection,
                                             temperature=0.3,
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
                         default="output/generated/Pen_102942_2025-02-19-21-43-44/Write_Smiley_Face.yaml")
    parser.add_argument('--env',
                        default='open_the_dishwasher_door-v0',
                        help='Environment to train on (default: open_the_dishwasher_door-v0)')
    parser.add_argument('--output_dir',
                        default='output/reflection',
                        help='Output directory')

    # Parse the arguments
    args = parser.parse_args()
    main(args)
