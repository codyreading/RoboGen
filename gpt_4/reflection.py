import yaml
from gpt_4.query import query_vlm, query
from gpt_4.parsing import reflection_parsing
from pathlib import Path
from utils import io_utils
from visualization import manipulation


def get_simulated_image(task_config_path, azimuth=165):
    env = manipulation.get_env(task_config_path)
    image = manipulation.visualize_image(env=env, azimuth=azimuth)

    # Save image
    image_path = Path(task_config_path).parents[0] / "simulated.png"
    io_utils.save_image(image=image, path=image_path)
    return image

def get_real_image(category, image_dir):
    image_path = image_dir / f"{category}.png"
    image = io_utils.load_image(image_path)
    return image

def reflect_vlm(simulated_images, real_images, task, temperature, model):
    system_prompt = """You are a computer vision expert specializing in analyzing differences between simulation and real-world environments. Your strength lies in precise object analysis and clear, structured feedback."""

    task_prompt = """In the two images provided:
- First image: A simulation environment
- Second image: A real-world reference

For the task: {task}

Analyze and report:

1. Object Scale Analysis
- Compare the relative sizes of all visible objects
- Flag any objects with incorrect scaling (too large/small)
- Focus on proportions between interacting objects

2. Object Placement Check
- Identify objects in physically impossible or unrealistic positions
- Check object-surface relationships and contact points
- Note any unnatural spatial arrangements

Format your response as:

SCALE ISSUES:
[Object name]: [Scale discrepancy] | [Task impact] | [Recommended fix]

PLACEMENT ISSUES:
[Object name]: [Position issue] | [Task impact] | [Recommended fix]

SUMMARY:
Brief overview of the most critical issues for task success."""

    images = simulated_images + real_images
    response = query_vlm(system=system_prompt, images=images, prompt=task_prompt, temperature=temperature, model=model)
    return response

def revise_task_config_from_reflection(task_config_path, reflection, temperature, model):
    with open(task_config_path, 'r') as file:
        task_config = yaml.safe_load(file)

    input_config = reflection_parsing.config_to_str(task_config)
    system, prompt = reflection_parsing.get_prompt(input_config, reflection=reflection)

    editing_operations = query(
        system,
        user_contents=[prompt],
        assistant_contents=[],
        temperature=temperature,
        model=model
    )

    revised_config = reflection_parsing.update_config_with_str(task_config=task_config, editing_operations=editing_operations)

    task_config_path = Path(task_config_path)
    revised_task_config_path = task_config_path.with_name(task_config_path.stem + "_edited" + task_config_path.suffix)
    with open(revised_task_config_path, 'w') as f:
        yaml.dump(revised_config, f, indent=4)

    return revised_task_config_path


def reflect_task_config(output_dir, task_config_path, category, task, image_dir, model_dict, temperature_dict):
    # Get images
    simulated_image = get_simulated_image(task_config_path)
    real_image = get_real_image(category=category, image_dir=image_dir)

    # Reflect with VLM
    reflection = reflect_vlm(task=task,
                             simulated_images=[simulated_image],
                             real_images=[real_image],
                             temperature=temperature_dict["reflection"],
                             model=model_dict["reflection"])

    # Save reflection
    reflection_path = Path(task_config_path).parents[0] / "reflection.txt"
    with open(reflection_path, "w") as file:
        file.write(reflection)


    # Update configs
    updated_config_path = revise_task_config_from_reflection(
        task_config_path=task_config_path,
        reflection=reflection,
        temperature=temperature_dict["editing"],
        model=model_dict["editing"]
    )
    return updated_config_path