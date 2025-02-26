import yaml
import re
from gpt_4.query import query_vlm, query
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

3. Object Presence Verification
- List objects visible in real world but absent in simulation
- Identify unnecessary objects in simulation
- Note missing environmental elements that could affect the task

Format your response as:

SCALE ISSUES:
[Object name]: [Scale discrepancy] | [Task impact] | [Recommended fix]

PLACEMENT ISSUES:
[Object name]: [Position issue] | [Task impact] | [Recommended fix]

MISSING/EXTRA:
[Object]: [Missing/Extra] | [Task impact] | [Recommended fix]

SUMMARY:
Brief overview of the most critical issues for task success."""

    images = simulated_images + real_images
    response = query_vlm(system=system_prompt, images=images, prompt=task_prompt)
    return response

def revise_task_config(task_config_path, reflection, temperature, model):
    #TODO Limit to updating just the config parts we care about, we are wasting tokens here
    with open(task_config_path, 'r') as file:
        task_config = file.read()

    system = ""
    prompt = f"""
You are tasked with modifying a YAML configuration file for a robotic simulator based on the following feedback.
The feedback describes the issues with current configuration. The config is a yaml file that has items in the following format:

```yaml
- use_table: whether the task requires using a table. This should be decided based on common sense. If a table is used, its location will be fixed at (0, 0, 0). The height of the table will be 0.6m.
# for each object involved in the task, we need to specify the following fields for it.
- type: mesh
  name: name of the object, so it can be referred to in the simulator
  size: describe the scale of the object mesh using 1 number in meters. The scale should match real everyday objects. E.g., an apple is of scale 0.08m. You can think of the scale to be the longest dimension of the object.
  lang: this should be a language description of the mesh. The language should be a bit detailed, such that the language description can be used to search an existing database of objects to find the object.
  path: this can be a string showing the path to the mesh of the object.
  on_table: whether the object needs to be placed on the table (if there is a table needed for the task). This should be based on common sense and the requirement of the task.
  center: the location of the object center. If there isn't a table needed for the task or the object does not need to be on the table, this center should be expressed in the world coordinate system. If there is a table in the task and the object needs to be placed on the table, this center should be expressed in terms of the table coordinate, where (0, 0, 0) is the lower corner of the table, and (1, 1, 1) is the higher corner of the table. In either case, you should try to specify a location such that there is no collision between objects. Note that the z-axis (x, y, z) is the gravity axis.
  all_uid/uid: Unique IDs for each object
- solution_path: path to the solution for the robotic mootion
- set_joint_angle_object_name: Name of the object to be manipulated
- spatial_relationships: Spatial relationships certain objects should have in the initial state
- task_description: extended task description
- task_name: task name
```

We have the following spatial relationships:
on, obj_A, obj_B: object A is on top of object B, e.g., a fork on the table.
in, obj_A, obj_B: object A is inside object B, e.g., a gold ring in the safe.

Ensure to either add new objects only update the following attributes: size, center, spatial_relationships.


Here is the current configuration:
```yaml
{task_config}
```

Here is the feedback describing the issues:
"{reflection}"

Make only the changes to fix the issues in the feedback. Return the entire updated YAML configuration.
Only return the YAML content without any explanations or additional text.
Make sure the output is valid YAML that can be parsed.
"""

    updated_config = query(system,
                     user_contents=[prompt],
                     assistant_contents=[],
                     temperature=temperature,
                     model=model)

    # Get valid YAML
     # Strip any markdown code block markers if present
    if updated_config.startswith("```yaml"):
        updated_config = updated_config[7:]
    if updated_config.startswith("```"):
        updated_config = updated_config[3:]
    if updated_config.endswith("```"):
        updated_config = updated_config[:-3]

    updated_config = updated_config.strip()

    # Validate the updated config
    try:
        updated_config = yaml.safe_load(updated_config)
        task_config_path = Path(task_config_path)
        revised_task_config_path = task_config_path.with_name(task_config_path.stem + "_revised" + task_config_path.suffix)
        with open(revised_task_config_path, 'w') as f:
            yaml.dump(updated_config, f, indent=4)

        return revised_task_config_path
    except:
        #TODO: Handle these better
        raise ValueError("Invalid YAML config")
