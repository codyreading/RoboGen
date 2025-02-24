import yaml
import re
from gpt_4.query import query_vlm, query
from pathlib import Path

def reflect_vlm(simulated_images, real_images, task):
    system_prompt = """You are an expert at comparing simulation and real-world images. Your task is to spot differences in object properties."""

    task_prompt = f"""IN IMAGE 1 (Simulation) and IMAGE 2 (Real World), analyze the scene for this task: {task}

Examine and list:
1. SIZE ISSUES
- Which objects are too big/small?
- Do size ratios between objects match?

2. PLACEMENT ISSUES
- Which objects are in unnatural positions?
- Are objects floating or incorrectly placed?


List each issue as:
[Object]: [Problem] -> [Impact on task] -> [Fix needed]"""

    images = simulated_images + real_images
    response = query_vlm(system=system_prompt, images=simulated_images, prompt=task_prompt)
    return response

def revise_task_config(task_config_path, reflection, temperature, model):
    with open(task_config_path, 'r') as file:
        task_config = yaml.safe_load(file)

    objects = []
    task_name = None
    task_description = None
    for config in task_config:
        if "task_name" in config:
            task_name = config["task_name"]
        if "task_description" in config:
            task_description = config["task_description"]
        if "center" in config:
            obj_config = {
                "name": config["name"],
                "center": config["center"],
                "size": config["size"]
            }
            objects.append(obj_config)

    system = """
You are a highly skilled robotic simulator assistant.
Your task is to revise 3D scene configurations based on the task requirements and any diagnosis provided. You should focus on adjusting object positions, ensuring they make sense according to the task description, and fixing any other issues outlined in the diagnosis. When revising the scene, consider factors such as object sizes, relationships, and logical placements.
"""

    # Construct the base prompt
    prompt = f"""
Task Name: {task_name}
Task Description: {task_description}

Diagnosis of the Current Configuration:
{reflection}

Current Configuration:
{yaml.dump(objects, default_flow_style=False, sort_keys=False)}

Please revise the configuration to address the issues described in the diagnosis.
Ensure that the objects' positions, sizes, and relationships make sense based on the task description.
Provide the revised configuration as a list of objects with the same format as the current configuration.
"""

    # response = query(system,
    #                  user_contents=[prompt],
    #                  assistant_contents=[],
    #                  temperature=temperature,
    #                  model=model)

    response = "Revised Configuration:\n\n- name: Pen\n  center: (0.5, 0.5, 0.01)  # Placed on the center of the paper with a slight elevation to avoid overlapping\n  size: 0.2  # Increased size for better proportion with the paper\n\n- name: Paper\n  center: (0.5, 0.5, 0)  # Centered on the table\n  size: 0.25  # Reduced size to be more proportionate with the pen"

    # Use regex to find the portion of the string that starts with "- name:"
    match = re.search(r"(- name:.*)", response, re.DOTALL)

    if match:
        yaml_cleaned = match.group(1)  # Extract everything from "- name:" onward
        revised_objects = yaml.safe_load(yaml_cleaned)  # Convert the cleaned YAML to a Python dictionary
        print(revised_objects)
    else:
        print("No valid configuration found.")
        revised_objects = []

    config_dict = {item['name']: item for item in revised_objects}

    revised_task_config = []
    for config in task_config:
        if "center" in config:
            name = config["name"]
            config["center"] = config_dict[name]["center"]
            config["size"] = config_dict[name]["size"]
            revised_task_config.append(config)
        else:
            revised_task_config.append(config)

    task_config_path = Path(task_config_path)
    revised_task_config_path = task_config_path.with_name(task_config_path.stem + "_revised" + task_config_path.suffix)
    with open(revised_task_config_path, 'w') as f:
        yaml.dump(revised_task_config, f, indent=4)

    return revised_task_config_path
