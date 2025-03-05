import yaml
import copy
import ast

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
                "size": config["size"],
                "on_table": config["on_table"]
            }
            input_config["objects"].append(obj_config)
    input_config = yaml.dump(input_config, sort_keys=False)
    return input_config

def get_prompt(input_config, reflection):
    system = "You are a highly skilled robotic simulator assistant."

    # Construct the base prompt
    prompt = f"""
You are tasked with creating specific object editing operations for a robotic simulator based on the following feedback.
The feedback describes the issues with current configuration. You will be given a config as a yaml file that has items in the following format:

objects: a list of objects that are in scene, where each object contains the following fields
    name: name of the object, so it can be referred to in the simulator
    size: describe the scale of the object mesh using 1 number in meters. The scale should match real everyday objects. E.g., an apple is of scale 0.08m. You can think of the scale to be the longest dimension of the object.
    center: the location of the object center. If there isn't a table needed for the task or the object does not need to be on the table, this center should be expressed in the world coordinate system. If there is a table in the task and the object needs to be placed on the table, this center should be expressed in terms of the table coordinate, where (0, 0, 0) is the lower corner of the table, and (1, 1, 1) is the higher corner of the table. In either case, you should try to specify a location such that there is no collision between objects. Note that the z-axis (x, y, z) is the gravity axis.
    on_table: whether the object needs to be placed on the table (if there is a table needed for the task). This should be based on common sense and the requirement of the task.
spatial_relationships: Spatial relationships certain objects should have in the initial state
task_description: extended task description
task_name: task name

Please generate a list of editing operations to resolve the feedback. The available editing operations are:
on, obj_A, obj_B: Put object A on top of object B (e.g., a fork on the table).
towards, obj_A, obj_B, distance_factor: Move object A towards object B. The distance_factor (0-1) controls how close object A moves; 0 means no movement, 1 means A reaches B.
away, obj_A, obj_B, distance_factor: Move object A away from object B. The distance_factor (>1) scales how far A moves; ex. 2 will move A double its current distance from B
between, obj_A, obj_B, obj_C: Place object A between object B and object C, ensuring equal spacing between them.
rescale, obj_A, scale_factor: Rescale object A by a scale factor (>0), where 1 means no change, <1 shrinks, and >1 enlarges the object.
near, obj_A, obj_B, distance: Move object A to be exactly 'distance' meters away from object B.

Here is the current configuration:
```yaml
{input_config}
```

Here is the feedback describing the issues:
"{reflection}"

Make only the changes to fix the issues in the feedback. Return a valid list of editing operations based on the available operations. Do not include extra explanations.

Example Output: ["on, for, table", "away, fork, plate, 1.5"]
"""
    return system, prompt

def update_config_with_str(task_config, editing_operations):
     # Validate the updated config
    try:
        operations = ast.literal_eval(editing_operations.strip())
    except:
        print("Invalid reflection updated, not changing anything")
        operations = []

    for config in task_config:
        if "spatial_relationships" in config:
            config["spatial_relationships"].extend(operations)

    return task_config
