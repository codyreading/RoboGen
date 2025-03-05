import yaml
import copy

def config_to_str(task_config):
    input_config = {"objects": []}
    keep_keys = ["task_name", "task_description", "spatial_relationships"]

    for config in task_config:
        for key in keep_keys:
            if key in config:
                input_config[key] = config[key]
        if "center" in config:
            obj_config = {
                "name": config["name"],
                "center": config["center"],
                "size": config["size"]
            }
            input_config["objects"].append(obj_config)
    input_config = yaml.dump(input_config, sort_keys=False)
    return input_config

def get_prompt(input_config, reflection):
    system = """
You are a highly skilled robotic simulator assistant.
"""

    # Construct the base prompt
    prompt = f"""
You are tasked with modifying a YAML configuration file for a robotic simulator based on the following feedback.
The feedback describes the issues with current configuration. The config is a yaml file that has items in the following format:

objects: a list of objects that are in scene, where each object contains the following fields
    name: name of the object, so it can be referred to in the simulator
    size: describe the scale of the object mesh using 1 number in meters. The scale should match real everyday objects. E.g., an apple is of scale 0.08m. You can think of the scale to be the longest dimension of the object.
    center: the location of the object center. If there isn't a table needed for the task or the object does not need to be on the table, this center should be expressed in the world coordinate system. If there is a table in the task and the object needs to be placed on the table, this center should be expressed in terms of the table coordinate, where (0, 0, 0) is the lower corner of the table, and (1, 1, 1) is the higher corner of the table. In either case, you should try to specify a location such that there is no collision between objects. Note that the z-axis (x, y, z) is the gravity axis.
    on_table: whether the object needs to be placed on the table (if there is a table needed for the task). This should be based on common sense and the requirement of the task.
spatial_relationships: Spatial relationships certain objects should have in the initial state
task_description: extended task description
task_name: task name

We have the following spatial relationships:
on, obj_A, obj_B: object A is on top of object B, e.g., a fork on the table.
in, obj_A, obj_B: object A is inside object B, e.g., a gold ring in the safe.

Ensure to only update and return the following attributes: size, center, spatial_relationships.


Here is the current configuration:
```yaml
{input_config}
```

Here is the feedback describing the issues:
"{reflection}"

Make only the changes to fix the issues in the feedback. Return the entire updated YAML configuration.
Only return the YAML content without any explanations or additional text.
Make sure the output is valid YAML that can be parsed.
"""
    return system, prompt

def update_config_with_str(task_config, updated_config):
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
        breakpoint()

        #TODO: Update config

    except:
        print("Invalid reflection updated, not changing anything")
        updated_config = task_config

    return updated_config
