import ast
import yaml
from utils import editing_utils

def is_valid_relationship(relationship, objects):
    words = relationship.lower().split(",")
    words = [word.strip().lstrip() for word in words]

    one_object_words = ["rescale"]
    two_object_words = ["on", "in", "towards", "away", "near"]
    three_object_worlds = ["between"]
    relationship_objects = []

    if words[0] in one_object_words:
        relationship_objects = [words[1]]
    elif words[0] in two_object_words:
        relationship_objects = [words[1], words[2]]
    elif words[0] in three_object_worlds:
        relationship_objects = [words[1], words[2], words[3]]

    valid = all(element in objects for element in relationship_objects)
    return valid

def error_fix_task_config(config_path, max_dist=1.0):
    with open(config_path, 'r') as file:
        task_config = yaml.safe_load(file)

    # Limit position to near center and get objects
    objects = []
    for config in task_config:
        if "name" in config:
            center = config["center"]
            center = ast.literal_eval(center)
            center = editing_utils.limit_range(center, distance=max_dist)
            config["center"] = str(center)
            objects.append(config["name"].lower())

    # Ensure all relationships are valid objects
    for config in task_config:
        if "spatial_relationships" in config:
            valid_relationships = []
            for relationship in config["spatial_relationships"]:
                if is_valid_relationship(relationship, objects):
                    valid_relationships.append(relationship)

            config["spatial_relationships"] = valid_relationships

    with open(config_path, 'w') as file:
         yaml.dump(task_config, file, indent=4)