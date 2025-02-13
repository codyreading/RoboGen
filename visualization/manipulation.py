import os
import yaml
import numpy as np
from manipulation.utils import build_up_env, take_round_images, save_numpy_as_gif


def get_env(task_config_path,
                         gui=False,
                         randomize=False, # whether to randomize the initial state of the environment.
                         obj_id=0): # which object to use from the list of possible objects.):
    with open(task_config_path, 'r') as file:
        task_config = yaml.safe_load(file)

    solution_path = None
    for obj in task_config:
        if "solution_path" in obj:
            solution_path = obj["solution_path"]
            break

    if not os.path.exists(solution_path):
        os.makedirs(solution_path, exist_ok=True)


    all_substeps = os.path.join(solution_path, "substeps.txt")
    with open(all_substeps, 'r') as f:
        substeps = f.readlines()
    print("all substeps:\n {}".format("".join(substeps)))

    action_spaces = os.path.join(solution_path, "action_spaces.txt")
    with open(action_spaces, 'r') as f:
        action_spaces = f.readlines()
    print("all action spaces:\n {}".format("".join(action_spaces)))

    substep = substeps[0].lstrip().rstrip()
    action_space = action_spaces[0].lstrip().rstrip()
    task_name = substep.replace(" ", "_")

    env, safe_config = build_up_env(
        task_config_path,
        solution_path,
        task_name,
        None,
        return_env_class=False,
        action_space=action_space,
        render=gui,
        randomize=randomize,
        obj_id=obj_id,
    )
    env.reset()
    return env

def visualize(env, output_path, distance=1.6, azimuth_interval=5):
    center = None
    if env.use_table:
        center = np.array([0, 0, 0.4])
    else:
        for name in env.urdf_ids:
            if name in ['robot', 'plane', 'init_table']:
                continue
            if env.urdf_types[name] != "urdf":
                continue
            object_id = env.urdf_ids[name]
            min_aabb, max_aabb = env.get_aabb(object_id)
            center = (min_aabb + max_aabb) / 2
            break
    if center is None:
        center = np.array([0, 0, 0.4])

    rgbs, depths = take_round_images(env, center=center, distance=distance, azimuth_interval=azimuth_interval)
    save_numpy_as_gif(np.array(rgbs), output_path,  fps=10)