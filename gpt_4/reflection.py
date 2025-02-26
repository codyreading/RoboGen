import yaml
from gpt_4.query import query_vlm, query
from gpt_4.parsing import reflection_parsing
from pathlib import Path

def reflect_vlm(simulated_images, real_images, task):
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
    response = query_vlm(system=system_prompt, images=images, prompt=task_prompt)
    return response

def revise_task_config(task_config_path, reflection, temperature, model):
    with open(task_config_path, 'r') as file:
        task_config = yaml.safe_load(file)

    input_config = reflection_parsing.config_to_str(task_config)
    system, prompt = reflection_parsing.get_prompt(input_config)

    revised_config = query(system,
                     user_contents=[prompt],
                     assistant_contents=[],
                     temperature=temperature,
                     model=model)

    revised_config = reflection_parsing.update_config_with_str(task_config=task_config, updated_config=revised_config)

    task_config_path = Path(task_config_path)
    revised_task_config_path = task_config_path.with_name(task_config_path.stem + "_revised" + task_config_path.suffix)
    with open(revised_task_config_path, 'w') as f:
        yaml.dump(revised_config, f, indent=4)

    return revised_task_config_path